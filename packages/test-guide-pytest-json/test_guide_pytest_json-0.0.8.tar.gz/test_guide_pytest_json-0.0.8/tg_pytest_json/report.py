import json
import os
import time


def pytest_sessionstart(session):
    session.config._json.session_start_time = time.time()
    session.config._json._scan_test_structure("tests")



class JSONReport:
    def __init__(self, json_path, project_name, ecu_name, ecu_version):
        self.json_path = os.path.abspath(
            os.path.expanduser(os.path.expandvars(json_path))
        )
        self.testcases = []
        self.testcase_folders = []
        self.document_data = {}
        self.run_index = 0
        self.timestamp = int(time.time() * 1000)
        self.logged_tests = {}
        self.project_name = project_name
        self.constants = self._load_constants(ecu_name, ecu_version)

    def _get_outcome(self, report):
        if report.failed:
            return "FAILED"
        if report.skipped:
            return "INCONCLUSIVE"
        if report.passed:
            return "PASSED"
        return "ERROR"

    def _load_constants(self, ecu_name, ecu_version):
        if ecu_version:
            version_parts = ecu_version.split(".")

            major = version_parts[0] if len(version_parts) > 0 else ""
            minor = version_parts[1] if len(version_parts) > 1 else ""
            subminor = version_parts[2] if len(version_parts) > 2 else ""

            return [
                {"key": "ECU", "value": ecu_name},
                {"key": "Release_Version_Major", "value": major},
                {"key": "Release_Version_Minor", "value": minor},
                {"key": "Release_Version_Subminor", "value": subminor},
            ]
        else:
            return [
                {"key": "ECU", "value": "Unknown"},
                {"key": "Release_Version_Major", "value": "Unknown"},
                {"key": "Release_Version_Minor", "value": "Unknown"},
                {"key": "Release_Version_Subminor", "value": "Unknown"},
            ]

    def _scan_test_structure(self, base="tests"):
        self.test_structure = set()
        base_path = os.path.abspath(base)

        for root, _, files in os.walk(base_path):
            for file in files:
                if file.startswith("test_") and file.endswith(".py"):
                    rel_path = os.path.relpath(
                        os.path.join(root, file), base_path
                    ).replace("\\", "/")
                    self.test_structure.add(rel_path)

    def _get_test_metadata(self, report):
        """Return the test classification and normalized name."""
        file_path, _, test_func = report.nodeid.partition("::")
        file_path = file_path.replace("\\", "/")
        folder_path = os.path.dirname(file_path)

        # Determine folder name from actual structure
        rel_path = os.path.relpath(folder_path, start="tests").replace("\\", "/")

        if rel_path != ".":
            test_type = "testcasefolder"
            folder_name = rel_path
            test_name = f"{os.path.basename(file_path)}::{test_func}"
            return test_type, folder_name, test_name
        else:
            test_type = "testcase"
            name = f"{os.path.basename(file_path)}::{test_func}"
            return test_type, None, name

    def _make_testcase_dict(self, report):
        verdict = self._get_outcome(report)
        exec_time = int(getattr(report, "duration", 0.0) * 1000)
        timestamp = self.timestamp
        artifacts = getattr(report, "artifacts", [])

        test_type, folder_name, test_name = self._get_test_metadata(report)

        testcase_data = {
            "@type": "testcase",
            "name": test_name,
            "verdict": verdict,
            "timestamp": timestamp,
            "executionTime": exec_time,
            "artifacts": artifacts,
            "constants": self.constants,
        }

        if folder_name:
            if folder_name not in self.logged_tests:
                self.logged_tests[folder_name] = {
                    "@type": "testcasefolder",
                    "name": folder_name,
                    "testcases": [],
                }
            # Avoid duplicates
            if test_name not in {
                t["name"] for t in self.logged_tests[folder_name]["testcases"]
            }:
                self.logged_tests[folder_name]["testcases"].append(testcase_data)
        else:
            if test_name not in self.logged_tests:
                self.logged_tests[test_name] = testcase_data

    def pytest_runtest_logreport(self, report):
        """Log individual test results (only on 'call' phase)."""
        if report.when != "call":
            return  # ✅ Ignore setup/teardown phases

        testcase_dict = self._make_testcase_dict(report)
        if not testcase_dict:
            return

        if hasattr(report, "testcases"):  # Folder-type
            self.testcase_folders.append(testcase_dict)
        else:
            file_test_case = report.nodeid.replace("::", ":")
            testcase_dict["name"] = file_test_case
            self.testcases.append(testcase_dict)

        # Add metadata if available
        if hasattr(report, "test_metadata"):
            for metadata in report.test_metadata:
                testcase_dict.setdefault("attributes", []).append(
                    {"key": metadata.get("key", ""), "value": metadata.get("value", "")}
                )

    def _insert_testcase_into_tree(self, path_parts, testcase_data):
        current_level = self.logged_tests

        for part in path_parts[:-1]:  # For all but last, create testcasefolder nodes
            if "children" not in current_level:
                current_level["children"] = {}

            if part not in current_level["children"]:
                current_level["children"][part] = {
                    "@type": "testcasefolder",
                    "name": part,
                    "testcases": [],
                }

            current_level = current_level["children"][part]

        # Insert the testcase at the correct level
        current_level["testcases"].append(testcase_data)

    def _make_testcase_dict(self, report):
        verdict = self._get_outcome(report)
        exec_time = int(getattr(report, "duration", 0.0) * 1000)
        timestamp = self.timestamp
        artifacts = getattr(report, "artifacts", [])

        test_type, folder_name, test_name = self._get_test_metadata(report)

        testcase_data = {
            "@type": "testcase",
            "name": test_name,
            "verdict": verdict,
            "timestamp": timestamp,
            "executionTime": exec_time,
            "artifacts": artifacts,
            "constants": self.constants,
        }

        if folder_name:
            path_parts = folder_name.strip("/").split("/")
            self._insert_testcase_into_tree(path_parts + [test_name], testcase_data)
        else:
            self.testcases.append(testcase_data)

    def _flatten_tree(self, node):
        """Recursively convert the nested tree into the schema format."""
        if "children" not in node:
            return []

        flattened = []
        for folder_name, child in node["children"].items():
            subfolders = self._flatten_tree(child)
            folder_entry = {
                "@type": "testcasefolder",
                "name": folder_name,
                "testcases": child["testcases"] + subfolders,
            }
            flattened.append(folder_entry)
        return flattened

    def _clean_testcase_names(self, entries):
        """Recursively clean testcase and folder names."""
        for entry in entries:
            if entry["@type"] == "testcasefolder":
                entry["name"] = self._clean_folder_name(entry["name"])
                self._clean_testcase_names(entry["testcases"])
            elif entry["@type"] == "testcase":
                entry["name"] = self._clean_testcase_name(entry["name"])

    def _clean_testcase_name(self, name):
        # Handle format like: test_chicken.py::test_chicken_talks
        if "::" in name:
            file_part, func_part = name.split("::", 1)
            file_part = os.path.splitext(os.path.basename(file_part))[0]  # remove .py
            file_part = file_part.removeprefix("test_")  # remove test_ from filename
            func_part = func_part.removeprefix("test_") # remove test_ from function name
            return f"{file_part}-{func_part}"
        else:
            # fallback for single names (legacy)
            return name.removeprefix("test_")

    def _clean_folder_name(self, name):
        # Remove 'test_' prefix if present and clean path parts
        return name.replace("test_", "").replace(".py", "")



    def pytest_sessionfinish(self, session):
        nested_folders = self._flatten_tree(self.logged_tests)
        testcases_output = nested_folders + self.testcases

        self._clean_testcase_names(testcases_output)

        report = {
            "name": self.project_name,
            "timestamp": self.timestamp,
            "testcases": testcases_output,
        }

        os.makedirs(os.path.dirname(self.json_path), exist_ok=True)
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)

    def pytest_terminal_summary(self, terminalreporter):
        terminalreporter.write_sep("-", f"Generated JSON report: {self.json_path}")
