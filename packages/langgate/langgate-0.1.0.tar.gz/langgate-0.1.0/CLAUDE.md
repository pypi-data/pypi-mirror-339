# LangGate Development Guide

## Build & Test Commands
- **Install dependencies:** `uv add <PACKAGE>`
- **Compile Protobufs:** `make protos-compile`
- **Install development dependencies:** `uv add --dev <PACKAGE>`
- **Run linting:** `make lint`
- **Run typechecking:** `make mypy`
- **Run tests (includes coverage):** `make test`
- **Run single test:** `uv run pytest tests/path/to/test.py::test_name -v`
- **Start development server locally:** `make run-local`
- **Start development server in docker:** `make compose-dev`

## Code Style Guidelines
- **Python version:** 3.13+
- **Line length:** 88 characters
- **Indent width:** 4 spaces
- **Imports:** Use isort order (stdlib, third-party, first-party)
- **Type hints:** Required for all functions and methods
- **Error handling:** Use structured logging with `structlog`
- **Naming:** Use snake_case for variables and functions, PascalCase for classes
- **Documentation:** Docstrings for all public modules, classes, and functions
- **Formatting:** Enforced by ruff (similar to black)
- **Tests:** Required for all new features with pytest

## Additional Notes
- Remember, we should NEVER be using the system Python. We are using `uv`. If a command is not in the Makefile, it should be run with `uv run <COMMAND>`.
- Never make any commits or stage changes. These will be reviewed by the team and we will commit them.
- We need to strictly adhere to SOLID principles and design patterns. The project makes widespread use of protocols and abstract classes.
- We use a custom logging library that is based on `structlog`. This is already set up in the project. We should use async logging where appropriate.
- We should seek to keep the code clear, concise, readable, and maintainable, avoiding fluff and complexity unless there is a good reason for it.
- We have tests in a `tests` directory (which contains both unit tests and "integration" test specs). We should aim for high test coverage.
- We prioritise integration tests that get the most "bang for our buck" in term of coverage and are more likely to catch bugs in practice.
- After making any code changes, run `make lint` to fix all linting errors. This should be done before reporting that a task is complete.
- When requesting permission to execute an action, please always try to explain your reasoning for what you hope to accomplish by the action (unless it is very obvious). This will help the user to better appraise your proposed action with an understanding of your intentions.
