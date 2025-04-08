import json
import os
import time


def pytest_sessionstart(session):
    session.config._json.session_start_time = time.time()
    session.config._json._scan_test_structure("tests")


def find_project_root():
    """Find the project root by looking for a known project marker."""
    current_path = os.path.abspath(__file__)

    while current_path:
        parent = os.path.dirname(current_path)

        # Check if we hit the filesystem root
        if parent == current_path:
            break

        # Check for common project markers
        for marker in ['pyproject.toml', 'setup.py', '.git']:
            if os.path.exists(os.path.join(parent, marker)):
                return os.path.basename(parent)

        current_path = parent  # Move up a level

    return os.path.basename(os.path.dirname(os.path.abspath(__file__)))  # Fallback


class JSONReport:
    def __init__(self, json_path, project_name="Test-Suite"):
        self.json_path = os.path.abspath(os.path.expanduser(os.path.expandvars(json_path)))
        self.testcases = []
        self.testcase_folders = []
        self.document_data = {}
        self.run_index = 0
        self.timestamp = int(time.time() * 1000)
        self.logged_tests = {}
        self.project_name = find_project_root()
        self.constants = self._load_constants()

    def _get_outcome(self, report):
        if report.failed:
            return "FAILED"
        if report.skipped:
            return "INCONCLUSIVE"
        if report.passed:
            return "PASSED"
        return "ERROR"

    def _load_constants(self):
        metadata_path = os.path.join(os.path.dirname(__file__), "..", "assets", "firmware", "metadata.json")
        try:
            with open(os.path.abspath(metadata_path), "r", encoding="utf-8") as f:
                data = json.load(f)
                component_id = data.get("ECUModel", {}).get("ComponentId", "")
                version = data.get("Version", "")
                version_parts = version.split(".")

                major = version_parts[0] if len(version_parts) > 0 else ""
                minor = version_parts[1] if len(version_parts) > 1 else ""
                subminor = version_parts[2] if len(version_parts) > 2 else ""

                return [
                    {"key": "ECU", "value": component_id},
                    {"key": "Release_Version_Major", "value": major},
                    {"key": "Release_Version_Minor", "value": minor},
                    {"key": "Release_Version_Subminor", "value": subminor},
                ]
        except Exception as e:
            print(f"Warning: Failed to load metadata.json constants: {e}")
            return []

    def _scan_test_structure(self, base="tests"):
        self.test_structure = set()
        base_path = os.path.abspath(base)

        for root, _, files in os.walk(base_path):
            for file in files:
                if file.startswith("test_") and file.endswith(".py"):
                    rel_path = os.path.relpath(os.path.join(root, file), base_path).replace("\\", "/")
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
                    "testcases": []
                }
            # Avoid duplicates
            if test_name not in {t["name"] for t in self.logged_tests[folder_name]["testcases"]}:
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
                testcase_dict.setdefault("attributes", []).append({
                    "key": metadata.get("key", ""),
                    "value": metadata.get("value", "")
                })

    def pytest_sessionfinish(self, session):
        testcases_output = []

        for key, data in self.logged_tests.items():
            testcases_output.append(data)

        report = {
            "name": self.project_name,
            "timestamp": self.timestamp,
            "testcases": testcases_output,
            # "constants": self.constants,
            # "documentData": self.document_data
        }

        os.makedirs(os.path.dirname(self.json_path), exist_ok=True)
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)

    def pytest_terminal_summary(self, terminalreporter):
        terminalreporter.write_sep("-", f"Generated JSON report: {self.json_path}")
