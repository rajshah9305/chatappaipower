"""
WebSocket connection management
"""

import asyncio
import json
import logging
from typing import Dict, Set, Optional, Any
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime

from app.core.config import settings

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.connection_metadata: Dict[str, Dict[str, Any]] = {}
        self.workflow_subscriptions: Dict[str, Set[str]] = {}
        self.agent_subscriptions: Dict[str, Set[str]] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str, metadata: Optional[Dict[str, Any]] = None):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        self.active_connections[client_id] = websocket
        self.connection_metadata[client_id] = {
            "connected_at": datetime.utcnow().isoformat(),
            "last_activity": datetime.utcnow().isoformat(),
            **(metadata or {})
        }
        logger.info(f"Client {client_id} connected")
    
    def disconnect(self, client_id: str):
        """Remove a WebSocket connection"""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        
        if client_id in self.connection_metadata:
            del self.connection_metadata[client_id]
        
        # Remove from all subscriptions
        for workflow_id, subscribers in self.workflow_subscriptions.items():
            subscribers.discard(client_id)
        
        for agent_id, subscribers in self.agent_subscriptions.items():
            subscribers.discard(client_id)
        
        logger.info(f"Client {client_id} disconnected")
    
    async def send_personal_message(self, message: dict, client_id: str):
        """Send a message to a specific client"""
        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_text(json.dumps(message))
                self.connection_metadata[client_id]["last_activity"] = datetime.utcnow().isoformat()
            except Exception as e:
                logger.error(f"Error sending message to {client_id}: {e}")
                self.disconnect(client_id)
    
    async def broadcast(self, message: dict):
        """Broadcast a message to all connected clients"""
        disconnected_clients = []
        
        for client_id, connection in self.active_connections.items():
            try:
                await connection.send_text(json.dumps(message))
                self.connection_metadata[client_id]["last_activity"] = datetime.utcnow().isoformat()
            except Exception as e:
                logger.error(f"Error broadcasting to {client_id}: {e}")
                disconnected_clients.append(client_id)
        
        # Clean up disconnected clients
        for client_id in disconnected_clients:
            self.disconnect(client_id)
    
    async def subscribe_to_workflow(self, client_id: str, workflow_id: str):
        """Subscribe a client to workflow updates"""
        if workflow_id not in self.workflow_subscriptions:
            self.workflow_subscriptions[workflow_id] = set()
        
        self.workflow_subscriptions[workflow_id].add(client_id)
        logger.info(f"Client {client_id} subscribed to workflow {workflow_id}")
    
    async def unsubscribe_from_workflow(self, client_id: str, workflow_id: str):
        """Unsubscribe a client from workflow updates"""
        if workflow_id in self.workflow_subscriptions:
            self.workflow_subscriptions[workflow_id].discard(client_id)
            if not self.workflow_subscriptions[workflow_id]:
                del self.workflow_subscriptions[workflow_id]
        
        logger.info(f"Client {client_id} unsubscribed from workflow {workflow_id}")
    
    async def subscribe_to_agent(self, client_id: str, agent_id: str):
        """Subscribe a client to agent updates"""
        if agent_id not in self.agent_subscriptions:
            self.agent_subscriptions[agent_id] = set()
        
        self.agent_subscriptions[agent_id].add(client_id)
        logger.info(f"Client {client_id} subscribed to agent {agent_id}")
    
    async def unsubscribe_from_agent(self, client_id: str, agent_id: str):
        """Unsubscribe a client from agent updates"""
        if agent_id in self.agent_subscriptions:
            self.agent_subscriptions[agent_id].discard(client_id)
            if not self.agent_subscriptions[agent_id]:
                del self.agent_subscriptions[agent_id]
        
        logger.info(f"Client {client_id} unsubscribed from agent {agent_id}")
    
    async def broadcast_workflow_update(self, workflow_id: str, message: dict):
        """Broadcast workflow update to subscribed clients"""
        if workflow_id in self.workflow_subscriptions:
            disconnected_clients = []
            
            for client_id in self.workflow_subscriptions[workflow_id]:
                try:
                    await self.send_personal_message(message, client_id)
                except Exception as e:
                    logger.error(f"Error sending workflow update to {client_id}: {e}")
                    disconnected_clients.append(client_id)
            
            # Clean up disconnected clients
            for client_id in disconnected_clients:
                self.disconnect(client_id)
    
    async def broadcast_agent_update(self, agent_id: str, message: dict):
        """Broadcast agent update to subscribed clients"""
        if agent_id in self.agent_subscriptions:
            disconnected_clients = []
            
            for client_id in self.agent_subscriptions[agent_id]:
                try:
                    await self.send_personal_message(message, client_id)
                except Exception as e:
                    logger.error(f"Error sending agent update to {client_id}: {e}")
                    disconnected_clients.append(client_id)
            
            # Clean up disconnected clients
            for client_id in disconnected_clients:
                self.disconnect(client_id)
    
    async def get_connection_info(self) -> dict:
        """Get information about active connections"""
        return {
            "total_connections": len(self.active_connections),
            "workflow_subscriptions": len(self.workflow_subscriptions),
            "agent_subscriptions": len(self.agent_subscriptions),
            "connections": [
                {
                    "client_id": client_id,
                    "metadata": metadata
                }
                for client_id, metadata in self.connection_metadata.items()
            ]
        }
    
    async def disconnect_all(self):
        """Disconnect all clients"""
        for client_id in list(self.active_connections.keys()):
            self.disconnect(client_id)
        
        logger.info("All WebSocket connections closed")


# Global WebSocket manager
websocket_manager = ConnectionManager()