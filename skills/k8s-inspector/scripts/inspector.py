#!/usr/bin/env python3
"""
Kubernetes Health Inspector
Performs comprehensive health checks on k8s resources.

Usage:
    python3 inspector.py --config /path/to/config.yaml
    python3 inspector.py --config /path/to/config.yaml --namespace production
    python3 inspector.py --config /path/to/config.yaml --output json
"""

import argparse
import json
import sys
import yaml
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

try:
    from kubernetes import client, config
    from kubernetes.client.exceptions import ApiException
except ImportError:
    print("Error: kubernetes client not installed. Run: pip install kubernetes")
    sys.exit(1)


@dataclass
class HealthIssue:
    resource_type: str
    resource_name: str
    namespace: str
    issue_type: str
    severity: str  # critical, warning, info
    message: str
    details: Dict[str, Any]
    timestamp: str


@dataclass
class InspectionReport:
    cluster: str
    namespace: str
    timestamp: str
    issues: List[HealthIssue]
    summary: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        return {
            "cluster": self.cluster,
            "namespace": self.namespace,
            "timestamp": self.timestamp,
            "issues": [asdict(i) for i in self.issues],
            "summary": self.summary
        }


class K8sInspector:
    def __init__(self, kubeconfig: str, namespace: str = "default"):
        self.kubeconfig = kubeconfig
        self.namespace = namespace
        self.issues: List[HealthIssue] = []
        
        # Load k8s config
        config.load_kube_config(config_file=kubeconfig)
        self.core_v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
        
        # Get cluster info
        self.cluster = self._get_cluster_name()
    
    def _get_cluster_name(self) -> str:
        """Extract cluster name from kubeconfig context."""
        try:
            contexts, active = config.list_kube_config_contexts(config_file=self.kubeconfig)
            if active and 'name' in active:
                return active['name']
        except Exception:
            pass
        return "unknown"
    
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
        
        # Check pod phase
        phase = pod.status.phase
        
        if check_status:
            # Pending pods
            if phase == "Pending":
                # Check if stuck
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
                severity = "critical" if reason == "CrashLoopBackOff" else "warning"
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
                              "container_error", "warning",
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
                          "replicas_not_ready", "warning",
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
    
    def run_inspection(self, config: Dict) -> InspectionReport:
        """Run full inspection based on configuration."""
        checks = config.get("inspection", {}).get("checks", {})
        
        # Check pods
        if checks.get("pod_status", True) or checks.get("restart_count", True):
            self.check_pods(
                check_status=checks.get("pod_status", True),
                check_restarts=checks.get("restart_count", True)
            )
        
        # Check deployments
        if checks.get("deployment_health", True):
            self.check_deployments()
        
        # Generate summary
        summary = self._generate_summary()
        
        return InspectionReport(
            cluster=self.cluster,
            namespace=self.namespace,
            timestamp=datetime.now(timezone.utc).isoformat(),
            issues=self.issues,
            summary=summary
        )
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate inspection summary."""
        severity_count = {"critical": 0, "warning": 0, "info": 0}
        type_count = {}
        
        for issue in self.issues:
            severity_count[issue.severity] = severity_count.get(issue.severity, 0) + 1
            type_count[issue.issue_type] = type_count.get(issue.issue_type, 0) + 1
        
        return {
            "total_issues": len(self.issues),
            "severity_breakdown": severity_count,
            "issue_types": type_count,
            "status": "healthy" if len(self.issues) == 0 else "issues_found"
        }


def format_message(report: InspectionReport) -> str:
    """Format report as human-readable message."""
    lines = [
        f"🔍 K8s Health Report: {report.cluster}",
        f"Namespace: {report.namespace}",
        f"Time: {report.timestamp}",
        ""
    ]
    
    summary = report.summary
    if summary["status"] == "healthy":
        lines.append("✅ All checks passed - cluster is healthy!")
    else:
        lines.append(f"⚠️ Found {summary['total_issues']} issues:")
        lines.append(f"  • Critical: {summary['severity_breakdown']['critical']}")
        lines.append(f"  • Warning: {summary['severity_breakdown']['warning']}")
        lines.append("")
        
        # List critical issues first
        critical = [i for i in report.issues if i.severity == "critical"]
        if critical:
            lines.append("🔴 Critical Issues:")
            for issue in critical[:5]:  # Limit to 5
                lines.append(f"  • [{issue.resource_type}] {issue.resource_name}: {issue.message}")
            if len(critical) > 5:
                lines.append(f"  ... and {len(critical) - 5} more")
            lines.append("")
        
        warnings = [i for i in report.issues if i.severity == "warning"]
        if warnings:
            lines.append("🟡 Warnings:")
            for issue in warnings[:3]:
                lines.append(f"  • [{issue.resource_type}] {issue.resource_name}: {issue.message}")
            if len(warnings) > 3:
                lines.append(f"  ... and {len(warnings) - 3} more")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Kubernetes Health Inspector")
    parser.add_argument("--config", "-c", required=True, help="Path to config file")
    parser.add_argument("--namespace", "-n", help="Override namespace")
    parser.add_argument("--output", "-o", choices=["json", "text"], default="text",
                       help="Output format")
    parser.add_argument("--message", "-m", action="store_true",
                       help="Output formatted message for OpenClaw")
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
    
    # Run inspection
    inspector = K8sInspector(kubeconfig, namespace)
    report = inspector.run_inspection(cfg)
    
    # Output
    if args.output == "json":
        print(json.dumps(report.to_dict(), indent=2))
    elif args.message:
        print(format_message(report))
    else:
        print(format_message(report))
        
        # Also print JSON for OpenClaw parsing
        print("\n---JSON---")
        print(json.dumps(report.to_dict()))


if __name__ == "__main__":
    main()
