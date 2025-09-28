"""
Workflow model
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Workflow(Base):
    """Workflow model"""
    
    __tablename__ = "workflows"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    status = Column(String(20), default="draft")  # draft, active, paused, completed, failed
    workflow_type = Column(String(20), default="linear")  # linear, parallel, conditional, loop
    config = Column(JSON)  # Workflow configuration
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer)  # User ID
    is_active = Column(Boolean, default=True)
    execution_count = Column(Integer, default=0)
    last_executed = Column(DateTime(timezone=True))
    
    # Relationships
    tasks = relationship("Task", back_populates="workflow", cascade="all, delete-orphan")
    executions = relationship("WorkflowExecution", back_populates="workflow", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Workflow(id={self.id}, name='{self.name}', status='{self.status}')>"


class WorkflowExecution(Base):
    """Workflow execution model"""
    
    __tablename__ = "workflow_executions"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False)
    status = Column(String(20), default="pending")  # pending, running, completed, failed, cancelled
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    input_data = Column(JSON)
    output_data = Column(JSON)
    error_message = Column(Text)
    execution_log = Column(JSON)  # Detailed execution log
    created_by = Column(Integer)  # User ID
    
    # Relationships
    workflow = relationship("Workflow", back_populates="executions")
    task_executions = relationship("TaskExecution", back_populates="workflow_execution", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<WorkflowExecution(id={self.id}, workflow_id={self.workflow_id}, status='{self.status}')>"