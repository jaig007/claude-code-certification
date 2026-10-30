---
description: Plan, implement and test a feature in three fixed steps
---
Feature request: $ARGUMENTS

Run these steps strictly in order. Don't start a step until the previous
one has finished and its handoff file exists.

1. Delegate to the planner subagent. Pass it the full feature request.
2. Gate: if docs/handoff/1-plan.md is missing or empty, stop and report.
3. Delegate to the implementer subagent. Tell it to read 1-plan.md.
4. Delegate to the tester subagent. Tell it to read 1-plan.md and 2-changes.md.
5. Summarise for me: what changed, the test result, and the path of
   each handoff file.