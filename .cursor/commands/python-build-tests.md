# Build Tests

- Load and follow all workspace rules before starting. Then execute the command.

## Your Task
Write pytest tests for the provided code. If no code is provided, ask which module or feature to cover.

## Team Conventions
- Run tests with: `uv run pytest`
- Use `custom-python-logger` for any test logging — never `print()`
- Use `pytest-dynamic-parameterize` for dynamic parameter generation
- Use `pytest-depends-on` for explicit test dependencies — never rely on execution order implicitly

## What to Cover
For each function or class, write tests for:
- Happy path
- Edge cases (empty input, None, zero, boundary values)
- Failure cases — use `pytest.raises` with `match=`

## conftest.py Placement
- Root `conftest.py` — only truly global fixtures
- Module-level `conftest.py` — fixtures shared within a directory
- Keep fixtures local to their test module when used by a single test module only
- `pytest_addoption` belongs in the subdirectory `conftest.py` unless the option is genuinely global

## Plugin Development
When writing pytest plugins:
- `pytest_addoption` — prefix options with a project-specific prefix to avoid conflicts
- `pytest_configure` — for plugin initialization
- `pytest_sessionfinish` — for cleanup and reporting
- Register via `[project.entry-points.pytest11]` in `pyproject.toml`
- Use `tryfirst=True` / `trylast=True` when hook execution order matters

## After Writing Tests
Run pre-commit on all new test files:
```bash
pre-commit run --files <new_test_files>
```
If pre-commit fails — fix and re-run before presenting the result.
