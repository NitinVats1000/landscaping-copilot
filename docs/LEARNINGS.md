# Learnings — AI Landscaping Copilot

A running log of concepts and gotchas as I build. Newest at top.

## Phase 2 — Project setup
- uv sync creates the project .venv + a uv.lock lockfile -> reproducible installs.s
- Walking skeleton = thinnest end-to-end runnable slice; proves plumbing before features.
- src/ layout prevents import bugs; pythonpath=["src"] lets pytest find the package.

## Phase 1 — Architecture
- Derive non-functionals, don't assert them.
- extra="forbid" on a Pydantic model turns typo'd fields into errors, not silent bugs.
- git loop: work -> add (stage) -> commit (save) -> push (upload).

## Phase 2 - 
- pyproject.toml = project's ID card + dependency shopping list; makes the setup reproducible on any machine.
- uv sync reads pyproject.toml → creates .venv (isolated toolbox) + uv.lock (exact versions) → reproducible setup
- Walking skeleton = smallest runnable end-to-end app; proves the plumbing before building features
- uv run <command> runs things inside the project's environment
- pre-commit hooks run ruff + mypy automatically before every commit → impossible to commit messy/broken code by accident.