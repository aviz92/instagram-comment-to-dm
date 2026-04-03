# Build CLI Tool

- Load and follow all workspace rules before starting. Then execute the command.

## Your Task
Build a CLI tool based on the provided requirements. If requirements are unclear, ask ONE focused question before starting.

## Team Conventions
- Preferred library: **Typer** (use `argparse` only if no third-party deps are allowed)
- Always run via: `uv run <tool-name>`
- Entry point signature must always be:
```python
  def main(argv: list[str] | None = None) -> None:
```
  This ensures the tool is testable without subprocess calls.
- Always include `-v/--version` flag using `importlib.metadata.version()`
- Register in `pyproject.toml` under `[project.scripts]`

## Structure
- CLI layer delegates to service layer — no business logic in command handlers
- Validate inputs early, fail fast with clear error messages
- Use `custom-python-logger` for logging — never `print()`

## After Writing
1. Write unit tests — test argument parsing and core logic separately
2. Run pre-commit:
```bash
pre-commit run --files <new_files>
```
If pre-commit fails — fix and re-run before presenting the result.
