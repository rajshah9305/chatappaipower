"""
Agent schemas
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime


class AgentBase(BaseModel):
    """Base agent schema"""
    name: str = Field(..., min_length=1, max_length=100)
    role: str = Field(..., min_length=1, max_length=200)
    goal: str = Field(..., min_length=1)
    backstory: Optional[str] = None
    model: str = Field(default="llama-4-maverick-17b-128e-instruct")
    temperature: str = Field(default="0.6")
    max_tokens: int = Field(default=32768, ge=1, le=32768)
    top_p: str = Field(default="0.9")
    is_active: bool = Field(default=True)
    config: Optional[Dict[str, Any]] = None
    capabilities: Optional[List[str]] = None
    tools: Optional[List[str]] = None


class AgentCreate(AgentBase):
    """Agent creation schema"""
    pass


class AgentUpdate(BaseModel):
    """Agent update schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    role: Optional[str] = Field(None, min_length=1, max_length=200)
    goal: Optional[str] = Field(None, min_length=1)
    backstory: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[str] = None
    max_tokens: Optional[int] = Field(None, ge=1, le=32768)
    top_p: Optional[str] = None
    is_active: Optional[bool] = None
    config: Optional[Dict[str, Any]] = None
    capabilities: Optional[List[str]] = None
    tools: Optional[List[str]] = None


class AgentResponse(AgentBase):
    """Agent response schema"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    
    class Config:
        from_attributes = True


class AgentTestRequest(BaseModel):
    """Agent test request schema"""
    input: str = Field(..., min_length=1)
    context: Optional[Dict[str, Any]] = None


class AgentTestResponse(BaseModel):
    """Agent test response schema"""
    agent_id: int
    input: str
    output: str
    execution_time: float
    tokens_used: int
    success: bool
    error: Optional[str] = None