# K8s Ops Bot Configuration Reference

## Overview

Complete reference for k8s-ops-bot configuration options.

## Configuration File Location

Default: `~/.openclaw/k8s-ops-bot.yaml`

Override with `--config` flag.

## Required Settings

### `kubeconfig`
**Type:** string  
**Required:** Yes

Path to Kubernetes kubeconfig file.

```yaml
kubeconfig: "/Users/me/.kube/config"
```

### `namespace`
**Type:** string  
**Required:** Yes

Namespace to monitor. Use `"all"` for cluster-wide monitoring.

```yaml
namespace: "production"
```

### `cluster_name`
**Type:** string  
**Required:** No (auto-detected)

Cluster identifier used in alerts and reports.

## Messaging Configuration

### `messaging.alert_channel`
**Type:** string  
**Default:** `"discord://k8s-alerts"`

OpenClaw channel for alert notifications. Format depends on your OpenClaw configuration.

Examples:
```yaml
alert_channel: "discord://k8s-alerts"
alert_channel: "telegram://ops-group"
alert_channel: "slack://#kubernetes"
```

### `messaging.command_channel`
**Type:** string  
**Default:** Same as alert_channel

Channel to listen for interactive commands.

### `messaging.compact`
**Type:** boolean  
**Default:** `false`

Use compact message format for alerts.

### `messaging.mention_on_critical`
**Type:** boolean  
**Default:** `true`

Mention users/roles on critical alerts.

## Watcher Configuration

### `watcher.enabled`
**Type:** boolean  
**Default:** `true`

Enable real-time event watching.

### `watcher.watch_resources`
**Type:** list of strings  
**Default:** `["events", "pods"]`

Resources to watch:
- `"events"` - Kubernetes Events API
- `"pods"` - Pod status changes
- `"deployments"` - Deployment status (future)

### `watcher.severity_filter`
**Type:** list of strings  
**Default:** `["Warning", "Error"]`

Filter events by type:
- `"Normal"` - Normal operations
- `"Warning"` - Warning conditions
- `"Error"` - Error conditions

### `watcher.alerting.cooldowns`
**Type:** map  
**Default:** See below

Cooldown periods to prevent alert spam:

```yaml
watcher:
  alerting:
    cooldowns:
      critical: 300    # 5 minutes
      high: 600        # 10 minutes
      warning: 1800    # 30 minutes
      info: 86400      # 24 hours
```

### `watcher.alerting.grouping`
**Type:** map  
**Default:** See below

Alert grouping configuration:

```yaml
watcher:
  alerting:
    grouping:
      enabled: true           # Enable grouping
      window_seconds: 60      # Group alerts within this window
      max_batch_size: 10      # Max alerts per batch
```

## Inspector Configuration

### `inspector.enabled`
**Type:** boolean  
**Default:** `true`

Enable periodic health inspection.

### `inspector.interval_minutes`
**Type:** integer  
**Default:** `30`

Documentation only - actual interval controlled by cron/scheduler.

### `inspector.checks`

Individual health checks:

| Check | Description | Performance |
|-------|-------------|-------------|
| `pod_status` | Detect CrashLoopBackOff, Pending, Failed | Fast |
| `restart_count` | Flag containers with >5 restarts | Fast |
| `deployment_health` | Check deployment replica status | Fast |
| `node_health` | Check node Ready status | Fast |
| `resource_usage` | Compare usage vs limits | Requires metrics-server |
| `probe_health` | Check probe failures | Requires metrics-server |

## Commander Configuration

### `commander.enabled`
**Type:** boolean  
**Default:** `true`

Enable interactive commands.

### `commander.authorization`

Optional access control:

```yaml
commander:
  authorization:
    allowed_users:          # Users allowed to run commands
      - "admin"
      - "ops-team"
    
    admin_users:            # Users with full access
      - "admin"
    
    restricted_commands:    # Commands requiring admin
      - "restart"
      - "scale"
      - "delete"
```

## Remediator Configuration

⚠️ **Use with caution!** Auto-remediation can have unintended side effects.

### `remediator.enabled`
**Type:** boolean  
**Default:** `false`

Enable auto-remediation engine.

### `remediator.auto_fix`
**Type:** boolean  
**Default:** `false`

Automatically apply fixes without confirmation.

### `remediator.auto_fix_severity`
**Type:** list of strings  
**Default:** `["critical"]`

Severities to auto-fix (if auto_fix is enabled).

### `remediator.require_confirm_for`
**Type:** list of strings  
**Default:** `["restart", "scale", "delete", "patch"]`

Actions that always require confirmation, even with auto_fix enabled.

### `remediator.playbooks_dir`
**Type:** string  
**Default:** `"./assets/playbooks"`

Directory containing remediation playbooks.

## Advanced Settings

### `advanced.api_timeout`
**Type:** integer  
**Default:** `30`

Kubernetes API request timeout in seconds.

### `advanced.retries`
**Type:** integer  
**Default:** `3`

Number of retry attempts for failed API calls.

### `advanced.retry_delay`
**Type:** integer  
**Default:** `5`

Delay between retries in seconds.

### `advanced.log_level`
**Type:** string  
**Default:** `"INFO"`

Log level: `DEBUG`, `INFO`, `WARNING`, `ERROR`.

## Example Configurations

### Development Environment

```yaml
kubeconfig: "/Users/dev/.kube/config"
namespace: "default"

watcher:
  enabled: true
  severity_filter: ["Error"]  # Only critical errors

inspector:
  enabled: false  # Manual runs only

commander:
  enabled: true
  # No auth restrictions in dev
```

### Production Environment

```yaml
kubeconfig: "/etc/kubernetes/admin.conf"
namespace: "all"

messaging:
  alert_channel: "discord://prod-alerts"
  mention_on_critical: true

watcher:
  enabled: true
  alerting:
    cooldowns:
      critical: 600    # 10 min in prod
      high: 1800       # 30 min
      warning: 3600    # 1 hour

inspector:
  enabled: true
  checks:
    pod_status: true
    restart_count: true
    deployment_health: true
    node_health: true

commander:
  enabled: true
  authorization:
    allowed_users: ["admin", "sre-team"]
    admin_users: ["admin"]
    restricted_commands: ["restart", "scale", "delete"]

remediator:
  enabled: false  # Manual approval only in prod
```

### Minimal Monitoring Only

```yaml
kubeconfig: "/Users/me/.kube/config"
namespace: "production"

watcher:
  enabled: true
  watch_resources: ["events"]
  severity_filter: ["Error"]

inspector:
  enabled: true
  checks:
    pod_status: true
    deployment_health: true

commander:
  enabled: false

remediator:
  enabled: false
```

## Security Best Practices

1. **Kubeconfig Permissions**: Use dedicated service account with minimal RBAC
2. **Command Authorization**: Always configure `allowed_users` in production
3. **Auto-remediation**: Keep disabled or use with extreme caution
4. **Network**: Ensure bot can reach k8s API but is isolated from workloads

## Troubleshooting

### "Failed to list pods: Unauthorized"
Check RBAC permissions for the kubeconfig user.

### Alerts not being sent
Verify `alert_channel` is correctly configured in OpenClaw.

### Commands not working
Check that `command_channel` matches where you're sending commands.

### Too many alerts
Increase cooldown periods or enable grouping.
