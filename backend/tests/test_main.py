"""
Test main application
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "CrewAI Cerebras Multi-Agent Workflow Platform" in response.json()["message"]


def test_health():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_docs():
    """Test API documentation endpoint"""
    response = client.get("/docs")
    assert response.status_code == 200