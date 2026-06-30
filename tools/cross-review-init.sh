#!/usr/bin/env bash
# cross-review-init.sh — scaffold the .cross-review/ handoff folder in the current project.
# Usage: bash tools/cross-review-init.sh <task-slug>
# Works the same from any terminal agent. Idempotent.
#
# Templates are resolved relative to this script (../templates/cross-review), so cloning the
# dual-agent-review repo and running tools/cross-review-init.sh works with no configuration.
set -euo pipefail

SLUG="${1:-}"
if [[ -z "$SLUG" ]]; then
  echo "usage: cross-review-init.sh <task-slug>" >&2
  exit 1
fi
# normalize slug to safe kebab-case
SLUG="$(echo "$SLUG" | tr '[:upper:] ' '[:lower:]-' | tr -cd 'a-z0-9-')"

# project root: top of the git repo if any, else the current directory
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
CR="$ROOT/.cross-review"

# templates: relative to this script, with a couple of fallbacks
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
TPL=""
for cand in "$SCRIPT_DIR/../templates/cross-review" "$SCRIPT_DIR/templates/cross-review" "$HOME/dual-agent-review/templates/cross-review"; do
  if [[ -d "$cand" ]]; then TPL="$cand"; break; fi
done

mkdir -p "$CR"

# protocol README at the folder root
if [[ ! -f "$CR/README.md" ]]; then
  if [[ -n "$TPL" && -f "$TPL/README.md" ]]; then
    cp "$TPL/README.md" "$CR/README.md"
  else
    echo "# .cross-review/ — handoff between two terminal agents. See PROTOCOL.md." > "$CR/README.md"
  fi
fi

# ensure .cross-review/ is gitignored (only if this is a git repo)
if git -C "$ROOT" rev-parse --git-dir >/dev/null 2>&1; then
  GI="$ROOT/.gitignore"
  if ! { [[ -f "$GI" ]] && grep -qxF '/.cross-review/' "$GI"; }; then
    printf '\n# cross-agent review handoff — local scratch\n/.cross-review/\n' >> "$GI"
    echo "-> added '/.cross-review/' to .gitignore"
  fi
fi

# next sequential number NN
N=1
while ls -d "$CR"/$(printf '%02d' "$N")-* >/dev/null 2>&1; do N=$((N+1)); done
DIR="$CR/$(printf '%02d' "$N")-$SLUG"

if [[ -d "$DIR" ]]; then
  echo "already exists: $DIR"
  exit 0
fi
mkdir -p "$DIR"

DATE="$(date +%Y-%m-%d)"
# 00-request.md from the template, with slug/date filled in
if [[ -n "$TPL" && -f "$TPL/00-request.md" ]]; then
  sed -e "s/^task: .*/task: $SLUG/" -e "s/^date: .*/date: $DATE/" "$TPL/00-request.md" > "$DIR/00-request.md"
else
  cat > "$DIR/00-request.md" <<EOF
---
task: $SLUG
date: $DATE
executor: claude | gemini
reviewer: gemini | claude
status: proposed
---

# Request
EOF
fi

echo "-> created: $DIR/00-request.md"
echo "Protocol: see PROTOCOL.md in the dual-agent-review repo"
