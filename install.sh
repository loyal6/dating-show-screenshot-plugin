#!/usr/bin/env sh
set -eu

REPO_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

python3 -m pip install -r "$REPO_ROOT/requirements.txt"

if ! command -v codex >/dev/null 2>&1; then
  echo "Codex CLI is required. Install it, then rerun this script." >&2
  exit 1
fi

codex plugin marketplace add "$REPO_ROOT"
codex plugin add "dating-show-screenshot@dating-show-screenshot"

echo "Installed dating-show-screenshot."
