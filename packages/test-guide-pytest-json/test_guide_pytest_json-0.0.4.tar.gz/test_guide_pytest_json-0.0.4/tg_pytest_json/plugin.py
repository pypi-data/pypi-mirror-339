import pytest
from tg_pytest_json.report import JSONReport



def pytest_addoption(parser):
    """Add command-line and ini options for JSON reporting."""
    group = parser.getgroup("terminal reporting")
    group.addoption(
        "--json",
        action="store",
        dest="json_path",
        default=None,
        help="Where to store the JSON report",
    )
    parser.addini("json_report", "Where to store the JSON report")


# @pytest.fixture(scope="session", autouse=True)
# def json_environment(request):
#     """Provide environment details for the JSON report."""
#     request.config._json_environment.extend(
#         [
#             ("Python", platform.python_version()),
#             ("Platform", platform.platform()),
#         ]
#     )


def _json_path(config):
    """Determine the JSON report path from CLI option or ini setting."""
    return config.option.json_path or config.getini("json_report") or None


@pytest.fixture
def json_report_path(request):
    """Fixture to provide the JSON report path."""
    return _json_path(request.config)


def pytest_configure(config):
    """Configure pytest for JSON reporting."""
    config._json_environment = []
    json_path = _json_path(config)

    if json_path and not hasattr(config, "workerinput"):
        config._json = JSONReport(json_path)
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
