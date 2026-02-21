#!/usr/bin/env python3
"""
K8s Remediator - Auto-remediation engine with playbook support.
Analyzes issues and suggests or executes fixes.
"""

import logging
import os
import re
import yaml
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path

try:
    from kubernetes import client, config
    from kubernetes.client.exceptions import ApiException
except ImportError:
    raise ImportError("kubernetes client not installed. Run: pip install kubernetes")

logger = logging.getLogger('k8s-ops-bot.remediator')


class RemediationAction:
    """Represents a remediation action."""
    
    def __init__(self, action_type: str, description: str, 
                 handler: Callable, requires_confirm: bool = True):
        self.type = action_type
        self.description = description
        self.handler = handler
        self.requires_confirm = requires_confirm
    
    def execute(self, context: Dict) -> Dict:
        """Execute the action."""
        try:
            result = self.handler(context)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}


class K8sRemediator:
    """Auto-remediation engine for common k8s issues."""
    
    def __init__(self, kubeconfig: str, namespace: str, message_bus, config: Dict):
        self.kubeconfig = kubeconfig
        self.namespace = namespace
        self.message_bus = message_bus
        self.config = config
        
        # Load k8s config
        config.load_kube_config(config_file=kubeconfig)
        self.core_v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
        
        # Playbooks directory
        self.playbooks_dir = Path(__file__).parent.parent / "assets" / "playbooks"
        self.playbooks = self._load_playbooks()
        
        # Action handlers
        self.action_handlers = {
            "analyze": self._handle_analyze,
            "suggest": self._handle_suggest,
            "confirm": self._handle_confirm,
            "restart": self._handle_restart,
            "scale": self._handle_scale,
            "patch": self._handle_patch,
            "delete": self._handle_delete,
        }
        
        # Auto-remediation settings
        self.auto_fix_enabled = config.get('auto_fix', False)
        self.auto_fix_severity = config.get('auto_fix_severity', ['critical'])
    
    def _load_playbooks(self) -> List[Dict]:
        """Load remediation playbooks from disk."""
        playbooks = []
        
        if not self.playbooks_dir.exists():
            logger.warning(f"Playbooks directory not found: {self.playbooks_dir}")
            return playbooks
        
        for pb_file in self.playbooks_dir.glob("*.yaml"):
            try:
                with open(pb_file, 'r') as f:
                    pb = yaml.safe_load(f)
                    if pb:
                        playbooks.append(pb)
                        logger.info(f"Loaded playbook: {pb.get('name', pb_file.stem)}")
            except Exception as e:
                logger.error(f"Failed to load playbook {pb_file}: {e}")
        
        return playbooks
    
    def analyze_issue(self, issue: Dict) -> List[RemediationAction]:
        """Analyze issue and return list of remediation actions."""
        actions = []
        
        issue_type = issue.get('issue_type', '')
        reason = issue.get('reason', '')
        message = issue.get('message', '')
        resource_type = issue.get('resource_type', '')
        
        # Check matching playbooks
        for playbook in self.playbooks:
            if self._matches_playbook(playbook, issue):
                for action_def in playbook.get('actions', []):
                    action = self._create_action(action_def, issue)
                    if action:
                        actions.append(action)
        
        # Built-in remediations
        if "OOMKilled" in reason or "oom_killed" in issue_type:
            actions.extend(self._get_oom_remediations(issue))
        
        if "CrashLoopBackOff" in reason or "crashloopbackoff" in issue_type.lower():
            actions.extend(self._get_crashloop_remediations(issue))
        
        if "ImagePullBackOff" in reason or "imagepullbackoff" in issue_type.lower():
            actions.extend(self._get_imagepull_remediations(issue))
        
        if "Pending" in reason or "pod_pending" in issue_type:
            actions.extend(self._get_pending_remediations(issue))
        
        return actions
    
    def _matches_playbook(self, playbook: Dict, issue: Dict) -> bool:
        """Check if playbook matches issue."""
        triggers = playbook.get('triggers', [])
        
        for trigger in triggers:
            if trigger.get('issue_type') == issue.get('issue_type'):
                return True
            if trigger.get('reason') == issue.get('reason'):
                return True
            if trigger.get('resource_type') == issue.get('resource_type'):
                return True
        
        return False
    
    def _create_action(self, action_def: Dict, context: Dict) -> Optional[RemediationAction]:
        """Create RemediationAction from playbook definition."""
        action_type = action_def.get('type')
        
        if action_type not in self.action_handlers:
            logger.warning(f"Unknown action type: {action_type}")
            return None
        
        handler = self.action_handlers[action_type]
        description = action_def.get('description', f"{action_type} action")
        requires_confirm = action_def.get('requires_confirm', True)
        
        # Wrap handler with action_def params
        def wrapped_handler(ctx):
            return handler(ctx, action_def)
        
        return RemediationAction(
            action_type=action_type,
            description=description,
            handler=wrapped_handler,
            requires_confirm=requires_confirm
        )
    
    def _get_oom_remediations(self, issue: Dict) -> List[RemediationAction]:
        """Get remediation actions for OOMKilled."""
        actions = []
        
        # Analyze memory usage
        def analyze_memory(ctx):
            # In real implementation, fetch metrics
            return {"current_limit": "512Mi", "suggested_limit": "1Gi", "peak_usage": "800Mi"}
        
        actions.append(RemediationAction(
            action_type="analyze",
            description="Analyze memory usage patterns",
            handler=analyze_memory,
            requires_confirm=False
        ))
        
        # Suggest memory increase
        def suggest_memory(ctx):
            return {"suggestion": "Increase memory limit from 512Mi to 1Gi"}
        
        actions.append(RemediationAction(
            action_type="suggest",
            description="Suggest memory limit increase",
            handler=suggest_memory,
            requires_confirm=False
        ))
        
        return actions
    
    def _get_crashloop_remediations(self, issue: Dict) -> List[RemediationAction]:
        """Get remediation actions for CrashLoopBackOff."""
        actions = []
        
        # Get logs
        def get_logs(ctx):
            return {"action": "Run `/k8s logs <pod>` to check error logs"}
        
        actions.append(RemediationAction(
            action_type="suggest",
            description="Check container logs for errors",
            handler=get_logs,
            requires_confirm=False
        ))
        
        # Restart pod
        def restart_pod(ctx):
            return {"action": "Pod will be automatically restarted"}
        
        actions.append(RemediationAction(
            action_type="restart",
            description="Force pod restart",
            handler=restart_pod,
            requires_confirm=True
        ))
        
        return actions
    
    def _get_imagepull_remediations(self, issue: Dict) -> List[RemediationAction]:
        """Get remediation actions for ImagePullBackOff."""
        actions = []
        
        # Check registry connectivity
        def check_registry(ctx):
            return {"diagnostic": "Checking registry connectivity and image existence..."}
        
        actions.append(RemediationAction(
            action_type="analyze",
            description="Check image registry connectivity",
            handler=check_registry,
            requires_confirm=False
        ))
        
        return actions
    
    def _get_pending_remediations(self, issue: Dict) -> List[RemediationAction]:
        """Get remediation actions for Pending pods."""
        actions = []
        
        # Analyze scheduling
        def analyze_scheduling(ctx):
            return {"diagnostic": "Checking resource availability and node capacity..."}
        
        actions.append(RemediationAction(
            action_type="analyze",
            description="Analyze scheduling constraints",
            handler=analyze_scheduling,
            requires_confirm=False
        ))
        
        return actions
    
    # Action handlers
    
    def _handle_analyze(self, context: Dict, action_def: Dict) -> Dict:
        """Handle analyze action."""
        return {"status": "analyzed", "findings": "Analysis complete"}
    
    def _handle_suggest(self, context: Dict, action_def: Dict) -
        if not self.config or not isinstance(self.config, dict):
            return {"status": "skipped", "reason": "No config available"}
        
        # Check if auto-fix is enabled for this severity
        if self.auto_fix_enabled:
            severity = context.get('severity', 'warning')
            if severity in self.auto_fix_severity:
                return {"status": "auto_fix_enabled", "action": action_def.get('message', '')}
        
        return {"status": "suggested", "message": action_def.get('message', '')}
    
    def _handle_confirm(self, context: Dict, action_def: Dict) -
        if not self.config or not isinstance(self.config, dict):
            return {"status": "skipped", "reason": "No config available"}
        
        return {"status": "needs_confirmation", "action": action_def.get('cmd', '')}
    
    def _handle_restart(self, context: Dict, action_def: Dict) -
        if not self.config or not isinstance(self.config, dict):
            return {"status": "skipped", "reason": "No config available"}
        
        # Implementation would delete pod or trigger deployment restart
        return {"status": "restart_initiated"}
    
    def _handle_scale(self, context: Dict, action_def: Dict) -
        if not self.config or not isinstance(self.config, dict):
            return {"status": "skipped", "reason": "No config available"}
        
        return {"status": "scale_suggested", "replicas": action_def.get('replicas', 1)}
    
    def _handle_patch(self, context: Dict, action_def: Dict) -
        if not self.config or not isinstance(self.config, dict):
            return {"status": "skipped", "reason": "No config available"}
        
        return {"status": "patch_prepared", "path": action_def.get('path', '')}
    
    def _handle_delete(self, context: Dict, action_def: Dict) -
        if not self.config or not isinstance(self.config, dict):
            return {"status": "skipped", "reason": "No config available"}
        
        return {"status": "delete_prepared"}
    
    def process_alert(self, alert: Dict) -
        if not self.config or not isinstance(self.config, dict):
            return {"status": "skipped", "reason": "No config available"}
        
        """Process an alert and return remediation suggestions."""
        logger.info(f"Processing alert for remediation: {alert.get('title', 'unknown')}")
        
        # Convert alert to issue format
        issue = {
            'issue_type': alert.get('reason', 'unknown'),
            'reason': alert.get('reason', ''),
            'message': alert.get('message', ''),
            'resource_type': alert.get('resource_type', ''),
            'resource_name': alert.get('resource_name', ''),
            'namespace': alert.get('namespace', ''),
            'severity': alert.get('severity', 'warning')
        }
        
        # Get remediation actions
        actions = self.analyze_issue(issue)
        
        if not actions:
            return {"status": "no_remediation", "issue": issue}
        
        # Execute non-confirm actions, collect confirm actions
        results = []
        pending_confirmations = []
        
        for action in actions:
            if action.requires_confirm:
                pending_confirmations.append({
                    "type": action.type,
                    "description": action.description
                })
            else:
                result = action.execute(issue)
                results.append({
                    "action": action.type,
                    "result": result
                })
        
        response = {
            "status": "processed",
            "issue": issue,
            "executed": results,
            "pending_confirmations": pending_confirmations
        }
        
        # Add to alert
        if pending_confirmations or results:
            suggestions = []
            for r in results:
                if r['result'].get('success'):
                    msg = r['result'].get('result', {}).get('suggestion', r['result'].get('result', {}).get('message', ''))
                    if msg:
                        suggestions.append(f"💡 {msg}")
            
            for pc in pending_confirmations:
                suggestions.append(f"⚠️ {pc['description']} (requires confirmation)")
            
            alert['suggestions'] = suggestions
        
        return response
