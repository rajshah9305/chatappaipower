"""
Workflow schemas
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime


class WorkflowBase(BaseModel):
    """Base workflow schema"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    workflow_type: str = Field(default="linear", regex="^(linear|parallel|conditional|loop)$")
    config: Optional[Dict[str, Any]] = None
    is_active: bool = Field(default=True)


class WorkflowCreate(WorkflowBase):
    """Workflow creation schema"""
    pass


class WorkflowUpdate(BaseModel):
    """Workflow update schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    workflow_type: Optional[str] = Field(None, regex="^(linear|parallel|conditional|loop)$")
    config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class WorkflowResponse(WorkflowBase):
    """Workflow response schema"""
    id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    execution_count: int = 0
    last_executed: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class WorkflowExecutionBase(BaseModel):
    """Base workflow execution schema"""
    workflow_id: int
    input_data: Optional[Dict[str, Any]] = None


class WorkflowExecutionCreate(WorkflowExecutionBase):
    """Workflow execution creation schema"""
    pass


class WorkflowExecutionResponse(WorkflowExecutionBase):
    """Workflow execution response schema"""
    id: int
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    execution_log: Optional[Dict[str, Any]] = None
    created_by: Optional[int] = None
    
    class Config:
        from_attributes = True


class WorkflowExecutionRequest(BaseModel):
    """Workflow execution request schema"""
    input_data: Optional[Dict[str, Any]] = None
    config: Optional[Dict[str, Any]] = None


class WorkflowStatus(BaseModel):
    """Workflow status schema"""
    workflow_id: int
    status: str
    progress: float = Field(ge=0, le=100)
    current_task: Optional[str] = None
    tasks_completed: int = 0
    total_tasks: int = 0
    estimated_completion: Optional[datetime] = None