"""
Task management endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskExecutionResponse
from app.services.task_service import TaskService
from app.core.exceptions import NotFoundError, ValidationError, AgentExecutionError

router = APIRouter()


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    workflow_id: Optional[int] = None,
    agent_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all tasks"""
    task_service = TaskService(db)
    tasks = await task_service.get_tasks(
        skip=skip,
        limit=limit,
        workflow_id=workflow_id,
        agent_id=agent_id,
        status=status
    )
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """Get task by ID"""
    task_service = TaskService(db)
    task = await task_service.get_task(task_id)
    if not task:
        raise NotFoundError("Task", str(task_id))
    return task


@router.post("/", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):
    """Create a new task"""
    task_service = TaskService(db)
    try:
        task = await task_service.create_task(task_data)
        return task
    except Exception as e:
        raise ValidationError(f"Failed to create task: {str(e)}")


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
):
    """Update a task"""
    task_service = TaskService(db)
    try:
        task = await task_service.update_task(task_id, task_data)
        if not task:
            raise NotFoundError("Task", str(task_id))
        return task
    except Exception as e:
        raise ValidationError(f"Failed to update task: {str(e)}")


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """Delete a task"""
    task_service = TaskService(db)
    success = await task_service.delete_task(task_id)
    if not success:
        raise NotFoundError("Task", str(task_id))
    return {"message": "Task deleted successfully"}


@router.post("/{task_id}/execute", response_model=TaskExecutionResponse)
async def execute_task(
    task_id: int,
    input_data: Optional[dict] = None,
    db: Session = Depends(get_db)
):
    """Execute a task"""
    task_service = TaskService(db)
    try:
        execution = await task_service.execute_task(task_id, input_data)
        return execution
    except Exception as e:
        raise AgentExecutionError(str(task_id), str(e))


@router.get("/{task_id}/executions", response_model=List[TaskExecutionResponse])
async def get_task_executions(
    task_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get task executions"""
    task_service = TaskService(db)
    executions = await task_service.get_task_executions(
        task_id=task_id,
        skip=skip,
        limit=limit
    )
    return executions


@router.get("/{task_id}/executions/{execution_id}", response_model=TaskExecutionResponse)
async def get_task_execution(
    task_id: int,
    execution_id: int,
    db: Session = Depends(get_db)
):
    """Get specific task execution"""
    task_service = TaskService(db)
    execution = await task_service.get_task_execution(execution_id)
    if not execution:
        raise NotFoundError("Task Execution", str(execution_id))
    return execution


@router.post("/{task_id}/retry")
async def retry_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """Retry a failed task"""
    task_service = TaskService(db)
    try:
        execution = await task_service.retry_task(task_id)
        return execution
    except Exception as e:
        raise AgentExecutionError(str(task_id), str(e))


@router.get("/workflow/{workflow_id}", response_model=List[TaskResponse])
async def get_workflow_tasks(
    workflow_id: int,
    db: Session = Depends(get_db)
):
    """Get all tasks for a workflow"""
    task_service = TaskService(db)
    tasks = await task_service.get_workflow_tasks(workflow_id)
    return tasks