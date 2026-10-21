import json, sys

data = json.load(sys.stdin)                       # Claude Code sends event JSON on stdin
path = data.get("tool_input", {}).get("file_path", "").replace("\\", "/")

PROTECTED = [".env", "tests/"]

for p in PROTECTED:
    if p in path:
        print(f"Blocked: {path} is protected ({p}). Do not modify it; "
              f"fix the source code instead.", file=sys.stderr)
        sys.exit(2)                                # 2 = block, stderr goes to Claude

sys.exit(0)                                        # 0 = no objection