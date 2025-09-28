"""
Agent management endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.agent import Agent
from app.schemas.agent import AgentCreate, AgentUpdate, AgentResponse
from app.services.agent_service import AgentService
from app.core.exceptions import NotFoundError, ValidationError

router = APIRouter()


@router.get("/", response_model=List[AgentResponse])
async def get_agents(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """Get all agents"""
    agent_service = AgentService(db)
    agents = await agent_service.get_agents(
        skip=skip,
        limit=limit,
        active_only=active_only
    )
    return agents


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: int,
    db: Session = Depends(get_db)
):
    """Get agent by ID"""
    agent_service = AgentService(db)
    agent = await agent_service.get_agent(agent_id)
    if not agent:
        raise NotFoundError("Agent", str(agent_id))
    return agent


@router.post("/", response_model=AgentResponse)
async def create_agent(
    agent_data: AgentCreate,
    db: Session = Depends(get_db)
):
    """Create a new agent"""
    agent_service = AgentService(db)
    try:
        agent = await agent_service.create_agent(agent_data)
        return agent
    except Exception as e:
        raise ValidationError(f"Failed to create agent: {str(e)}")


@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: int,
    agent_data: AgentUpdate,
    db: Session = Depends(get_db)
):
    """Update an agent"""
    agent_service = AgentService(db)
    try:
        agent = await agent_service.update_agent(agent_id, agent_data)
        if not agent:
            raise NotFoundError("Agent", str(agent_id))
        return agent
    except Exception as e:
        raise ValidationError(f"Failed to update agent: {str(e)}")


@router.delete("/{agent_id}")
async def delete_agent(
    agent_id: int,
    db: Session = Depends(get_db)
):
    """Delete an agent"""
    agent_service = AgentService(db)
    success = await agent_service.delete_agent(agent_id)
    if not success:
        raise NotFoundError("Agent", str(agent_id))
    return {"message": "Agent deleted successfully"}


@router.post("/{agent_id}/test")
async def test_agent(
    agent_id: int,
    test_input: dict,
    db: Session = Depends(get_db)
):
    """Test an agent with sample input"""
    agent_service = AgentService(db)
    try:
        result = await agent_service.test_agent(agent_id, test_input)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Agent test failed: {str(e)}"
        )


@router.get("/{agent_id}/capabilities")
async def get_agent_capabilities(
    agent_id: int,
    db: Session = Depends(get_db)
):
    """Get agent capabilities"""
    agent_service = AgentService(db)
    agent = await agent_service.get_agent(agent_id)
    if not agent:
        raise NotFoundError("Agent", str(agent_id))
    
    return {
        "agent_id": agent_id,
        "capabilities": agent.capabilities or [],
        "tools": agent.tools or []
    }