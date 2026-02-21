---
name: k8s-inspector
description: Kubernetes cluster health inspection with two modes - (1) Watch mode using Informer for real-time event push notifications on Pod/Deployment failures, restarts, and anomalies; (2) Scheduled inspection mode for periodic health reports on resource status, resource usage, and configuration issues. Use when users need to monitor k8s cluster health, receive alerts on container failures, or generate periodic health reports. Supports namespace-specific monitoring and uses OpenClaw messaging channels for notifications.
---

# K8s Inspector

## Overview

Kubernetes cluster health monitoring skill with dual operation modes:
- **Watch Mode**: Real-time event monitoring via Informer API
- **Inspection Mode**: Periodic health checks with comprehensive reports

Notifications are sent through OpenClaw's configured messaging channels.

## Prerequisites

- Valid kubeconfig file with cluster access permissions
- Python 3.9+ with kubernetes client library: `pip install kubernetes`
- OpenClaw messaging channel configured (Discord/Telegram/etc.)

## Configuration

Copy `assets/config.template.yaml` to `~/.openclaw/k8s-inspector.yaml` and customize:

```yaml
# Required
kubeconfig: "/path/to/your/kubeconfig"
namespace: "default"  # or "all" for cluster-wide

# Watch Mode - Event Push
events:
  enabled: true
  watch_resources: ["pods", "deployments"]
  severity: ["Warning", "Error"]  # Filter event types
  
# Inspection Mode - Periodic Check
inspection:
  enabled: true
  interval_minutes: 30
  checks:
    pod_status: true      # CrashLoopBackOff, Pending, OOMKilled
    restart_count: true   # Containers with high restart counts
    resource_usage: true  # CPU/Memory approaching limits
    probe_health: true    # Liveness/Readiness probe failures

# Notification Settings
notifications:
  # Uses OpenClaw message tool automatically
  # Optional: customize message format
  include_yaml: false     # Attach resource YAML to alerts
  max_events_per_batch: 10
```

See [references/config.md](references/config.md) for full configuration reference.

## Usage

### Start Watch Mode (Real-time Events)

```bash
python3 scripts/informer.py --config ~/.openclaw/k8s-inspector.yaml
```

Runs continuously, pushing k8s events matching configured filters.

### Run Inspection (One-time Report)

```bash
python3 scripts/inspector.py --config ~/.openclaw/k8s-inspector.yaml
```

Outputs health report to stdout and sends summary via OpenClaw message.

### Schedule Periodic Inspections

```bash
# Add to crontab for every 30 minutes
*/30 * * * * cd /path/to/skill && python3 scripts/inspector.py --config ~/.openclaw/k8s-inspector.yaml
```

Or use OpenClaw's cron tool for isolated execution.

## Inspection Check Details

### Pod Status Checks
- **CrashLoopBackOff**: Container failing repeatedly
- **ImagePullBackOff**: Cannot pull container image
- **Pending**: Pod stuck > 5 minutes
- **OOMKilled**: Container exceeded memory limit
- **Evicted**: Pod evicted due to resource pressure

### Restart Analysis
- Flag containers with > 5 restarts in 24h
- Include last termination reason

### Resource Utilization
- Compare request vs actual usage
- Alert when usage > 80% of limit

## Integration with OpenClaw

This skill is designed to be called by OpenClaw agent:

```python
# Example: Trigger inspection from OpenClaw
result = exec("python3 scripts/inspector.py", ...)
if result.has_issues:
    message.send(to="alerts-channel", message=result.summary)
```

The scripts output structured JSON that OpenClaw can parse and forward.

## Resources

- **scripts/informer.py**: Real-time k8s event watcher using Informer API
- **scripts/inspector.py**: Health inspection with comprehensive checks
- **assets/config.template.yaml**: Configuration template
- **references/config.md**: Full configuration documentation
