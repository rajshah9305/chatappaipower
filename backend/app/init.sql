-- Initialize database schema
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE,
    preferences TEXT
);

-- Create agents table
CREATE TABLE IF NOT EXISTS agents (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(200) NOT NULL,
    goal TEXT NOT NULL,
    backstory TEXT,
    model VARCHAR(100) NOT NULL DEFAULT 'llama-4-maverick-17b-128e-instruct',
    temperature VARCHAR(10) DEFAULT '0.6',
    max_tokens INTEGER DEFAULT 32768,
    top_p VARCHAR(10) DEFAULT '0.9',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by INTEGER REFERENCES users(id),
    config JSONB,
    capabilities JSONB,
    tools JSONB
);

-- Create workflows table
CREATE TABLE IF NOT EXISTS workflows (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'draft',
    workflow_type VARCHAR(20) DEFAULT 'linear',
    config JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by INTEGER REFERENCES users(id),
    is_active BOOLEAN DEFAULT TRUE,
    execution_count INTEGER DEFAULT 0,
    last_executed TIMESTAMP WITH TIME ZONE
);

-- Create tasks table
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    workflow_id INTEGER NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
    agent_id INTEGER NOT NULL REFERENCES agents(id),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    task_type VARCHAR(50) DEFAULT 'ai_task',
    status VARCHAR(20) DEFAULT 'pending',
    priority INTEGER DEFAULT 0,
    "order" INTEGER DEFAULT 0,
    input_data JSONB,
    output_data JSONB,
    config JSONB,
    dependencies JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by INTEGER REFERENCES users(id),
    is_active BOOLEAN DEFAULT TRUE
);

-- Create workflow_executions table
CREATE TABLE IF NOT EXISTS workflow_executions (
    id SERIAL PRIMARY KEY,
    workflow_id INTEGER NOT NULL REFERENCES workflows(id),
    status VARCHAR(20) DEFAULT 'pending',
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    input_data JSONB,
    output_data JSONB,
    error_message TEXT,
    execution_log JSONB,
    created_by INTEGER REFERENCES users(id)
);

-- Create task_executions table
CREATE TABLE IF NOT EXISTS task_executions (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL REFERENCES tasks(id),
    workflow_execution_id INTEGER REFERENCES workflow_executions(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'pending',
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    input_data JSONB,
    output_data JSONB,
    error_message TEXT,
    execution_log JSONB,
    tokens_used INTEGER DEFAULT 0,
    execution_time INTEGER,
    created_by INTEGER REFERENCES users(id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_agents_name ON agents(name);
CREATE INDEX IF NOT EXISTS idx_agents_is_active ON agents(is_active);
CREATE INDEX IF NOT EXISTS idx_workflows_name ON workflows(name);
CREATE INDEX IF NOT EXISTS idx_workflows_status ON workflows(status);
CREATE INDEX IF NOT EXISTS idx_workflows_is_active ON workflows(is_active);
CREATE INDEX IF NOT EXISTS idx_tasks_workflow_id ON tasks(workflow_id);
CREATE INDEX IF NOT EXISTS idx_tasks_agent_id ON tasks(agent_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_workflow_executions_workflow_id ON workflow_executions(workflow_id);
CREATE INDEX IF NOT EXISTS idx_workflow_executions_status ON workflow_executions(status);
CREATE INDEX IF NOT EXISTS idx_task_executions_task_id ON task_executions(task_id);
CREATE INDEX IF NOT EXISTS idx_task_executions_workflow_execution_id ON task_executions(workflow_execution_id);
CREATE INDEX IF NOT EXISTS idx_task_executions_status ON task_executions(status);

-- Insert default agents
INSERT INTO agents (name, role, goal, backstory, model, is_active, capabilities, tools) VALUES
('Researcher', 'Research Specialist', 'Gather and analyze information from various sources', 'An expert researcher with years of experience in data analysis and information gathering', 'llama-4-maverick-17b-128e-instruct', TRUE, '["Web Search", "Data Analysis", "Report Generation"]', '["search_tool", "analysis_tool"]'),
('Writer', 'Content Creator', 'Create high-quality written content based on research and requirements', 'A skilled writer with expertise in various writing styles and formats', 'llama-4-maverick-17b-128e-instruct', TRUE, '["Content Writing", "Editing", "SEO Optimization"]', '["writing_tool", "editing_tool"]'),
('Analyst', 'Data Analyst', 'Analyze data and provide insights and recommendations', 'A data scientist with strong analytical skills and business acumen', 'llama-4-maverick-17b-128e-instruct', TRUE, '["Statistical Analysis", "Visualization", "Trend Analysis"]', '["analysis_tool", "visualization_tool"]'),
('Coordinator', 'Project Coordinator', 'Coordinate tasks and manage workflow execution', 'An experienced project manager with excellent organizational skills', 'llama-4-maverick-17b-128e-instruct', TRUE, '["Task Management", "Workflow Coordination", "Progress Tracking"]', '["coordination_tool", "tracking_tool"]')
ON CONFLICT (name) DO NOTHING;