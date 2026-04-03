# Python Refactoring

Load and follow all workspace rules before starting.

## Step 1 — Understand Before Touching
- Read the full file and identify the scope of the refactor.
- Search the codebase for all call sites of the function/class being changed.
- Identify tests that cover the code. Note if coverage is missing.
- State your plan before making any edits: what changes, what stays, and why.

## Step 2 — Classify the Refactor

| Category | Examples |
|---|---|
| **Extract** | Long function → atomic helpers |
| **Rename** | Unclear names → intention-revealing names |
| **Restructure** | Move to correct module; fix layering violation |
| **Simplify** | Remove dead code; flatten nesting; replace loops with comprehensions |
| **Type Safety** | Add missing type hints; narrow `Any` |
| **Pattern Apply** | Factory, Strategy, Repository, etc. |

## Step 3 — Rules
- Fix only what the task requires + obvious violations in the immediate vicinity.
- Do NOT refactor unrelated parts of the file.
- Make ONE logical change per edit block — do not mix rename + extract + restructure.
- Never change public function signatures without explicit instruction.
- If a signature must change, list all affected call sites in chat first.

## Step 4 — Validate
1. Confirm logic equivalence — behavior must not change.
2. Run: `uv run pre-commit run --all-files`
3. Run affected tests: `uv run pytest <path/to/relevant/tests>`
4. If no tests exist for the refactored code, flag it:
   > ⚠️ No tests found for `<function_name>`. Consider adding coverage before merging.

## Output Format
```
## Refactor Summary

**Type**: <category>
**Files changed**: <list>
**What changed**: <short description>
**Why**: <reason — too long, violation, layering issue, etc.>
**Interface preserved**: ✅ / ⚠️ <what changed>
**Tests**: <passing / missing / added>
**Pre-commit**: ✅ / ❌
```
