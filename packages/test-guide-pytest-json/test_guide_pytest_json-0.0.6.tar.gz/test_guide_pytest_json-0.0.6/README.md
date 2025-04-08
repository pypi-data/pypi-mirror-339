## pytest-test-guide-json

A Python package to convert `pytest` test results into a **JSON format compatible with [test.guide](https://www.tracetronic.com/products/testguide/)** by TraceTronic.

## 📘 Overview

**test.guide** by TraceTronic is a powerful tool for managing and analyzing automated test results. However, it does **not natively support `pytest`** output.

This package bridges the gap by:

- Collecting test results from `pytest`
- Converting them into a structured JSON format
- Ensuring full compatibility with test.guide’s expected JSON schema

## 🚀 Features

- Easy integration with existing `pytest` test suites
- Generates test.guide-compatible JSON reports
- Captures test case hierarchy, verdicts (`PASSED`, `FAILED`, `ERROR`, `INCONCLUSIVE`, etc.), durations, and more
- Supports nested folder/test structures for proper grouping in test.guide

## 🧪 Example Usage

1. **Install the package**:
```bash
pip install test-guide-pytest-json
```

2. Run your tests with the JSON report option:

The following items are now required when you call --json:
- `--json` (or `-j`) - The path to the JSON report file. If not specified, a timestamped file will be created in the current working directory.
- `--project-name` (or `-p`) - The name of the project
- `--ecu-name` (or `-e`) - The name of the ECU
- `--ecu-version` (or `-v`) - The version of the ECU

```bash
# Timestamped file in default path with specific tests
pytest ./tests/ --json

# Custom path
pytest --json some/path/report.json

# Timestamped file in project root
pytest --json --project-name my_project --ecu-name my_ecu --ecu-version 0.0.1

# Short options
pytest -j some/path/report.json -p my_project -e my_ecu -v 0.0.1

# No JSON report (unless specified in pytest.ini)
pytest
```