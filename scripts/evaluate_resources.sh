#!/usr/bin/env bash
# Evaluates URLs queued in resources/tmp/ and writes reviews to resources/reviews/.
# Safe to call as often as needed (cron runs it every 5 minutes).

REPO_DIR="/mnt/d/ai-playbooks"
TMP_DIR="$REPO_DIR/resources/tmp"
LOG="$HOME/resource_evaluator.log"
CLAUDE="/home/gsarig/.local/bin/claude"

cd "$REPO_DIR" || exit 1

shopt -s nullglob
files=("$TMP_DIR"/*.md)

# Filter out the README
pending=()
for f in "${files[@]}"; do
  [[ "$(basename "$f")" == "README.md" ]] && continue
  pending+=("$f")
done

if [ ${#pending[@]} -eq 0 ]; then
  exit 0
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Found ${#pending[@]} file(s) to process." >> "$LOG"

for file in "${pending[@]}"; do
  filename=$(basename "$file")
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Processing: $filename" >> "$LOG"

  "$CLAUDE" --dangerously-skip-permissions \
    -p "Process the queued resource at resources/tmp/$filename using the evaluate-resource-auto skill." \
    >> "$LOG" 2>&1

  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Done: $filename" >> "$LOG"
done
