# Weather App - Deployment Guide

## 🚀 Production Deployment Architecture

### **Recommended Production Stack**
```
Internet → Load Balancer → Nginx → Gunicorn → Flask App → MySQL
                      ↓
                   Static Files
```

---

## 🐳 Docker Deployment

### **Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

### **docker-compose.yml**
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=mysql://weather_user:password@db:3306/weather_app
      - WEATHER_API_KEY=${WEATHER_API_KEY}
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  db:
    image: mysql:8.0
    environment:
      - MYSQL_DATABASE=weather_app
      - MYSQL_USER=weather_user
      - MYSQL_PASSWORD=password
      - MYSQL_ROOT_PASSWORD=rootpassword
    volumes:
      - mysql_data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "3306:3306"
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web
    restart: unless-stopped

volumes:
  mysql_data:
  redis_data:
```

---

## 🔧 Nginx Configuration

### **nginx.conf**
```nginx
events {
    worker_connections 1024;
}

http {
    upstream flask_app {
        server web:5000;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/m;
    limit_req_zone $binary_remote_addr zone=weather:10m rate=60r/m;

    server {
        listen 80;
        server_name your-domain.com;

        # Redirect HTTP to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        # SSL Configuration
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;

        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";

        # Static files
        location /static/ {
            alias /app/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # API endpoints with rate limiting
        location /api/weather/ {
            limit_req zone=weather burst=5 nodelay;
            proxy_pass http://flask_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /api/ {
            limit_req zone=api burst=10 nodelay;
            proxy_pass http://flask_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Main application
        location / {
            proxy_pass http://flask_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

---

## ☁️ Cloud Deployment Options

### **AWS Deployment**

#### **Architecture**
```
Route 53 → CloudFront → ALB → ECS/Fargate → RDS MySQL
                            ↓
                         ElastiCache Redis
```

#### **ECS Task Definition**
```json
{
  "family": "weather-app",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "weather-app",
      "image": "your-repo/weather-app:latest",
      "portMappings": [
        {
          "containerPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "FLASK_ENV",
          "value": "production"
        }
      ],
      "secrets": [
        {
          "name": "DATABASE_URL",
          "valueFrom": "arn:aws:ssm:region:account:parameter/weather-app/database-url"
        },
        {
          "name": "WEATHER_API_KEY",
          "valueFrom": "arn:aws:ssm:region:account:parameter/weather-app/api-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/weather-app",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### **Google Cloud Platform**

#### **app.yaml (App Engine)**
```yaml
runtime: python311

env_variables:
  FLASK_ENV: production
  DATABASE_URL: mysql+pymysql://user:password@/weather_app?unix_socket=/cloudsql/project:region:instance
  WEATHER_API_KEY: your-api-key

automatic_scaling:
  min_instances: 1
  max_instances: 10
  target_cpu_utilization: 0.6

resources:
  cpu: 1
  memory_gb: 0.5
  disk_size_gb: 10

handlers:
- url: /static
  static_dir: static
  secure: always

- url: /.*
  script: auto
  secure: always
```

### **Azure Deployment**

#### **Azure Container Instances**
```yaml
apiVersion: 2019-12-01
location: eastus
name: weather-app
properties:
  containers:
  - name: weather-app
    properties:
      image: your-registry/weather-app:latest
      resources:
        requests:
          cpu: 1.0
          memoryInGb: 1.5
      ports:
      - port: 5000
        protocol: TCP
      environmentVariables:
      - name: FLASK_ENV
        value: production
      - name: DATABASE_URL
        secureValue: mysql://user:password@server/database
      - name: WEATHER_API_KEY
        secureValue: your-api-key
  osType: Linux
  ipAddress:
    type: Public
    ports:
    - protocol: tcp
      port: 5000
tags: {}
type: Microsoft.ContainerInstance/containerGroups
```

---

## 🔐 Environment Configuration

### **Production Environment Variables**
```bash
# Application
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-super-secret-key

# Database
DATABASE_URL=mysql://user:password@host:port/database
DB_POOL_SIZE=20
DB_POOL_TIMEOUT=30

# External APIs
WEATHER_API_KEY=your-weatherapi-key

# Cache
REDIS_URL=redis://host:port/0
CACHE_TIMEOUT=300

# Security
CORS_ORIGINS=https://your-domain.com
SSL_DISABLE=False

# Monitoring
LOG_LEVEL=INFO
SENTRY_DSN=your-sentry-dsn
```

### **Configuration Class**
```python
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key'
    
    # Database
    DATABASE_URL = os.environ.get('DATABASE_URL')
    DB_POOL_SIZE = int(os.environ.get('DB_POOL_SIZE', 10))
    
    # External APIs
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')
    
    # Cache
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_TIMEOUT = int(os.environ.get('CACHE_TIMEOUT', 300))
    
    # Security
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    
class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'
```

---

## 📊 Monitoring and Logging

### **Application Monitoring**
```python
import logging
from logging.handlers import RotatingFileHandler
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

# Sentry integration
sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)

# Logging configuration
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler(
        'logs/weather_app.log',
        maxBytes=10240000,
        backupCount=10
    )
    
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

### **Health Check Endpoint**
```python
@app.route('/health')
def health_check():
    try:
        # Check database connectivity
        connection = get_db_connection()
        if connection:
            connection.close()
            db_status = "healthy"
        else:
            db_status = "unhealthy"
        
        # Check external API
        api_status = "healthy" if API_KEY else "missing_key"
        
        return jsonify({
            'status': 'healthy' if db_status == 'healthy' else 'unhealthy',
            'database': db_status,
            'external_api': api_status,
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 503
```

---

## 🔒 Security Hardening

### **Security Checklist**
- [ ] Use HTTPS with valid SSL certificates
- [ ] Implement rate limiting on API endpoints
- [ ] Sanitize all user inputs
- [ ] Use parameterized SQL queries
- [ ] Store secrets in environment variables or secret managers
- [ ] Enable CORS with specific origins only
- [ ] Add security headers (HSTS, CSP, etc.)
- [ ] Regular security updates and dependency scanning
- [ ] Database access with least privilege principle
- [ ] Enable database encryption at rest and in transit

### **Security Headers Middleware**
```python
@app.after_request
def after_request(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
    return response
```

---

## 🚀 Deployment Commands

### **Production Deployment Steps**
```bash
# 1. Build and push Docker image
docker build -t weather-app:latest .
docker tag weather-app:latest your-registry/weather-app:latest
docker push your-registry/weather-app:latest

# 2. Deploy with Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# 3. Run database migrations
docker-compose exec web python -c "from app import init_database; init_database()"

# 4. Verify deployment
curl https://your-domain.com/health

# 5. Monitor logs
docker-compose logs -f web
```

### **Rolling Update Strategy**
```bash
# Zero-downtime deployment
docker-compose -f docker-compose.prod.yml up -d --no-deps web
docker-compose -f docker-compose.prod.yml exec web python -c "from app import health_check; health_check()"
```

---

## 📈 Performance Optimization

### **Database Optimization**
- Add indexes on frequently queried columns
- Implement connection pooling
- Use read replicas for historical data queries
- Archive old weather data periodically

### **Application Optimization**
- Implement Redis caching for weather data
- Use CDN for static assets
- Enable gzip compression
- Optimize database queries with EXPLAIN
- Implement API response caching

### **Infrastructure Scaling**
- Horizontal scaling with multiple app instances
- Database clustering or sharding
- Load balancing with health checks
- Auto-scaling based on CPU/memory metrics

This comprehensive deployment guide covers
