"""
WebSocket endpoints
"""

import json
import uuid
from typing import Dict, Any
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.websocket import websocket_manager
from app.services.workflow_service import WorkflowService
from app.services.task_service import TaskService

router = APIRouter()


@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    """Main WebSocket endpoint"""
    client_id = str(uuid.uuid4())
    
    try:
        await websocket_manager.connect(websocket, client_id)
        
        # Send welcome message
        await websocket_manager.send_personal_message({
            "type": "connection_established",
            "client_id": client_id,
            "message": "Connected to CrewAI Cerebras Platform"
        }, client_id)
        
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            await handle_websocket_message(client_id, message)
            
    except WebSocketDisconnect:
        websocket_manager.disconnect(client_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        websocket_manager.disconnect(client_id)


@router.websocket("/workflow/{workflow_id}")
async def workflow_websocket(websocket: WebSocket, workflow_id: int):
    """Workflow-specific WebSocket endpoint"""
    client_id = str(uuid.uuid4())
    
    try:
        await websocket_manager.connect(websocket, client_id, {"workflow_id": workflow_id})
        
        # Subscribe to workflow updates
        await websocket_manager.subscribe_to_workflow(client_id, str(workflow_id))
        
        # Send welcome message
        await websocket_manager.send_personal_message({
            "type": "workflow_connected",
            "workflow_id": workflow_id,
            "client_id": client_id,
            "message": f"Connected to workflow {workflow_id}"
        }, client_id)
        
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle workflow-specific messages
            await handle_workflow_message(client_id, workflow_id, message)
            
    except WebSocketDisconnect:
        websocket_manager.disconnect(client_id)
    except Exception as e:
        print(f"Workflow WebSocket error: {e}")
        websocket_manager.disconnect(client_id)


@router.websocket("/agent/{agent_id}")
async def agent_websocket(websocket: WebSocket, agent_id: int):
    """Agent-specific WebSocket endpoint"""
    client_id = str(uuid.uuid4())
    
    try:
        await websocket_manager.connect(websocket, client_id, {"agent_id": agent_id})
        
        # Subscribe to agent updates
        await websocket_manager.subscribe_to_agent(client_id, str(agent_id))
        
        # Send welcome message
        await websocket_manager.send_personal_message({
            "type": "agent_connected",
            "agent_id": agent_id,
            "client_id": client_id,
            "message": f"Connected to agent {agent_id}"
        }, client_id)
        
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle agent-specific messages
            await handle_agent_message(client_id, agent_id, message)
            
    except WebSocketDisconnect:
        websocket_manager.disconnect(client_id)
    except Exception as e:
        print(f"Agent WebSocket error: {e}")
        websocket_manager.disconnect(client_id)


async def handle_websocket_message(client_id: str, message: Dict[str, Any]):
    """Handle general WebSocket messages"""
    message_type = message.get("type")
    
    if message_type == "ping":
        await websocket_manager.send_personal_message({
            "type": "pong",
            "timestamp": message.get("timestamp")
        }, client_id)
    
    elif message_type == "subscribe_workflow":
        workflow_id = message.get("workflow_id")
        if workflow_id:
            await websocket_manager.subscribe_to_workflow(client_id, str(workflow_id))
            await websocket_manager.send_personal_message({
                "type": "subscribed",
                "workflow_id": workflow_id,
                "message": f"Subscribed to workflow {workflow_id}"
            }, client_id)
    
    elif message_type == "unsubscribe_workflow":
        workflow_id = message.get("workflow_id")
        if workflow_id:
            await websocket_manager.unsubscribe_from_workflow(client_id, str(workflow_id))
            await websocket_manager.send_personal_message({
                "type": "unsubscribed",
                "workflow_id": workflow_id,
                "message": f"Unsubscribed from workflow {workflow_id}"
            }, client_id)
    
    elif message_type == "subscribe_agent":
        agent_id = message.get("agent_id")
        if agent_id:
            await websocket_manager.subscribe_to_agent(client_id, str(agent_id))
            await websocket_manager.send_personal_message({
                "type": "subscribed",
                "agent_id": agent_id,
                "message": f"Subscribed to agent {agent_id}"
            }, client_id)
    
    elif message_type == "unsubscribe_agent":
        agent_id = message.get("agent_id")
        if agent_id:
            await websocket_manager.unsubscribe_from_agent(client_id, str(agent_id))
            await websocket_manager.send_personal_message({
                "type": "unsubscribed",
                "agent_id": agent_id,
                "message": f"Unsubscribed from agent {agent_id}"
            }, client_id)
    
    else:
        await websocket_manager.send_personal_message({
            "type": "error",
            "message": f"Unknown message type: {message_type}"
        }, client_id)


async def handle_workflow_message(client_id: str, workflow_id: int, message: Dict[str, Any]):
    """Handle workflow-specific WebSocket messages"""
    message_type = message.get("type")
    
    if message_type == "get_workflow_status":
        # Get workflow status and send update
        await websocket_manager.send_personal_message({
            "type": "workflow_status",
            "workflow_id": workflow_id,
            "status": "running"  # This would be fetched from the database
        }, client_id)
    
    elif message_type == "get_workflow_tasks":
        # Get workflow tasks and send update
        await websocket_manager.send_personal_message({
            "type": "workflow_tasks",
            "workflow_id": workflow_id,
            "tasks": []  # This would be fetched from the database
        }, client_id)
    
    else:
        await websocket_manager.send_personal_message({
            "type": "error",
            "message": f"Unknown workflow message type: {message_type}"
        }, client_id)


async def handle_agent_message(client_id: str, agent_id: int, message: Dict[str, Any]):
    """Handle agent-specific WebSocket messages"""
    message_type = message.get("type")
    
    if message_type == "get_agent_status":
        # Get agent status and send update
        await websocket_manager.send_personal_message({
            "type": "agent_status",
            "agent_id": agent_id,
            "status": "idle"  # This would be fetched from the database
        }, client_id)
    
    elif message_type == "test_agent":
        # Test agent with provided input
        test_input = message.get("input", "")
        await websocket_manager.send_personal_message({
            "type": "agent_test_result",
            "agent_id": agent_id,
            "input": test_input,
            "output": "Test result would be here"  # This would be the actual test result
        }, client_id)
    
    else:
        await websocket_manager.send_personal_message({
            "type": "error",
            "message": f"Unknown agent message type: {message_type}"
        }, client_id)