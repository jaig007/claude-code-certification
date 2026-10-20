---
description: Reviews one Python file against the team checklist. Use when the user asks to review or check a Python file.
argument-hint: [filename]
---

Review the file $ARGUMENTS against this checklist and report PASS or FAIL for each item:

1. Every function has type hints
2. Every function has a one-line docstring
3. Errors are handled (no unhandled division by zero or bad input)
4. There is at least one test for it in tests/

End with a one-line verdict. Do not change any files.