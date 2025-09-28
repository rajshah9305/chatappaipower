# 🔌 API Documentation

The CrewAI Cerebras Platform provides a comprehensive REST API for managing AI agents, workflows, and executions.

## 🌐 Base URL

- **Development:** `http://localhost:8000`
- **Production:** `https://your-domain.com`

## 🔑 Authentication

Currently, the API does not require authentication. In production, implement proper authentication using JWT tokens.

## 📚 API Endpoints

### Agents

#### Get All Agents
```http
GET /api/v1/agents/
```

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Maximum number of records to return (default: 100)
- `active_only` (bool): Filter only active agents (default: true)

**Response:**
```json
[
  {
    "id": 1,
    "name": "Researcher",
    "role": "Research Specialist",
    "goal": "Gather and analyze information from various sources",
    "backstory": "An expert researcher with years of experience...",
    "model": "llama-4-maverick-17b-128e-instruct",
    "temperature": "0.6",
    "max_tokens": 32768,
    "top_p": "0.9",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "created_by": null,
    "config": null,
    "capabilities": ["Web Search", "Data Analysis", "Report Generation"],
    "tools": ["search_tool", "analysis_tool"]
  }
]
```

#### Get Agent by ID
```http
GET /api/v1/agents/{agent_id}
```

**Response:**
```json
{
  "id": 1,
  "name": "Researcher",
  "role": "Research Specialist",
  "goal": "Gather and analyze information from various sources",
  "backstory": "An expert researcher with years of experience...",
  "model": "llama-4-maverick-17b-128e-instruct",
  "temperature": "0.6",
  "max_tokens": 32768,
  "top_p": "0.9",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "created_by": null,
  "config": null,
  "capabilities": ["Web Search", "Data Analysis", "Report Generation"],
  "tools": ["search_tool", "analysis_tool"]
}
```

#### Create Agent
```http
POST /api/v1/agents/
```

**Request Body:**
```json
{
  "name": "New Agent",
  "role": "Agent Role",
  "goal": "Agent goal description",
  "backstory": "Agent backstory (optional)",
  "model": "llama-4-maverick-17b-128e-instruct",
  "temperature": "0.6",
  "max_tokens": 32768,
  "top_p": "0.9",
  "is_active": true,
  "config": {},
  "capabilities": ["Capability 1", "Capability 2"],
  "tools": ["tool1", "tool2"]
}
```

#### Update Agent
```http
PUT /api/v1/agents/{agent_id}
```

**Request Body:** (Same as create, all fields optional)

#### Delete Agent
```http
DELETE /api/v1/agents/{agent_id}
```

#### Test Agent
```http
POST /api/v1/agents/{agent_id}/test
```

**Request Body:**
```json
{
  "input": "Test input for the agent",
  "context": {
    "additional": "context data"
  }
}
```

**Response:**
```json
{
  "agent_id": 1,
  "input": "Test input for the agent",
  "output": "Agent response",
  "execution_time": 1.23,
  "tokens_used": 150,
  "success": true,
  "error": null
}
```

### Workflows

#### Get All Workflows
```http
GET /api/v1/workflows/
```

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Maximum number of records to return (default: 100)
- `active_only` (bool): Filter only active workflows (default: true)

#### Get Workflow by ID
```http
GET /api/v1/workflows/{workflow_id}
```

#### Create Workflow
```http
POST /api/v1/workflows/
```

**Request Body:**
```json
{
  "name": "New Workflow",
  "description": "Workflow description",
  "workflow_type": "linear",
  "config": {},
  "is_active": true
}
```

#### Update Workflow
```http
PUT /api/v1/workflows/{workflow_id}
```

#### Delete Workflow
```http
DELETE /api/v1/workflows/{workflow_id}
```

#### Execute Workflow
```http
POST /api/v1/workflows/{workflow_id}/execute
```

**Request Body:**
```json
{
  "input_data": {
    "key": "value"
  },
  "config": {
    "additional": "configuration"
  }
}
```

**Response:**
```json
{
  "id": 1,
  "workflow_id": 1,
  "status": "pending",
  "started_at": "2024-01-15T10:30:00Z",
  "completed_at": null,
  "input_data": {"key": "value"},
  "output_data": null,
  "error_message": null,
  "execution_log": null,
  "created_by": null
}
```

#### Get Workflow Executions
```http
GET /api/v1/workflows/{workflow_id}/executions
```

#### Pause Workflow
```http
POST /api/v1/workflows/{workflow_id}/pause
```

#### Resume Workflow
```http
POST /api/v1/workflows/{workflow_id}/resume
```

#### Cancel Workflow
```http
POST /api/v1/workflows/{workflow_id}/cancel
```

### Tasks

#### Get All Tasks
```http
GET /api/v1/tasks/
```

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Maximum number of records to return (default: 100)
- `workflow_id` (int): Filter by workflow ID
- `agent_id` (int): Filter by agent ID
- `status` (str): Filter by status

#### Get Task by ID
```http
GET /api/v1/tasks/{task_id}
```

#### Create Task
```http
POST /api/v1/tasks/
```

**Request Body:**
```json
{
  "workflow_id": 1,
  "agent_id": 1,
  "name": "Task Name",
  "description": "Task description",
  "task_type": "ai_task",
  "priority": 0,
  "order": 0,
  "input_data": {},
  "config": {},
  "dependencies": [],
  "is_active": true
}
```

