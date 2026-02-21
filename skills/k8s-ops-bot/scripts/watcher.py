#!/usr/bin/env python3
"""
K8s Watcher - Real-time event monitoring with Informer-like behavior.
Integrates with MessageBus for OpenClaw notifications.
"""

import json
import logging
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict

try:
    from kubernetes import client, config, watch
    from kubernetes.client.exceptions import ApiException
except ImportError:
    raise ImportError("kubernetes client not installed. Run: pip install kubernetes")

logger = logging.getLogger('k8s-ops-bot.watcher')


@dataclass
class K8sEvent:
    event_type: str      # ADDED, MODIFIED, DELETED
    resource_type: str
    resource_name: str
    namespace: str
    reason: str
    message: str
    severity: str
    timestamp: str
    cluster: str
    raw_object: Optional[Dict] = None
    
    def to_alert(self) -> Dict:
        """Convert to alert format for MessageBus."""
        return {
            "type": "k8s_event",
            "title": f"{self.event_type}: {self.resource_type}/{self.resource_name}",
            "severity": self.severity,
            "resource_type": self.resource_type,
            "resource_name": self.resource_name,
            "namespace": self.namespace,
            "message": self.message,
            "timestamp": self.timestamp,
            "cluster": self.cluster,
            "reason": self.reason
        }


