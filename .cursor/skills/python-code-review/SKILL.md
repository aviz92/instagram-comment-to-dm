---
name: python-code-review
description: Conducts expert Python code reviews following project standards—function design, type hints, architecture, testing, security, and best practices. Use when reviewing code changes, pull requests, or when the user asks for code review, code quality feedback, or PR review.
---

# Python Code Review Expert

## When to Apply

- User asks for code review, PR review, or code quality feedback
- Reviewing code changes or pull requests
- User mentions code quality, best practices, or code standards

## Pre-Review: Run Pre-commit Checks

**Mandatory**: Before review approval, verify pre-commit passes:

```bash
uv run pre-commit run --all-files
```

If hooks fail, mark as **Critical Issue**—code must be fixed before approval.

## Review Principles

### 1. Function Design - Atomic & Single Responsibility

- **Atomic**: Functions do ONE thing well
- **Length**: Aim for < 7 lines ideally, max 15 lines. Prioritize clarity and single responsibility over strict line counts
- **Parameters**: Max 5-6 parameters; use data classes/dicts for complex inputs (not objects as input)
- **Naming**: Verb-based, clear purpose (`get_user_by_id`, `validate_email`)
- **Return values**: Consistent types; avoid returning `None` when possible (use `Optional` or raise exceptions)
- **Side effects**: Minimal; prefer pure functions

**Extract when**: Logic block exceeds 10 lines or contains distinct sub-steps → extract to private helper function.

### 2. Type Hints - Mandatory

- **All functions**: Complete type hints for parameters and return types
- **Built-in types**: Use `list`, `dict`, `tuple`, `set` directly (Python 3.12+)
- **Generics**: Use appropriately (`list[str]`, `dict[str, Any]`, `tuple[int, str]`)
- **Avoid `Any`**: Only when absolutely necessary
- **Type completeness**: Accurate and specific types

### 3. Code Structure & Organization

- **Architecture**: Follow architectural principles (SOLID, separation of concerns, layered architecture)
- **Modularity**: Logical, cohesive modules with single purpose
- **File organization**: Related code grouped together; avoid circular dependencies
- **Function placement**: Most appropriate module/file; shared utilities in common modules
- **Domain logic**: Not in views/controllers; extract to service layers

### 4. Error Handling

- **Specific exceptions**: Not bare `except:`
- **Clear messages**: Actionable error messages with context
- **Logging**: Log errors appropriately (follow standard-libraries.mdc)
- **Validation**: Validate inputs early; fail fast

### 5. Security

- **Input validation**: Always validate and sanitize user inputs
- **Secrets**: Never hardcode; use environment variables
- **Authentication/authorization**: Checks in place where needed

### 6. Testing

- **Framework**: pytest (follow testing-expert skill)
- **Testability**: Code easily testable (dependency injection, mocking)
- **Coverage**: Critical paths have tests
- **Organization**: Tests mirror code structure

### 7. Code Style

- **PEP 8**: Follow project style (code-style.mdc)
- **Line length**: Max 120 characters
- **Naming**: Classes `PascalCase`, functions `snake_case`, constants `UPPER_SNAKE_CASE`
- **Indentation**: 4 spaces (never tabs)
- **Keyword arguments**: Prefer `func(param=value)`

## Review Checklist

### Structure & Organization
- [ ] Code organized logically?
- [ ] Functions/classes in right location?
- [ ] Imports organized correctly?
- [ ] Proper separation of concerns?

### Function Quality
- [ ] Functions atomic and focused?
- [ ] Functions appropriately sized (< 15 lines ideally)?
- [ ] Function names clearly describe purpose?
- [ ] Parameters reasonable (max 5-6)?
- [ ] Minimal side effects?

### Type Safety
- [ ] All functions fully type-hinted?
- [ ] Type hints accurate and specific?
- [ ] `Any` avoided where possible?
- [ ] Generic types used appropriately?

### Error Handling
- [ ] Exceptions handled appropriately?
- [ ] Error messages clear?
- [ ] Input validation present?

### Performance
- [ ] Database queries optimized?
- [ ] No unnecessary computation?
- [ ] No N+1 query problems?

### Security
- [ ] Input validation present?
- [ ] Secrets handled securely?
- [ ] Authentication/authorization checks in place?

### Documentation
- [ ] Complex functions have docstrings (Google-style)?
- [ ] Docstrings clear and complete when present?

## Review Format

1. **Summary**: High-level overview
2. **Categorize**: Group by severity (Critical, Major, Minor, Suggestions)
3. **Be specific**: Point to exact lines with examples
4. **Be constructive**: Explain WHY and HOW to fix
5. **Acknowledge**: Highlight what was done well
6. **Provide examples**: Show how to improve
7. **Keep it short**: Practical, focused, easy to read

## Example Review Comment

**Good:**
```
❌ Issue: Function `process_data` is too long (150 lines) and handles multiple responsibilities.

📍 Location: lines 45-195 in `utils.py`

🔍 Problem: This function validates input, processes data, makes API calls, and handles errors all in one place.

💡 Solution: Break this into smaller, atomic functions:
- `validate_input_data(data: dict[str, Any]) -> bool`
- `transform_data(data: dict[str, Any]) -> dict[str, Any]`
- `call_external_api(data: dict[str, Any]) -> Response`
- `process_data(data: dict[str, Any]) -> dict[str, Any]` (orchestrator)
```

**Bad:**
```
This function is too long.
```

## Severity Levels

- **Critical**: Must fix before merge (security, missing type hints, broken functionality, pre-commit failures)
- **Major**: Should fix (performance, structure, best practices)
- **Minor**: Nice to have (style, documentation improvements)
- **Suggestions**: Optional improvements (optimizations, refactoring opportunities)

## Remember

- Code reviews improve code quality, not criticize developers
- Keep it short, focused, and actionable
- Balance perfectionism with pragmatism
- Consider context and deadlines, but don't compromise on critical issues
