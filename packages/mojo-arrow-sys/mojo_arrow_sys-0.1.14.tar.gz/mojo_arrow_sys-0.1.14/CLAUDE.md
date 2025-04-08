# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands
- Install: `make install`
- Development build: `make build`
- Run all tests: `make test`
- Run a single test: `python -m pytest tests/test_mojo_arrow_sys.py::TestMojoArrowSys::test_function_name -v`
- Clean: `make clean`
- Distribution: `make dist`
- Lint: `python -m ruff check .`

## Code Style Guidelines
- Python: Supports Python 3.10+
- C: Standard C99 with -Wall -Wextra flags
- Python imports: Group standard library, then third-party, then local imports
- Error handling: Use proper error codes/objects, check PyErr states in C code
- Testing: Use pytest and unittest frameworks
- Types: Use Python type annotations when possible
- Naming: snake_case for Python functions/variables, camelCase for C functions
- Documentation: C99-style comments in C code; docstrings for Python