# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

### 📡 Tailscale - 远程访问 VPN

**用途**：在任何地方访问 Mac mini（无需公网 IP）

**设备列表**：
| 设备 | Tailscale IP | 说明 |
|------|-------------|------|
| cgzmac-mini | `100.71.105.40` | Mac mini（本机） |
| cgzmbp14 | `100.70.66.73` | MacBook Pro |

**常用命令**：
```bash
# 启动 Tailscale App（首次需要登录）
open /Applications/Tailscale.app

# 连接 VPN
tailscale up

# 查看状态
tailscale status

# 查看本机 IP
tailscale ip

# 关闭连接
tailscale down
```

**远程访问方式**：
```bash
# SSH 连接
ssh cgz@100.71.105.40

# 屏幕共享（VNC）
open vnc://100.71.105.40
```

**注意**：
- 不需要 sudo，直接用 `tailscale up/down`
- 两台设备需登录同一 Tailscale 账号
- 账号：cgznzb@（记不清完整邮箱，登录时查看）

---

Add whatever helps you do your job. This is your cheat sheet.
