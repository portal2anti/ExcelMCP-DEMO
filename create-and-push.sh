#!/bin/bash
# Create excel-mcp-demo on GitHub and push this repo. Requires a GitHub personal access token.
# Usage: GITHUB_TOKEN=your_token ./create-and-push.sh
# Or:   ./create-and-push.sh   (will prompt for token)
set -e
cd "$(dirname "$0")"

REPO="excel-mcp-demo"

if [ -z "$GITHUB_TOKEN" ]; then
  echo "Paste your GitHub personal access token (with 'repo' scope):"
  read -s GITHUB_TOKEN
  echo
fi
if [ -z "$GITHUB_TOKEN" ]; then
  echo "Need GITHUB_TOKEN. Create one at: https://github.com/settings/tokens"
  exit 1
fi

USERNAME=$(curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user | grep '"login"' | head -1 | sed 's/.*"login": *"\([^"]*\)".*/\1/')
if [ -z "$USERNAME" ]; then
  echo "Failed to get GitHub username. Check your token."
  exit 1
fi

echo "Creating repo $USERNAME/$REPO..."
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos -d "{\"name\":\"$REPO\",\"description\":\"FP&A test data, capacity scenario, Power Query demo\"}" >/dev/null

echo "Pushing to origin..."
git remote set-url origin "https://${GITHUB_TOKEN}@github.com/${USERNAME}/${REPO}.git"
git push -u origin main

# Remove token from remote URL for future pushes
git remote set-url origin "https://github.com/${USERNAME}/${REPO}.git"

echo "Done. Share: https://github.com/${USERNAME}/${REPO}"
