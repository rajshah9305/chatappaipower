# 🚀 CrewAI Cerebras Multi-Agent Workflow Platform

A revolutionary web application that enables users to create, manage, and execute complex AI agent workflows powered by Cerebras inference models. Built with modern technologies for maximum performance, scalability, and user experience.

## ✨ Features

- **Visual Workflow Builder**: Drag-and-drop interface for creating agent workflows
- **Real-time Agent Execution**: Live monitoring of agent tasks and communication
- **Cerebras Model Integration**: Direct integration with multiple Cerebras models
- **Collaborative Workspace**: Multi-user real-time collaboration
- **Agent Marketplace**: Pre-built agent templates and custom agents
- **Advanced Analytics**: Comprehensive monitoring and performance metrics
- **Production Ready**: Fully containerized with Docker and Kubernetes support

## 🏗️ Architecture

### Technology Stack

**Backend:**
- FastAPI (Python) - High-performance async API framework
- CrewAI - Multi-agent AI framework
- Cerebras SDK - AI model inference
- PostgreSQL - Primary database
- Redis - Caching and real-time features
- WebSockets - Real-time communication

**Frontend:**
- React 18 - Modern UI framework
- TypeScript - Type-safe development
- Tailwind CSS - Utility-first styling
- React Flow - Visual workflow builder
- Socket.io - Real-time updates
- Vite - Fast build tool

**Infrastructure:**
- Docker & Docker Compose - Containerization
- Nginx - Reverse proxy
- Kubernetes - Orchestration (optional)
- GitHub Actions - CI/CD

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 14+
- Redis 6+

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd crewai-cerebras-platform
```

2. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Start with Docker Compose:**
```bash
docker-compose up -d
```

4. **Or run locally:**
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### Environment Variables

```env
# Cerebras API
CEREBRAS_API_KEY=csk-fd9554wf4jdn99yd8wd5j3cyhcwmn53f8vt8nwn9h5449ek5

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/crewai_db
REDIS_URL=redis://localhost:6379

# Application
SECRET_KEY=your-secret-key
DEBUG=True
FRONTEND_URL=http://localhost:3000
```

## 📖 API Documentation

Once running, visit:
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Frontend: http://localhost:3000

## 🎯 Core Concepts

### Agents
AI agents with specific roles and capabilities:
- **Researcher**: Gathers and analyzes information
- **Writer**: Creates content and documentation
- **Analyst**: Performs data analysis and insights
- **Coordinator**: Manages workflow execution

### Workflows
Sequential or parallel execution of agent tasks:
- **Linear Workflows**: Sequential task execution
- **Parallel Workflows**: Concurrent task execution
- **Conditional Workflows**: Branching based on conditions
- **Loop Workflows**: Iterative task execution

### Tasks
Individual units of work performed by agents:
- **Input Processing**: Handle user inputs
- **AI Processing**: Execute AI model inference
- **Output Generation**: Create results and responses
- **Data Storage**: Persist workflow data

## 🔧 Development

### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Database Migrations
```bash
cd backend
alembic upgrade head
```

### Testing
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 🚀 Deployment

### Docker Deployment
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes Deployment
```bash
kubectl apply -f k8s/
```

### Environment-specific Configuration
- Development: `docker-compose.yml`
- Production: `docker-compose.prod.yml`
- Staging: `docker-compose.staging.yml`

## 📊 Monitoring

- **Health Checks**: `/health` endpoint
- **Metrics**: Prometheus-compatible metrics
- **Logging**: Structured JSON logging
- **Tracing**: Distributed tracing support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

- Documentation: [Wiki](link-to-wiki)
- Issues: [GitHub Issues](link-to-issues)
- Discussions: [GitHub Discussions](link-to-discussions)

---

Built with ❤️ by the RAJ NEXUS team