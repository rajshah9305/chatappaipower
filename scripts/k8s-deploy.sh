#!/bin/bash

# CrewAI Cerebras Platform Kubernetes Deployment Script
# This script deploys the application to Kubernetes

set -e

echo "🚀 Deploying CrewAI Cerebras Platform to Kubernetes..."

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install kubectl first."
    exit 1
fi

# Check if cluster is accessible
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Kubernetes cluster is not accessible. Please check your kubeconfig."
    exit 1
fi

# Create namespace
echo "📁 Creating namespace..."
kubectl apply -f k8s/namespace.yaml

# Create configmap
echo "⚙️ Creating configmap..."
kubectl apply -f k8s/configmap.yaml

# Create secrets
echo "🔐 Creating secrets..."
kubectl apply -f k8s/secret.yaml

# Deploy PostgreSQL
echo "🐘 Deploying PostgreSQL..."
kubectl apply -f k8s/postgres.yaml

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
kubectl wait --for=condition=ready pod -l app=postgres -n crewai-cerebras --timeout=300s

# Deploy Redis
echo "🔴 Deploying Redis..."
kubectl apply -f k8s/redis.yaml

# Wait for Redis to be ready
echo "⏳ Waiting for Redis to be ready..."
kubectl wait --for=condition=ready pod -l app=redis -n crewai-cerebras --timeout=300s

# Deploy backend
echo "🐍 Deploying backend..."
kubectl apply -f k8s/backend.yaml

# Wait for backend to be ready
echo "⏳ Waiting for backend to be ready..."
kubectl wait --for=condition=ready pod -l app=backend -n crewai-cerebras --timeout=300s

# Deploy frontend
echo "⚛️ Deploying frontend..."
kubectl apply -f k8s/frontend.yaml

# Wait for frontend to be ready
echo "⏳ Waiting for frontend to be ready..."
kubectl wait --for=condition=ready pod -l app=frontend -n crewai-cerebras --timeout=300s

# Deploy ingress
echo "🌐 Deploying ingress..."
kubectl apply -f k8s/ingress.yaml

# Get service information
echo "📊 Getting service information..."
kubectl get services -n crewai-cerebras

echo "✅ Deployment complete!"
echo ""
echo "The application is now running in Kubernetes."
echo "To access the application:"
echo "  kubectl port-forward -n crewai-cerebras service/frontend-service 3000:3000"
echo "  kubectl port-forward -n crewai-cerebras service/backend-service 8000:8000"
echo ""
echo "To view logs:"
echo "  kubectl logs -f -n crewai-cerebras -l app=backend"
echo "  kubectl logs -f -n crewai-cerebras -l app=frontend"
echo ""
echo "To delete the deployment:"
echo "  kubectl delete namespace crewai-cerebras"