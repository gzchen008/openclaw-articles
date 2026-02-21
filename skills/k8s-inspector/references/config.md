# K8s Inspector Configuration Reference

## Configuration File Location

Default: `~/.openclaw/k8s-inspector.yaml`

Override with `--config` flag on scripts.

## Required Settings

### `kubeconfig`
**Type:** string  
**Required:** Yes

Path to your Kubernetes kubeconfig file. Must have read access to target namespace(s).

```yaml
kubeconfig: "/Users/me/.kube/config"
```

### `namespace`
**Type:** string  
**Required:** Yes

Namespace to monitor. Use `"all"` for cluster-wide monitoring.

```yaml
namespace: "production"     # Specific namespace
namespace: "all"            # All namespaces
```

## Event Watch Mode Configuration

### `events.enabled`
**Type:** boolean  
**Default:** `true`

Enable/disable real-time event watching.

### `events.watch_resources`
**Type:** list of strings  
**Default:** `["events", "pods"]`

Resources to watch for real-time events:
- `"events"` - Kubernetes Events API (Warning/Error events)
- `"pods"` - Pod status changes and container failures
- `"deployments"` - Deployment replica issues

### `events.severity`
**Type:** list of strings  
**Default:** `["Warning", "Error"]`

Filter events by severity type. Options:
- `"Normal"` - Normal operations
- `"Warning"` - Warning conditions
- `"Error"` - Error conditions

## Inspection Mode Configuration

### `inspection.enabled`
**Type:** boolean  
**Default:** `true`

Enable/disable periodic health inspection.

### `inspection.interval_minutes`
**Type:** integer  
**Default:** `30`

Documentation only - actual interval controlled by cron/scheduler.

### `inspection.checks`

Individual check toggles:

| Check | Description | Performance |
|-------|-------------|-------------|
| `pod_status` | Detect CrashLoopBackOff, Pending, Failed, OOMKilled | Fast |
| `restart_count` | Flag containers with >5 restarts | Fast |
| `deployment_health` | Check deployment replica status | Fast |
| `resource_usage` | Compare usage vs limits | Requires metrics-server |
| `probe_health` | Check probe failures | Requires metrics-server |

## Notification Configuration

### `notifications.compact`
**Type:** boolean  
**Default:** `false`

Send compact summaries instead of detailed messages.

### `notifications.include_yaml`
**Type:** boolean  
**Default:** `false`

Attach full resource YAML to notifications. Use with caution - can be very verbose.

### `notifications.max_events_per_batch`
**Type:** integer  
**Default:** `10`

Maximum events to include in a single notification batch.

### `notifications.cooldown_seconds`
**Type:** integer  
**Default:** `300`

Cooldown period between similar alerts to prevent notification spam.

### `notifications.group_by`
**Type:** list of strings  
**Default:** `["namespace", "severity"]`

Group alerts by these fields before sending.

## Example Configurations

### Minimal Config (Single Namespace)

```yaml
kubeconfig: "/Users/me/.kube/config"
namespace: "production"
```

### Full Cluster Monitoring

```yaml
kubeconfig: "/Users/me/.kube/config"
namespace: "all"

events:
  enabled: true
  watch_resources: ["events", "pods", "deployments"]
  severity: ["Warning", "Error"]

inspection:
  enabled: true
  checks:
    pod_status: true
    restart_count: true
    deployment_health: true
    resource_usage: false
    probe_health: false

notifications:
  compact: true
  cooldown_seconds: 600
```

### Events-Only Mode

```yaml
kubeconfig: "/Users/me/.kube/config"
namespace: "default"

events:
  enabled: true
  watch_resources: ["events"]
  severity: ["Error"]

inspection:
  enabled: false
```

### Inspection-Only Mode

```yaml
kubeconfig: "/Users/me/.kube/config"
namespace: "production"

events:
  enabled: false

inspection:
  enabled: true
  checks:
    pod_status: true
    restart_count: true
    deployment_health: true
```

## Security Notes

1. **Kubeconfig Permissions**: Ensure kubeconfig has appropriate RBAC permissions:
   - Read access to Pods, Deployments, Events
   - List and Get permissions

2. **Sensitive Data**: Resource YAML may contain secrets. Use `include_yaml: false` in production.

3. **API Rate Limits**: Watch mode maintains long-lived connections. Ensure your cluster can handle the watch load.

## Troubleshooting

### "Failed to list pods: Unauthorized"
Check kubeconfig permissions. Need at least:
```yaml
rules:
- apiGroups: [""]
  resources: ["pods", "events"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch"]
```

### No events being captured
- Check `events.severity` filter - may be too restrictive
- Verify `watch_resources` includes the resources you want
- Ensure namespace exists and has activity

### High memory usage
- Reduce `watch_resources` list
- Enable `notifications.compact`
- Reduce `max_events_per_batch`
