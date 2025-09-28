"""
Task schemas
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime


class TaskBase(BaseModel):
    """Base task schema"""
    workflow_id: int
    agent_id: int
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    task_type: str = Field(default="ai_task", regex="^(ai_task|data_task|api_task|custom_task)$")
    priority: int = Field(default=0, ge=0, le=10)
    order: int = Field(default=0, ge=0)
    input_data: Optional[Dict[str, Any]] = None
    config: Optional[Dict[str, Any]] = None
    dependencies: Optional[List[int]] = None
    is_active: bool = Field(default=True)


class TaskCreate(TaskBase):
    """Task creation schema"""
    pass


class TaskUpdate(BaseModel):
    """Task update schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    task_type: Optional[str] = Field(None, regex="^(ai_task|data_task|api_task|custom_task)$")
    priority: Optional[int] = Field(None, ge=0, le=10)
    order: Optional[int] = Field(None, ge=0)
    input_data: Optional[Dict[str, Any]] = None
    config: Optional[Dict[str, Any]] = None
    dependencies: Optional[List[int]] = None
    is_active: Optional[bool] = None


class TaskResponse(TaskBase):
    """Task response schema"""
    id: int
    status: str
    output_data: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    
    class Config:
        from_attributes = True


class TaskExecutionBase(BaseModel):
    """Base task execution schema"""
    task_id: int
    workflow_execution_id: int
    input_data: Optional[Dict[str, Any]] = None


class TaskExecutionCreate(TaskExecutionBase):
    """Task execution creation schema"""
    pass


class TaskExecutionResponse(TaskExecutionBase):
    """Task execution response schema"""
    id: int
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    execution_log: Optional[Dict[str, Any]] = None
    tokens_used: int = 0
    execution_time: Optional[int] = None
    created_by: Optional[int] = None
    
    class Config:
        from_attributes = True


class TaskExecutionRequest(BaseModel):
    """Task execution request schema"""
    input_data: Optional[Dict[str, Any]] = None
    config: Optional[Dict[str, Any]] = None


class TaskStatus(BaseModel):
    """Task status schema"""
    task_id: int
    status: str
    progress: float = Field(ge=0, le=100)
    started_at: Optional[datetime] = None
    estimated_completion: Optional[datetime] = None
    agent_name: Optional[str] = None
    error_message: Optional[str] = None