# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Code

```bash
python calc.py
```

## Running Tests

No test framework is configured. To run a quick manual test:

```bash
python -c "from calc import add, subtract, multiply, divide, average; print(add(1,2))"
```

## Architecture

This is a minimal Python calculator library (`calc.py`) exposing five pure functions: `add`, `subtract`, `multiply`, `divide`, and `average`. There are no external dependencies. `divide` raises `ValueError` on zero divisor; `average` has no guard against an empty list.

## Coding rules
- Every Python function must have type hints and a one-line docstring.
- Put tests in tests/test_calc.py using pytest.
- Run `python calc.py` after any change to check it still works.