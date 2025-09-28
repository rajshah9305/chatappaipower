"""
Execution management endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.execution import ExecutionResponse, ExecutionStats
from app.services.execution_service import ExecutionService
from app.core.exceptions import NotFoundError

router = APIRouter()


@router.get("/", response_model=List[ExecutionResponse])
async def get_executions(
    skip: int = 0,
    limit: int = 100,
    workflow_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all executions"""
    execution_service = ExecutionService(db)
    executions = await execution_service.get_executions(
        skip=skip,
        limit=limit,
        workflow_id=workflow_id,
        status=status
    )
    return executions


@router.get("/stats", response_model=ExecutionStats)
async def get_execution_stats(
    workflow_id: Optional[int] = None,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get execution statistics"""
    execution_service = ExecutionService(db)
    stats = await execution_service.get_execution_stats(
        workflow_id=workflow_id,
        days=days
    )
    return stats


@router.get("/{execution_id}", response_model=ExecutionResponse)
async def get_execution(
    execution_id: int,
    db: Session = Depends(get_db)
):
    """Get execution by ID"""
    execution_service = ExecutionService(db)
    execution = await execution_service.get_execution(execution_id)
    if not execution:
        raise NotFoundError("Execution", str(execution_id))
    return execution


@router.get("/{execution_id}/logs")
async def get_execution_logs(
    execution_id: int,
    db: Session = Depends(get_db)
):
    """Get execution logs"""
    execution_service = ExecutionService(db)
    logs = await execution_service.get_execution_logs(execution_id)
    if not logs:
        raise NotFoundError("Execution", str(execution_id))
    return {"execution_id": execution_id, "logs": logs}


@router.post("/{execution_id}/cancel")
async def cancel_execution(
    execution_id: int,
    db: Session = Depends(get_db)
):
    """Cancel an execution"""
    execution_service = ExecutionService(db)
    success = await execution_service.cancel_execution(execution_id)
    if not success:
        raise NotFoundError("Execution", str(execution_id))
    return {"message": "Execution cancelled successfully"}


@router.get("/{execution_id}/status")
async def get_execution_status(
    execution_id: int,
    db: Session = Depends(get_db)
):
    """Get execution status"""
    execution_service = ExecutionService(db)
    status = await execution_service.get_execution_status(execution_id)
    if not status:
        raise NotFoundError("Execution", str(execution_id))
    return {"execution_id": execution_id, "status": status}