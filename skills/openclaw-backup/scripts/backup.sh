#!/usr/bin/env bash
# OpenClaw Backup Script
# Usage: backup.sh [auto|full|workspace|config|db] [--keep DAYS]
set -euo pipefail

KEEP_DAYS="${KEEP_DAYS:-7}"
BACKUP_DIR="${BACKUP_DIR:-$HOME/.openclaw/backups}"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
MODE="${1:-auto}"

mkdir -p "$BACKUP_DIR"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }

get_size() {
  if command -v du &>/dev/null; then
    du -sh "$1" 2>/dev/null | cut -f1
  else
    echo "unknown"
  fi
}

backup_workspace() {
  local dest="$BACKUP_DIR/workspace-${TIMESTAMP}.tar.gz"
  log "📦 Backing up workspace..."
  tar -czf "$dest" -C "$HOME/.openclaw" workspace/ 2>/dev/null || true
  log "✅ Workspace backup: $(get_size "$dest")"
  echo "$dest"
}

backup_config() {
  local dest="$BACKUP_DIR/config-${TIMESTAMP}.tar.gz"
  log "📦 Backing up config..."
  # 只备份配置文件，排除 workspace/sessions（可能很大）
  tar -czf "$dest" -C "$HOME/.openclaw" \
    openclaw.json extensions/ \
    $(find agents -maxdepth 2 -name 'agent' -type d 2>/dev/null | sed 's|^|agents/|') \
    $(find agents -maxdepth 1 -name 'SOUL.md' 2>/dev/null | sed 's|^|agents/|') \
    2>/dev/null || true
  log "✅ Config backup: $(get_size "$dest")"
  echo "$dest"
}

backup_db() {
  local src="$HOME/.openclaw"
  local dest="$BACKUP_DIR/db-${TIMESTAMP}.tar.gz"
  log "📦 Backing up databases & sessions..."
  tar -czf "$dest" -C "$src" \
    sessions/ sessions.sqlite tasks/ memory/ 2>/dev/null || true
  log "✅ DB backup: $(get_size "$dest")"
  echo "$dest"
}

backup_full() {
  local dest="$BACKUP_DIR/full-${TIMESTAMP}.tar.gz"
  log "📦 Full backup (excluding node_modules/cache)..."
  tar -czf "$dest" -C "$HOME" .openclaw/ \
    --exclude='.openclaw/node_modules' \
    --exclude='.openclaw/.cache' \
    --exclude='.openclaw/backups' \
    --exclude='.openclaw/agents/*/sessions' \
    2>/dev/null || true
  log "✅ Full backup: $(get_size "$dest")"
  echo "$dest"
}

cleanup() {
  log "🧹 Cleaning up backups older than ${KEEP_DAYS} days..."
  local count=0
  if command -v find &>/dev/null; then
    count=$(find "$BACKUP_DIR" -name '*.tar.gz' -mtime +$KEEP_DAYS -delete -print 2>/dev/null | wc -l | tr -d ' ')
  fi
  log "🧹 Removed $count old backup(s)"
}

# Main
case "$MODE" in
  auto)
    backup_workspace
    backup_config
    backup_db
    cleanup
    ;;
  full)
    backup_full
    cleanup
    ;;
  workspace) backup_workspace ;;
  config) backup_config ;;
  db) backup_db ;;
  *)
    echo "Usage: backup.sh [auto|full|workspace|config|db] [--keep DAYS]"
    exit 1
    ;;
esac

log "🎉 Backup complete"
