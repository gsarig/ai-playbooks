#!/usr/bin/env bash
# Process watchlist and ratings queues for the Watchlog vault.
# Safe to call as often as needed — exits immediately when both queues are empty.
#
# Set WATCHLOG_VAULT to your vault path, or edit VAULT below.
# Example crontab entry (every 15 minutes):
#   */15 * * * * WATCHLOG_VAULT=/path/to/watchlog /path/to/watchlog/scripts/watchlog_queue.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT="${WATCHLOG_VAULT:-$(dirname "$SCRIPT_DIR")}"
LOG="$HOME/watchlog_queue.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting queue processing." >> "$LOG"

cd "$VAULT" || { echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: vault not found at $VAULT." >> "$LOG"; exit 1; }

/usr/bin/python3 scripts/process_queues.py >> "$LOG" 2>&1 || { echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: process_queues.py failed." >> "$LOG"; exit 1; }

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Done." >> "$LOG"
