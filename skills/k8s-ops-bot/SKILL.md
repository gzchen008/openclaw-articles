---
name: k8s-ops-bot
description: Kubernetes operations bot that integrates deeply with OpenClaw for automated monitoring, alerting, and interactive cluster management. Provides real-time event monitoring via Informer, scheduled health inspections, interactive commands via messaging (/status, /logs, /restart), auto-remediation suggestions, and intelligent alert grouping. Use when users need a comprehensive k8s operations assistant that can monitor clusters, respond to incidents, and provide interactive cluster management through OpenClaw's messaging channels.
---

# K8s Ops Bot

## Overview

A Kubernetes operations robot deeply integrated with OpenClaw messaging system.

**Core Capabilities:**
1. **Real-time Monitoring** - Informer-based event watching with intelligent alert grouping
2. **Interactive Commands** - Query and control cluster via chat messages
3. **Auto-Inspection** - Scheduled health reports with trend analysis
4. **Smart Remediation** - Auto-suggest or execute fixes for common issues
5. **Incident Management** - Alert correlation, escalation, and resolution tracking

## Quick Start

### 1. Install Dependencies

```bash
pip install kubernetes pyyaml
```

### 2. Configure

Copy and customize:
```bash
cp assets/config.template.yaml ~/.openclaw/k8s-ops-bot.yaml
# Edit: set kubeconfig path and notification channel
```

### 3. Start the Bot

```bash
# Background daemon mode
python3 scripts/bot.py --config ~/.openclaw/k8s-ops-bot.yaml --daemon

# Or run via OpenClaw
openclaw run k8s-ops-bot --config ~/.openclaw/k8s-ops-bot.yaml
```

## Interactive Commands

Send commands via configured OpenClaw channel:

| Command | Description | Example |
|---------|-------------|---------|
| `/k8s status` | Cluster health summary | `/k8s status` |
| `/k8s pods [namespace]` | List problematic pods | `/k8s pods production` |
| `/k8s logs <pod>` | Get recent logs | `/k8s logs nginx-abc123` |
| `/k8s events` | Recent warning events | `/k8s events --last=1h` |
| `/k8s top` | Resource usage top list | `/k8s top --namespace=all` |
| `/k8s restart <deployment>` | Rolling restart | `/k8s restart api-gateway` |
| `/k8s scale <deploy> <replicas>` | Scale deployment | `/k8s scale worker 5` |
| `/k8s describe <resource>` | Detailed resource info | `/k8s describe pod/nginx-abc` |

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    K8s Ops Bot                          │
├─────────────┬─────────────┬─────────────┬───────────────┤
│   Watcher   │  Inspector  │   Handler   │  Commander    │
│  (Informer) │  (Periodic) │ (Alert Mgr) │  (Interactive)│
├─────────────┴─────────────┴─────────────┴───────────────┤
│              OpenClaw Message Integration               │
│         (send alerts, receive commands)                 │
└─────────────────────────────────────────────────────────┘
```

### Components

- **scripts/bot.py** - Main controller, orchestrates all components
- **scripts/watcher.py** - Real-time k8s event watcher
- **scripts/inspector.py** - Periodic health inspection
- **scripts/commander.py** - Interactive command handler
- **scripts/remediator.py** - Auto-remediation engine
- **assets/playbooks/** - Remediation playbooks for common issues

## Alert Management

### Severity Levels

| Level | Trigger | Action | Cooldown |
|-------|---------|--------|----------|
| **P0-Critical** | Pod CrashLoopBackOff, NodeNotReady | Immediate alert + mention | 5min |
| **P1-High** | ImagePullBackOff, OOMKilled | Alert within 1min | 10min |
| **P2-Medium** | High restart count, Pending pods | Batch in summary | 30min |
| **P3-Low** | Resource pressure warnings | Daily digest | 24h |

### Alert Grouping

Related alerts are automatically grouped:
- Same deployment replicas failing → Single grouped alert
- Multiple pods on same node failing → Node issue alert
- ImagePullBackOff from same registry → Registry issue alert

### Smart Deduplication

- Identical alerts within cooldown → Suppressed
- Flapping pods (rapid restart) → Single alert with count
- Recovering alerts → Send recovery notification

## Auto-Remediation

Enabled via `remediation.enabled: true` in config.

### Supported Actions

| Issue | Auto-Action | Manual Confirm Required |
|-------|-------------|------------------------|
| OOMKilled | Suggest memory limit increase | Yes |
| ImagePullBackOff | Check registry connectivity | No (diagnose only) |
| High restarts | Suggest describe logs | No |
| Pending (resource) | Suggest node scaling | Yes |
| Failed probe | Suggest probe adjustment | Yes |

### Playbook System

Custom remediation logic in `assets/playbooks/`:

```yaml
# assets/playbooks/oom-killed.yaml
name: "OOM Killed Recovery"
triggers:
  - reason: "OOMKilled"
