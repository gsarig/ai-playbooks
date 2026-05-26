#!/usr/bin/env bash
# Evaluates URLs queued in resources/tmp/ and writes reviews to resources/reviews/.
# Cron runs it every 5 minutes. A flock guard ensures only one instance runs at a
# time: if a run is still going when the next fires, the new one exits immediately.
# This prevents overlapping runs from processing the same queued file twice (a file
# is only removed at the end of its evaluation, so it stays visible to other runs).

REPO_DIR="/mnt/d/ai-playbooks"
TMP_DIR="$REPO_DIR/resources/tmp"
LOG="$HOME/resource_evaluator.log"
CLAUDE="/home/gsarig/.local/bin/claude"
LOCK="$HOME/.evaluate_resources.lock"

# Take a non-blocking lock so an overlapping run exits immediately. The lock lives
# on the Linux filesystem because advisory locking is unreliable on the /mnt/d
# DrvFs mount, and flock releases it automatically on exit, so a crash leaves no
# stale lock behind.
exec 200>"$LOCK"
flock -n 200 || exit 0

cd "$REPO_DIR" || exit 1

# Rename any queued files whose names contain emoji or other non-ASCII
# characters. WSL's 9P bridge throws an I/O error when listing directories
# that contain such filenames, which makes the glob below silently return
# zero matches and skip processing.
/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -NoProfile -ExecutionPolicy Bypass \
    -File "$(wslpath -w "$REPO_DIR/scripts/sanitize_tmp.ps1")" >/dev/null 2>&1

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
