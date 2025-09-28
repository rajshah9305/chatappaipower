"""
Task service for managing AI tasks
"""

import asyncio
import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from app.models.task import Task, TaskExecution
from app.models.workflow import Workflow
from app.models.agent import Agent
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskExecutionResponse
from app.core.exceptions import NotFoundError, ValidationError, AgentExecutionError

logger = logging.getLogger(__name__)


class TaskService:
    """Service for managing AI tasks"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_tasks(
        self,
        skip: int = 0,
        limit: int = 100,
        workflow_id: Optional[int] = None,
        agent_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[TaskResponse]:
        """Get all tasks"""
        try:
            query = self.db.query(Task)
            
            if workflow_id:
                query = query.filter(Task.workflow_id == workflow_id)
            
            if agent_id:
                query = query.filter(Task.agent_id == agent_id)
            
            if status:
                query = query.filter(Task.status == status)
            
            tasks = query.offset(skip).limit(limit).all()
            
            return [TaskResponse.from_orm(task) for task in tasks]
            
        except Exception as e:
            logger.error(f"Error getting tasks: {e}")
            raise ValidationError(f"Failed to retrieve tasks: {str(e)}")
    
    async def get_task(self, task_id: int) -> Optional[TaskResponse]:
        """Get task by ID"""
        try:
            task = self.db.query(Task).filter(Task.id == task_id).first()
            
            if not task:
                return None
            
            return TaskResponse.from_orm(task)
            
        except Exception as e:
            logger.error(f"Error getting task {task_id}: {e}")
            raise ValidationError(f"Failed to retrieve task: {str(e)}")
    
    async def create_task(self, task_data: TaskCreate) -> TaskResponse:
        """Create a new task"""
        try:
            # Validate workflow exists
            workflow = self.db.query(Workflow).filter(Workflow.id == task_data.workflow_id).first()
            if not workflow:
                raise ValidationError(f"Workflow {task_data.workflow_id} not found")
            
            # Validate agent exists
            agent = self.db.query(Agent).filter(Agent.id == task_data.agent_id).first()
            if not agent:
                raise ValidationError(f"Agent {task_data.agent_id} not found")
            
            task = Task(
                workflow_id=task_data.workflow_id,
                agent_id=task_data.agent_id,
                name=task_data.name,
                description=task_data.description,
                task_type=task_data.task_type,
                priority=task_data.priority,
                order=task_data.order,
                input_data=task_data.input_data,
                config=task_data.config,
                dependencies=task_data.dependencies,
                is_active=task_data.is_active
            )
            
            self.db.add(task)
            self.db.commit()
            self.db.refresh(task)
            
            logger.info(f"Created task: {task.name}")
            return TaskResponse.from_orm(task)
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating task: {e}")
            raise ValidationError(f"Failed to create task: {str(e)}")
    
    async def update_task(self, task_id: int, task_data: TaskUpdate) -> Optional[TaskResponse]:
        """Update a task"""
        try:
            task = self.db.query(Task).filter(Task.id == task_id).first()
            
            if not task:
                return None
            
            # Update fields
            update_data = task_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(task, field, value)
            
            self.db.commit()
            self.db.refresh(task)
            
            logger.info(f"Updated task: {task.name}")
            return TaskResponse.from_orm(task)
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating task {task_id}: {e}")
            raise ValidationError(f"Failed to update task: {str(e)}")
    
    async def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        try:
            task = self.db.query(Task).filter(Task.id == task_id).first()
            
            if not task:
                return False
            
            self.db.delete(task)
            self.db.commit()
            
            logger.info(f"Deleted task: {task.name}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting task {task_id}: {e}")
            raise ValidationError(f"Failed to delete task: {str(e)}")
    
    async def execute_task(self, task_id: int, input_data: Optional[Dict[str, Any]] = None) -> TaskExecutionResponse:
        """Execute a task"""
        try:
            task = self.db.query(Task).filter(Task.id == task_id).first()
            
            if not task:
                raise NotFoundError("Task", str(task_id))
            
            if not task.is_active:
                raise AgentExecutionError(str(task_id), "Task is not active")
            
            # Create task execution
            task_execution = TaskExecution(
                task_id=task_id,
                workflow_execution_id=None,  # Standalone execution
                input_data=input_data or task.input_data,
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
            
            logger.info(f"Executed task: {task.name}")
            return TaskExecutionResponse.from_orm(task_execution)
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error executing task {task_id}: {e}")
            raise AgentExecutionError(str(task_id), str(e))
    
    async def _execute_ai_task(self, task_execution: TaskExecution, task: Task):
        """Execute AI task using agent"""
        try:
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
Input Data: {task_execution.input_data}
"""
            
            # Generate response
            response = await cerebras_service.generate_agent_response(
                agent_prompt=prompt,
                context=task_execution.input_data,
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
    
    async def get_task_executions(
        self,
        task_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[TaskExecutionResponse]:
        """Get task executions"""
        try:
            executions = self.db.query(TaskExecution).filter(
                TaskExecution.task_id == task_id
            ).offset(skip).limit(limit).all()
            
            return [TaskExecutionResponse.from_orm(execution) for execution in executions]
            
        except Exception as e:
            logger.error(f"Error getting task executions: {e}")
            raise ValidationError(f"Failed to retrieve task executions: {str(e)}")
    
    async def get_task_execution(self, execution_id: int) -> Optional[TaskExecutionResponse]:
        """Get specific task execution"""
        try:
            execution = self.db.query(TaskExecution).filter(TaskExecution.id == execution_id).first()
            
            if not execution:
                return None
            
            return TaskExecutionResponse.from_orm(execution)
            
        except Exception as e:
            logger.error(f"Error getting task execution {execution_id}: {e}")
            raise ValidationError(f"Failed to retrieve task execution: {str(e)}")
    
    async def retry_task(self, task_id: int) -> TaskExecutionResponse:
        """Retry a failed task"""
        try:
            task = self.db.query(Task).filter(Task.id == task_id).first()
            
            if not task:
                raise NotFoundError("Task", str(task_id))
            
            # Get the last failed execution
            last_execution = self.db.query(TaskExecution).filter(
                and_(
                    TaskExecution.task_id == task_id,
                    TaskExecution.status == "failed"
                )
            ).order_by(TaskExecution.started_at.desc()).first()
            
            if not last_execution:
                raise ValidationError("No failed execution found for this task")
            
            # Create new execution with same input
            task_execution = TaskExecution(
                task_id=task_id,
                workflow_execution_id=last_execution.workflow_execution_id,
                input_data=last_execution.input_data,
                status="running"
            )
            
            self.db.add(task_execution)
            self.db.commit()
            self.db.refresh(task_execution)
            
            # Execute task
            if task.task_type == "ai_task":
                await self._execute_ai_task(task_execution, task)
            else:
                task_execution.status = "completed"
                task_execution.output_data = {"message": "Task completed"}
            
            task_execution.completed_at = func.now()
            self.db.commit()
            
            logger.info(f"Retried task: {task.name}")
            return TaskExecutionResponse.from_orm(task_execution)
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error retrying task {task_id}: {e}")
            raise AgentExecutionError(str(task_id), str(e))
    
    async def get_workflow_tasks(self, workflow_id: int) -> List[TaskResponse]:
        """Get all tasks for a workflow"""
        try:
            tasks = self.db.query(Task).filter(
                and_(
                    Task.workflow_id == workflow_id,
                    Task.is_active == True
                )
            ).order_by(Task.order).all()
            
            return [TaskResponse.from_orm(task) for task in tasks]
            
        except Exception as e:
            logger.error(f"Error getting workflow tasks: {e}")
            raise ValidationError(f"Failed to retrieve workflow tasks: {str(e)}")
    
    async def update_task_status(self, task_id: int, status: str) -> bool:
        """Update task status"""
        try:
            task = self.db.query(Task).filter(Task.id == task_id).first()
            
            if not task:
                return False
            
            task.status = status
            self.db.commit()
            
            logger.info(f"Updated task {task_id} status to {status}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating task status {task_id}: {e}")
            raise ValidationError(f"Failed to update task status: {str(e)}")
    
    async def get_task_dependencies(self, task_id: int) -> List[TaskResponse]:
        """Get task dependencies"""
        try:
            task = self.db.query(Task).filter(Task.id == task_id).first()
            
            if not task or not task.dependencies:
                return []
            
            dependencies = self.db.query(Task).filter(
                Task.id.in_(task.dependencies)
            ).all()
            
            return [TaskResponse.from_orm(dep) for dep in dependencies]
            
        except Exception as e:
            logger.error(f"Error getting task dependencies {task_id}: {e}")
            raise ValidationError(f"Failed to retrieve task dependencies: {str(e)}")