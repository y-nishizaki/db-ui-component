# デプロイメントガイド

このガイドでは、Databricks UI Component Libraryを本番環境にデプロイする方法を説明します。

## 🎯 概要

本番環境へのデプロイメントでは、パフォーマンス、セキュリティ、可用性を考慮した適切な設定が必要です。

## 🚀 デプロイメント戦略

### 1. 環境別デプロイメント

```python
# 環境設定クラス
class EnvironmentConfig:
    def __init__(self, environment):
        self.environment = environment
        self.configs = {
            'development': {
                'debug': True,
                'log_level': 'DEBUG',
                'cache_enabled': False,
                'max_data_size': 10000
            },
            'staging': {
                'debug': False,
                'log_level': 'INFO',
                'cache_enabled': True,
                'max_data_size': 50000
            },
            'production': {
                'debug': False,
                'log_level': 'WARNING',
                'cache_enabled': True,
                'max_data_size': 100000,
                'rate_limiting': True,
                'ssl_required': True
            }
        }
    
    def get_config(self):
        """環境設定を取得"""
        return self.configs.get(self.environment, self.configs['development'])
    
    def is_production(self):
        """本番環境かどうかを判定"""
        return self.environment == 'production'

# 使用例
config = EnvironmentConfig('production')
settings = config.get_config()
print(f"本番環境設定: {settings}")
```

### 2. 設定ファイルの管理

```python
import yaml
import os

# 設定ファイルの管理
class ConfigManager:
    def __init__(self, config_path='config.yaml'):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self):
        """設定ファイルを読み込み"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as file:
                return yaml.safe_load(file)
        else:
            return self.get_default_config()
    
    def get_default_config(self):
        """デフォルト設定を取得"""
        return {
            'database': {
                'host': 'localhost',
                'port': 5432,
                'name': 'dashboard_db',
                'user': 'dashboard_user'
            },
            'security': {
                'ssl_required': True,
                'session_timeout': 3600,
                'max_login_attempts': 5
            },
            'performance': {
                'cache_enabled': True,
                'cache_ttl': 300,
                'max_data_size': 100000
            },
            'logging': {
                'level': 'INFO',
                'file': 'dashboard.log',
                'max_size': '10MB',
                'backup_count': 5
            }
        }
    
    def get_database_config(self):
        """データベース設定を取得"""
        return self.config.get('database', {})
    
    def get_security_config(self):
        """セキュリティ設定を取得"""
        return self.config.get('security', {})
    
    def get_performance_config(self):
        """パフォーマンス設定を取得"""
        return self.config.get('performance', {})

# 使用例
config_manager = ConfigManager()
db_config = config_manager.get_database_config()
security_config = config_manager.get_security_config()
```

## 🐳 Docker デプロイメント

### 1. Dockerfile の作成

```dockerfile
# Dockerfile
FROM python:3.9-slim

# 作業ディレクトリの設定
WORKDIR /app

# システム依存関係のインストール
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Python依存関係のコピー
COPY requirements.txt .

# Python依存関係のインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードのコピー
COPY . .

# 環境変数の設定
ENV PYTHONPATH=/app
ENV FLASK_ENV=production
ENV FLASK_APP=app.py

# ポートの公開
EXPOSE 5000

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# アプリケーションの起動
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

### 2. Docker Compose の設定

```yaml
# docker-compose.yml
version: '3.8'

services:
  dashboard-app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/dashboard
      - REDIS_URL=redis://redis:6379
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=dashboard
      - POSTGRES_USER=dashboard_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - dashboard-app

volumes:
  postgres_data:
  redis_data:
