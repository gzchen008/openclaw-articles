# K8s Ops Bot Troubleshooting Guide

## Installation Issues

### "kubernetes client not installed"

**Symptom:**
```
Error: kubernetes client not installed. Run: pip install kubernetes
```

**Solution:**
```bash
pip install kubernetes pyyaml
```

### "Failed to load kubeconfig"

**Symptom:**
```
Error: kubeconfig not specified or invalid
```

**Solution:**
1. Verify kubeconfig path:
   ```bash
   ls -la ~/.kube/config
   ```
2. Set correct path in config:
   ```yaml
   kubeconfig: "/Users/YOUR_USERNAME/.kube/config"
   ```

## Connection Issues

### "Failed to list pods: Unauthorized"

**Symptom:** API calls return 403 Forbidden

**Solution:**
1. Check current context:
   ```bash
   kubectl config current-context
   ```
2. Verify permissions:
   ```bash
   kubectl auth can-i list pods
   ```
3. Apply RBAC for bot service account:
   ```yaml
   apiVersion: rbac.authorization.k8s.io/v1
   kind: ClusterRole
   metadata:
     name: k8s-ops-bot
   rules:
   - apiGroups: ["", "apps", "events.k8s.io"]
     resources: ["pods", "deployments", "services", "events", "nodes"]
     verbs: ["get", "list", "watch"]
   - apiGroups: ["apps"]
     resources: ["deployments/scale"]
     verbs: ["patch", "update"]
   ```

### "Connection refused" to k8s API

**Symptom:**
```
urllib3.exceptions.MaxRetryError: HTTPConnectionPool(host='localhost', port=8080)
```

**Solution:**
1. Ensure kubeconfig has correct server URL
2. Check network connectivity to API server
3. Verify no firewall blocking port 6443

## Runtime Issues

### No alerts being sent

**Symptom:** Bot runs but no notifications received

**Diagnostics:**
1. Check log level:
   ```yaml
   advanced:
     log_level: "DEBUG"
   ```
2. Verify alert channel configuration:
   ```yaml
   messaging:
     alert_channel: "discord://CORRECT_CHANNEL"
   ```
3. Check OpenClaw message tool is working

### Too many duplicate alerts

**Symptom:** Same alert sent repeatedly

**Solution:**
1. Increase cooldown periods:
   ```yaml
   watcher:
     alerting:
       cooldowns:
         critical: 600    # Increase from 300
         high: 1800
         warning: 3600
   ```
2. Enable grouping:
   ```yaml
   watcher:
     alerting:
       grouping:
         enabled: true
         window_seconds: 120
   ```

### Commands not responding

**Symptom:** `/k8s status` doesn't return anything

**Solution:**
1. Verify commander is enabled:
   ```yaml
   commander:
     enabled: true
   ```
2. Check command channel matches where you're typing
3. Check authorization:
   ```yaml
   commander:
     authorization:
       allowed_users: ["YOUR_USERNAME"]  # Add your user
   ```

### High memory/CPU usage

**Symptom:** Bot consuming excessive resources

**Solutions:**
1. Reduce watch scope:
   ```yaml
   namespace: "specific-ns"  # Instead of "all"
   ```
2. Limit watched resources:
   ```yaml
   watcher:
     watch_resources: ["events"]  # Only critical events
   ```
3. Increase inspection interval
4. Check for memory leaks in logs

## Specific Error Messages

### "ImagePullBackOff" alerts but images exist

**Possible causes:**
1. Registry authentication issues
2. Network connectivity to registry
3. Wrong image tag in deployment

**Diagnosis:**
```bash
kubectl describe pod POD_NAME
kubectl get events --field-selector reason=Failed
```

### "Pending" pods never scheduled

**Possible causes:**
1. Insufficient node resources
2. Node selector/affinity constraints
3. Taints without tolerations
4. PVC not bound

**Diagnosis:**
```bash
kubectl describe pod POD_NAME
kubectl get nodes -o yaml | grep -A5 "allocatedResources"
```

### Metrics not available

**Symptom:** `/k8s top` returns error

**Solution:**
1. Install metrics-server:
   ```bash
   kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
   ```
2. Wait for metrics to populate (1-2 minutes)
3. Verify:
   ```bash
   kubectl top nodes
   ```

## Performance Tuning

### Optimizing for large clusters

```yaml
# Reduce API load
namespace: "specific-namespace"  # Don't watch "all"

watcher:
  watch_resources: ["events"]  # Events cover most issues
  
inspector:
  checks:
    pod_status: true
    restart_count: false       # Skip expensive checks
    node_health: false         # Run separately

advanced:
  api_timeout: 60
  max_concurrent_requests: 5
```

### Optimizing alert noise

```yaml
watcher:
  severity_filter: ["Error"]   # Only critical errors
  alerting:
    cooldowns:
      critical: 900     # 15 minutes
      high: 3600        # 1 hour
      warning: 7200     # 2 hours
    grouping:
      enabled: true
      window_seconds: 300    # 5 minute batches
```

## Debugging

### Enable debug logging

```yaml
advanced:
  log_level: "DEBUG"
```

### Run single inspection

```bash
python3 scripts/bot.py --config config.yaml --once
```

### Test specific command

```bash
python3 scripts/bot.py --config config.yaml --command "/k8s status"
```

### Check bot health

```bash
# If running as systemd
systemctl status k8s-ops-bot

# View logs
journalctl -u k8s-ops-bot -f
```

## Getting Help

1. Check logs for detailed error messages
2. Verify configuration with `--once` mode
3. Test API connectivity with kubectl
4. Review OpenClaw message tool configuration

## Common Patterns

### Restart bot after config changes

```bash
# If running as systemd
sudo systemctl restart k8s-ops-bot

# If running manually
Ctrl+C  # Stop
python3 scripts/bot.py --config config.yaml --daemon  # Restart
```

### Temporary disable alerts

```yaml
# In config
watcher:
  enabled: false
inspector:
  enabled: false
```

Or use maintenance mode (future feature).
