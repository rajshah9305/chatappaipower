"""
Agent service for managing AI agents
"""

import asyncio
import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.agent import Agent
from app.schemas.agent import AgentCreate, AgentUpdate, AgentResponse, AgentTestResponse
from app.services.cerebras_service import cerebras_service
from app.core.exceptions import NotFoundError, ValidationError

logger = logging.getLogger(__name__)


class AgentService:
    """Service for managing AI agents"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_agents(
        self,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = True
    ) -> List[AgentResponse]:
        """Get all agents"""
        try:
            query = self.db.query(Agent)
            
            if active_only:
                query = query.filter(Agent.is_active == True)
            
            agents = query.offset(skip).limit(limit).all()
            
            return [AgentResponse.from_orm(agent) for agent in agents]
            
        except Exception as e:
            logger.error(f"Error getting agents: {e}")
            raise ValidationError(f"Failed to retrieve agents: {str(e)}")
    
    async def get_agent(self, agent_id: int) -> Optional[AgentResponse]:
        """Get agent by ID"""
        try:
            agent = self.db.query(Agent).filter(Agent.id == agent_id).first()
            
            if not agent:
                return None
            
            return AgentResponse.from_orm(agent)
            
        except Exception as e:
            logger.error(f"Error getting agent {agent_id}: {e}")
            raise ValidationError(f"Failed to retrieve agent: {str(e)}")
    
    async def create_agent(self, agent_data: AgentCreate) -> AgentResponse:
        """Create a new agent"""
        try:
            # Validate model
            if not await cerebras_service.validate_model(agent_data.model):
                raise ValidationError(f"Invalid model: {agent_data.model}")
            
            # Create agent
            agent = Agent(
                name=agent_data.name,
                role=agent_data.role,
                goal=agent_data.goal,
                backstory=agent_data.backstory,
                model=agent_data.model,
                temperature=agent_data.temperature,
                max_tokens=agent_data.max_tokens,
                top_p=agent_data.top_p,
                is_active=agent_data.is_active,
                config=agent_data.config,
                capabilities=agent_data.capabilities,
                tools=agent_data.tools
            )
            
            self.db.add(agent)
            self.db.commit()
            self.db.refresh(agent)
            
            logger.info(f"Created agent: {agent.name}")
            return AgentResponse.from_orm(agent)
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating agent: {e}")
            raise ValidationError(f"Failed to create agent: {str(e)}")
    
    async def update_agent(self, agent_id: int, agent_data: AgentUpdate) -> Optional[AgentResponse]:
        """Update an agent"""
        try:
            agent = self.db.query(Agent).filter(Agent.id == agent_id).first()
            
            if not agent:
                return None
            
            # Validate model if provided
            if agent_data.model and not await cerebras_service.validate_model(agent_data.model):
                raise ValidationError(f"Invalid model: {agent_data.model}")
            
            # Update fields
            update_data = agent_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(agent, field, value)
            
            self.db.commit()
            self.db.refresh(agent)
            
            logger.info(f"Updated agent: {agent.name}")
            return AgentResponse.from_orm(agent)
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating agent {agent_id}: {e}")
            raise ValidationError(f"Failed to update agent: {str(e)}")
    
    async def delete_agent(self, agent_id: int) -> bool:
        """Delete an agent"""
        try:
            agent = self.db.query(Agent).filter(Agent.id == agent_id).first()
            
            if not agent:
                return False
            
            self.db.delete(agent)
            self.db.commit()
            
            logger.info(f"Deleted agent: {agent.name}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting agent {agent_id}: {e}")
            raise ValidationError(f"Failed to delete agent: {str(e)}")
    
    async def test_agent(self, agent_id: int, test_input: Dict[str, Any]) -> AgentTestResponse:
        """Test an agent with sample input"""
        try:
            agent = self.db.query(Agent).filter(Agent.id == agent_id).first()
            
            if not agent:
                raise NotFoundError("Agent", str(agent_id))
            
            # Build agent prompt
            agent_prompt = self._build_agent_prompt(agent, test_input)
            
            # Generate response
            start_time = asyncio.get_event_loop().time()
            
            response = await cerebras_service.generate_agent_response(
                agent_prompt=agent_prompt,
                context=test_input.get("context"),
                model=agent.model,
                max_tokens=agent.max_tokens,
                temperature=float(agent.temperature),
                top_p=float(agent.top_p)
            )
            
            end_time = asyncio.get_event_loop().time()
            execution_time = end_time - start_time
            
            return AgentTestResponse(
                agent_id=agent_id,
                input=test_input.get("input", ""),
                output=response["response"],
                execution_time=execution_time,
                tokens_used=response["tokens_used"],
                success=True
            )
            
        except Exception as e:
            logger.error(f"Error testing agent {agent_id}: {e}")
            return AgentTestResponse(
                agent_id=agent_id,
                input=test_input.get("input", ""),
                output="",
                execution_time=0.0,
                tokens_used=0,
                success=False,
                error=str(e)
            )
    
    def _build_agent_prompt(self, agent: Agent, test_input: Dict[str, Any]) -> str:
        """Build prompt for agent testing"""
        prompt = f"""
Agent Role: {agent.role}
Agent Goal: {agent.goal}
Agent Backstory: {agent.backstory}

Task: {test_input.get('input', '')}

Please provide a response based on your role and goal.
"""
        return prompt
    
    async def get_agent_capabilities(self, agent_id: int) -> Dict[str, Any]:
        """Get agent capabilities and tools"""
        try:
            agent = self.db.query(Agent).filter(Agent.id == agent_id).first()
            
            if not agent:
                raise NotFoundError("Agent", str(agent_id))
            
            return {
                "agent_id": agent_id,
                "capabilities": agent.capabilities or [],
                "tools": agent.tools or [],
                "model": agent.model,
                "config": agent.config or {}
            }
            
        except Exception as e:
            logger.error(f"Error getting agent capabilities {agent_id}: {e}")
            raise ValidationError(f"Failed to get agent capabilities: {str(e)}")
    
    async def activate_agent(self, agent_id: int) -> bool:
        """Activate an agent"""
        try:
            agent = self.db.query(Agent).filter(Agent.id == agent_id).first()
            
            if not agent:
                return False
            
            agent.is_active = True
            self.db.commit()
            
            logger.info(f"Activated agent: {agent.name}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error activating agent {agent_id}: {e}")
            raise ValidationError(f"Failed to activate agent: {str(e)}")
    
    async def deactivate_agent(self, agent_id: int) -> bool:
        """Deactivate an agent"""
        try:
            agent = self.db.query(Agent).filter(Agent.id == agent_id).first()
            
            if not agent:
                return False
            
            agent.is_active = False
            self.db.commit()
            
            logger.info(f"Deactivated agent: {agent.name}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deactivating agent {agent_id}: {e}")
            raise ValidationError(f"Failed to deactivate agent: {str(e)}")