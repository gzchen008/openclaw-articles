---
name: imsg-notify
description: Send iMessage/SMS notifications to predefined contacts. Use when you need to send alerts, reminders, or notifications via iMessage or SMS on macOS.
---

# iMessage Notify

Send notifications via iMessage/SMS on macOS.

## Prerequisites

- Messages.app signed in
- Full Disk Access for terminal
- `imsg` CLI installed (`brew install steipete/tap/imsg`)

## Quick Send

```bash
# Send to phone number
imsg send --to "+8618826243872" --text "Your message here"

# Send to email (iMessage)
imsg send --to "user@example.com" --text "Your message here"
```

## Script Helper

For predefined recipients, use the bundled script:

```bash
# Send notification (uses default recipient from config)
scripts/notify.sh "你的通知内容"

# Send to specific recipient
scripts/notify.sh "消息内容" "+8618826243872"
```

## Notes

- Use `--service imessage|sms|auto` to control delivery method
- Messages are sent from the signed-in Apple ID
