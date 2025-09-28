"""
Database configuration and session management
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import asyncio
from typing import AsyncGenerator, Generator

from app.core.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    echo=settings.DEBUG
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Metadata for migrations
metadata = MetaData()


def get_db() -> Generator[Session, None, None]:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def init_db():
    """Initialize database tables"""
    # Import all models to ensure they are registered
    from app.models import agent, workflow, task, user  # noqa
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Run any initialization tasks
    await create_default_data()


async def create_default_data():
    """Create default data for the application"""
    from app.models.agent import Agent
    from app.models.workflow import Workflow
    from app.models.user import User
    from app.core.database import get_db
    
    db = next(get_db())
    
    try:
        # Check if default data already exists
        if db.query(Agent).first() is not None:
            return
        
        # Create default agents
        default_agents = [
            Agent(
                name="Researcher",
                role="Research Specialist",
                goal="Gather and analyze information from various sources",
                backstory="An expert researcher with years of experience in data analysis and information gathering",
                model="llama-4-maverick-17b-128e-instruct",
                is_active=True
            ),
            Agent(
                name="Writer",
                role="Content Creator",
                goal="Create high-quality written content based on research and requirements",
                backstory="A skilled writer with expertise in various writing styles and formats",
                model="llama-4-maverick-17b-128e-instruct",
                is_active=True
            ),
            Agent(
                name="Analyst",
                role="Data Analyst",
                goal="Analyze data and provide insights and recommendations",
                backstory="A data scientist with strong analytical skills and business acumen",
                model="llama-4-maverick-17b-128e-instruct",
                is_active=True
            ),
            Agent(
                name="Coordinator",
                role="Project Coordinator",
                goal="Coordinate tasks and manage workflow execution",
                backstory="An experienced project manager with excellent organizational skills",
                model="llama-4-maverick-17b-128e-instruct",
                is_active=True
            )
        ]
        
        for agent in default_agents:
            db.add(agent)
        
        db.commit()
        print("Default agents created successfully")
        
    except Exception as e:
        print(f"Error creating default data: {e}")
        db.rollback()
    finally:
        db.close()