#!/usr/bin/env python3
"""
Kubernetes Event Informer
Watches k8s events in real-time and outputs structured data for OpenClaw notification.

Usage:
    python3 informer.py --config /path/to/config.yaml
    python3 informer.py --config /path/to/config.yaml --once  # Run once and exit
"""

import argparse
import json
import sys
import signal
import yaml
from datetime import datetime, timezone
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, asdict

try:
    from kubernetes import client, config, watch
    from kubernetes.client.exceptions import ApiException
except ImportError:
    print("Error: kubernetes client not installed. Run: pip install kubernetes")
    sys.exit(1)


@dataclass
class K8sEvent:
    event_type: str      # ADDED, MODIFIED, DELETED
    resource_type: str   # Pod, Deployment, etc.
    resource_name: str
    namespace: str
    reason: str
    message: str
    severity: str        # inferred from event
    timestamp: str
    raw_object: Dict


class K8sInformer:
    """Kubernetes resource watcher using Watch API."""
    
    # Event reasons that indicate problems
    PROBLEM_REASONS = {
        "critical": [
            "Failed", "FailedScheduling", "FailedMount", "FailedAttachVolume",
            "CrashLoopBackOff", "ImagePullBackOff", "ErrImagePull",
            "OOMKilling", "SystemOOM", "Evicted", "NodeNotReady"
        ],
        "warning": [
            "BackOff", "Unhealthy", "ProbeWarning", "Rebooted",
            "NodeHasDiskPressure", "NodeHasMemoryPressure",
            "Killing", "ExceededGracePeriod", "FailedBinding"
        ]
    }
    
    def __init__(self, kubeconfig: str, namespace: str = "default"):
        self.kubeconfig = kubeconfig
        self.namespace = namespace
        self.running = True
        self.handlers: List[Callable[[K8sEvent], None]] = []
        
        # Load k8s config
        config.load_kube_config(config_file=kubeconfig)
        self.core_v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print(f"\nReceived signal {signum}, shutting down...")
        self.running = False
    
    def _infer_severity(self, reason: str, message: str = "") -> str:
        """Infer severity from event reason."""
        reason_lower = reason.lower() if reason else ""
        message_lower = message.lower() if message else ""
        
        for sev, reasons in self.PROBLEM_REASONS.items():
            for r in reasons:
                if r.lower() in reason_lower or r.lower() in message_lower:
                    return sev
        return "info"
    
    def _create_event(self, event_type: str, obj: Dict, resource_type: str) -> Optional[K8sEvent]:
        """Create K8sEvent from k8s object."""
        metadata = obj.get("metadata", {})
        status = obj.get("status", {})
        
        name = metadata.get("name", "unknown")
        namespace = metadata.get("namespace", "default")
        
        # Extract reason and message based on resource type
        reason = ""
        message = ""
        
        if resource_type == "Event":
            reason = obj.get("reason", "")
            message = obj.get("message", "")
        elif resource_type == "Pod":
            # Check container statuses for issues
            container_statuses = status.get("containerStatuses", [])
            for cs in container_statuses:
                state = cs.get("state", {})
                if "waiting" in state:
                    reason = state["waiting"].get("reason", "")
                    message = state["waiting"].get("message", "")
                    break
                elif "terminated" in state:
                    term = state["terminated"]
                    if term.get("reason") in ["OOMKilled", "Error"]:
                        reason = term.get("reason", "")
                        message = f"Exit code: {term.get('exitCode', 'unknown')}"
                        break
        
        severity = self._infer_severity(reason, message)
        
        # Only return if it's an issue or significant event
        if severity in ["critical", "warning"] or event_type in ["DELETED"]:
            return K8sEvent(
                event_type=event_type,
                resource_type=resource_type,
                resource_name=name,
                namespace=namespace,
                reason=reason or event_type,
                message=message,
                severity=severity,
                timestamp=datetime.now(timezone.utc).isoformat(),
                raw_object=obj
            )
        return None
    
    def watch_pods(self, timeout_seconds: Optional[int] = None) -> None:
        """Watch pod events."""
        print(f"Starting Pod watcher for namespace: {self.namespace}")
        
        w = watch.Watch()
        
        try:
            if self.namespace == "all":
                stream = w.stream(
                    self.core_v1.list_pod_for_all_namespaces,
                    timeout_seconds=timeout_seconds
                )
            else:
                stream = w.stream(
                    self.core_v1.list_namespaced_pod,
                    namespace=self.namespace,
                    timeout_seconds=timeout_seconds
                )
            
            for event in stream:
                if not self.running:
                    break
                
                event_type = event['type']  # ADDED, MODIFIED, DELETED
                pod = event['object']
                
                # Skip if pod is still running fine
                if event_type == "MODIFIED":
                    phase = pod.status.phase if hasattr(pod, 'status') else "Unknown"
                    if phase == "Running":
                        continue
                
                # Convert to dict for processing
                pod_dict = self._sanitize_object(pod.to_dict())
                k8s_event = self._create_event(event_type, pod_dict, "Pod")
                
                if k8s_event:
                    self._notify(k8s_event)
                    
        except ApiException as e:
            print(f"API Error watching pods: {e}")
        except Exception as e:
            print(f"Error watching pods: {e}")
    
    def watch_deployments(self, timeout_seconds: Optional[int] = None) -> None:
        """Watch deployment events."""
        print(f"Starting Deployment watcher for namespace: {self.namespace}")
        
        w = watch.Watch()
        
        try:
            if self.namespace == "all":
                stream = w.stream(
                    self.apps_v1.list_deployment_for_all_namespaces,
                    timeout_seconds=timeout_seconds
                )
            else:
                stream = w.stream(
                    self.apps_v1.list_namespaced_deployment,
                    namespace=self.namespace,
                    timeout_seconds=timeout_seconds
                )
            
            for event in stream:
                if not self.running:
                    break
                
                event_type = event['type']
                deploy = event['object']
                
                # Check for issues
                deploy_dict = self._sanitize_object(deploy.to_dict())
                
                # Check replica mismatch
                status = deploy_dict.get("status", {})
                spec = deploy_dict.get("spec", {})
                
                desired = spec.get("replicas", 0)
                ready = status.get("readyReplicas", 0)
                
                if ready < desired:
                    k8s_event = K8sEvent(
                        event_type=event_type,
                        resource_type="Deployment",
                        resource_name=deploy_dict.get("metadata", {}).get("name", "unknown"),
                        namespace=deploy_dict.get("metadata", {}).get("namespace", "default"),
                        reason="ReplicasNotReady",
                        message=f"Only {ready}/{desired} replicas ready",
                        severity="warning",
                        timestamp=datetime.now(timezone.utc).isoformat(),
                        raw_object=deploy_dict
                    )
                    self._notify(k8s_event)
                    
        except ApiException as e:
            print(f"API Error watching deployments: {e}")
        except Exception as e:
            print(f"Error watching deployments: {e}")
    
    def watch_events(self, timeout_seconds: Optional[int] = None, 
                     severity_filter: List[str] = None) -> None:
        """Watch k8s Events (from event API)."""
        print(f"Starting Event watcher for namespace: {self.namespace}")
        
        severity_filter = severity_filter or ["Warning", "Error"]
        w = watch.Watch()
        
        try:
            if self.namespace == "all":
                stream = w.stream(
                    self.core_v1.list_event_for_all_namespaces,
                    timeout_seconds=timeout_seconds
                )
            else:
                stream = w.stream(
                    self.core_v1.list_namespaced_event,
                    namespace=self.namespace,
                    timeout_seconds=timeout_seconds
                )
            
            for event in stream:
                if not self.running:
                    break
                
                k8s_event_obj = event['object']
                event_type = event['type']
                
                # Filter by type
                event_type_filter = k8s_event_obj.type
                if event_type_filter not in severity_filter:
                    continue
                
                event_dict = self._sanitize_object(k8s_event_obj.to_dict())
                
                k8s_event = K8sEvent(
                    event_type=event_type,
                    resource_type=event_dict.get("involvedObject", {}).get("kind", "Unknown"),
                    resource_name=event_dict.get("involvedObject", {}).get("name", "unknown"),
                    namespace=event_dict.get("metadata", {}).get("namespace", "default"),
                    reason=event_dict.get("reason", ""),
                    message=event_dict.get("message", ""),
                    severity="critical" if event_type_filter == "Error" else "warning",
                    timestamp=event_dict.get("lastTimestamp") or datetime.now(timezone.utc).isoformat(),
                    raw_object=event_dict
                )
                
                self._notify(k8s_event)
                
        except ApiException as e:
            print(f"API Error watching events: {e}")
        except Exception as e:
            print(f"Error watching events: {e}")
    
    def _sanitize_object(self, obj: Dict) -> Dict:
        """Remove unnecessary fields from k8s object."""
        # Remove managedFields which are verbose
        if isinstance(obj, dict):
            if "metadata" in obj and "managedFields" in obj["metadata"]:
                del obj["metadata"]["managedFields"]
        return obj
    
    def _notify(self, event: K8sEvent) -> None:
        """Output event for OpenClaw to capture and send notification."""
        # Output JSON that OpenClaw can parse
        output = {
            "type": "k8s_event",
            "data": asdict(event)
        }
        print(json.dumps(output, ensure_ascii=False))
        
        # Also call handlers
        for handler in self.handlers:
            handler(event)
    
    def add_handler(self, handler: Callable[[K8sEvent], None]) -> None:
        """Add event handler callback."""
        self.handlers.append(handler)
    
    def run(self, config: Dict, once: bool = False) -> None:
        """Run informer with configuration."""
        events_config = config.get("events", {})
        
        if not events_config.get("enabled", True):
            print("Events disabled in config")
            return
        
        watch_resources = events_config.get("watch_resources", ["events", "pods"])
        severity = events_config.get("severity", ["Warning", "Error"])
        timeout = 60 if once else None
        
        print(f"Starting K8s Informer for cluster with resources: {watch_resources}")
        print("Press Ctrl+C to stop")
        
        try:
            while self.running:
                if "events" in watch_resources:
                    self.watch_events(timeout_seconds=timeout, severity_filter=severity)
                
                if "pods" in watch_resources:
                    self.watch_pods(timeout_seconds=timeout)
                
                if "deployments" in watch_resources:
                    self.watch_deployments(timeout_seconds=timeout)
                
                if once:
                    break
                    
        except KeyboardInterrupt:
            print("\nShutting down...")
            self.running = False