actions:
  - type: "analyze"
    cmd: "get_memory_usage"
  - type: "suggest"
    message: "Consider increasing memory limit to {{ recommended }}Mi"
  - type: "confirm"
    cmd: "patch_resource"
    params:
      path: "/spec/template/spec/containers/0/resources/limits/memory"
      value: "{{ recommended }}Mi"
```

## Integration with OpenClaw

### Receiving Commands

The bot listens for messages matching `/k8s <command>` pattern via OpenClaw's message system.

Example OpenClaw integration:
```python
# In OpenClaw skill handler
if message.content.startswith("/k8s"):
    result = bot.execute_command(message.content)
    message.reply(result)
```

### Sending Alerts

Alerts are sent via OpenClaw's message tool:
```python
# Bot internally calls
message.send(
    channel=config.alert_channel,
    content=format_alert(alert),
    mention_on_critical=True
)
```

## Configuration

See [references/config.md](references/config.md) for complete reference.

Key settings:
- `kubeconfig` - Path to kubeconfig
- `alert_channel` - OpenClaw channel for alerts
- `command_channel` - Channel to listen for commands
- `remediation.enabled` - Enable auto-remediation
- `alerting.cooldowns` - Alert cooldown periods

## Deployment Patterns

### As OpenClaw Skill

```bash
# Package and install
openclaw skill install k8s-ops-bot.skill

# Configure in OpenClaw
openclaw config set k8s-ops-bot.kubeconfig=/path/to/config
openclaw config set k8s-ops-bot.alert_channel=discord://alerts

# Start
openclaw run k8s-ops-bot
```

### As Standalone Daemon

```bash
# Systemd service
sudo cp assets/k8s-ops-bot.service /etc/systemd/system/
sudo systemctl enable k8s-ops-bot
sudo systemctl start k8s-ops-bot
```

### As Kubernetes Deployment

See `assets/k8s-deployment.yaml` for running the bot inside the cluster.

## Security

### RBAC Requirements

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: k8s-ops-bot
rules:
  # Read access for monitoring
  - apiGroups: ["", "apps", "events.k8s.io"]
    resources: ["pods", "deployments", "services", "events", "nodes"]
    verbs: ["get", "list", "watch"]
  # Write access for remediation (optional)
  - apiGroups: ["apps"]
    resources: ["deployments/scale", "deployments"]
    verbs: ["patch", "update"]
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["delete"]  # For pod restart
```

### Command Authorization

Restrict interactive commands by user:
```yaml
authorization:
  allowed_users: ["admin", "ops-team"]
  restricted_commands: ["restart", "scale", "delete"]
```

## Troubleshooting

See [references/troubleshooting.md](references/troubleshooting.md) for common issues.

## Development

### Adding New Commands

1. Add handler in `scripts/commander.py`
2. Register in `COMMAND_REGISTRY`
3. Update this documentation

### Adding Remediation Playbooks

1. Create YAML in `assets/playbooks/`
2. Define triggers and actions
3. Test with `--dry-run`

## Resources

- **scripts/bot.py** - Main bot controller
- **scripts/watcher.py** - Event watcher with Informer
- **scripts/inspector.py** - Health inspection engine
- **scripts/commander.py** - Interactive command handler
- **scripts/remediator.py** - Auto-remediation engine
- **assets/config.template.yaml** - Configuration template
- **assets/playbooks/** - Remediation playbooks
- **references/config.md** - Configuration reference
- **references/troubleshooting.md** - Troubleshooting guide
