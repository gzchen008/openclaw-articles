#!/usr/bin/env python3
"""
K8s Inspector - Periodic health inspection with trend analysis.
Generates comprehensive reports and sends via MessageBus.
"""

import json
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

try:
    from kubernetes import client, config
    from kubernetes.client.exceptions import ApiException
except ImportError:
    raise ImportError("kubernetes client not installed. Run: pip install kubernetes")

logger = logging.getLogger('k8s-ops-bot.inspector')


@dataclass
class HealthIssue:
    resource_type: str
    resource_name: str
    namespace: str
    issue_type: str
    severity: str
    message: str
    details: Dict[str, Any]
    timestamp: str


class K8sInspector:
    """Performs periodic health inspections of k8s cluster."""
    
    def __init__(self, kubeconfig: str, namespace: str, message_bus, config: Dict):
        self.kubeconfig = kubeconfig
        self.namespace = namespace
        self.message_bus = message_bus
        self.config = config
        
        # Load k8s config
        config.load_kube_config(config_file=kubeconfig)
        self.core_v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
        
        # Get cluster info
        self.cluster = self._get_cluster_name()
        
        # Inspection state
        self.issues: List[HealthIssue] = []
        self.previous_report: Optional[Dict] = None
    
    def _get_cluster_name(self) -> str:
        """Extract cluster name from current context."""
        try:
            contexts, active = config.list_kube_config_contexts(config_file=self.kubeconfig)
            if active and 'name' in active:
                return active['name']
        except Exception:
            pass
        return "unknown"
    
    def _add_issue(self, resource_type: str, resource_name: str, namespace: str,
                   issue_type: str, severity: str, message: str, details: Dict) -> None:
        """Add an issue to the list."""
        self.issues.append(HealthIssue(
            resource_type=resource_type,
            resource_name=resource_name,
            namespace=namespace,
            issue_type=issue_type,
            severity=severity,
            message=message,
            details=details,
            timestamp=datetime.now(timezone.utc).isoformat()
        ))
    
    def check_pods(self, check_status: bool = True, check_restarts: bool = True) -> None:
        """Check pod health status and restart counts."""
        try:
            if self.namespace == "all":
                pods = self.core_v1.list_pod_for_all_namespaces()
            else:
                pods = self.core_v1.list_namespaced_pod(namespace=self.namespace)
            
            for pod in pods.items:
                self._analyze_pod(pod, check_status, check_restarts)
                
        except ApiException as e:
            self._add_issue("Cluster", "API", "all",
                          "api_error", "critical",
                          f"Failed to list pods: {e.reason}", {})
    
    def _analyze_pod(self, pod, check_status: bool, check_restarts: bool) -> None:
        """Analyze individual pod health."""
        ns = pod.metadata.namespace
        name = pod.metadata.name
        
        phase = pod.status.phase
        
        if check_status:
            # Pending pods
            if phase == "Pending":
                creation_time = pod.metadata.creation_timestamp
                if creation_time:
                    age = datetime.now(timezone.utc) - creation_time.replace(tzinfo=timezone.utc)
                    if age.total_seconds() > 300:  # > 5 minutes
                        reason = self._get_pending_reason(pod)
                        self._add_issue("Pod", name, ns, "pod_pending", "warning",
                                      f"Pod pending for {age.seconds//60}m: {reason}",
                                      {"phase": phase, "reason": reason})
            
            # Failed pods
            if phase == "Failed":
                reason = pod.status.reason or "Unknown"
                self._add_issue("Pod", name, ns, "pod_failed", "critical",
                              f"Pod in Failed state: {reason}",
                              {"phase": phase, "reason": reason})
            
            # Check container statuses
            if pod.status.container_statuses:
                for container in pod.status.container_statuses:
                    self._check_container_status(ns, name, container)
        
        # Check restart counts
        if check_restarts and pod.status.container_statuses:
            for container in pod.status.container_statuses:
                if container.restart_count > 5:
                    self._add_issue("Pod", name, ns, "high_restarts", "warning",
                                  f"Container {container.name} has {container.restart_count} restarts",
                                  {"container": container.name,
                                   "restart_count": container.restart_count})
    
    def _check_container_status(self, ns: str, pod_name: str, container) -> None:
        """Check individual container status."""
        name = container.name
        
        # Waiting state
        if container.state.waiting:
            reason = container.state.waiting.reason
            message = container.state.waiting.message or ""
            
            if reason in ["CrashLoopBackOff", "ImagePullBackOff",
                         "ErrImagePull", "CreateContainerError"]:
                severity = "critical" if reason == "CrashLoopBackOff" else "high"
                self._add_issue("Container", f"{pod_name}/{name}", ns,
                              f"container_{reason.lower()}", severity,
                              f"{reason}: {message}",
                              {"reason": reason, "message": message})
        
        # Terminated state
        if container.state.terminated:
            reason = container.state.terminated.reason
            exit_code = container.state.terminated.exit_code
            
            if reason == "OOMKilled":
                self._add_issue("Container", f"{pod_name}/{name}", ns,
                              "oom_killed", "critical",
                              f"Container OOMKilled (exit code: {exit_code})",
                              {"reason": reason, "exit_code": exit_code})
            elif reason == "Error":
                self._add_issue("Container", f"{pod_name}/{name}", ns,
                              "container_error", "high",
                              f"Container exited with error (code: {exit_code})",
                              {"reason": reason, "exit_code": exit_code})
    
    def _get_pending_reason(self, pod) -> str:
        """Get reason why pod is pending."""
        if pod.status.conditions:
            for cond in pod.status.conditions:
                if cond.type == "PodScheduled" and cond.status == "False":
                    return cond.reason or "Unknown"
        return "Unknown"
    
    def check_deployments(self) -> None:
        """Check deployment health."""
        try:
            if self.namespace == "all":
                deployments = self.apps_v1.list_deployment_for_all_namespaces()
            else:
                deployments = self.apps_v1.list_namespaced_deployment(namespace=self.namespace)
            
            for deploy in deployments.items:
                self._analyze_deployment(deploy)
                
        except ApiException as e:
            self._add_issue("Cluster", "API", "all",
                          "api_error", "critical",
                          f"Failed to list deployments: {e.reason}", {})
    
    def _analyze_deployment(self, deploy) -> None:
        """Analyze deployment health."""
        ns = deploy.metadata.namespace
        name = deploy.metadata.name
        
        spec_replicas = deploy.spec.replicas or 0
        ready_replicas = deploy.status.ready_replicas or 0
        available_replicas = deploy.status.available_replicas or 0
        
        # Check if replicas don't match
        if ready_replicas < spec_replicas:
            self._add_issue("Deployment", name, ns,
                          "replicas_not_ready", "high",
                          f"Only {ready_replicas}/{spec_replicas} replicas ready",
                          {"desired": spec_replicas, "ready": ready_replicas,
                           "available": available_replicas})
        
        # Check conditions
        if deploy.status.conditions:
            for cond in deploy.status.conditions:
                if cond.type == "Progressing" and cond.status == "False":
                    self._add_issue("Deployment", name, ns,
                                  "deployment_stuck", "critical",
                                  f"Deployment not progressing: {cond.message}",
                                  {"reason": cond.reason, "message": cond.message})
    
    def check_nodes(self) -> None:
        """Check node health."""
        try:
            nodes = self.core_v1.list_node()
            
            for node in nodes.items:
                # Check Ready condition
                ready_condition = None
                for cond in node.status.conditions:
                    if cond.type == "Ready":
                        ready_condition = cond
                        break
                
                if ready_condition and ready_condition.status != "True":
                    self._add_issue("Node", node.metadata.name, "all",
                                  "node_not_ready", "critical",
                                  f"Node not ready: {ready_condition.message}",
                                  {"reason": ready_condition.reason,
                                   "message": ready_condition.message})
                
                # Check other conditions
                for cond in node.status.conditions:
                    if cond.type in ["DiskPressure", "MemoryPressure", "PIDPressure"]:
                        if cond.status == "True":
                            self._add_issue("Node", node.metadata.name, "all",
                                          f"node_{cond.type.lower()}", "warning",
                                          f"Node has {cond.type}: {cond.message}",
                                          {"reason": cond.reason, "message": cond.message})
                    
        except ApiException as e:
            self._add_issue("Cluster", "API", "all",
                          "api_error", "critical",
                          f"Failed to list nodes: {e.reason}", {})
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate inspection summary."""
        severity_count = {"critical": 0, "high": 0, "warning": 0, "info": 0}
        type_count = {}
        
        for issue in self.issues:
            severity_count[issue.severity] = severity_count.get(issue.severity, 0) + 1
            type_count[issue.issue_type] = type_count.get(issue.issue_type, 0) + 1
        
        # Get top issues
        sorted_issues = sorted(
            self.issues,
            key=lambda x: ["critical", "high", "warning", "info"].index(x.severity)
        )
        
        top_issues = []
        for issue in sorted_issues[:10]:
            top_issues.append({
                "severity": issue.severity,
                "resource": f"{issue.resource_type}/{issue.resource_name}",
                "message": issue.message
            })
        
        return {
            "total_issues": len(self.issues),
            "severity_breakdown": severity_count,
            "issue_types": type_count,
            "status": "healthy" if len(self.issues) == 0 else "issues_found",
            "top_issues": top_issues
        }
    
    def _generate_trend(self, current: Dict) -> Optional[Dict]:
        """Compare with previous report to show trends."""
        if not self.previous_report:
            return None
        
        prev = self.previous_report
        prev_total = prev.get('total_issues', 0)
        curr_total = current['total_issues']
        
        trend = {
            "total_change": curr_total - prev_total,
            "improved": prev_total > curr_total,
            "worsened": prev_total < curr_total,
            "same": prev_total == curr_total
        }
        
        return trend
    
    def run_inspection(self) -> Dict:
        """Run full inspection and generate report."""
        logger.info("Starting health inspection...")
        
        self.issues = []
        checks = self.config.get('checks', {})
        
        # Run checks
        if checks.get('pod_status', True) or checks.get('restart_count', True):
            logger.info("Checking pods...")
            self.check_pods(
                check_status=checks.get('pod_status', True),
                check_restarts=checks.get('restart_count', True)
            )
        
        if checks.get('deployment_health', True):
            logger.info("Checking deployments...")
            self.check_deployments()
        
        if checks.get('node_health', True):
            logger.info("Checking nodes...")
            self.check_nodes()
        
        # Generate report
        summary = self._generate_summary()
        trend = self._generate_trend(summary)
        
        report = {
            "cluster": self.cluster,
            "namespace": self.namespace,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "issues": [asdict(i) for i in self.issues],
            "summary": summary,
            "trend": trend
        }
        
        # Store for next comparison
        self.previous_report = summary
        
        # Send report via MessageBus
        self.message_bus.send_summary(report)
        
        logger.info(f"Inspection complete: {summary['total_issues']} issues found")
        
        return report
