# Learnings — AI Landscaping Copilot

A running log of concepts and gotchas as I build. Newest at top.

## Phase 2 — Project setup
- uv sync creates the project .venv + a uv.lock lockfile -> reproducible installs.
- Walking skeleton = thinnest end-to-end runnable slice; proves plumbing before features.
- src/ layout prevents import bugs; pythonpath=["src"] lets pytest find the package.

## Phase 1 — Architecture
- Derive non-functionals, don't assert them.
- extra="forbid" on a Pydantic model turns typo'd fields into errors, not silent bugs.
- git loop: work -> add (stage) -> commit (save) -> push (upload).
