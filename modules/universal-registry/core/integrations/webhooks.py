#!/usr/bin/env python3
"""
Advanced Webhook & Multi-Level Communication System
Enterprise-grade notifications and integrations
Version: ∞.8
"""

import asyncio
import httpx
import json
import hmac
import hashlib
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime, timedelta
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


class WebhookEvent(str, Enum):
    """Webhook event types"""
    PLUGIN_REGISTERED = "plugin.registered"
    PLUGIN_UPDATED = "plugin.updated"
    PLUGIN_DELETED = "plugin.deleted"
    SERVICE_DISCOVERED = "service.discovered"
    HEALTH_CHANGED = "health.changed"
    ALERT_TRIGGERED = "alert.triggered"
    METRIC_THRESHOLD = "metric.threshold"
    CONFIGURATION_CHANGED = "configuration.changed"
    DEPLOYMENT_STARTED = "deployment.started"
    DEPLOYMENT_COMPLETED = "deployment.completed"
    DEPLOYMENT_FAILED = "deployment.failed"


class NotificationChannel(str, Enum):
    """Notification channels"""
    WEBHOOK = "webhook"
    EMAIL = "email"
    SLACK = "slack"
    TEAMS = "teams"
    PAGERDUTY = "pagerduty"
    SMS = "sms"
    PUSH = "push"
    DISCORD = "discord"


