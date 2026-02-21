#!/bin/bash
# imsg-notify - Send iMessage/SMS notification
# Usage: notify.sh "message" [phone_number]

DEFAULT_RECIPIENT="+8618826243872"
MESSAGE="$1"
RECIPIENT="${2:-$DEFAULT_RECIPIENT}"

if [ -z "$MESSAGE" ]; then
  echo "Usage: notify.sh \"message\" [phone_number]"
  exit 1
fi

imsg send --to "$RECIPIENT" --text "$MESSAGE"
