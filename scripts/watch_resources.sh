#!/usr/bin/env bash
# Watches ~/resource-tmp/ for new clipped files and triggers evaluation immediately.
# Runs as a persistent background service (started via cron @reboot).

WATCH_DIR="$HOME/resource-tmp"
SCRIPT="/mnt/d/ai-playbooks/scripts/evaluate_resources.sh"
LOG="$HOME/resource_evaluator.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Watcher started on $WATCH_DIR" >> "$LOG"

inotifywait -m -e close_write,moved_to --format '%f' "$WATCH_DIR" 2>/dev/null \
| while read -r filename; do
  [[ "$filename" == *.md ]] || continue
  [[ "$filename" == "README.md" ]] && continue
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] inotify: $filename" >> "$LOG"
  "$SCRIPT"
done