class AlertManager:
    """Manages alert deduplication, grouping, and cooldown."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.cooldowns: Dict[str, float] = {}
        self.alert_history: List[Dict] = []
        self.pending_alerts: List[K8sEvent] = []
        self.last_batch_time = time.time()
        
        # Cooldown periods by severity (seconds)
        self.cooldown_periods = {
            "critical": config.get('cooldowns', {}).get('critical', 300),    # 5min
            "high": config.get('cooldowns', {}).get('high', 600),           # 10min
            "warning": config.get('cooldowns', {}).get('warning', 1800),    # 30min
            "info": config.get('cooldowns', {}).get('info', 86400)          # 24h
        }
        
        # Grouping configuration
        self.grouping_enabled = config.get('grouping', {}).get('enabled', True)
        self.grouping_window = config.get('grouping', {}).get('window_seconds', 60)
        self.max_batch_size = config.get('grouping', {}).get('max_batch_size', 10)
    
    def _get_alert_key(self, event: K8sEvent) -> str:
        """Generate unique key for alert deduplication."""
        return f"{event.namespace}/{event.resource_type}/{event.resource_name}/{event.reason}"
    
    def should_alert(self, event: K8sEvent) -> bool:
        """Check if alert should be sent (cooldown check)."""
        key = self._get_alert_key(event)
        now = time.time()
        cooldown = self.cooldown_periods.get(event.severity, 300)
        
        if key in self.cooldowns:
            if now - self.cooldowns[key] < cooldown:
                logger.debug(f"Alert suppressed (cooldown): {key}")
                return False
        
        self.cooldowns[key] = now
        return True
    
    def add_event(self, event: K8sEvent) -> Optional[List[K8sEvent]]:
        """
        Add event to alert manager.
        Returns batch of alerts if grouping window expired or batch full.
        """
        # Check cooldown
        if not self.should_alert(event):
            return None
        
        self.pending_alerts.append(event)
        
        # Check if should flush
        now = time.time()
        should_flush = (
            len(self.pending_alerts) >= self.max_batch_size or
            (now - self.last_batch_time) >= self.grouping_window
        )
        
        if should_flush and self.pending_alerts:
            batch = self.pending_alerts[:]
            self.pending_alerts = []
            self.last_batch_time = now
            return batch
        
        return None
    
    def flush(self) -> List[K8sEvent]:
        """Force flush pending alerts."""
        batch = self.pending_alerts[:]
        self.pending_alerts = []
        self.last_batch_time = time.time()
        return batch
    
    def group_alerts(self, alerts: List[K8sEvent]) -> List[Dict]:
        """Group related alerts together."""
        if not self.grouping_enabled:
            return [a.to_alert() for a in alerts]
        
        # Group by namespace and issue type
        groups: Dict[str, List[K8sEvent]] = {}
        
        for alert in alerts:
            # Group key: namespace + reason
            key = f"{alert.namespace}:{alert.reason}"
            if key not in groups:
                groups[key] = []
            groups[key].append(alert)
        
        # Create grouped alerts
        grouped = []
        for key, events in groups.items():
            if len(events) == 1:
                grouped.append(events[0].to_alert())
            else:
                # Create summary alert
                ns, reason = key.split(":", 1)
                resources = [e.resource_name for e in events]
                severity = max(events, key=lambda e: ["info", "warning", "high", "critical"].index(e.severity)).severity
                
                grouped_alert = {
                    "type": "k8s_grouped_alert",
                    "title": f"Multiple {reason} events in {ns}",
                    "severity": severity,
                    "resource_type": events[0].resource_type,
                    "namespace": ns,
                    "message": f"{len(events)} resources affected: {', '.join(resources[:5])}" + (
                        f" and {len(events)-5} more" if len(events) > 5 else ""
                    ),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "cluster": events[0].cluster,
                    "affected_resources": resources,
                    "reason": reason
                }
                grouped.append(grouped_alert)
        
        return grouped


class K8sWatcher:
    """Watches Kubernetes resources and sends alerts via MessageBus."""
    
    # Problem event reasons
    PROBLEM_REASONS = {
        "critical": [
            "Failed", "FailedScheduling", "FailedMount", "FailedAttachVolume",
            "CrashLoopBackOff", "ImagePullBackOff", "ErrImagePull",
            "OOMKilling", "SystemOOM", "Evicted", "NodeNotReady",
            "ContainerCannotRun", "CreateContainerError"
        ],
        "high": [
            "BackOff", "Unhealthy", "ProbeWarning", "Rebooted",
            "NodeHasDiskPressure", "NodeHasMemoryPressure",
            "Killing", "ExceededGracePeriod", "FailedBinding"
        ],
        "warning": [
            "Pulling", "Pulled", "Created", "Started",
            "Scheduled", "SuccessfulCreate", "ScalingReplicaSet"
        ]
    }
    
    def __init__(self, kubeconfig: str, namespace: str, message_bus, config: Dict):
        self.kubeconfig = kubeconfig
        self.namespace = namespace
        self.message_bus = message_bus
        self.config = config
        
        # Load k8s config
        config.load_kube_config(config_file=kubeconfig)
        self.core_v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
        
        # Get cluster name
        self.cluster = self._get_cluster_name()
        
        # Alert manager
        self.alert_manager = AlertManager(config.get('alerting', {}))
        
        # Running state
        self.running = False
        
        # Watch configuration
        self.watch_resources = config.get('watch_resources', ['events', 'pods'])
        self.severity_filter = config.get('severity_filter', ['Warning', 'Error'])
    
    def _get_cluster_name(self) -> str:
        """Extract cluster name from current context."""
        try:
            contexts, active = config.list_kube_config_contexts(config_file=self.kubeconfig)
            if active and 'name' in active:
                return active['name']
        except Exception:
            pass
        return "unknown"
    
    def _infer_severity(self, reason: str, message: str = "") -> str:
        """Infer severity from event reason."""
        text = f"{reason} {message}".lower()
        
        for severity, reasons in self.PROBLEM_REASONS.items():
            for r in reasons:
                if r.lower() in text:
                    return severity
        return "info"
    
    def _should_notify(self, event: K8sEvent) -> bool:
        """Check if event should trigger notification."""
        # Filter by severity
        if event.severity not in ["critical", "high", "warning"]:
            return False
        
        # Alert manager cooldown check
        return self.alert_manager.should_alert(event)
    
    def _send_batch(self, events: List[K8sEvent]) -> None:
        """Send batch of events as alerts."""
        if not events:
            return
        
        # Group related alerts
        grouped = self.alert_manager.group_alerts(events)
        
        for alert in grouped:
            is_critical = alert.get('severity') == 'critical'
            self.message_bus.send_alert(alert, mention=is_critical)
    
    def watch_events(self) -> None:
        """Watch Kubernetes Events API."""
        logger.info(f"Watching Events for namespace: {self.namespace}")
        
        w = watch.Watch()
        
        try:
            if self.namespace == "all":
                stream = w.stream(self.core_v1.list_event_for_all_namespaces)
            else:
                stream = w.stream(
                    self.core_v1.list_namespaced_event,
                    namespace=self.namespace
                )
            
            for event in stream:
                if not self.running:
                    break
                
                k8s_event = event['object']
                event_type = event['type']
                
                # Filter by event type (Warning/Error)
                event_severity = k8s_event.type
                if event_severity not in self.severity_filter:
                    continue
                
                # Create event object
                involved = k8s_event.involved_object
                e = K8sEvent(
                    event_type=event_type,
                    resource_type=involved.kind if involved else "Unknown",
                    resource_name=involved.name if involved else "unknown",
                    namespace=k8s_event.metadata.namespace or "default",
                    reason=k8s_event.reason or "",
                    message=k8s_event.message or "",
                    severity="critical" if event_severity == "Error" else "warning",
                    timestamp=k8s_event.last_timestamp.isoformat() if k8s_event.last_timestamp else datetime.now(timezone.utc).isoformat(),
                    cluster=self.cluster
                )
                
                # Process through alert manager
                batch = self.alert_manager.add_event(e)
                if batch:
                    self._send_batch(batch)
                    
        except ApiException as e:
            logger.error(f"API error watching events: {e}")
        except Exception as e:
            logger.error(f"Error watching events: {e}")
    
    def watch_pods(self) -> None:
        """Watch Pod status changes."""
        logger.info(f"Watching Pods for namespace: {self.namespace}")
        
        w = watch.Watch()
        
        try:
            if self.namespace == "all":
                stream = w.stream(self.core_v1.list_pod_for_all_namespaces)
            else:
                stream = w.stream(
                    self.core_v1.list_namespaced_pod,
                    namespace=self.namespace
                )
            
            for event in stream:
                if not self.running:
                    break
                
                pod = event['object']
                event_type = event['type']
                
                # Skip normal running pods
                if event_type == "MODIFIED" and pod.status.phase == "Running":
                    continue
                
                # Analyze pod for issues
                self._analyze_pod(pod, event_type)
                
        except ApiException as e:
            logger.error(f"API error watching pods: {e}")
        except Exception as e:
            logger.error(f"Error watching pods: {e}")
    
    def _analyze_pod(self, pod, event_type: str) -> None:
        """Analyze pod for issues and generate events."""
        ns = pod.metadata.namespace
        name = pod.metadata.name
        phase = pod.status.phase
        
        # Check container statuses
        if not pod.status.container_statuses:
            return
        
        for container in pod.status.container_statuses:
            # Check waiting state
            if container.state.waiting:
                reason = container.state.waiting.reason
                message = container.state.waiting.message or ""
                severity = self._infer_severity(reason, message)
                
                if severity in ["critical", "high"]:
                    e = K8sEvent(
                        event_type=event_type,
                        resource_type="Pod",
                        resource_name=name,
                        namespace=ns,
                        reason=reason,
                        message=f"Container {container.name}: {message}",
                        severity=severity,
                        timestamp=datetime.now(timezone.utc).isoformat(),
                        cluster=self.cluster
                    )
                    
                    batch = self.alert_manager.add_event(e)
                    if batch:
                        self._send_batch(batch)
            
            # Check terminated state
            if container.state.terminated:
                term = container.state.terminated
                if term.reason in ["OOMKilled", "Error"]:
                    severity = "critical" if term.reason == "OOMKilled" else "high"
                    e = K8sEvent(
                        event_type=event_type,
                        resource_type="Pod",
                        resource_name=name,
                        namespace=ns,
                        reason=term.reason,
                        message=f"Container {container.name} terminated (exit: {term.exit_code})",
                        severity=severity,
                        timestamp=datetime.now(timezone.utc).isoformat(),
                        cluster=self.cluster
                    )
                    
                    batch = self.alert_manager.add_event(e)
                    if batch:
                        self._send_batch(batch)
    
    def watch(self) -> None:
        """Main watch loop - runs all configured watchers."""
        self.running = True
        
        logger.info(f"Starting K8s Watcher for cluster: {self.cluster}")
        
        try:
            while self.running:
                try:
                    if "events" in self.watch_resources:
                        self.watch_events()
                    
                    if "pods" in self.watch_resources:
                        self.watch_pods()
                    
                    # Flush any remaining alerts
                    remaining = self.alert_manager.flush()
                    if remaining:
                        self._send_batch(remaining)
                    
                    # Small delay before reconnecting
                    if self.running:
                        time.sleep(1)
                        
                except Exception as e:
                    logger.error(f"Watch loop error: {e}")
                    time.sleep(5)
                    
        except KeyboardInterrupt:
            logger.info("Watcher stopped by user")
        finally:
            self.running = False
            # Final flush
            remaining = self.alert_manager.flush()
            if remaining:
                self._send_batch(remaining)
