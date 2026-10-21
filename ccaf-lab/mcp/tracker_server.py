import json, os
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "tracker",
    instructions="Team issue tracker for the ccaf-lab project. "
                 "Use it to list, create and close bugs and tasks.",
)

DATA = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")) / "issues.json"

def load():
    return json.loads(DATA.read_text()) if DATA.exists() else []

def save(issues):
    DATA.write_text(json.dumps(issues, indent=2))


@mcp.tool()
def list_issues(status: str = "open") -> str:
    """List issues in the team tracker.
    status: 'open' (default), 'closed' or 'all'.
    Returns one line per issue: id, status, title."""
    if status not in ("open", "closed", "all"):
        raise ValueError("Invalid status. Use 'open', 'closed' or 'all'.")
    issues = [i for i in load() if status == "all" or i["status"] == status]
    if not issues:
        return f"No {status} issues."
    return "\n".join(f"#{i['id']} [{i['status']}] {i['title']}" for i in issues)


@mcp.tool()
def create_issue(title: str, details: str = "") -> str:
    """Create a new issue in the team tracker.
    Use when the user reports a bug or asks to log a task.
    title: short summary (required). details: optional longer description."""
    if not title.strip():
        raise ValueError("Title is empty. Provide a short summary of the issue.")
    issues = load()
    new_id = max((i["id"] for i in issues), default=0) + 1
    issues.append({"id": new_id, "title": title, "details": details, "status": "open"})
    save(issues)
    return f"Created issue #{new_id}: {title}"


@mcp.tool()
def close_issue(issue_id: int) -> str:
    """Close an existing issue by its numeric id (e.g. 3, not '#3')."""
    issues = load()
    for i in issues:
        if i["id"] == issue_id:
            i["status"] = "closed"
            save(issues)
            return f"Closed issue #{issue_id}."
    raise ValueError(f"Issue {issue_id} not found. "
                     f"Call list_issues(status='all') to see valid ids.")


if __name__ == "__main__":
    mcp.run()   # stdio transport by default