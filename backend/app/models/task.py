"""
Task model
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Task(Base):
    """Task model"""
    
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    task_type = Column(String(50), default="ai_task")  # ai_task, data_task, api_task, custom_task
    status = Column(String(20), default="pending")  # pending, running, completed, failed, skipped
    priority = Column(Integer, default=0)  # Higher number = higher priority
    order = Column(Integer, default=0)  # Execution order within workflow
    input_data = Column(JSON)
    output_data = Column(JSON)
    config = Column(JSON)  # Task-specific configuration
    dependencies = Column(JSON)  # Task dependencies
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer)  # User ID
    is_active = Column(Boolean, default=True)
    
    # Relationships
    workflow = relationship("Workflow", back_populates="tasks")
    agent = relationship("Agent")
    executions = relationship("TaskExecution", back_populates="task", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Task(id={self.id}, name='{self.name}', status='{self.status}')>"


class TaskExecution(Base):
    """Task execution model"""
    
    __tablename__ = "task_executions"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    workflow_execution_id = Column(Integer, ForeignKey("workflow_executions.id"), nullable=False)
    status = Column(String(20), default="pending")  # pending, running, completed, failed, skipped
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    input_data = Column(JSON)
    output_data = Column(JSON)
    error_message = Column(Text)
    execution_log = Column(JSON)  # Detailed execution log
    tokens_used = Column(Integer, default=0)
    execution_time = Column(Integer)  # Execution time in milliseconds
    created_by = Column(Integer)  # User ID
    
    # Relationships
    task = relationship("Task", back_populates="executions")
    workflow_execution = relationship("WorkflowExecution", back_populates="task_executions")
    
    def __repr__(self):
        return f"<TaskExecution(id={self.id}, task_id={self.task_id}, status='{self.status}')>"