```

### 3. Nginx 設定

```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream dashboard_app {
        server dashboard-app:5000;
    }

    server {
        listen 80;
        server_name your-domain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        # セキュリティヘッダー
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";

        location / {
            proxy_pass http://dashboard_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # 静的ファイルの配信
        location /static/ {
            alias /app/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

## ☁️ クラウドデプロイメント

### 1. AWS デプロイメント

```python
# AWS デプロイメント設定
import boto3
import json

class AWSDeployment:
    def __init__(self, region='us-east-1'):
        self.region = region
        self.ec2 = boto3.client('ec2', region_name=region)
        self.ecs = boto3.client('ecs', region_name=region)
        self.elbv2 = boto3.client('elbv2', region_name=region)
    
    def create_ecs_cluster(self, cluster_name):
        """ECSクラスターの作成"""
        try:
            response = self.ecs.create_cluster(
                clusterName=cluster_name,
                capacityProviders=['FARGATE'],
                defaultCapacityProviderStrategy=[
                    {
                        'capacityProvider': 'FARGATE',
                        'weight': 1
                    }
                ]
            )
            return response['cluster']
        except Exception as e:
            print(f"クラスター作成エラー: {e}")
            return None
    
    def create_task_definition(self, family, image_uri):
        """タスク定義の作成"""
        task_definition = {
            'family': family,
            'networkMode': 'awsvpc',
            'requiresCompatibilities': ['FARGATE'],
            'cpu': '256',
            'memory': '512',
            'executionRoleArn': 'arn:aws:iam::account:role/ecsTaskExecutionRole',
            'containerDefinitions': [
                {
                    'name': 'dashboard-app',
                    'image': image_uri,
                    'portMappings': [
                        {
                            'containerPort': 5000,
                            'protocol': 'tcp'
                        }
                    ],
                    'environment': [
                        {
                            'name': 'DATABASE_URL',
                            'value': 'postgresql://user:password@db:5432/dashboard'
                        }
                    ],
                    'logConfiguration': {
                        'logDriver': 'awslogs',
                        'options': {
                            'awslogs-group': '/ecs/dashboard-app',
                            'awslogs-region': self.region,
                            'awslogs-stream-prefix': 'ecs'
                        }
                    }
                }
            ]
        }
        
        try:
            response = self.ecs.register_task_definition(**task_definition)
            return response['taskDefinition']
        except Exception as e:
            print(f"タスク定義作成エラー: {e}")
            return None

# 使用例
aws_deployment = AWSDeployment('us-east-1')
cluster = aws_deployment.create_ecs_cluster('dashboard-cluster')
task_def = aws_deployment.create_task_definition('dashboard-task', 'your-registry/dashboard-app:latest')
```

### 2. Azure デプロイメント

```python
# Azure デプロイメント設定
from azure.identity import DefaultAzureCredential
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.containerinstance.models import ContainerGroup, Container, ResourceRequests, ResourceRequirements

class AzureDeployment:
    def __init__(self, subscription_id, resource_group):
        self.subscription_id = subscription_id
        self.resource_group = resource_group
        self.credential = DefaultAzureCredential()
        self.container_client = ContainerInstanceManagementClient(
            credential=self.credential,
            subscription_id=subscription_id
        )
    
    def create_container_group(self, name, image, location='eastus'):
        """コンテナグループの作成"""
        container_group = ContainerGroup(
            location=location,
            containers=[
                Container(
                    name='dashboard-app',
                    image=image,
                    resources=ResourceRequirements(
                        requests=ResourceRequests(
                            memory_in_gb=1.0,
                            cpu=1.0
                        )
                    ),
                    ports=[{'port': 5000}]
                )
            ],
            os_type='Linux',
            ip_address={
                'type': 'Public',
                'ports': [
                    {
                        'protocol': 'TCP',
                        'port': 5000
                    }
                ]
            }
        )
        
        try:
            poller = self.container_client.container_groups.begin_create_or_update(
                resource_group_name=self.resource_group,
                container_group_name=name,
                container_group=container_group
            )
            result = poller.result()
            return result
        except Exception as e:
            print(f"コンテナグループ作成エラー: {e}")
            return None

# 使用例
azure_deployment = AzureDeployment('subscription-id', 'resource-group')
container_group = azure_deployment.create_container_group(
    'dashboard-app',
    'your-registry.azurecr.io/dashboard-app:latest'
)
```

## 🔄 CI/CD パイプライン

### 1. GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy Dashboard App

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run tests
      run: |
        pytest tests/
    
    - name: Run linting
      run: |
        flake8 db_ui_components/
        black --check db_ui_components/

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v1
    
    - name: Login to Docker Hub
      uses: docker/login-action@v1
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v2
      with:
        context: .
        push: true
        tags: |
          your-username/dashboard-app:latest
          your-username/dashboard-app:${{ github.sha }}
    
    - name: Deploy to production
      run: |
        # デプロイメントスクリプトの実行
        ./deploy.sh production

  deploy-staging:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to staging
      run: |
        ./deploy.sh staging
```

### 2. Jenkins Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'dashboard-app'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pip install -r requirements-dev.txt'
                sh 'pytest tests/'
                sh 'flake8 db_ui_components/'
                sh 'black --check db_ui_components/'
            }
        }
        
        stage('Build') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }
        
        stage('Push') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
                        docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push()
                        docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push('latest')
                    }
                }
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh './deploy.sh production'
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
```

## 📊 監視とログ

### 1. アプリケーション監視

```python
# 監視システム
import time
import psutil
import logging
from prometheus_client import Counter, Histogram, Gauge

class MonitoringSystem:
    def __init__(self):
        self.request_counter = Counter('http_requests_total', 'Total HTTP requests')
        self.request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')
        self.memory_usage = Gauge('memory_usage_bytes', 'Memory usage in bytes')
        self.cpu_usage = Gauge('cpu_usage_percent', 'CPU usage percentage')
        
        # ログ設定
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('app.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def monitor_request(self, func):
        """リクエスト監視デコレータ"""
        def wrapper(*args, **kwargs):
            start_time = time.time()
            self.request_counter.inc()
            
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                self.request_duration.observe(duration)
                self.logger.info(f"Request completed in {duration:.2f}s")
                return result
            except Exception as e:
                self.logger.error(f"Request failed: {e}")
                raise
        
        return wrapper
    
    def update_system_metrics(self):
        """システムメトリクスの更新"""
        memory = psutil.virtual_memory()
        cpu = psutil.cpu_percent()
        
        self.memory_usage.set(memory.used)
        self.cpu_usage.set(cpu)
        
        self.logger.info(f"Memory: {memory.percent}%, CPU: {cpu}%")

# 使用例
monitoring = MonitoringSystem()

@monitoring.monitor_request
def render_dashboard(data):
    # ダッシュボードのレンダリング
    return dashboard.render()

# 定期的なメトリクス更新
import threading
import time

def update_metrics():
    while True:
        monitoring.update_system_metrics()
        time.sleep(60)  # 1分間隔

metrics_thread = threading.Thread(target=update_metrics, daemon=True)
metrics_thread.start()
```

### 2. ログ集約

```python
# ログ集約システム
import json
from datetime import datetime

class LogAggregator:
    def __init__(self, log_file='aggregated.log'):
        self.log_file = log_file
    
    def log_event(self, event_type, data, level='INFO'):
        """イベントログを記録"""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': level,
            'event_type': event_type,
            'data': data
        }
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def get_recent_logs(self, hours=24):
        """最近のログを取得"""
        logs = []
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        with open(self.log_file, 'r') as f:
            for line in f:
                try:
                    log_entry = json.loads(line.strip())
                    log_time = datetime.fromisoformat(log_entry['timestamp'])
                    if log_time >= cutoff_time:
                        logs.append(log_entry)
                except json.JSONDecodeError:
                    continue
        
        return logs

# 使用例
log_aggregator = LogAggregator()

# イベントログの記録
log_aggregator.log_event('dashboard_rendered', {
    'user_id': 'user1',
    'chart_count': 5,
    'render_time': 2.5
})

# 最近のログを取得
recent_logs = log_aggregator.get_recent_logs(1)  # 過去1時間
```

## 🚀 次のステップ

- [パフォーマンス最適化](./performance.md) - パフォーマンスの最適化
- [セキュリティ](./security.md) - セキュリティのベストプラクティス
- [トラブルシューティング](../troubleshooting/faq.md) - デプロイメント関連のFAQ

## ❓ サポート

デプロイメントで問題が発生した場合は、以下を確認してください：

- [よくある問題](../troubleshooting/faq.md)
- [エラーリファレンス](../troubleshooting/errors.md)
- [GitHub Issues](https://github.com/databricks/db-ui-components/issues)