def format_event_for_message(event: K8sEvent) -> str:
    """Format event as notification message."""
    emoji = "🔴" if event.severity == "critical" else "🟡"
    
    lines = [
        f"{emoji} K8s {event.event_type}: {event.resource_type}/{event.resource_name}",
        f"Namespace: {event.namespace}",
        f"Reason: {event.reason}",
    ]
    
    if event.message:
        lines.append(f"Message: {event.message}")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Kubernetes Event Informer")
    parser.add_argument("--config", "-c", required=True, help="Path to config file")
    parser.add_argument("--namespace", "-n", help="Override namespace")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    args = parser.parse_args()
    
    # Load config
    with open(args.config, 'r') as f:
        cfg = yaml.safe_load(f)
    
    # Get settings
    kubeconfig = cfg.get("kubeconfig")
    namespace = args.namespace or cfg.get("namespace", "default")
    
    if not kubeconfig:
        print("Error: kubeconfig not specified in config file")
        sys.exit(1)
    
    # Create informer
    informer = K8sInformer(kubeconfig, namespace)
    
    # Add handler to print formatted messages
    def print_handler(event: K8sEvent):
        print("\n" + "="*50)
        print(format_event_for_message(event))
        print("="*50)
    
    informer.add_handler(print_handler)
    
    # Run
    informer.run(cfg, once=args.once)


if __name__ == "__main__":
    main()