#### Update Task
```http
PUT /api/v1/tasks/{task_id}
```

#### Delete Task
```http
DELETE /api/v1/tasks/{task_id}
```

#### Execute Task
```http
POST /api/v1/tasks/{task_id}/execute
```

#### Get Task Executions
```http
GET /api/v1/tasks/{task_id}/executions
```

#### Retry Task
```http
POST /api/v1/tasks/{task_id}/retry
```

#### Get Workflow Tasks
```http
GET /api/v1/tasks/workflow/{workflow_id}
```

### Executions

#### Get All Executions
```http
GET /api/v1/executions/
```

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Maximum number of records to return (default: 100)
- `workflow_id` (int): Filter by workflow ID
- `status` (str): Filter by status

#### Get Execution by ID
```http
GET /api/v1/executions/{execution_id}
```

#### Get Execution Statistics
```http
GET /api/v1/executions/stats
```

**Query Parameters:**
- `workflow_id` (int): Filter by workflow ID
- `days` (int): Number of days to include (default: 30)

**Response:**
```json
{
  "total_executions": 100,
  "successful_executions": 95,
  "failed_executions": 5,
  "running_executions": 2,
  "success_rate": 95.0,
  "average_execution_time": 120.5,
  "total_tokens_used": 50000,
  "executions_by_day": [
    {
      "date": "2024-01-15",
      "count": 10,
      "successful": 9,
      "failed": 1
    }
  ],
  "top_workflows": [
    {
      "workflow_id": 1,
      "count": 50,
      "successful": 48,
      "failed": 2
    }
  ],
  "error_breakdown": [
    {
      "error": "Connection timeout",
      "count": 3
    }
  ]
}
```

#### Get Execution Logs
```http
GET /api/v1/executions/{execution_id}/logs
```

#### Cancel Execution
```http
POST /api/v1/executions/{execution_id}/cancel
```

#### Get Execution Status
```http
GET /api/v1/executions/{execution_id}/status
```

## 🔌 WebSocket API

### Connection

Connect to WebSocket endpoint:
```
ws://localhost:8000/ws/
```

### Message Types

#### Ping/Pong
```json
{
  "type": "ping",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### Subscribe to Workflow
```json
{
  "type": "subscribe_workflow",
  "workflow_id": 1
}
```

#### Subscribe to Agent
```json
{
  "type": "subscribe_agent",
  "agent_id": 1
}
```

### Event Types

#### Workflow Started
```json
{
  "type": "workflow_started",
  "workflow_id": 1,
  "execution_id": 1,
  "status": "running"
}
```

#### Workflow Completed
```json
{
  "type": "workflow_completed",
  "workflow_id": 1,
  "execution_id": 1,
  "status": "completed"
}
```

#### Task Completed
```json
{
  "type": "task_completed",
  "task_id": 1,
  "execution_id": 1,
  "status": "completed"
}
```

## 📊 Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict
- `422` - Unprocessable Entity
- `429` - Too Many Requests
- `500` - Internal Server Error
- `503` - Service Unavailable

## 🚨 Error Responses

```json
{
  "error": "ERROR_CODE",
  "message": "Human readable error message",
  "details": {
    "additional": "error details"
  }
}
```

## 🔄 Rate Limiting

- **API Requests:** 100 requests per minute per IP
- **WebSocket Connections:** 5 connections per minute per IP

## 📝 Examples

### Complete Workflow Example

1. **Create Agent:**
```bash
curl -X POST http://localhost:8000/api/v1/agents/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Content Writer",
    "role": "Content Creator",
    "goal": "Create engaging content",
    "model": "llama-4-maverick-17b-128e-instruct"
  }'
```

2. **Create Workflow:**
```bash
curl -X POST http://localhost:8000/api/v1/workflows/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Content Pipeline",
    "description": "Automated content creation",
    "workflow_type": "linear"
  }'
```

3. **Create Task:**
```bash
curl -X POST http://localhost:8000/api/v1/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_id": 1,
    "agent_id": 1,
    "name": "Write Article",
    "description": "Write a blog article about AI",
    "task_type": "ai_task"
  }'
```

4. **Execute Workflow:**
```bash
curl -X POST http://localhost:8000/api/v1/workflows/1/execute \
  -H "Content-Type: application/json" \
  -d '{
    "input_data": {
      "topic": "AI in Healthcare",
      "length": "1000 words"
    }
  }'
```

## 🔧 SDK Examples

### Python SDK
```python
import requests

# Get all agents
response = requests.get('http://localhost:8000/api/v1/agents/')
agents = response.json()

# Create new agent
agent_data = {
    "name": "Python Agent",
    "role": "Python Developer",
    "goal": "Write Python code",
    "model": "llama-4-maverick-17b-128e-instruct"
}
response = requests.post('http://localhost:8000/api/v1/agents/', json=agent_data)
```

### JavaScript SDK
```javascript
// Get all agents
fetch('http://localhost:8000/api/v1/agents/')
  .then(response => response.json())
  .then(agents => console.log(agents));

// Create new agent
const agentData = {
  name: "JS Agent",
  role: "JavaScript Developer",
  goal: "Write JavaScript code",
  model: "llama-4-maverick-17b-128e-instruct"
};

fetch('http://localhost:8000/api/v1/agents/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(agentData)
})
.then(response => response.json())
.then(agent => console.log(agent));
```

---

**For more detailed API documentation, visit:** `http://localhost:8000/docs`