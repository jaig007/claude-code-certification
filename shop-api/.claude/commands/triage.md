---
description: Classify a request and route it to one specialist subagent
---
Request: $ARGUMENTS

Step 1: classify the request as exactly one of these:
- bug: something behaves wrongly        -> bug-fixer
- docs: documentation or docstrings      -> doc-writer
- tests: missing or new tests            -> tester
- question: how or why something works   -> code-explainer

If it mixes several, pick the one that must happen first and list the
rest as follow-ups. Don't do any work yourself.

Step 2: print one line: Route: <category> -> <subagent> because <reason>

Step 3: delegate to that subagent only, passing the full request.

Step 4: report its summary and any follow-ups.