"""
Main API router
"""

from fastapi import APIRouter
from app.api.v1.endpoints import agents, workflows, tasks, executions, websocket

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(workflows.router, prefix="/workflows", tags=["workflows"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(executions.router, prefix="/executions", tags=["executions"])
api_router.include_router(websocket.router, prefix="/ws", tags=["websocket"])