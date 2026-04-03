---
name: testing-expert
description: Guides writing and improving Python tests with pytest—fixtures, parametrization, mocking, and structure. Use when writing tests, adding test coverage, debugging test failures, or when the user asks for testing help, unit tests, integration tests, or TDD.
---

# Testing Expert

## When to Apply

- User asks to write tests, add coverage, or fix failing tests
- Code changes affect behavior and tests should be added or updated
- User mentions unit test, integration test, TDD, pytest, or fixtures

## Run Tests

```bash
uv run pytest
```

Run specific path or marker: `uv run pytest tests/path/to/test_file.py` or `uv run pytest -m "marker_name"`.

## Test Structure and Naming

- **Location**: Tests live under `tests/`. Mirror source layout when helpful (e.g. `tests/unit/`, `tests/integration/`).
- **Files**: `test_*.py` or `*_test.py`. Pytest discovers both.
- **Test names**: `test_<behavior>_<scenario>` (e.g. `test_parse_returns_none_when_empty`).
- **Classes** (optional): Group related tests in a class; name it `Test<Subject>` (e.g. `TestUserService`). Use when sharing setup or when it improves readability.
- **Style**: Follow project code style—type hints on test functions, PEP 8, max line length 120.

## Fixtures

- **Shared fixtures**: Define in `conftest.py` in the same package or in `tests/conftest.py` for project-wide use.
- **Prefer fixtures** over manual setup/teardown in test bodies.
- **Scope**: Use `function` (default), `class`, `module`, or `session` only when it clearly reduces duplication and is safe (no shared mutable state).
- **Naming**: Descriptive names; use `_` prefix only for “private” fixtures that are not used by name in test signatures.

```python
# conftest.py
import pytest

@pytest.fixture
def sample_user() -> dict[str, str]:
    return {"id": "1", "name": "Alice"}
```

Inject by name: `def test_foo(sample_user): ...`.

## Parametrization

Use `@pytest.mark.parametrize` for multiple inputs/outputs instead of looping or copy-paste.

```python
@pytest.mark.parametrize(("input_val", "expected"), [
    ("a", 1),
    ("b", 2),
])
def test_map_returns_expected(input_val: str, expected: int) -> None:
    assert get_value(input_val) == expected
```

Register custom markers in `pytest.ini` under `[pytest] markers =`; this project uses `--strict-markers`.

## Mocking and Isolation

- **Mock at boundaries**: External HTTP, DB, file I/O, time—not internal logic.
- **Prefer dependency injection** and fixtures over patching; pass fakes or mocks into the code under test.
- **Patch**: Use `unittest.mock.patch` (or `pytest-mock` if the project uses it) with the canonical “object’s use” path (where it’s used, not where it’s defined).
- **Avoid over-mocking**: Prefer real objects or small fakes when fast and simple.

## Assertions

- Use **pytest’s assert**; avoid `assertTrue(x)` in favor of `assert x` or `assert result == expected`.
- Add **brief messages** for non-obvious failures: `assert len(items) > 0, "expected at least one item"`.
- For exceptions: `pytest.raises(ValueError): ...` or `with pytest.raises(ValueError) as exc_info: ...` when you need to check the exception.

## Test Quality

- **One logical behavior per test**; avoid testing many things in a single test.
- **Arrange–Act–Assert**: Set up, call the code under test, assert outcomes.
- **Deterministic**: No flakiness from time, randomness, or shared global state; fix or quarantine flaky tests.
- **Fast**: Prefer fast unit tests; move slow or external tests to integration and run them separately if needed.

## Suggesting Tests

When suggesting new tests:

1. Identify the behavior or edge case to cover.
2. Propose a minimal fixture/setup and a single, clear assertion.
3. Use existing project patterns (e.g. `conftest.py`, same naming and structure as current tests).
4. Run `uv run pytest` (or the relevant subset) and fix any failures or lint issues.

## Anti-Patterns

- **Don’t** test implementation details (e.g. private methods) unless necessary for complex behavior.
- **Don’t** use raw `print` or manual logging for assertions; use assertions and pytest’s `-s` only when debugging.
- **Don’t** share mutable state across tests via module-level or broad-scoped fixtures without clear need.
- **Don’t** suggest `pip` or `python -m pytest`; use `uv run pytest` per project standards.
