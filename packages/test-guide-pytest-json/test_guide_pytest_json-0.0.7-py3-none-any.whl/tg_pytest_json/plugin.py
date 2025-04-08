import pytest
import os
from datetime import datetime
from tg_pytest_json.report import JSONReport

def pytest_addoption(parser):
    """Add command-line and ini options for JSON reporting and custom project details."""
    group = parser.getgroup("terminal reporting")
    group.addoption(
        "--json", "-J",  # Short option -J for --json
        nargs="?",  # Allow optional argument
        dest="json_path",
        const="",  # Default to empty string if no value is provided
        help="Where to store the JSON report (optional). If omitted, a timestamped report will be created at the project root.",
    )
    parser.addini("json_report", "Where to store the JSON report")

    # Add options for project details
    group.addoption(
        "--project-name", "-P",
        required=True,
        help="The name of the project"
    )
    group.addoption(
        "--ecu-name", "-E",
        required=True,
        help="The name of the ECU"
    )
    group.addoption(
        "--ecu-version", "-X",
        required=True,
        help="The version of the ECU"
    )

def _json_path(config):
    """Determine the JSON report path from CLI option or ini setting."""
    cli_path = config.option.json_path
    ini_path = config.getini("json_report")

    if cli_path:
        return cli_path
    if ini_path:
        return ini_path

    # Auto-generate filename at project root
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"{timestamp}_report.json"
    root_dir = config.rootpath if hasattr(config, "rootpath") else os.getcwd()
    return os.path.join(str(root_dir), filename)

@pytest.fixture
def json_report_path(request):
    """Fixture to provide the JSON report path."""
    return _json_path(request.config)

def pytest_configure(config):
    """Configure pytest for JSON reporting and capture project details."""
    config._json_environment = []
    json_path = _json_path(config)

    # Capture the custom project details
    project_name = config.option.project_name
    ecu_name = config.option.ecu_name
    ecu_version = config.option.ecu_version

    # Print or store the collected information
    print(f"Project: {project_name}, ECU: {ecu_name}, Version: {ecu_version}")

    # You can store these details in the report or other places if needed
    config._json_environment.append({
        "project_name": project_name,
        "ecu_name": ecu_name,
        "ecu_version": ecu_version
    })

    if json_path and not hasattr(config, "workerinput"):
        config._json = JSONReport(json_path, project_name, ecu_name, ecu_version)
        config.pluginmanager.register(config._json)

    if hasattr(config, "workeroutput"):
        config.workeroutput["json_environment"] = config._json_environment

@pytest.mark.optionalhook
def pytest_testnodedown(node):
    """Handle distributed testing (xdist)."""
    if hasattr(node, "workeroutput"):
        node.config._json_environment = node.workeroutput["json_environment"]

def pytest_unconfigure(config):
    """Unregister the JSON report plugin on pytest exit."""
    if hasattr(config, "_json"):
        config.pluginmanager.unregister(config._json)
        del config._json
