#!/usr/bin/env python3
"""
Push agent/sc1.png and agent/sc2.png to GitHub as proper binary blobs
so they render in the README. Uses Git Data API (blob with encoding base64).
Requires: GITHUB_TOKEN env var with 'repo' scope.
Usage: GITHUB_TOKEN=ghp_xxx python3 push_agent_images_to_github.py
"""
import base64
import json
import os
import sys
import urllib.request
import urllib.error

OWNER = "portal2anti"
REPO = "ExcelMCP-DEMO"
BRANCH = "main"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILES = ["agent/sc1.png", "agent/sc2.png"]


def api(method, url, data=None, token=None):
    token = token or os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Set GITHUB_TOKEN (e.g. export GITHUB_TOKEN=ghp_xxx)", file=sys.stderr)
        sys.exit(1)
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def main():
    base = f"https://api.github.com/repos/{OWNER}/{REPO}"

    ref = api("GET", f"{base}/git/ref/heads/{BRANCH}")
    commit_sha = ref["object"]["sha"]
    commit = api("GET", f"{base}/git/commits/{commit_sha}")
    tree_sha = commit["tree"]["sha"]

    tree_entries = []
    for path in FILES:
        file_full = os.path.join(SCRIPT_DIR, path)
        if not os.path.isfile(file_full):
            print(f"File not found: {file_full}", file=sys.stderr)
            sys.exit(1)
        with open(file_full, "rb") as f:
            content_b64 = base64.b64encode(f.read()).decode("ascii")
        blob = api(
            "POST",
            f"{base}/git/blobs",
            json.dumps({"content": content_b64, "encoding": "base64"}).encode(),
        )
        tree_entries.append({"path": path, "mode": "100644", "type": "blob", "sha": blob["sha"]})

    tree = api(
        "POST",
        f"{base}/git/trees",
        json.dumps({"base_tree": tree_sha, "tree": tree_entries}).encode(),
    )
    new_tree_sha = tree["sha"]

    new_commit = api(
        "POST",
        f"{base}/git/commits",
        json.dumps(
            {
                "tree": new_tree_sha,
                "parents": [commit_sha],
                "message": "Fix agent screenshots: store as binary PNGs for README",
            }
        ).encode(),
    )
    api("PATCH", f"{base}/git/refs/heads/{BRANCH}", json.dumps({"sha": new_commit["sha"]}).encode())

    print(f"Pushed {', '.join(FILES)} to https://github.com/{OWNER}/{REPO}")


if __name__ == "__main__":
    main()
