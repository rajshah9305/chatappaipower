"""
Test agent endpoints
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_agents():
    """Test getting all agents"""
    response = client.get("/api/v1/agents/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_agent():
    """Test getting a specific agent"""
    response = client.get("/api/v1/agents/1")
    assert response.status_code == 200
    assert "name" in response.json()


def test_create_agent():
    """Test creating a new agent"""
    agent_data = {
        "name": "Test Agent",
        "role": "Test Role",
        "goal": "Test Goal",
        "model": "llama-4-maverick-17b-128e-instruct"
    }
    response = client.post("/api/v1/agents/", json=agent_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Agent"


def test_update_agent():
    """Test updating an agent"""
    update_data = {
        "name": "Updated Agent",
        "role": "Updated Role"
    }
    response = client.put("/api/v1/agents/1", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Agent"


def test_delete_agent():
    """Test deleting an agent"""
    response = client.delete("/api/v1/agents/1")
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]