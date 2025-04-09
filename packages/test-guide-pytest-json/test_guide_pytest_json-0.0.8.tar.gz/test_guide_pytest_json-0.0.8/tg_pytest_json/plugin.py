import pytest
import os
from datetime import datetime
from tg_pytest_json.report import JSONReport
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file

def pytest_addoption(parser):
    """Only keep JSON-related options here, not project details."""
    group = parser.getgroup("terminal reporting")
    group.addoption(
        "--json", "-J",
        nargs="?",
        dest="json_path",
        const="",
        help="Where to store the JSON report (optional)."
    )
    parser.addini("json_report", "Where to store the JSON report")

def _json_path(config):
    cli_path = config.option.json_path
    if cli_path is None:
        return None
    if cli_path == "":
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"{timestamp}_report.json"
        root_dir = config.rootpath if hasattr(config, "rootpath") else os.getcwd()
        return os.path.join(str(root_dir), filename)
    return cli_path

@pytest.fixture
def json_report_path(request):
    return _json_path(request.config)

def pytest_configure(config):
    config._json_environment = []

    json_path = _json_path(config)
    if json_path is None:
        return

    # Load from environment
    project_name = os.getenv("PROJECT_NAME")
    ecu_name = os.getenv("ECU_NAME")
    ecu_version = os.getenv("ECU_VERSION")

    config._json_environment.append({
        "project_name": project_name,
        "ecu_name": ecu_name,
        "ecu_version": ecu_version
    })

    if not hasattr(config, "workerinput"):
        config._json = JSONReport(json_path, project_name, ecu_name, ecu_version)
        config.pluginmanager.register(config._json)

    if hasattr(config, "workeroutput"):
        config.workeroutput["json_environment"] = config._json_environment

@pytest.mark.optionalhook
def pytest_testnodedown(node):
    if hasattr(node, "workeroutput"):
        node.config._json_environment = node.workeroutput.get("json_environment", [])

def pytest_unconfigure(config):
    if hasattr(config, "_json"):
        config.pluginmanager.unregister(config._json)
        del config._json
