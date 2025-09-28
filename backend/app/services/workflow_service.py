"""
Workflow service for managing AI workflows
"""

import asyncio
import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from app.models.workflow import Workflow, WorkflowExecution
from app.models.task import Task, TaskExecution
from app.models.agent import Agent
from app.schemas.workflow import WorkflowCreate, WorkflowUpdate, WorkflowResponse, WorkflowExecutionResponse
from app.core.exceptions import NotFoundError, ValidationError, WorkflowExecutionError
from app.core.websocket import websocket_manager

logger = logging.getLogger(__name__)


class WorkflowService:
    """Service for managing AI workflows"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_workflows(
        self,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = True
    ) -> List[WorkflowResponse]:
        """Get all workflows"""
        try:
            query = self.db.query(Workflow)
            
            if active_only:
                query = query.filter(Workflow.is_active == True)
            
            workflows = query.offset(skip).limit(limit).all()
            
            return [WorkflowResponse.from_orm(workflow) for workflow in workflows]
            
        except Exception as e:
            logger.error(f"Error getting workflows: {e}")
            raise ValidationError(f"Failed to retrieve workflows: {str(e)}")
    
    async def get_workflow(self, workflow_id: int) -> Optional[WorkflowResponse]:
        """Get workflow by ID"""
        try:
            workflow = self.db.query(Workflow).filter(Workflow.id == workflow_id).first()
            
            if not workflow:
                return None
            
            return WorkflowResponse.from_orm(workflow)
            
        except Exception as e:
            logger.error(f"Error getting workflow {workflow_id}: {e}")
            raise ValidationError(f"Failed to retrieve workflow: {str(e)}")
    
    async def create_workflow(self, workflow_data: WorkflowCreate) -> WorkflowResponse:
        """Create a new workflow"""
        try:
            workflow = Workflow(
                name=workflow_data.name,
                description=workflow_data.description,
                workflow_type=workflow_data.workflow_type,
                config=workflow_data.config,
                is_active=workflow_data.is_active
            )
            
            self.db.add(workflow)
            self.db.commit()
            self.db.refresh(workflow)
            
            logger.info(f"Created workflow: {workflow.name}")
            return WorkflowResponse.from_orm(workflow)
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating workflow: {e}")
            raise ValidationError(f"Failed to create workflow: {str(e)}")
    
    async def update_workflow(self, workflow_id: int, workflow_data: WorkflowUpdate) -> Optional[WorkflowResponse]:
        """Update a workflow"""
        try:
            workflow = self.db.query(Workflow).filter(Workflow.id == workflow_id).first()
            
            if not workflow:
                return None
            
            # Update fields
            update_data = workflow_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(workflow, field, value)
            
            self.db.commit()
            self.db.refresh(workflow)
            
            logger.info(f"Updated workflow: {workflow.name}")
            return WorkflowResponse.from_orm(workflow)
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating workflow {workflow_id}: {e}")
            raise ValidationError(f"Failed to update workflow: {str(e)}")
    
    async def delete_workflow(self, workflow_id: int) -> bool:
        """Delete a workflow"""
        try:
            workflow = self.db.query(Workflow).filter(Workflow.id == workflow_id).first()
            
            if not workflow:
                return False
            
            self.db.delete(workflow)
            self.db.commit()
            
            logger.info(f"Deleted workflow: {workflow.name}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting workflow {workflow_id}: {e}")
            raise ValidationError(f"Failed to delete workflow: {str(e)}")
    
    async def execute_workflow(self, workflow_id: int, input_data: Optional[Dict[str, Any]] = None) -> WorkflowExecutionResponse:
        """Execute a workflow"""
        try:
            workflow = self.db.query(Workflow).filter(Workflow.id == workflow_id).first()
            
            if not workflow:
                raise NotFoundError("Workflow", str(workflow_id))
            
            if not workflow.is_active:
                raise WorkflowExecutionError(str(workflow_id), "Workflow is not active")
            
            # Create workflow execution
            execution = WorkflowExecution(
                workflow_id=workflow_id,
                input_data=input_data,
                status="pending"
            )
            
            self.db.add(execution)
            self.db.commit()
            self.db.refresh(execution)
            
            # Update workflow execution count
            workflow.execution_count += 1
            self.db.commit()
            
            # Start workflow execution asynchronously
            asyncio.create_task(self._execute_workflow_async(execution.id))
            
            # Notify WebSocket subscribers
            await websocket_manager.broadcast_workflow_update(
                str(workflow_id),
                {
                    "type": "workflow_started",
                    "workflow_id": workflow_id,
                    "execution_id": execution.id,
                    "status": "running"
                }
            )
            
            logger.info(f"Started workflow execution: {execution.id}")
            return WorkflowExecutionResponse.from_orm(execution)
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error executing workflow {workflow_id}: {e}")
            raise WorkflowExecutionError(str(workflow_id), str(e))
    
    async def _execute_workflow_async(self, execution_id: int):
        """Execute workflow asynchronously"""
        try:
            execution = self.db.query(WorkflowExecution).filter(WorkflowExecution.id == execution_id).first()
            
            if not execution:
                return
            
            # Update status to running
            execution.status = "running"
            self.db.commit()
            
            # Get workflow tasks
            tasks = self.db.query(Task).filter(
                and_(
                    Task.workflow_id == execution.workflow_id,
                    Task.is_active == True
                )
            ).order_by(Task.order).all()
            
            if not tasks:
                execution.status = "completed"
                execution.completed_at = func.now()
                self.db.commit()
                return
            
            # Execute tasks based on workflow type
            workflow = self.db.query(Workflow).filter(Workflow.id == execution.workflow_id).first()
            
            if workflow.workflow_type == "linear":
                await self._execute_linear_workflow(execution, tasks)
            elif workflow.workflow_type == "parallel":
                await self._execute_parallel_workflow(execution, tasks)
            else:
                await self._execute_linear_workflow(execution, tasks)
            
            # Update execution status
            execution.status = "completed"
            execution.completed_at = func.now()
            self.db.commit()
            
            # Notify WebSocket subscribers
            await websocket_manager.broadcast_workflow_update(
                str(execution.workflow_id),
                {
                    "type": "workflow_completed",
                    "workflow_id": execution.workflow_id,
                    "execution_id": execution.id,
                    "status": "completed"
                }
            )
            
        except Exception as e:
            logger.error(f"Error in workflow execution {execution_id}: {e}")
            
            # Update execution status to failed
            execution = self.db.query(WorkflowExecution).filter(WorkflowExecution.id == execution_id).first()
            if execution:
                execution.status = "failed"
                execution.error_message = str(e)
                execution.completed_at = func.now()
                self.db.commit()
            
            # Notify WebSocket subscribers
            await websocket_manager.broadcast_workflow_update(
                str(execution.workflow_id),
                {
                    "type": "workflow_failed",
                    "workflow_id": execution.workflow_id,
                    "execution_id": execution.id,
                    "status": "failed",
                    "error": str(e)
                }
            )
    
    async def _execute_linear_workflow(self, execution: WorkflowExecution, tasks: List[Task]):
        """Execute workflow tasks linearly"""
        for task in tasks:
            try:
                # Execute task
                await self._execute_task(execution, task)
                
                # Check if task failed
                task_execution = self.db.query(TaskExecution).filter(
                    and_(
                        TaskExecution.task_id == task.id,
                        TaskExecution.workflow_execution_id == execution.id
                    )
                ).first()
                
                if task_execution and task_execution.status == "failed":
                    break
                    
            except Exception as e:
                logger.error(f"Error executing task {task.id}: {e}")
                break
    
    async def _execute_parallel_workflow(self, execution: WorkflowExecution, tasks: List[Task]):
        """Execute workflow tasks in parallel"""
        # Create tasks for parallel execution
        task_coroutines = [self._execute_task(execution, task) for task in tasks]
        
        # Execute all tasks in parallel
        await asyncio.gather(*task_coroutines, return_exceptions=True)
    
    async def _execute_task(self, execution: WorkflowExecution, task: Task):
        """Execute a single task"""
        try:
            # Create task execution record
            task_execution = TaskExecution(
                task_id=task.id,
                workflow_execution_id=execution.id,
                input_data=task.input_data,
                status="running"
            )
            
            self.db.add(task_execution)
            self.db.commit()
            self.db.refresh(task_execution)
            
            # Execute task based on type
            if task.task_type == "ai_task":
                await self._execute_ai_task(task_execution, task)
            else:
                # Handle other task types
                task_execution.status = "completed"
                task_execution.output_data = {"message": "Task completed"}
            
            task_execution.completed_at = func.now()
            self.db.commit()
            
            # Notify WebSocket subscribers
            await websocket_manager.broadcast_agent_update(
                str(task.agent_id),
                {
                    "type": "task_completed",
                    "task_id": task.id,
                    "execution_id": task_execution.id,
                    "status": task_execution.status
                }
            )
            
        except Exception as e:
            logger.error(f"Error executing task {task.id}: {e}")
            
            task_execution.status = "failed"
            task_execution.error_message = str(e)
            task_execution.completed_at = func.now()
            self.db.commit()
    
    async def _execute_ai_task(self, task_execution: TaskExecution, task: Task):
        """Execute AI task using agent"""
        try:
            from app.services.agent_service import AgentService
            from app.services.cerebras_service import cerebras_service
            
            # Get agent
            agent = self.db.query(Agent).filter(Agent.id == task.agent_id).first()
            if not agent:
                raise Exception(f"Agent {task.agent_id} not found")
            
            # Build prompt
            prompt = f"""
