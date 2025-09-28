"""
Execution service for managing workflow and task executions
"""

import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc
from datetime import datetime, timedelta

from app.models.workflow import WorkflowExecution
from app.models.task import TaskExecution
from app.schemas.execution import ExecutionResponse, ExecutionStats, ExecutionLog, ExecutionMetrics
from app.core.exceptions import NotFoundError, ValidationError

logger = logging.getLogger(__name__)


class ExecutionService:
    """Service for managing executions"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_executions(
        self,
        skip: int = 0,
        limit: int = 100,
        workflow_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[ExecutionResponse]:
        """Get all executions"""
        try:
            query = self.db.query(WorkflowExecution)
            
            if workflow_id:
                query = query.filter(WorkflowExecution.workflow_id == workflow_id)
            
            if status:
                query = query.filter(WorkflowExecution.status == status)
            
            executions = query.order_by(desc(WorkflowExecution.started_at)).offset(skip).limit(limit).all()
            
            return [ExecutionResponse.from_orm(execution) for execution in executions]
            
        except Exception as e:
            logger.error(f"Error getting executions: {e}")
            raise ValidationError(f"Failed to retrieve executions: {str(e)}")
    
    async def get_execution(self, execution_id: int) -> Optional[ExecutionResponse]:
        """Get execution by ID"""
        try:
            execution = self.db.query(WorkflowExecution).filter(WorkflowExecution.id == execution_id).first()
            
            if not execution:
                return None
            
            return ExecutionResponse.from_orm(execution)
            
        except Exception as e:
            logger.error(f"Error getting execution {execution_id}: {e}")
            raise ValidationError(f"Failed to retrieve execution: {str(e)}")
    
    async def get_execution_stats(
        self,
        workflow_id: Optional[int] = None,
        days: int = 30
    ) -> ExecutionStats:
        """Get execution statistics"""
        try:
            # Calculate date range
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            # Base query
            query = self.db.query(WorkflowExecution).filter(
                WorkflowExecution.started_at >= start_date
            )
            
            if workflow_id:
                query = query.filter(WorkflowExecution.workflow_id == workflow_id)
            
            executions = query.all()
            
            # Calculate statistics
            total_executions = len(executions)
            successful_executions = len([e for e in executions if e.status == "completed"])
            failed_executions = len([e for e in executions if e.status == "failed"])
            running_executions = len([e for e in executions if e.status == "running"])
            
            success_rate = (successful_executions / total_executions * 100) if total_executions > 0 else 0
            
            # Calculate average execution time
            completed_executions = [e for e in executions if e.status == "completed" and e.completed_at]
            if completed_executions:
                total_time = sum([
                    (e.completed_at - e.started_at).total_seconds()
                    for e in completed_executions
                ])
                average_execution_time = total_time / len(completed_executions)
            else:
                average_execution_time = 0
            
            # Calculate total tokens used
            total_tokens = sum([
                sum([te.tokens_used for te in e.task_executions])
                for e in executions
            ])
            
            # Get executions by day
            executions_by_day = self._get_executions_by_day(executions, start_date, end_date)
            
            # Get top workflows
            top_workflows = self._get_top_workflows(executions)
            
            # Get error breakdown
            error_breakdown = self._get_error_breakdown(executions)
            
            return ExecutionStats(
                total_executions=total_executions,
                successful_executions=successful_executions,
                failed_executions=failed_executions,
                running_executions=running_executions,
                success_rate=success_rate,
                average_execution_time=average_execution_time,
                total_tokens_used=total_tokens,
                executions_by_day=executions_by_day,
                top_workflows=top_workflows,
                error_breakdown=error_breakdown
            )
            
        except Exception as e:
            logger.error(f"Error getting execution stats: {e}")
            raise ValidationError(f"Failed to retrieve execution statistics: {str(e)}")
    
    def _get_executions_by_day(self, executions: List[WorkflowExecution], start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get executions grouped by day"""
        executions_by_day = {}
        
        for execution in executions:
            day = execution.started_at.date()
            if day not in executions_by_day:
                executions_by_day[day] = {"date": day.isoformat(), "count": 0, "successful": 0, "failed": 0}
            
            executions_by_day[day]["count"] += 1
            if execution.status == "completed":
                executions_by_day[day]["successful"] += 1
            elif execution.status == "failed":
                executions_by_day[day]["failed"] += 1
        
        return list(executions_by_day.values())
    
    def _get_top_workflows(self, executions: List[WorkflowExecution]) -> List[Dict[str, Any]]:
        """Get top workflows by execution count"""
        workflow_counts = {}
        
        for execution in executions:
            workflow_id = execution.workflow_id
            if workflow_id not in workflow_counts:
                workflow_counts[workflow_id] = {"workflow_id": workflow_id, "count": 0, "successful": 0, "failed": 0}
            
            workflow_counts[workflow_id]["count"] += 1
            if execution.status == "completed":
                workflow_counts[workflow_id]["successful"] += 1
            elif execution.status == "failed":
                workflow_counts[workflow_id]["failed"] += 1
        
        # Sort by count and return top 10
        top_workflows = sorted(workflow_counts.values(), key=lambda x: x["count"], reverse=True)[:10]
        return top_workflows
    
    def _get_error_breakdown(self, executions: List[WorkflowExecution]) -> List[Dict[str, Any]]:
        """Get error breakdown for failed executions"""
        error_counts = {}
        
        for execution in executions:
            if execution.status == "failed" and execution.error_message:
                error = execution.error_message
                if error not in error_counts:
                    error_counts[error] = {"error": error, "count": 0}
                error_counts[error]["count"] += 1
        
        # Sort by count and return top 10
        error_breakdown = sorted(error_counts.values(), key=lambda x: x["count"], reverse=True)[:10]
        return error_breakdown
    
    async def get_execution_logs(self, execution_id: int) -> List[ExecutionLog]:
        """Get execution logs"""
        try:
            execution = self.db.query(WorkflowExecution).filter(WorkflowExecution.id == execution_id).first()
            
            if not execution:
                return []
            
            logs = []
            
            # Add execution start log
            logs.append(ExecutionLog(
                timestamp=execution.started_at,
                level="INFO",
                message=f"Workflow execution started",
                details={"execution_id": execution_id, "workflow_id": execution.workflow_id}
            ))
            
            # Add task execution logs
            for task_execution in execution.task_executions:
                logs.append(ExecutionLog(
                    timestamp=task_execution.started_at,
                    level="INFO",
                    message=f"Task {task_execution.task_id} started",
                    details={"task_execution_id": task_execution.id, "task_id": task_execution.task_id}
                ))
                
                if task_execution.completed_at:
                    level = "INFO" if task_execution.status == "completed" else "ERROR"
                    message = f"Task {task_execution.task_id} {task_execution.status}"
                    details = {
                        "task_execution_id": task_execution.id,
                        "task_id": task_execution.task_id,
                        "status": task_execution.status,
                        "tokens_used": task_execution.tokens_used
                    }
                    
                    if task_execution.error_message:
                        details["error"] = task_execution.error_message
                    
                    logs.append(ExecutionLog(
                        timestamp=task_execution.completed_at,
                        level=level,
                        message=message,
                        details=details
                    ))
            
            # Add execution completion log
            if execution.completed_at:
                level = "INFO" if execution.status == "completed" else "ERROR"
                message = f"Workflow execution {execution.status}"
                details = {
                    "execution_id": execution_id,
                    "workflow_id": execution.workflow_id,
                    "status": execution.status
                }
                
                if execution.error_message:
                    details["error"] = execution.error_message
                
                logs.append(ExecutionLog(
                    timestamp=execution.completed_at,
                    level=level,
                    message=message,
                    details=details
                ))
            
            # Sort logs by timestamp
            logs.sort(key=lambda x: x.timestamp)
            
            return logs
            
        except Exception as e:
            logger.error(f"Error getting execution logs {execution_id}: {e}")
            raise ValidationError(f"Failed to retrieve execution logs: {str(e)}")
    
    async def cancel_execution(self, execution_id: int) -> bool:
        """Cancel an execution"""
        try:
            execution = self.db.query(WorkflowExecution).filter(WorkflowExecution.id == execution_id).first()
            
            if not execution:
                return False
            
            if execution.status in ["completed", "failed", "cancelled"]:
                return False
            
            execution.status = "cancelled"
            execution.completed_at = func.now()
            self.db.commit()
            
            logger.info(f"Cancelled execution: {execution_id}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error cancelling execution {execution_id}: {e}")
            raise ValidationError(f"Failed to cancel execution: {str(e)}")
    
    async def get_execution_status(self, execution_id: int) -> Optional[str]:
        """Get execution status"""
        try:
            execution = self.db.query(WorkflowExecution).filter(WorkflowExecution.id == execution_id).first()
            
            if not execution:
                return None
            
            return execution.status
            
        except Exception as e:
            logger.error(f"Error getting execution status {execution_id}: {e}")
            raise ValidationError(f"Failed to retrieve execution status: {str(e)}")
    
    async def get_execution_metrics(self, execution_id: int) -> Optional[ExecutionMetrics]:
        """Get execution metrics"""
        try:
            execution = self.db.query(WorkflowExecution).filter(WorkflowExecution.id == execution_id).first()
            
            if not execution:
                return None
            
            task_executions = execution.task_executions
            
            total_tasks = len(task_executions)
            completed_tasks = len([te for te in task_executions if te.status == "completed"])
            failed_tasks = len([te for te in task_executions if te.status == "failed"])
            
            total_tokens = sum([te.tokens_used for te in task_executions])
            
            if execution.completed_at:
                total_time = (execution.completed_at - execution.started_at).total_seconds()
            else:
                total_time = 0
            
            average_task_time = total_time / total_tasks if total_tasks > 0 else 0
            success_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            
            return ExecutionMetrics(
                execution_id=execution_id,
                total_tasks=total_tasks,
                completed_tasks=completed_tasks,
                failed_tasks=failed_tasks,
                total_tokens=total_tokens,
                total_time=total_time,
                average_task_time=average_task_time,
                success_rate=success_rate
            )
            
        except Exception as e:
            logger.error(f"Error getting execution metrics {execution_id}: {e}")
            raise ValidationError(f"Failed to retrieve execution metrics: {str(e)}")