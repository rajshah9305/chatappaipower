"""
Execution schemas
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime


class ExecutionResponse(BaseModel):
    """Execution response schema"""
    id: int
    workflow_id: int
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    input_data: Optional[Dict[str, Any]] = None
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    execution_log: Optional[Dict[str, Any]] = None
    created_by: Optional[int] = None
    
    class Config:
        from_attributes = True


class ExecutionStats(BaseModel):
    """Execution statistics schema"""
    total_executions: int
    successful_executions: int
    failed_executions: int
    running_executions: int
    success_rate: float
    average_execution_time: float
    total_tokens_used: int
    executions_by_day: List[Dict[str, Any]]
    top_workflows: List[Dict[str, Any]]
    error_breakdown: List[Dict[str, Any]]


class ExecutionLog(BaseModel):
    """Execution log schema"""
    timestamp: datetime
    level: str
    message: str
    details: Optional[Dict[str, Any]] = None


class ExecutionMetrics(BaseModel):
    """Execution metrics schema"""
    execution_id: int
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    total_tokens: int
    total_time: float
    average_task_time: float
    success_rate: float