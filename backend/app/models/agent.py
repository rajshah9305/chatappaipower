"""
Agent model
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.core.database import Base


class Agent(Base):
    """AI Agent model"""
    
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    role = Column(String(200), nullable=False)
    goal = Column(Text, nullable=False)
    backstory = Column(Text)
    model = Column(String(100), nullable=False, default="llama-4-maverick-17b-128e-instruct")
    temperature = Column(String(10), default="0.6")
    max_tokens = Column(Integer, default=32768)
    top_p = Column(String(10), default="0.9")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer)  # User ID
    config = Column(JSON)  # Additional configuration
    capabilities = Column(JSON)  # Agent capabilities
    tools = Column(JSON)  # Available tools
    
    def __repr__(self):
        return f"<Agent(id={self.id}, name='{self.name}', role='{self.role}')>"