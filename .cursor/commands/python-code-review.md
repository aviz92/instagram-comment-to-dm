# Python Code Review

- Load and follow all workspace rules before starting. Then execute the command.
- Before reviewing, execute the following steps automatically.

## Step 1 — Pre-commit
Run pre-commit on the changed files:
```bash
pre-commit run --files <changed_files>
```
If pre-commit fails — report the output and stop. Do not proceed to review until the code is clean.

## Step 2 — Run Relevant Tests
Identify and run tests related to the changed code:
```bash
pytest <relevant_test_paths> -v
```
- Infer relevant tests from the changed file names and imports.
- If tests fail — report the failures and flag them as **Critical** in the review.
- If no tests exist for the changed code — flag it as **Major**.

## Step 3 — Code Review
Apply all workspace rules: code style, type hints, organization, testing, security, and logging.

## Step 4 — Logic Review
- Does the code do what it's supposed to do?
- Are all edge cases handled? (empty input, None, zero, negative values, large datasets)
- Are conditionals correct and in the right order?
- Are there off-by-one errors or boundary issues?
- Is the flow logical and complete?
- Does the error handling cover realistic failure scenarios?
- Are there hidden assumptions about input that could break in production?

### Severity Levels
- **Critical** — must fix before merge (security, broken functionality, missing type hints, failing tests)
- **Major** — should fix (structure, performance, best practices, missing test coverage)
- **Minor** — nice to have (style, documentation)
- **Suggestion** — optional improvements

### Output Format

**Summary**
One paragraph — overall quality, test results, pre-commit status, and what was done well.

**Issues**
For each issue:
```
[SEVERITY] Short title
📍 Location: file.py, line X
🔍 Problem: what's wrong and why it matters
💡 Fix: concrete code example
```

**Verdict**
`APPROVED` / `APPROVED WITH COMMENTS` / `CHANGES REQUESTED`

### Focus Areas
- Type hints — all parameters and return types, no bare `Any`
- Function size and single responsibility
- Error handling — specific exceptions, clear messages, logging with context
- Business logic belongs in services, not views or controllers
- No hardcoded secrets or magic numbers
- Testability — dependency injection, no hidden side effects
- N+1 queries and unnecessary computation

## Tone
Strict but constructive. Be as short as possible — flag real issues, skip obvious ones.
