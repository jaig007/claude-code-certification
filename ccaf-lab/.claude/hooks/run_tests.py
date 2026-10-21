import json, subprocess, sys

data = json.load(sys.stdin)
path = data.get("tool_input", {}).get("file_path", "")

if not path.endswith(".py"):
    sys.exit(0)                                    # only care about Python files

result = subprocess.run([sys.executable, "-m", "pytest", "-q"],
                        capture_output=True, text=True)

if result.returncode != 0:
    print("Tests FAILED after this edit:\n" + result.stdout[-2000:], file=sys.stderr)
    sys.exit(2)                                    # feedback to Claude: fix it

sys.exit(0)