Agent Role: {agent.role}
Agent Goal: {agent.goal}
Agent Backstory: {agent.backstory}

Task: {task.description}
Input Data: {task.input_data}
"""
            
            # Generate response
            response = await cerebras_service.generate_agent_response(
                agent_prompt=prompt,
                context=task.input_data,
                model=agent.model,
                max_tokens=agent.max_tokens,
                temperature=float(agent.temperature),
                top_p=float(agent.top_p)
            )
            
            # Update task execution
            task_execution.status = "completed"
            task_execution.output_data = {
                "response": response["response"],
                "tokens_used": response["tokens_used"]
            }
            task_execution.tokens_used = response["tokens_used"]
            
        except Exception as e:
            logger.error(f"Error executing AI task {task.id}: {e}")
            task_execution.status = "failed"
            task_execution.error_message = str(e)
    
    async def get_workflow_executions(
        self,
        workflow_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[WorkflowExecutionResponse]:
        """Get workflow executions"""
        try:
            executions = self.db.query(WorkflowExecution).filter(
                WorkflowExecution.workflow_id == workflow_id
            ).offset(skip).limit(limit).all()
            
            return [WorkflowExecutionResponse.from_orm(execution) for execution in executions]
            
        except Exception as e:
            logger.error(f"Error getting workflow executions: {e}")
            raise ValidationError(f"Failed to retrieve workflow executions: {str(e)}")
    
    async def get_workflow_execution(self, execution_id: int) -> Optional[WorkflowExecutionResponse]:
        """Get specific workflow execution"""
        try:
            execution = self.db.query(WorkflowExecution).filter(WorkflowExecution.id == execution_id).first()
            
            if not execution:
                return None
            
            return WorkflowExecutionResponse.from_orm(execution)
            
        except Exception as e:
            logger.error(f"Error getting workflow execution {execution_id}: {e}")
            raise ValidationError(f"Failed to retrieve workflow execution: {str(e)}")
    
    async def pause_workflow(self, workflow_id: int) -> bool:
        """Pause a workflow"""
        try:
            workflow = self.db.query(Workflow).filter(Workflow.id == workflow_id).first()
            
            if not workflow:
                return False
            
            workflow.status = "paused"
            self.db.commit()
            
            logger.info(f"Paused workflow: {workflow.name}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error pausing workflow {workflow_id}: {e}")
            raise ValidationError(f"Failed to pause workflow: {str(e)}")
    
    async def resume_workflow(self, workflow_id: int) -> bool:
        """Resume a workflow"""
        try:
            workflow = self.db.query(Workflow).filter(Workflow.id == workflow_id).first()
            
            if not workflow:
                return False
            
            workflow.status = "active"
            self.db.commit()
            
            logger.info(f"Resumed workflow: {workflow.name}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error resuming workflow {workflow_id}: {e}")
            raise ValidationError(f"Failed to resume workflow: {str(e)}")
    
    async def cancel_workflow(self, workflow_id: int) -> bool:
        """Cancel a workflow"""
        try:
            workflow = self.db.query(Workflow).filter(Workflow.id == workflow_id).first()
            
            if not workflow:
                return False
            
            workflow.status = "cancelled"
            self.db.commit()
            
            logger.info(f"Cancelled workflow: {workflow.name}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error cancelling workflow {workflow_id}: {e}")
            raise ValidationError(f"Failed to cancel workflow: {str(e)}")