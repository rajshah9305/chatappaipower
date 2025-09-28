"""
Workflow management endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.workflow import WorkflowCreate, WorkflowUpdate, WorkflowResponse, WorkflowExecutionResponse
from app.services.workflow_service import WorkflowService
from app.core.exceptions import NotFoundError, ValidationError, WorkflowExecutionError

router = APIRouter()


@router.get("/", response_model=List[WorkflowResponse])
async def get_workflows(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """Get all workflows"""
    workflow_service = WorkflowService(db)
    workflows = await workflow_service.get_workflows(
        skip=skip,
        limit=limit,
        active_only=active_only
    )
    return workflows


@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(
    workflow_id: int,
    db: Session = Depends(get_db)
):
    """Get workflow by ID"""
    workflow_service = WorkflowService(db)
    workflow = await workflow_service.get_workflow(workflow_id)
    if not workflow:
        raise NotFoundError("Workflow", str(workflow_id))
    return workflow


@router.post("/", response_model=WorkflowResponse)
async def create_workflow(
    workflow_data: WorkflowCreate,
    db: Session = Depends(get_db)
):
    """Create a new workflow"""
    workflow_service = WorkflowService(db)
    try:
        workflow = await workflow_service.create_workflow(workflow_data)
        return workflow
    except Exception as e:
        raise ValidationError(f"Failed to create workflow: {str(e)}")


@router.put("/{workflow_id}", response_model=WorkflowResponse)
async def update_workflow(
    workflow_id: int,
    workflow_data: WorkflowUpdate,
    db: Session = Depends(get_db)
):
    """Update a workflow"""
    workflow_service = WorkflowService(db)
    try:
        workflow = await workflow_service.update_workflow(workflow_id, workflow_data)
        if not workflow:
            raise NotFoundError("Workflow", str(workflow_id))
        return workflow
    except Exception as e:
        raise ValidationError(f"Failed to update workflow: {str(e)}")


@router.delete("/{workflow_id}")
async def delete_workflow(
    workflow_id: int,
    db: Session = Depends(get_db)
):
    """Delete a workflow"""
    workflow_service = WorkflowService(db)
    success = await workflow_service.delete_workflow(workflow_id)
    if not success:
        raise NotFoundError("Workflow", str(workflow_id))
    return {"message": "Workflow deleted successfully"}


@router.post("/{workflow_id}/execute", response_model=WorkflowExecutionResponse)
async def execute_workflow(
    workflow_id: int,
    input_data: Optional[dict] = None,
    db: Session = Depends(get_db)
):
    """Execute a workflow"""
    workflow_service = WorkflowService(db)
    try:
        execution = await workflow_service.execute_workflow(workflow_id, input_data)
        return execution
    except Exception as e:
        raise WorkflowExecutionError(str(workflow_id), str(e))


@router.get("/{workflow_id}/executions", response_model=List[WorkflowExecutionResponse])
async def get_workflow_executions(
    workflow_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get workflow executions"""
    workflow_service = WorkflowService(db)
    executions = await workflow_service.get_workflow_executions(
        workflow_id=workflow_id,
        skip=skip,
        limit=limit
    )
    return executions


@router.get("/{workflow_id}/executions/{execution_id}", response_model=WorkflowExecutionResponse)
async def get_workflow_execution(
    workflow_id: int,
    execution_id: int,
    db: Session = Depends(get_db)
):
    """Get specific workflow execution"""
    workflow_service = WorkflowService(db)
    execution = await workflow_service.get_workflow_execution(execution_id)
    if not execution:
        raise NotFoundError("Workflow Execution", str(execution_id))
    return execution


@router.post("/{workflow_id}/pause")
async def pause_workflow(
    workflow_id: int,
    db: Session = Depends(get_db)
):
    """Pause a workflow execution"""
    workflow_service = WorkflowService(db)
    success = await workflow_service.pause_workflow(workflow_id)
    if not success:
        raise NotFoundError("Workflow", str(workflow_id))
    return {"message": "Workflow paused successfully"}


@router.post("/{workflow_id}/resume")
async def resume_workflow(
    workflow_id: int,
    db: Session = Depends(get_db)
):
    """Resume a paused workflow"""
    workflow_service = WorkflowService(db)
    success = await workflow_service.resume_workflow(workflow_id)
    if not success:
        raise NotFoundError("Workflow", str(workflow_id))
    return {"message": "Workflow resumed successfully"}


@router.post("/{workflow_id}/cancel")
async def cancel_workflow(
    workflow_id: int,
    db: Session = Depends(get_db)
):
    """Cancel a workflow execution"""
    workflow_service = WorkflowService(db)
    success = await workflow_service.cancel_workflow(workflow_id)
    if not success:
        raise NotFoundError("Workflow", str(workflow_id))
    return {"message": "Workflow cancelled successfully"}