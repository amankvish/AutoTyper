# Contributing to AutoTyper

We welcome contributions to the AutoTyper desktop application from developers, testers, and designers!

## How to Contribute

1. **Report Bugs**: If you find an issue, search the [KNOWN_ISSUES.md](docs/KNOWN_ISSUES.md) list or open a new issue detailing steps to reproduce the bug.
2. **Feature Requests**: We focus on keeping AutoTyper lightweight, safe, and minimal. Before submitting feature requests, ensure they align with our [ROADMAP.md](ROADMAP.md).
3. **Submit Pull Requests**:
   * Fork the repository.
   * Create a branch (`feature/your-feature` or `bugfix/your-fix`).
   * Write tests for your changes inside `test_core.py`.
   * Ensure tests pass before pushing.
   * Open a PR with detailed explanations of changes.

## Development Setup

1. Setup virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run tests:
   ```bash
   python test_core.py
   ```

## Code Quality Standards
* Strictly adhere to **PEP8** guidelines.
* Include **type hints** for all function parameters and return types.
* Write clear docstrings for classes and methods.
* Run automated regression tests to verify that no layout formatting or unicode typing regressions are introduced.
