
# Deployment Guide

Comprehensive guide for deploying the Algorithmic Debugging & Efficiency Coach system in various environments.

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Local Development Setup](#local-development-setup)
4. [Docker Deployment](#docker-deployment)
5. [Kubernetes Deployment](#kubernetes-deployment)
6. [IBM Cloud Deployment](#ibm-cloud-deployment)
7. [Environment Configuration](#environment-configuration)
8. [Database Setup](#database-setup)
9. [Monitoring & Logging](#monitoring--logging)
10. [Security Configuration](#security-configuration)
11. [Scaling & Performance](#scaling--performance)
12. [Backup & Disaster Recovery](#backup--disaster-recovery)
13. [Troubleshooting](#troubleshooting)

## Overview

The system supports multiple deployment strategies:

- **Local Development**: Individual services running on localhost
- **Docker Compose**: Containerized services for development/testing
- **Kubernetes**: Production-grade orchestration with auto-scaling
- **IBM Cloud**: Fully managed deployment with IBM services

## Prerequisites

### Required Tools

```bash
# Docker & Docker Compose
docker --version  # 20.10+
docker-compose --version  # 2.0+

# Kubernetes (for K8s deployment)
kubectl version  # 1.24+
helm version  # 3.10+

# IBM Cloud CLI (for IBM Cloud deployment)
ibmcloud --version  # 2.0+
ibmcloud plugin install container-service
ibmcloud plugin install container-registry
```

### Required Accounts

- **IBM Cloud Account**: For watsonx.ai and watsonx Orchestrate
- **Container Registry**: Docker Hub, IBM Container Registry, or private registry
- **Domain & SSL**: For production deployment

## Local Development Setup

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd algo-coach
```

### Step 2: Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies for each service
cd services/debugging-engine
pip install -r requirements.txt

cd ../efficiency-analyzer
pip install -r requirements.txt

cd ../watsonx-ai-integration
pip install -r requirements.txt

cd ../watsonx-orchestrate-integration
pip install -r requirements.txt
```

### Step 3: Configure Environment

Create `.env` file:

```bash
# IBM watsonx Configuration
WATSONX_API_KEY=your_api_key
WATSONX_PROJECT_ID=your_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Service Ports
DEBUGGING_ENGINE_PORT=8001
EFFICIENCY_ANALYZER_PORT=8002
WATSONX_AI_PORT=8003
WATSONX_ORCHESTRATE_PORT=8004

# Logging
LOG_LEVEL=INFO
```

### Step 4: Start Services

```bash
# Terminal 1: Debugging Engine
cd services/debugging-engine
python -m app.main

# Terminal 2: Efficiency Analyzer
cd services/efficiency-analyzer
python -m app.main

# Terminal 3: watsonx.ai Integration
cd services/watsonx-ai-integration
python -m app.handler

# Terminal 4: watsonx Orchestrate Integration
cd services/watsonx-orchestrate-integration
python -m app.handler
```

## Docker Deployment

### Step 1: Build Docker Images

```bash
# Build all images
docker-compose build

# Or build individually
docker build -t algo-coach/debugging-engine:latest ./services/debugging-engine
docker build -t algo-coach/efficiency-analyzer:latest ./services/efficiency-analyzer
docker build -t algo-coach/watsonx-ai:latest ./services/watsonx-ai-integration
docker build -t algo-coach/watsonx-orchestrate:latest ./services/watsonx-orchestrate-integration
```

### Step 2: Create Docker Compose File

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  debugging-engine:
    build: ./services/debugging-engine
    ports:
      - "8001:8001"
    environment:
      - LOG_LEVEL=INFO
      - PORT=8001
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  efficiency-analyzer:
    build: ./services/efficiency-analyzer
    ports:
      - "8002:8002"
    environment:
      - LOG_LEVEL=INFO
      - PORT=8002
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8002/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  watsonx-ai-integration:
    build: ./services/watsonx-ai-integration
    ports:
      - "8003:8003"
    environment:
      - WATSONX_API_KEY=${WATSONX_API_KEY}
      - WATSONX_PROJECT_ID=${WATSONX_PROJECT_ID}
      - WATSONX_URL=${WATSONX_URL}
      - LOG_LEVEL=INFO
      - PORT=8003
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8003/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  watsonx-orchestrate-integration:
    build: ./services/watsonx-orchestrate-integration
    ports:
      - "8004:8004"
    environment:
      - WATSONX_API_KEY=${WATSONX_API_KEY}
      - LOG_LEVEL=INFO
      - PORT=8004
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8004/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  # Optional: PostgreSQL for data persistence
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=algo_coach
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  # Optional: Redis for caching
  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

### Step 3: Start Services

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Stop services
docker-compose down
```

### Step 4: Verify Deployment

```bash
# Check service health
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
curl http://localhost:8004/health
```

## Kubernetes Deployment

### Step 1: Create Kubernetes Manifests

Create `k8s/` directory structure:

```
k8s/
├── namespace.yaml
├── configmap.yaml
├── secrets.yaml
├── debugging-engine/
│   ├── deployment.yaml
│   └── service.yaml
├── efficiency-analyzer/
│   ├── deployment.yaml
│   └── service.yaml
├── watsonx-ai/
│   ├── deployment.yaml
│   └── service.yaml
└── watsonx-orchestrate/
    ├── deployment.yaml
    └── service.yaml
```

### Step 2: Namespace Configuration

`k8s/namespace.yaml`:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: algo-coach
  labels:
    name: algo-coach
```

### Step 3: ConfigMap

`k8s/configmap.yaml`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: algo-coach-config
  namespace: algo-coach
data:
  LOG_LEVEL: "INFO"
  WATSONX_URL: "https://us-south.ml.cloud.ibm.com"
```

### Step 4: Secrets

```bash
# Create secrets from environment variables
kubectl create secret generic algo-coach-secrets \
  --from-literal=watsonx-api-key=${WATSONX_API_KEY} \
  --from-literal=watsonx-project-id=${WATSONX_PROJECT_ID} \
  --namespace=algo-coach
```

### Step 5: Deployment Example

`k8s/debugging-engine/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: debugging-engine
  namespace: algo-coach
  labels:
    app: debugging-engine
spec:
  replicas: 3
  selector:
    matchLabels:
      app: debugging-engine
  template:
    metadata:
      labels:
        app: debugging-engine
    spec:
      containers:
      - name: debugging-engine
        image: algo-coach/debugging-engine:latest
        ports:
        - containerPort: 8001
          name: http
        env:
        - name: PORT
          value: "8001"
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: algo-coach-config
              key: LOG_LEVEL
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8001
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8001
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: debugging-engine
  namespace: algo-coach
spec:
  selector:
    app: debugging-engine
  ports:
  - port: 8001
    targetPort: 8001
    name: http
  type: ClusterIP
```

### Step 6: Horizontal Pod Autoscaler

`k8s/debugging-engine/hpa.yaml`:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: debugging-engine-hpa
  namespace: algo-coach
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: debugging-engine
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Step 7: Ingress Configuration

`k8s/ingress.yaml`:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: algo-coach-ingress
  namespace: algo-coach
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - api.algo-coach.example.com
    secretName: algo-coach-tls
  rules:
  - host: api.algo-coach.example.com
    http:
      paths:
      - path: /debugging
        pathType: Prefix
        backend:
          service:
            name: debugging-engine
            port:
              number: 8001
      - path: /efficiency
        pathType: Prefix
        backend:
          service:
            name: efficiency-analyzer
            port:
              number: 8002
      - path: /watsonx-ai
        pathType: Prefix
        backend:
          service:
            name: watsonx-ai
            port:
              number: 8003
      - path: /watsonx-orchestrate
        pathType: Prefix
        backend:
          service:
            name: watsonx-orchestrate
            port:
              number: 8004
```

### Step 8: Deploy to Kubernetes

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create ConfigMap and Secrets
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml

# Deploy services
kubectl apply -f k8s/debugging-engine/
kubectl apply -f k8s/efficiency-analyzer/
kubectl apply -f k8s/watsonx-ai/
kubectl apply -f k8s/watsonx-orchestrate/

# Deploy Ingress
kubectl apply -f k8s/ingress.yaml

# Verify deployment
kubectl get pods -n algo-coach
kubectl get services -n algo-coach
kubectl get ingress -n algo-coach
```

## IBM Cloud Deployment

### Step 1: Set Up IBM Cloud CLI

```bash
# Login to IBM Cloud
ibmcloud login --sso

# Target resource group
ibmcloud target -g default

# Set region
ibmcloud target -r us-south
```

### Step 2: Create Kubernetes Cluster

```bash
# Create IKS cluster
ibmcloud ks cluster create classic \
  --name algo-coach-cluster \
  --zone dal10 \
  --flavor b3c.4x16 \
  --workers 3 \
  --public-vlan <vlan-id> \
  --private-vlan <vlan-id>

# Wait for cluster to be ready
ibmcloud ks cluster get --cluster algo-coach-cluster

# Configure kubectl
ibmcloud ks cluster config --cluster algo-coach-cluster
```

### Step 3: Set Up Container Registry

```bash
# Create namespace in IBM Container Registry
ibmcloud cr namespace-add algo-coach

# Build and push images
docker tag algo-coach/debugging-engine:latest \
  us.icr.io/algo-coach/debugging-engine:latest

docker push us.icr.io/algo-coach/debugging-engine:latest

# Repeat for other services
```

### Step 4: Configure watsonx Services

```bash
# Create watsonx.ai instance
ibmcloud resource service-instance-create \
  watsonx-ai watsonxai lite us-south

# Get API key
ibmcloud resource service-key-create \
  watsonx-ai-key Manager \
  --instance-name watsonx-ai

# Create watsonx Orchestrate instance
ibmcloud resource service-instance-create \
  watsonx-orchestrate watsonx-orchestrate lite us-south
```

### Step 5: Deploy to IBM Cloud

```bash
# Update image references in K8s manifests to use IBM Container Registry
# us.icr.io/algo-coach/debugging-engine:latest

# Deploy to cluster
kubectl apply -f k8s/

# Verify deployment
kubectl get all -n algo-coach
```

## Environment Configuration

### Production Environment Variables

```bash
# IBM watsonx
WATSONX_API_KEY=<production-api-key>
WATSONX_PROJECT_ID=<production-project-id>
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Database
POSTGRES_HOST=<db-host>
POSTGRES_PORT=5432
POSTGRES_DB=algo_coach_prod
POSTGRES_USER=<db-user>
POSTGRES_PASSWORD=<secure-password>

# Redis
REDIS_HOST=<redis-host>
REDIS_PORT=6379
REDIS_PASSWORD=<secure-password>

# Security
JWT_SECRET=<random-secret-key>
API_KEY_SALT=<random-salt>

# Monitoring
PROMETHEUS_ENABLED=true
GRAFANA_ENABLED=true
LOG_LEVEL=INFO

# Performance
MAX_WORKERS=4
TIMEOUT=30
RATE_LIMIT=100
```

## Database Setup

### PostgreSQL Schema

```sql
-- Create database
CREATE DATABASE algo_coach_prod;

-- Create tables
CREATE TABLE submissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255),
    code TEXT NOT NULL,
    language VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE analysis_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    submission_id UUID REFERENCES submissions(id),
    service_name VARCHAR(100) NOT NULL,
    results JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_submissions_user_id ON submissions(user_id);
CREATE INDEX idx_submissions_created_at ON submissions(created_at);
CREATE INDEX idx_analysis_submission_id ON analysis_results(submission_id);
```

## Monitoring & Logging

### Prometheus Configuration

```yaml
# prometheus-config.yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'debugging-engine'
    static_configs:
      - targets: ['debugging-engine:8001']
  
  - job_name: 'efficiency-analyzer'
    static_configs:
      - targets: ['efficiency-analyzer:8002']
```

### Grafana Dashboards

Import pre-built dashboards for:
- Service health and uptime
- Request rates and latency
- Error rates
- Resource utilization

### Centralized Logging

```yaml
# fluentd-config.yaml
<source>
  @type forward
  port 24224
</source>

<match **>
  @type elasticsearch
  host elasticsearch
  port 9200
  logstash_format true
</match>
```

## Security Configuration

### SSL/TLS Setup

```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.12.0/cert-manager.yaml

# Create ClusterIssuer
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF
```

### Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: algo-coach-network-policy
  namespace: algo-coach
spec:
  podSelector:
    matchLabels:
      app: debugging-engine
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: nginx-ingress
    ports:
    - protocol: TCP
      port: 8001
```

## Scaling & Performance

### Auto-scaling Configuration

```bash
# Enable cluster autoscaler
kubectl apply -f - <<EOF
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: debugging-engine-vpa
  namespace: algo-coach
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: debugging-engine
  updatePolicy:
    updateMode: "Auto"
EOF
```

### Performance Tuning

- Enable connection pooling
- Configure Redis caching
- Optimize database queries
- Use CDN for static assets
- Enable gzip compression

## Backup & Disaster Recovery

### Database Backup

```bash
# Automated daily backups
kubectl create cronjob postgres-backup \
  --image=postgres:15 \
  --schedule="0 2 * * *" \
  -- pg_dump -h postgres -U postgres algo_coach_prod > /backups/backup-$(date +%Y%m%d).sql
```

### Disaster Recovery Plan

1. Regular backups (daily)
2. Multi-region deployment
3. Database replication
4. Automated failover
5. Recovery time objective (RTO): 1 hour
6. Recovery point objective (RPO): 24 hours

## Troubleshooting

### Common Issues

**Pods not starting**:
```bash
kubectl describe pod <pod-name> -n algo-coach
kubectl logs <pod-name> -n algo-coach
```

**Service unreachable**:
```bash
kubectl get svc -n algo-coach
kubectl get endpoints -n algo-coach
```

**High memory usage**:
```bash
kubectl top pods -n algo-coach
kubectl describe hpa -n algo-coach
```

### Health Checks

```bash
# Check all services
for port in 8001 8002 8003 8004; do
  curl http://localhost:$port/health
done
```

---

For additional support, refer to:
- [Getting Started Guide](GETTING_STARTED.md)
- [API Reference](API_REFERENCE.md)
- [Architecture Documentation](ARCHITECTURE.md)
