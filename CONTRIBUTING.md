# Contributing

Thanks for your interest in improving python-sysadmin-utils.

## Getting started

1. Fork and clone the repository.
2. Create a virtual environment and install dev dependencies:
   ```bash
   python -m venv .venv && source .venv/bin/activate
   make dev
   ```
3. Create a feature branch: `git checkout -b feat/my-change`.

## Standards

- Code targets Python 3.8+ and follows PEP 8 (enforced by flake8, max line 100).
- Add or update tests under `tests/` for any behavior change.
- Keep functions small and documented with docstrings.
- Run `make lint test` before opening a pull request.

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/):
`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `ci:`, `build:`, `chore:`.
