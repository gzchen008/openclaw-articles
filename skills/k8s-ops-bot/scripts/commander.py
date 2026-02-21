#!/usr/bin/env python3
"""
K8s Commander - Interactive command handler for chat-based cluster management.
Handles commands like /k8s status, /k8s logs, /k8s restart, etc.
"""

import re
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

try:
    from kubernetes import client, config
    from kubernetes.client.exceptions import ApiException
    from kubernetes.stream import stream
except ImportError:
    raise ImportError("kubernetes client not installed. Run: pip install kubernetes")

logger = logging.getLogger('k8s-ops-bot.commander')


class K8sCommander:
    """Handles interactive commands from OpenClaw messages."""
    
    # Command registry: pattern -> handler method
    COMMANDS = {
        r'status': 'cmd_status',
        r'pods?(?:\s+(\S+))?': 'cmd_pods',
        r'logs?\s+(\S+)': 'cmd_logs',
        r'events?(?:\s+--?(\w+)(?:=(\S+))?)?': 'cmd_events',
        r'top(?:\s+--?namespace(?:=(\S+))?)?': 'cmd_top',
        r'restart\s+(\S+)': 'cmd_restart',
        r'scale\s+(\S+)\s+(\d+)': 'cmd_scale',
        r'describe\s+(\S+)(?:/(\S+))?': 'cmd_describe',
        r'get\s+(\S+)(?:\s+--?namespace(?:=(\S+))?)?': 'cmd_get',
        r'nodes?': 'cmd_nodes',
        r'help': 'cmd_help',
    }
    
    def __init__(self, kubeconfig: str, namespace: str, message_bus, config: Dict):
        self.kubeconfig = kubeconfig
        self.default_namespace = namespace
        self.message_bus = message_bus
        self.config = config
        
        # Load k8s config
        config.load_kube_config(config_file=kubeconfig)
        self.core_v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
        self.metrics = None
        
        # Try to load metrics API
        try:
            self.metrics = client.CustomObjectsApi()
        except Exception:
            pass
        
        # Authorization
        self.allowed_users = config.get('authorization', {}).get('allowed_users', [])
        self.restricted_commands = config.get('authorization', {}).get('restricted_commands', [])
    
    def _check_auth(self, user: str, command: str) -> bool:
        """Check if user is authorized for command."""
        # If no restrictions, allow all
        if not self.allowed_users:
            return True
        
        # Check if user is allowed
        if user not in self.allowed_users:
            return False
        
        # Check if command is restricted
        cmd_base = command.split()[0] if command else ""
        if cmd_base in self.restricted_commands:
            # Additional check for restricted commands
            return user in self.config.get('authorization', {}).get('admin_users', [])
        
        return True
    
    def handle_command(self, command_str: str, user: str = "unknown") -> Optional[Dict]:
        """
        Parse and execute command.
        Returns response dict or None if not handled.
        """
        # Parse command
        cmd_match = re.match(r'/k8s\s+(\w+)(?:\s+(.*))?$', command_str.strip())
        if not cmd_match:
            return None
        
        cmd = cmd_match.group(1)
        args = cmd_match.group(2) or ""
        
        logger.info(f"Command from {user}: {cmd} {args}")
        
        # Check authorization
        if not self._check_auth(user, cmd):
            return {
                "success": False,
                "message": "⛔ You are not authorized to run this command."
            }
        
        # Find handler
        for pattern, handler_name in self.COMMANDS.items():
            match = re.match(pattern, f"{cmd} {args}".strip())
            if match:
                handler = getattr(self, handler_name)
                try:
                    return handler(*match.groups())
                except Exception as e:
                    logger.error(f"Command error: {e}")
                    return {
                        "success": False,
                        "message": f"❌ Error executing command: {str(e)}"
                    }
        
        return {
            "success": False,
            "message": f"❓ Unknown command: {cmd}\nType `/k8s help` for available commands."
        }
    
    def cmd_status(self) -> Dict:
        """Get cluster health summary."""
        try:
            # Get node status
            nodes = self.core_v1.list_node()
            total_nodes = len(nodes.items)
            ready_nodes = sum(
                1 for n in nodes.items
                if any(c.type == 'Ready' and c.status == 'True' for c in n.status.conditions)
            )
            
            # Get pod counts
            if self.default_namespace == "all":
                pods = self.core_v1.list_pod_for_all_namespaces()
            else:
                pods = self.core_v1.list_namespaced_pod(namespace=self.default_namespace)
            
            total_pods = len(pods.items)
            running_pods = sum(1 for p in pods.items if p.status.phase == "Running")
            failed_pods = sum(1 for p in pods.items if p.status.phase == "Failed")
            pending_pods = sum(1 for p in pods.items if p.status.phase == "Pending")
            
            # Get deployment status
            if self.default_namespace == "all":
                deployments = self.apps_v1.list_deployment_for_all_namespaces()
            else:
                deployments = self.apps_v1.list_namespaced_deployment(namespace=self.default_namespace)
            
            deploys = len(deployments.items)
            ready_deploys = sum(
                1 for d in deployments.items
                if d.status.ready_replicas == d.spec.replicas
            )
            
            # Build message
            status_emoji = "✅" if failed_pods == 0 and pending_pods == 0 else "⚠️"
            
            lines = [
                f"{status_emoji} **Cluster Status**",
                f"",
                f"**Nodes:** {ready_nodes}/{total_nodes} ready",
                f"**Pods:** {running_pods}/{total_pods} running",
            ]
            
            if failed_pods > 0:
                lines.append(f"  🔴 Failed: {failed_pods}")
            if pending_pods > 0:
                lines.append(f"  🟡 Pending: {pending_pods}")
            
            lines.extend([
                f"**Deployments:** {ready_deploys}/{deploys} healthy",
                f"",
                f"Namespace: {self.default_namespace}",
                f"Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}"
            ])
            
            return {
                "success": True,
                "message": "\n".join(lines)
            }
            
        except ApiException as e:
            return {"success": False, "message": f"API Error: {e.reason}"}
    
    def cmd_pods(self, namespace: str = None) -> Dict:
        """List problematic pods."""
        ns = namespace or self.default_namespace
        
        try:
            if ns == "all":
                pods = self.core_v1.list_pod_for_all_namespaces()
            else:
                pods = self.core_v1.list_namespaced_pod(namespace=ns)
            
            # Filter problematic pods
            problems = []
            for pod in pods.items:
                phase = pod.status.phase
                if phase in ["Failed", "Pending", "Unknown"]:
                    problems.append({
                        "name": pod.metadata.name,
                        "namespace": pod.metadata.namespace,
                        "phase": phase,
                        "age": self._get_age(pod.metadata.creation_timestamp)
                    })
                    continue
                
                # Check container issues
                if pod.status.container_statuses:
                    for cs in pod.status.container_statuses:
                        if cs.restart_count > 5:
                            problems.append({
                                "name": pod.metadata.name,
                                "namespace": pod.metadata.namespace,
                                "phase": f"HighRestarts({cs.restart_count})",
                                "age": self._get_age(pod.metadata.creation_timestamp)
                            })
            
            if not problems:
                return {
                    "success": True,
                    "message": f"✅ No problematic pods in namespace '{ns}'"
                }
            
            lines = [f"⚠️ **Problematic Pods** (namespace: {ns})", ""]
            for p in problems[:20]:  # Limit to 20
                emoji = "🔴" if p['phase'] == "Failed" else "🟡"
                lines.append(f"{emoji} `{p['name']}` - {p['phase']} - {p['age']}")
            
            if len(problems) > 20:
                lines.append(f"\n... and {len(problems) - 20} more")
            
            return {"success": True, "message": "\n".join(lines)}
            
        except ApiException as e:
            return {"success": False, "message": f"API Error: {e.reason}"}
    
    def cmd_logs(self, pod_name: str, lines: int = 50) -> Dict:
        """Get pod logs."""
        try:
            # Try to find pod in namespace
            pod = self._find_pod(pod_name)
            if not pod:
                return {"success": False, "message": f"❌ Pod '{pod_name}' not found"}
            
            logs = self.core_v1.read_namespaced_pod_log(
                name=pod.metadata.name,
                namespace=pod.metadata.namespace,
                tail_lines=lines
            )
            
            # Truncate if too long
            max_len = 1900  # Discord limit consideration
            if len(logs) > max_len:
                logs = "..." + logs[-max_len:]
            
            message = f"📄 **Logs for `{pod.metadata.name}`** (last {lines} lines)\n```\n{logs}\n```"
            
            return {"success": True, "message": message}
            
        except ApiException as e:
            return {"success": False, "message": f"❌ Failed to get logs: {e.reason}"}
    
    def cmd_events(self, flag: str = None, value: str = None) -> Dict:
        """Get recent events."""
        try:
            if self.default_namespace == "all":
                events = self.core_v1.list_event_for_all_namespaces()
            else:
                events = self.core_v1.list_namespaced_event(namespace=self.default_namespace)
            
            # Filter warning/error events
            warnings = [e for e in events.items if e.type in ["Warning", "Error"]]
            
            if not warnings:
                return {"success": True, "message": "✅ No recent warning events"}
            
            lines = [f"⚠️ **Recent Warning Events** (last 10)", ""]
            
            for e in sorted(warnings, key=lambda x: x.last_timestamp or datetime.min, reverse=True)[:10]:
                emoji = "🔴" if e.type == "Error" else "🟡"
                resource = f"{e.involved_object.kind}/{e.involved_object.name}" if e.involved_object else "Unknown"
                lines.append(f"{emoji} `{resource}` - {e.reason}: {e.message[:80]}...")
            
            return {"success": True, "message": "\n".join(lines)}
            
        except ApiException as e:
            return {"success": False, "message": f"API Error: {e.reason}"}
    
    def cmd_top(self, namespace: str = None) -> Dict:
        """Show resource usage (requires metrics-server)."""
        if not self.metrics:
            return {
                "success": False,
                "message": "❌ Metrics API not available. Is metrics-server installed?"
            }
        
        ns = namespace or self.default_namespace
        
        try:
            # Get pod metrics
            if ns == "all":
                metrics = self.metrics.list_cluster_custom_object(
                    "metrics.k8s.io", "v1beta1", "pods"
                )
            else:
                metrics = self.metrics.list_namespaced_custom_object(
                    "metrics.k8s.io", "v1beta1", ns, "pods"
                )
            
            items = metrics.get('items', [])
            
            if not items:
                return {"success": True, "message": "📊 No metrics available"}
            
            lines = [f"📊 **Top Resource Usage** (namespace: {ns})", ""]
            lines.append(f"{'Pod':<30} {'CPU':<10} {'Memory':<10}")
            lines.append("-" * 50)
            
            for item in items[:15]:
                name = item['metadata']['name']
                containers = item.get('containers', [])
                if containers:
                    cpu = containers[0].get('usage', {}).get('cpu', 'N/A')
                    mem = containers[0].get('usage', {}).get('memory', 'N/A')
                    lines.append(f"{name:<30} {cpu:<10} {mem:<10}")
            
            return {"success": True, "message": "\n".join(lines)}
            
        except Exception as e:
            return {"success": False, "message": f"❌ Failed to get metrics: {str(e)}"}
    
    def cmd_restart(self, deployment_name: str) -> Dict:
        """Rolling restart a deployment."""
        try:
            # Find deployment
            deploy = self._find_deployment(deployment_name)
            if not deploy:
                return {"success": False, "message": f"❌ Deployment '{deployment_name}' not found"}
            
            # Trigger restart by updating annotation
            from kubernetes.client import V1Deployment
            
            if not deploy.spec.template.metadata.annotations:
                deploy.spec.template.metadata.annotations = {}
            
            deploy.spec.template.metadata.annotations['kubectl.kubernetes.io/restartedAt'] = \
                datetime.now(timezone.utc).isoformat()
            
            self.apps_v1.replace_namespaced_deployment(
                name=deploy.metadata.name,
                namespace=deploy.metadata.namespace,
                body=deploy
            )
            
            return {
                "success": True,
                "message": f"🔄 Restart triggered for deployment `{deploy.metadata.name}` in `{deploy.metadata.namespace}`"
            }
            
        except ApiException as e:
            return {"success": False, "message": f"❌ Failed to restart: {e.reason}"}
    
    def cmd_scale(self, deployment_name: str, replicas: str) -> Dict:
        """Scale a deployment."""
        try:
            deploy = self._find_deployment(deployment_name)
            if not deploy:
                return {"success": False, "message": f"❌ Deployment '{deployment_name}' not found"}
            
            # Patch deployment
            patch = {'spec': {'replicas': int(replicas)}}
            
            self.apps_v1.patch_namespaced_deployment_scale(
                name=deploy.metadata.name,
                namespace=deploy.metadata.namespace,
                body=patch
            )
            
            return {
                "success": True,
                "message": f"📏 Scaled deployment `{deploy.metadata.name}` to {replicas} replicas"
            }
            
        except ApiException as e:
            return {"success": False, "message": f"❌ Failed to scale: {e.reason}"}
    
    def cmd_describe(self, resource_type: str, resource_name: str = None) -> Dict:
        """Describe a resource."""
        # Handle pod/name format
        if "/" in resource_type and not resource_name:
            resource_type, resource_name = resource_type.split("/", 1)
        
        if not resource_name:
            return {"success": False, "message": "❌ Usage: /k8s describe <type>/<name>"}
        
        try:
            if resource_type.lower() in ["pod", "pods"]:
                pod = self._find_pod(resource_name)
                if not pod:
                    return {"success": False, "message": f"❌ Pod '{resource_name}' not found"}
                
                details = self._format_pod_describe(pod)
                return {"success": True, "message": details}
            
            elif resource_type.lower() in ["deploy", "deployment", "deployments"]:
                deploy = self._find_deployment(resource_name)
                if not deploy:
                    return {"success": False, "message": f"❌ Deployment '{resource_name}' not found"}
                
                details = self._format_deployment_describe(deploy)
                return {"success": True, "message": details}
            
            else:
                return {"success": False, "message": f"❌ Unsupported resource type: {resource_type}"}
            
        except ApiException as e:
            return {"success": False, "message": f"API Error: {e.reason}"}
    
    def cmd_get(self, resource_type: str, namespace: str = None) -> Dict:
        """Get resources list."""
        ns = namespace or self.default_namespace
        
        try:
            if resource_type.lower() in ["pod", "pods"]:
                if ns == "all":
                    pods = self.core_v1.list_pod_for_all_namespaces()
                else:
                    pods = self.core_v1.list_namespaced_pod(namespace=ns)
                
                lines = [f"📦 **Pods** (namespace: {ns})", ""]
                for pod in pods.items[:20]:
                    status = "🟢" if pod.status.phase == "Running" else "🟡"
                    lines.append(f"{status} `{pod.metadata.name}` - {pod.status.phase}")
                
                return {"success": True, "message": "\n".join(lines)}
            
            elif resource_type.lower() in ["deploy", "deployment", "deployments"]:
                if ns == "all":
                    deploys = self.apps_v1.list_deployment_for_all_namespaces()
                else:
                    deploys = self.apps_v1.list_namespaced_deployment(namespace=ns)
                
                lines = [f"🚀 **Deployments** (namespace: {ns})", ""]
                for d in deploys.items[:20]:
                    ready = d.status.ready_replicas or 0
                    desired = d.spec.replicas or 0
                    status = "🟢" if ready == desired else "🟡"
                    lines.append(f"{status} `{d.metadata.name}` - {ready}/{desired} ready")
                
                return {"success": True, "message": "\n".join(lines)}
            
            else:
                return {"success": False, "message": f"❌ Unsupported resource type: {resource_type}"}
            
        except ApiException as e:
            return {"success": False, "message": f"API Error: {e.reason}"}
    
    def cmd_nodes(self) -> Dict:
        """List nodes status."""
        try:
            nodes = self.core_v1.list_node()
            
            lines = ["🖥️ **Nodes Status**", ""]
            
            for node in nodes.items:
                # Get ready status
                ready = any(
                    c.type == 'Ready' and c.status == 'True'
                    for c in node.status.conditions
                )
                
                emoji = "🟢" if ready else "🔴"
                version = node.status.node_info.kubelet_version if node.status.node_info else "unknown"
                
                lines.append(f"{emoji} `{node.metadata.name}` - Kubelet {version}")
            
            return {"success": True, "message": "\n".join(lines)}
            
        except ApiException as e:
            return {"success": False, "message": f"API Error: {e.reason}"}
    
    def cmd_help(self) -> Dict:
        """Show help message."""
        message = """🤖 **K8s Ops Bot Commands**

**Status & Monitoring:**
• `/k8s status` - Cluster health summary
• `/k8s pods [namespace]` - List problematic pods
• `/k8s nodes` - List nodes status
• `/k8s top [--namespace=xxx]` - Resource usage (needs metrics-server)
• `/k8s events` - Recent warning events

**Debugging:**
• `/k8s logs <pod>` - Get pod logs
• `/k8s describe <type>/<name>` - Describe resource details
• `/k8s get pods [--namespace=xxx]` - List pods
• `/k8s get deployments` - List deployments

**Operations:**
• `/k8s restart <deployment>` - Rolling restart deployment
• `/k8s scale <deployment> <replicas>` - Scale deployment

**Examples:**
• `/k8s pods production`
• `/k8s logs nginx-abc123`
• `/k8s describe pod/my-app-xyz`
• `/k8s restart api-gateway`
"""
        return {"success": True, "message": message}
    
    # Helper methods
    
    def _find_pod(self, name: str) -> Optional[client.V1Pod]:
        """Find pod by name (partial match supported)."""
        if self.default_namespace == "all":
            pods = self.core_v1.list_pod_for_all_namespaces()
        else:
            pods = self.core_v1.list_namespaced_pod(namespace=self.default_namespace)
        
        # Try exact match first
        for pod in pods.items:
            if pod.metadata.name == name:
                return pod
        
        # Try partial match
        for pod in pods.items:
            if name in pod.metadata.name:
                return pod
        
        return None
    
    def _find_deployment(self, name: str) -> Optional[client.V1Deployment]:
        """Find deployment by name (partial match supported)."""
        if self.default_namespace == "all":
            deploys = self.apps_v1.list_deployment_for_all_namespaces()
        else:
            deploys = self.apps_v1.list_namespaced_deployment(namespace=self.default_namespace)
        
        # Try exact match first
        for deploy in deploys.items:
            if deploy.metadata.name == name:
                return deploy
        
        # Try partial match
        for deploy in deploys.items:
            if name in deploy.metadata.name:
                return deploy
        
        return None
    
    def _get_age(self, timestamp) -> str:
        """Get human-readable age."""
        if not timestamp:
            return "unknown"
        
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        age = now - timestamp.replace(tzinfo=timezone.utc)
        
        if age.days > 0:
            return f"{age.days}d"
        hours = age.seconds // 3600
        if hours > 0:
            return f"{hours}h"
        minutes = (age.seconds % 3600) // 60
        return f"{minutes}m"
    
    def _format_pod_describe(self, pod: client.V1Pod) -> str:
        """Format pod description."""
        lines = [
            f"📋 **Pod:** `{pod.metadata.name}`",
            f"Namespace: {pod.metadata.namespace}",
            f"Status: {pod.status.phase}",
            f"Node: {pod.spec.node_name or 'Not assigned'}",
            f"IP: {pod.status.pod_ip or 'N/A'}",
            "",
            "**Containers:**"
        ]
        
        for cs in pod.status.container_statuses or []:
            state = "Unknown"
            if cs.state.running:
                state = f"Running (started: {self._get_age(cs.state.running.started_at)})"
            elif cs.state.waiting:
                state = f"Waiting: {cs.state.waiting.reason}"
            elif cs.state.terminated:
                state = f"Terminated: {cs.state.terminated.reason}"
            
            lines.append(f"  • {cs.name}: {state} (restarts: {cs.restart_count})")
        
        return "\n".join(lines)
    
    def _format_deployment_describe(self, deploy: client.V1Deployment) -> str:
        """Format deployment description."""
        ready = deploy.status.ready_replicas or 0
        desired = deploy.spec.replicas or 0
        
        lines = [
            f"🚀 **Deployment:** `{deploy.metadata.name}`",
            f"Namespace: {deploy.metadata.namespace}",
            f"Replicas: {ready}/{desired} ready",
            f"Strategy: {deploy.spec.strategy.type if deploy.spec.strategy else 'N/A'}",
            "",
            "**Conditions:**"
        ]
        
        for cond in deploy.status.conditions or []:
            emoji = "🟢" if cond.status == "True" else "🔴"
            lines.append(f"  {emoji} {cond.type}: {cond.status}")
            if cond.message:
                lines.append(f"     {cond.message}")
        
        return "\n".join(lines)
