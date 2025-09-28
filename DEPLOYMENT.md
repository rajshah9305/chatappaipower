# 🚀 Deployment Guide

This guide covers different deployment options for the CrewAI Cerebras Platform.

## 📋 Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)
- Kubernetes cluster (for K8s deployment)

## 🐳 Docker Deployment

### Quick Start

1. **Clone the repository:**
```bash
git clone <repository-url>
cd crewai-cerebras-platform
```

2. **Set up environment:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Start the application:**
```bash
docker-compose up -d
```

4. **Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Production Deployment

1. **Use production configuration:**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

2. **Monitor the application:**
```bash
docker-compose -f docker-compose.prod.yml logs -f
```

## ☸️ Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (1.20+)
- kubectl configured
- Ingress controller (optional)

### Deploy to Kubernetes

1. **Deploy all components:**
```bash
./scripts/k8s-deploy.sh
```

2. **Access the application:**
```bash
# Port forward to access locally
kubectl port-forward -n crewai-cerebras service/frontend-service 3000:3000
kubectl port-forward -n crewai-cerebras service/backend-service 8000:8000
```

3. **Check deployment status:**
```bash
kubectl get pods -n crewai-cerebras
kubectl get services -n crewai-cerebras
```

### Customize Deployment

Edit the Kubernetes manifests in the `k8s/` directory:

- `namespace.yaml` - Namespace configuration
- `configmap.yaml` - Application configuration
- `secret.yaml` - Sensitive data (API keys, passwords)
- `postgres.yaml` - Database deployment
- `redis.yaml` - Cache deployment
- `backend.yaml` - Backend API deployment
- `frontend.yaml` - Frontend deployment
- `ingress.yaml` - Ingress configuration

## 🔧 Environment Configuration

### Required Environment Variables

```env
# Cerebras API
CEREBRAS_API_KEY=your-cerebras-api-key

# Database
DATABASE_URL=postgresql://user:password@host:port/database
REDIS_URL=redis://host:port

# Application
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
DEBUG=False
ENVIRONMENT=production

# Frontend
REACT_APP_API_URL=http://your-backend-url
REACT_APP_WS_URL=ws://your-backend-url
```

### Optional Environment Variables

```env
# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://your-domain.com

# File Upload
MAX_FILE_SIZE=10485760
UPLOAD_DIR=uploads

# Monitoring
SENTRY_DSN=your-sentry-dsn
PROMETHEUS_PORT=9090

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## 📊 Monitoring and Logs

### Docker Deployment

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# View container status
docker-compose ps
```

### Kubernetes Deployment

```bash
# View pod logs
kubectl logs -f -n crewai-cerebras -l app=backend
kubectl logs -f -n crewai-cerebras -l app=frontend

# View pod status
kubectl get pods -n crewai-cerebras

# Describe pod for troubleshooting
kubectl describe pod <pod-name> -n crewai-cerebras
```

## 🔍 Health Checks

### Application Health

- **Backend Health:** `GET /health`
- **Frontend Health:** `GET /` (should return 200)

### Database Health

```bash
# Docker
docker-compose exec postgres pg_isready

# Kubernetes
kubectl exec -n crewai-cerebras deployment/postgres -- pg_isready
```

### Redis Health

```bash
# Docker
docker-compose exec redis redis-cli ping

# Kubernetes
kubectl exec -n crewai-cerebras deployment/redis -- redis-cli ping
```

## 🚨 Troubleshooting

### Common Issues

1. **Port conflicts:**
   - Change ports in docker-compose.yml
   - Update REACT_APP_API_URL in .env

2. **Database connection issues:**
   - Check DATABASE_URL format
   - Ensure PostgreSQL is running
   - Verify network connectivity

3. **API key issues:**
   - Verify CEREBRAS_API_KEY is correct
   - Check API key permissions
   - Test API key with curl

4. **Memory issues:**
   - Increase Docker memory limits
   - Scale Kubernetes resources
   - Monitor resource usage

### Debug Mode

Enable debug mode for detailed logging:

```env
DEBUG=True
LOG_LEVEL=DEBUG
```

### Performance Optimization

1. **Database:**
   - Enable connection pooling
   - Optimize queries
   - Add indexes

2. **Caching:**
   - Configure Redis properly
   - Implement cache strategies
   - Monitor cache hit rates

3. **Frontend:**
   - Enable gzip compression
   - Use CDN for static assets
   - Implement lazy loading

## 🔄 Updates and Maintenance

### Rolling Updates

```bash
# Docker
docker-compose pull
docker-compose up -d

# Kubernetes
kubectl rollout restart deployment/backend -n crewai-cerebras
kubectl rollout restart deployment/frontend -n crewai-cerebras
```

### Database Migrations

```bash
# Docker
docker-compose exec backend alembic upgrade head

# Kubernetes
kubectl exec -n crewai-cerebras deployment/backend -- alembic upgrade head
```

### Backup and Restore

```bash
# Database backup
docker-compose exec postgres pg_dump -U postgres crewai_db > backup.sql

# Database restore
docker-compose exec -T postgres psql -U postgres crewai_db < backup.sql
```

## 📈 Scaling

### Horizontal Scaling

```yaml
# Kubernetes
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  replicas: 3  # Increase replicas
```

### Vertical Scaling

```yaml
# Kubernetes
resources:
  requests:
    memory: "1Gi"
    cpu: "500m"
  limits:
    memory: "2Gi"
    cpu: "1000m"
```

## 🔐 Security

### Production Security Checklist

- [ ] Change default passwords
- [ ] Use HTTPS/TLS
- [ ] Enable firewall rules
- [ ] Regular security updates
- [ ] Monitor access logs
- [ ] Implement rate limiting
- [ ] Use secrets management
- [ ] Enable audit logging

### SSL/TLS Configuration

1. **Obtain SSL certificates**
2. **Update nginx configuration**
3. **Redirect HTTP to HTTPS**
4. **Update environment variables**

## 📞 Support

For deployment issues:

1. Check the logs
2. Verify configuration
3. Test connectivity
4. Review documentation
5. Create an issue

---

**Happy Deploying! 🚀**