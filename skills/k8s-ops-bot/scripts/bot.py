#!/usr/bin/env python3
"""
K8s Ops Bot - Main Controller
Orchestrates watcher, inspector, commander, and remediator components.
Integrates deeply with OpenClaw messaging system.

Usage:
    python3 bot.py --config /path/to/config.yaml
    python3 bot.py --config /path/to/config.yaml --daemon
    python3 bot.py --config /path/to/config.yaml --once  # Single inspection
"""

import argparse
import asyncio
import json
import logging
import signal
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('k8s-ops-bot')


class MessageBus:
    """
    Message bus for OpenClaw integration.
    Simulates communication with OpenClaw messaging system.
    In production, this interfaces with OpenClaw's message tool.
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.alert_channel = config.get('alert_channel', 'default')
        self.command_channel = config.get('command_channel', 'default')
        self.command_handlers: List[Callable] = []
        
    def send_alert(self, alert: Dict, mention: bool = False) -> None:
        """Send alert notification via OpenClaw."""
        formatted = self._format_alert(alert)
        
        # In real implementation, this calls OpenClaw message tool
        # For now, output structured JSON that OpenClaw can capture
        output = {
            "type": "k8s_alert",
            "channel": self.alert_channel,
            "mention": mention,
            "content": formatted,
            "raw": alert
        }
        print(json.dumps(output, ensure_ascii=False))
        logger.info(f"Alert sent: {alert.get('title', 'unknown')}")
    
    def send_summary(self, summary: Dict) -> None:
        """Send periodic summary report."""
        formatted = self._format_summary(summary)
        output = {
            "type": "k8s_summary",
            "channel": self.alert_channel,
            "content": formatted,
            "raw": summary
        }
        print(json.dumps(output, ensure_ascii=False))
    
    def register_command_handler(self, handler: Callable) -> None:
        """Register handler for incoming commands."""
        self.command_handlers.append(handler)
    
    def process_command(self, command_str: str, user: str = "unknown") -> Dict:
        """Process incoming command from OpenClaw."""
        logger.info(f"Processing command from {user}: {command_str}")
        
        for handler in self.command_handlers:
            result = handler(command_str, user)
            if result:
                return result
        
        return {
            "success": False,
            "message": f"Unknown command: {command_str}"
        }
    
    def _format_alert(self, alert: Dict) -> str:
        """Format alert for human reading."""
        severity_emoji = {
            "critical": "🔴",
            "high": "🟠", 
            "warning": "🟡",
            "info": "🔵"
        }
        
        emoji = severity_emoji.get(alert.get('severity', 'info'), "⚪")
        lines = [
            f"{emoji} **K8s Alert** - {alert.get('title', 'Unknown')}",
            f"Severity: {alert.get('severity', 'unknown').upper()}",
            f"Resource: {alert.get('resource_type', 'Unknown')}/{alert.get('resource_name', 'Unknown')}",
            f"Namespace: {alert.get('namespace', 'unknown')}",
            f"Time: {alert.get('timestamp', datetime.now(timezone.utc).isoformat())}",
            "",
            f"**Message:** {alert.get('message', 'No details')}",
        ]
        
        if alert.get('suggestion'):
            lines.extend(["", f"💡 **Suggestion:** {alert['suggestion']}"])
        
        if alert.get('actions'):
            lines.extend(["", "**Actions:**"])
            for action in alert['actions']:
                lines.append(f"  • {action}")
        
        return "\n".join(lines)
    
    def _format_summary(self, summary: Dict) -> str:
        """Format summary report."""
        status_emoji = "✅" if summary.get('status') == 'healthy' else "⚠️"
        
        lines = [
            f"{status_emoji} **K8s Health Summary** - {summary.get('cluster', 'Unknown')}",
            f"Namespace: {summary.get('namespace', 'all')}",
            f"Time: {summary.get('timestamp', datetime.now(timezone.utc).isoformat())}",
            "",
            f"**Issues Found:** {summary.get('total_issues', 0)}",
        ]
        
        severity = summary.get('severity_breakdown', {})
        if severity.get('critical', 0) > 0:
            lines.append(f"  🔴 Critical: {severity['critical']}")
        if severity.get('high', 0) > 0:
            lines.append(f"  🟠 High: {severity['high']}")
        if severity.get('warning', 0) > 0:
            lines.append(f"  🟡 Warning: {severity['warning']}")
        
        # Add top issues
        top_issues = summary.get('top_issues', [])
        if top_issues:
            lines.extend(["", "**Top Issues:**"])
            for issue in top_issues[:5]:
                lines.append(f"  • [{issue.get('severity', 'unknown')}] {issue.get('resource', 'unknown')}: {issue.get('message', '')[:50]}...")
        
        return "\n".join(lines)


class K8sOpsBot:
    """Main bot controller."""
    
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.message_bus = MessageBus(self.config.get('messaging', {}))
        self.running = False
        
        # Component instances
        self.watcher = None
        self.inspector = None
        self.commander = None
        self.remediator = None
        
        # Threads
        self.threads: List[threading.Thread] = []
        
        # Signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _load_config(self, path: str) -> Dict:
        """Load configuration from YAML."""
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}, shutting down...")
        self.running = False
    
    def _init_components(self) -> None:
        """Initialize all bot components."""
        # Import components dynamically to avoid loading unused modules
        try:
            from watcher import K8sWatcher
            from inspector import K8sInspector
            from commander import K8sCommander
            from remediator import K8sRemediator
        except ImportError as e:
            logger.error(f"Failed to import components: {e}")
            logger.error("Make sure all scripts are in the same directory")
            sys.exit(1)
        
        # Initialize watcher
        if self.config.get('watcher', {}).get('enabled', True):
            self.watcher = K8sWatcher(
                kubeconfig=self.config['kubeconfig'],
                namespace=self.config.get('namespace', 'default'),
                message_bus=self.message_bus,
                config=self.config.get('watcher', {})
            )
            logger.info("Watcher initialized")
        
        # Initialize inspector
        if self.config.get('inspector', {}).get('enabled', True):
            self.inspector = K8sInspector(
                kubeconfig=self.config['kubeconfig'],
                namespace=self.config.get('namespace', 'default'),
                message_bus=self.message_bus,
                config=self.config.get('inspector', {})
            )
            logger.info("Inspector initialized")
        
        # Initialize commander
        if self.config.get('commander', {}).get('enabled', True):
            self.commander = K8sCommander(
                kubeconfig=self.config['kubeconfig'],
                namespace=self.config.get('namespace', 'default'),
                message_bus=self.message_bus,
                config=self.config.get('commander', {})
            )
            self.message_bus.register_command_handler(self.commander.handle_command)
            logger.info("Commander initialized")
        
        # Initialize remediator
        if self.config.get('remediator', {}).get('enabled', False):
            self.remediator = K8sRemediator(
                kubeconfig=self.config['kubeconfig'],
                namespace=self.config.get('namespace', 'default'),
                message_bus=self.message_bus,
                config=self.config.get('remediator', {})
            )
            logger.info("Remediator initialized")
    
    def start_watcher(self) -> None:
        """Start event watcher in background thread."""
        if not self.watcher:
            return
        
        def watch_loop():
            while self.running:
                try:
                    self.watcher.watch()
                except Exception as e:
                    logger.error(f"Watcher error: {e}")
                    time.sleep(10)  # Retry after delay
        
        thread = threading.Thread(target=watch_loop, name="watcher")
        thread.daemon = True
        thread.start()
        self.threads.append(thread)
        logger.info("Watcher thread started")
    
    def start_inspector(self) -> None:
        """Start periodic inspector in background thread."""
        if not self.inspector:
            return
        
        interval = self.config.get('inspector', {}).get('interval_minutes', 30)
        
        def inspect_loop():
            while self.running:
                try:
                    self.inspector.run_inspection()
                except Exception as e:
                    logger.error(f"Inspector error: {e}")
                
                # Sleep with interrupt check
                for _ in range(interval * 60):
                    if not self.running:
                        break
                    time.sleep(1)
        
        thread = threading.Thread(target=inspect_loop, name="inspector")
        thread.daemon = True
        thread.start()
        self.threads.append(thread)
        logger.info(f"Inspector thread started (interval: {interval}min)")
    
    def run_once(self) -> Dict:
        """Run single inspection cycle."""
        self._init_components()
        
        if self.inspector:
            return self.inspector.run_inspection()
        
        return {"error": "Inspector not enabled"}
    
    def run_daemon(self) -> None:
        """Run bot in daemon mode with all components."""
        logger.info("Starting K8s Ops Bot in daemon mode...")
        
        self._init_components()
        self.running = True
        
        # Start background threads
        self.start_watcher()
        self.start_inspector()
        
        logger.info("Bot is running. Press Ctrl+C to stop.")
        
        # Keep main thread alive
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        finally:
            self.shutdown()
    
    def shutdown(self) -> None:
        """Graceful shutdown."""
        logger.info("Shutting down...")
        self.running = False
        
        # Wait for threads
        for thread in self.threads:
            thread.join(timeout=5)
        
        logger.info("Shutdown complete")
    
    def handle_openclaw_message(self, message: Dict) -> Dict:
        """
        Entry point for OpenClaw message integration.
        Called when OpenClaw receives a message for this bot.
        """
        content = message.get('content', '')
        user = message.get('user', 'unknown')
        
        # Check if it's a command
        if content.startswith('/k8s'):
            return self.message_bus.process_command(content, user)
        
        # Could handle other message types here
        return {"success": False, "message": "Not a bot command"}


def main():
    parser = argparse.ArgumentParser(description="K8s Ops Bot")
    parser.add_argument("--config", "-c", required=True, help="Path to config file")
    parser.add_argument("--daemon", "-d", action="store_true", help="Run in daemon mode")
    parser.add_argument("--once", action="store_true", help="Run single inspection")
    parser.add_argument("--command", help="Execute single command and exit")
    args = parser.parse_args()
    
    bot = K8sOpsBot(args.config)
    
    if args.command:
        # Single command mode
        result = bot.handle_openclaw_message({
            'content': args.command,
            'user': 'cli'
        })
        print(json.dumps(result, indent=2))
    elif args.once:
        # Single inspection
        result = bot.run_once()
        print(json.dumps(result, indent=2))
    elif args.daemon:
        # Daemon mode
        bot.run_daemon()
    else:
        # Default: show help
        parser.print_help()
        print("\nExamples:")
        print(f"  python3 {sys.argv[0]} --config config.yaml --daemon")
        print(f"  python3 {sys.argv[0]} --config config.yaml --once")
        print(f"  python3 {sys.argv[0]} --config config.yaml --command '/k8s status'")


if __name__ == "__main__":
    main()