class NotificationPriority(str, Enum):
    """Notification priority"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class WebhookConfig:
    """Webhook configuration"""
    id: str
    name: str
    url: str
    events: List[WebhookEvent]
    secret: Optional[str] = None
    active: bool = True
    headers: Dict[str, str] = field(default_factory=dict)
    retry_policy: Dict[str, Any] = field(default_factory=lambda: {
        "max_retries": 3,
        "backoff_base": 2,
        "backoff_multiplier": 1.5
    })
    filters: Dict[str, Any] = field(default_factory=dict)
    transform: Optional[str] = None  # Transformation template
    timeout: int = 30
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    # Statistics
    total_sent: int = 0
    total_failed: int = 0
    last_sent: Optional[str] = None
    last_error: Optional[str] = None


@dataclass
class NotificationRule:
    """Notification rule"""
    id: str
    name: str
    channel: NotificationChannel
    priority: NotificationPriority
    conditions: Dict[str, Any]
    template: str
    config: Dict[str, Any] = field(default_factory=dict)
    active: bool = True
    cooldown: int = 300  # Seconds
    last_triggered: Optional[str] = None


@dataclass
class WebhookDelivery:
    """Webhook delivery attempt"""
    id: str
    webhook_id: str
    event_type: WebhookEvent
    payload: Dict[str, Any]
    attempt: int = 1
    status: str = "pending"  # pending, success, failed
    response_code: Optional[int] = None
    response_body: Optional[str] = None
    error: Optional[str] = None
    delivered_at: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class WebhookManager:
    """Manage webhooks and deliveries"""
    
    def __init__(self):
        self.webhooks: Dict[str, WebhookConfig] = {}
        self.deliveries: List[WebhookDelivery] = []
        self.max_deliveries = 1000
        
        # Dead letter queue for failed deliveries
        self.dlq: List[WebhookDelivery] = []
        
        # HTTP client with connection pooling
        self.client = httpx.AsyncClient(timeout=30.0)
    
    def register_webhook(self, config: WebhookConfig):
        """Register a new webhook"""
        self.webhooks[config.id] = config
        logger.info(f"Registered webhook: {config.name} ({config.id})")
    
    def remove_webhook(self, webhook_id: str):
        """Remove a webhook"""
        if webhook_id in self.webhooks:
            del self.webhooks[webhook_id]
            logger.info(f"Removed webhook: {webhook_id}")
    
    async def trigger(self, event_type: WebhookEvent, payload: Dict[str, Any]):
        """Trigger webhooks for event"""
        matching_webhooks = [
            webhook for webhook in self.webhooks.values()
            if webhook.active and event_type in webhook.events
            and self._matches_filters(payload, webhook.filters)
        ]
        
        if not matching_webhooks:
            return
        
        # Create deliveries
        tasks = []
        for webhook in matching_webhooks:
            delivery = WebhookDelivery(
                id=f"del_{datetime.utcnow().timestamp()}_{webhook.id}",
                webhook_id=webhook.id,
                event_type=event_type,
                payload=payload
            )
            self.deliveries.append(delivery)
            
            # Trim deliveries
            if len(self.deliveries) > self.max_deliveries:
                self.deliveries.pop(0)
            
            # Deliver asynchronously
            tasks.append(self._deliver_webhook(webhook, delivery))
        
        # Execute in parallel
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _deliver_webhook(self, webhook: WebhookConfig, delivery: WebhookDelivery):
        """Deliver webhook with retry logic"""
        max_retries = webhook.retry_policy["max_retries"]
        backoff_base = webhook.retry_policy["backoff_base"]
        backoff_multiplier = webhook.retry_policy["backoff_multiplier"]
        
        for attempt in range(1, max_retries + 1):
            delivery.attempt = attempt
            
            try:
                # Prepare payload
                payload = delivery.payload.copy()
                
                # Apply transformation if configured
                if webhook.transform:
                    payload = self._apply_transform(payload, webhook.transform)
                
                # Add metadata
                payload["event_type"] = delivery.event_type.value
                payload["delivery_id"] = delivery.id
                payload["timestamp"] = datetime.utcnow().isoformat()
                
                # Sign payload if secret configured
                headers = webhook.headers.copy()
                if webhook.secret:
                    signature = self._sign_payload(payload, webhook.secret)
                    headers["X-Webhook-Signature"] = signature
                
                # Send request
                response = await self.client.post(
                    webhook.url,
                    json=payload,
                    headers=headers,
                    timeout=webhook.timeout
                )
                
                delivery.response_code = response.status_code
                delivery.response_body = response.text[:1000]
                
                if response.status_code < 300:
                    # Success
                    delivery.status = "success"
                    delivery.delivered_at = datetime.utcnow().isoformat()
                    webhook.total_sent += 1
                    webhook.last_sent = delivery.delivered_at
                    logger.info(f"Webhook delivered: {webhook.name} ({delivery.id})")
                    return
                else:
                    # HTTP error
                    delivery.error = f"HTTP {response.status_code}"
                    logger.warning(f"Webhook HTTP error: {webhook.name} - {delivery.error}")
            
            except Exception as e:
                delivery.error = str(e)
                logger.error(f"Webhook delivery failed: {webhook.name} - {e}")
            
            # Retry with backoff
            if attempt < max_retries:
                wait_time = backoff_base ** attempt * backoff_multiplier
                await asyncio.sleep(wait_time)
        
        # All retries failed
        delivery.status = "failed"
        webhook.total_failed += 1
        webhook.last_error = delivery.error
        
        # Add to dead letter queue
        self.dlq.append(delivery)
        
        logger.error(f"Webhook permanently failed after {max_retries} attempts: {webhook.name}")
    
    def _matches_filters(self, payload: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        """Check if payload matches filters"""
        if not filters:
            return True
        
        for key, value in filters.items():
            if key not in payload:
                return False
            
            if isinstance(value, list):
                if payload[key] not in value:
                    return False
            elif payload[key] != value:
                return False
        
        return True
    
    def _apply_transform(self, payload: Dict[str, Any], template: str) -> Dict[str, Any]:
        """Apply transformation template"""
        # Simple template substitution
        # In production, use Jinja2 or similar
        try:
            result = {}
            for line in template.split('\n'):
                if '=' in line:
                    key, expr = line.split('=', 1)
                    key = key.strip()
                    expr = expr.strip()
                    
                    # Simple eval (dangerous in production - use safe template engine)
                    if expr.startswith('payload.'):
                        field = expr[8:]
                        result[key] = payload.get(field)
                    else:
                        result[key] = expr
            
            return result if result else payload
        except Exception as e:
            logger.error(f"Transform failed: {e}")
            return payload
    
    def _sign_payload(self, payload: Dict[str, Any], secret: str) -> str:
        """Sign payload with HMAC"""
        payload_bytes = json.dumps(payload, sort_keys=True).encode()
        signature = hmac.new(
            secret.encode(),
            payload_bytes,
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def get_stats(self) -> Dict[str, Any]:
        """Get webhook statistics"""
        return {
            "total_webhooks": len(self.webhooks),
            "active_webhooks": len([w for w in self.webhooks.values() if w.active]),
            "total_deliveries": len(self.deliveries),
            "dlq_size": len(self.dlq),
            "webhooks": {
                wh_id: {
                    "name": wh.name,
                    "total_sent": wh.total_sent,
                    "total_failed": wh.total_failed,
                    "last_sent": wh.last_sent,
                    "success_rate": wh.total_sent / (wh.total_sent + wh.total_failed) * 100
                    if (wh.total_sent + wh.total_failed) > 0 else 0
                }
                for wh_id, wh in self.webhooks.items()
            }
        }


class NotificationManager:
    """Manage multi-channel notifications"""
    
    def __init__(self):
        self.rules: Dict[str, NotificationRule] = {}
        self.channels: Dict[NotificationChannel, Callable] = {}
        
        # Notification history
        self.history: List[Dict[str, Any]] = []
        self.max_history = 500
        
        # Setup default channels
        self._setup_default_channels()
    
    def _setup_default_channels(self):
        """Setup default notification channels"""
        self.channels[NotificationChannel.WEBHOOK] = self._send_webhook
        self.channels[NotificationChannel.EMAIL] = self._send_email
        self.channels[NotificationChannel.SLACK] = self._send_slack
        self.channels[NotificationChannel.TEAMS] = self._send_teams
        self.channels[NotificationChannel.PAGERDUTY] = self._send_pagerduty
    
    def add_rule(self, rule: NotificationRule):
        """Add notification rule"""
        self.rules[rule.id] = rule
        logger.info(f"Added notification rule: {rule.name}")
    
    def remove_rule(self, rule_id: str):
        """Remove notification rule"""
        if rule_id in self.rules:
            del self.rules[rule_id]
            logger.info(f"Removed notification rule: {rule_id}")
    
    async def notify(self, event: Dict[str, Any]):
        """Evaluate and send notifications"""
        matching_rules = []
        
        for rule in self.rules.values():
            if not rule.active:
                continue
            
            # Check cooldown
            if rule.last_triggered:
                last = datetime.fromisoformat(rule.last_triggered)
                if (datetime.utcnow() - last).total_seconds() < rule.cooldown:
                    continue
            
            # Evaluate conditions
            if self._evaluate_conditions(event, rule.conditions):
                matching_rules.append(rule)
        
        # Send notifications
        tasks = []
        for rule in matching_rules:
            tasks.append(self._send_notification(rule, event))
        
        await asyncio.gather(*tasks, return_exceptions=True)
    
    def _evaluate_conditions(self, event: Dict[str, Any], conditions: Dict[str, Any]) -> bool:
        """Evaluate notification conditions"""
        for key, condition in conditions.items():
            if key not in event:
                return False
            
            value = event[key]
            
            # Handle different condition types
            if isinstance(condition, dict):
                if "eq" in condition and value != condition["eq"]:
                    return False
                if "gt" in condition and value <= condition["gt"]:
                    return False
                if "lt" in condition and value >= condition["lt"]:
                    return False
                if "in" in condition and value not in condition["in"]:
                    return False
            elif value != condition:
                return False
        
        return True
    
    async def _send_notification(self, rule: NotificationRule, event: Dict[str, Any]):
        """Send notification via channel"""
        try:
            # Render template
            message = self._render_template(rule.template, event)
            
            # Send via channel
            if rule.channel in self.channels:
                await self.channels[rule.channel](message, rule.config)
            
            # Update rule
            rule.last_triggered = datetime.utcnow().isoformat()
            
            # Add to history
            self.history.append({
                "rule_id": rule.id,
                "rule_name": rule.name,
                "channel": rule.channel.value,
                "priority": rule.priority.value,
                "message": message[:200],
                "timestamp": rule.last_triggered
            })
            
            if len(self.history) > self.max_history:
                self.history.pop(0)
            
            logger.info(f"Sent notification: {rule.name} via {rule.channel.value}")
        
        except Exception as e:
            logger.error(f"Failed to send notification: {rule.name} - {e}")
    
    def _render_template(self, template: str, event: Dict[str, Any]) -> str:
        """Render notification template"""
        # Simple template rendering
        message = template
        for key, value in event.items():
            message = message.replace(f"{{{{{key}}}}}", str(value))
        return message
    
    async def _send_webhook(self, message: str, config: Dict[str, Any]):
        """Send webhook notification"""
        url = config.get("url")
        if not url:
            return
        
        async with httpx.AsyncClient() as client:
            await client.post(url, json={"message": message})
    
    async def _send_email(self, message: str, config: Dict[str, Any]):
        """Send email notification"""
        # Placeholder - integrate with SMTP/SendGrid/etc
        logger.info(f"EMAIL: {message}")
    
    async def _send_slack(self, message: str, config: Dict[str, Any]):
        """Send Slack notification"""
        webhook_url = config.get("webhook_url")
        if not webhook_url:
            return
        
        async with httpx.AsyncClient() as client:
            await client.post(webhook_url, json={"text": message})
    
    async def _send_teams(self, message: str, config: Dict[str, Any]):
        """Send Microsoft Teams notification"""
        webhook_url = config.get("webhook_url")
        if not webhook_url:
            return
        
        async with httpx.AsyncClient() as client:
            await client.post(webhook_url, json={"text": message})
    
    async def _send_pagerduty(self, message: str, config: Dict[str, Any]):
        """Send PagerDuty alert"""
        routing_key = config.get("routing_key")
        if not routing_key:
            return
        
        payload = {
            "routing_key": routing_key,
            "event_action": "trigger",
            "payload": {
                "summary": message,
                "severity": "critical",
                "source": "universal-registry"
            }
        }
        
        async with httpx.AsyncClient() as client:
            await client.post("https://events.pagerduty.com/v2/enqueue", json=payload)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get notification statistics"""
        return {
            "total_rules": len(self.rules),
            "active_rules": len([r for r in self.rules.values() if r.active]),
            "total_sent": len(self.history),
            "by_channel": defaultdict(int),
            "by_priority": defaultdict(int),
            "recent_notifications": self.history[-10:]
        }


# Global instances
webhook_manager = WebhookManager()
notification_manager = NotificationManager()
