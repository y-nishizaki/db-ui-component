# セキュリティガイド

このドキュメントでは、db-ui-componentsライブラリのセキュリティ機能とベストプラクティスについて説明します。

## セキュリティ機能

### XSS攻撃防止

ライブラリはXSS（クロスサイトスクリプティング）攻撃を防ぐための機能を提供します：

```python
from db_ui_components import ChartComponent
import pandas as pd

# 悪意のあるスクリプトを含むデータ
malicious_data = pd.DataFrame({
    'x': [1, 2, 3],
    'y': [1, 4, 9],
    'label': ['<script>alert("XSS")</script>', 'Normal', 'Data']
})

# 自動的にHTMLエスケープ処理が実行される
chart = ChartComponent(
    data=malicious_data,
    chart_type='scatter',
    x_column='x',
    y_column='y'
)

# 安全にレンダリング
displayHTML(chart.render())
```

### 入力値サニタイゼーション

すべてのユーザー入力は自動的にサニタイゼーションされます：

```python
# 特殊文字を含むデータ
special_chars_data = pd.DataFrame({
    'category': ['A&B', 'C<D>', 'E"F', "G'H"],
    'value': [10, 20, 30, 40]
})

# 自動的にエスケープ処理される
table = TableComponent(data=special_chars_data)
displayHTML(table.render())
```

### SQLインジェクション防止

データベースコンポーネントでは、SQLインジェクション攻撃を防ぐ機能を提供します：

```python
from db_ui_components import DatabaseComponent

db = DatabaseComponent(
    component_id="secure-db",
    workspace_url="https://your-workspace.cloud.databricks.com",
    token="your-token"
)

# パラメータ化クエリを使用
safe_query = "SELECT * FROM users WHERE name = %s"
result = db.execute_query(safe_query, params=["user_input"])
```

## セキュリティベストプラクティス

### 1. 認証情報の管理

```python
import os
from db_ui_components import DatabaseComponent

# 環境変数から認証情報を取得
db = DatabaseComponent(
    component_id="secure-db",
    workspace_url=os.getenv('DATABRICKS_WORKSPACE_URL'),
    token=os.getenv('DATABRICKS_TOKEN')
)
```

### 2. データの暗号化

```python
# 機密データの暗号化
import hashlib

def hash_sensitive_data(data):
    """機密データをハッシュ化"""
    return hashlib.sha256(data.encode()).hexdigest()

# 使用例
sensitive_df = pd.DataFrame({
    'user_id': ['user1', 'user2'],
    'hashed_password': [hash_sensitive_data('password1'), hash_sensitive_data('password2')]
})
```

### 3. アクセス制御

```python
# ユーザー権限の確認
def check_user_permission(user_id, required_role):
    """ユーザーの権限を確認"""
    user_roles = get_user_roles(user_id)
    return required_role in user_roles

# 権限に基づいてコンポーネントを表示
if check_user_permission(current_user, 'admin'):
    admin_chart = ChartComponent(data=admin_data, chart_type='line')
    displayHTML(admin_chart.render())
```

### 4. セッション管理

```python
# セッションタイムアウトの設定
import time

class SecureSession:
    def __init__(self, timeout_minutes=30):
        self.timeout_minutes = timeout_minutes
        self.last_activity = time.time()
    
    def is_valid(self):
        """セッションが有効かチェック"""
        return (time.time() - self.last_activity) < (self.timeout_minutes * 60)
    
    def update_activity(self):
        """アクティビティを更新"""
        self.last_activity = time.time()

# 使用例
session = SecureSession(timeout_minutes=15)
if session.is_valid():
    # コンポーネントを表示
    chart = ChartComponent(data=df, chart_type='line')
    displayHTML(chart.render())
    session.update_activity()
else:
    print("セッションが期限切れです")
```

## セキュリティ設定

### コンポーネントレベルのセキュリティ

```python
# セキュリティ設定付きコンポーネント
chart = ChartComponent(
    data=df,
    chart_type='line',
    x_column='x',
    y_column='y',
    security_config={
        'enable_xss_protection': True,
        'enable_csrf_protection': True,
        'content_security_policy': "default-src 'self'",
        'max_data_size': 10000  # 最大データサイズ
    }
)
```

### ダッシュボードレベルのセキュリティ

```python
from db_ui_components import Dashboard

dashboard = Dashboard(
    title="Secure Dashboard",
    security_config={
        'require_authentication': True,
        'allowed_roles': ['admin', 'user'],
        'session_timeout': 30,
        'enable_audit_log': True
    }
)
```

## 監査ログ

### アクセスログの記録

```python
import logging
from datetime import datetime

# 監査ログの設定
audit_logger = logging.getLogger('audit')
audit_logger.setLevel(logging.INFO)

def log_component_access(user_id, component_type, action):
    """コンポーネントアクセスをログに記録"""
    audit_logger.info(
        f"User: {user_id}, Component: {component_type}, "
        f"Action: {action}, Timestamp: {datetime.now()}"
    )

# 使用例
log_component_access('user123', 'ChartComponent', 'render')
```

### データアクセスログ

```python
def log_data_access(user_id, data_source, query, result_count):
    """データアクセスをログに記録"""
    audit_logger.info(
        f"User: {user_id}, Data Source: {data_source}, "
        f"Query: {query}, Results: {result_count}, "
        f"Timestamp: {datetime.now()}"
    )
```

## セキュリティテスト

### 自動セキュリティテスト

```python
import pytest
from db_ui_components import ChartComponent

def test_xss_protection():
    """XSS攻撃の防止テスト"""
    malicious_data = pd.DataFrame({
        'x': [1, 2, 3],
        'y': [1, 4, 9],
        'label': ['<script>alert("XSS")</script>', 'Normal', 'Data']
    })
    
    chart = ChartComponent(data=malicious_data, chart_type='scatter')
    html_output = chart.render()
    
    # スクリプトタグがエスケープされていることを確認
    assert '<script>' not in html_output
    assert '&lt;script&gt;' in html_output

def test_sql_injection_protection():
    """SQLインジェクション攻撃の防止テスト"""
    malicious_input = "'; DROP TABLE users; --"
    
    # パラメータ化クエリを使用
    safe_query = "SELECT * FROM users WHERE name = %s"
    # この実装では、パラメータ化クエリが使用されることを確認
```

### 手動セキュリティテスト

```python
# セキュリティテスト用のユーティリティ
def test_security_features():
    """セキュリティ機能のテスト"""
    
    # 1. XSSテスト
    test_xss_protection()
    
    # 2. SQLインジェクションテスト
    test_sql_injection_protection()
    
    # 3. 認証テスト
    test_authentication()
    
    # 4. 権限テスト
    test_authorization()
    
    print("すべてのセキュリティテストが完了しました")
```

## セキュリティチェックリスト

### 開発時

- [ ] 入力値のサニタイゼーション
- [ ] XSS攻撃の防止
- [ ] SQLインジェクションの防止
- [ ] 認証情報の安全な管理
- [ ] セッション管理の実装
- [ ] アクセス制御の実装
- [ ] 監査ログの記録

### デプロイ時

- [ ] HTTPSの使用
- [ ] セキュリティヘッダーの設定
- [ ] 環境変数の適切な管理
- [ ] ファイアウォールの設定
- [ ] ログの監視
- [ ] バックアップの設定

### 運用時

- [ ] 定期的なセキュリティ監査
- [ ] 脆弱性スキャンの実行
- [ ] パッチの適用
- [ ] アクセスログの監視
- [ ] 異常検知の実装

## セキュリティインシデント対応

### インシデント検出

```python
import re

def detect_security_incident(log_entry):
    """セキュリティインシデントを検出"""
    suspicious_patterns = [
        r'<script>',
        r'javascript:',
        r'DROP TABLE',
        r'UNION SELECT'
    ]
    
    for pattern in suspicious_patterns:
        if re.search(pattern, log_entry, re.IGNORECASE):
            return True
    return False
```

### インシデント対応

```python
import logging
import time
from collections import defaultdict

# 監査ログの設定
audit_logger = logging.getLogger('audit')
audit_logger.setLevel(logging.INFO)

# セッション管理システム
class SessionManager:
    def __init__(self, session_timeout=3600):  # 1時間
        self.sessions = defaultdict(dict)
        self.session_timeout = session_timeout
    
    def create_session(self, user_id, token):
        """セッションの作成"""
        session_id = secrets.token_hex(32)
        self.sessions[session_id] = {
            'user_id': user_id,
            'token': token,
            'created_at': time.time(),
            'last_activity': time.time()
        }
        return session_id
    
    def validate_session(self, session_id):
        """セッションの検証"""
        if session_id not in self.sessions:
            return False
        
        session = self.sessions[session_id]
        current_time = time.time()
        
        # セッションタイムアウトのチェック
        if current_time - session['last_activity'] > self.session_timeout:
            del self.sessions[session_id]
            return False
        
        # 最終アクティビティの更新
        session['last_activity'] = current_time
        return True
    
    def end_session(self, session_id):
        """セッションの終了"""
        if session_id in self.sessions:
            del self.sessions[session_id]

def handle_security_incident(incident_type, details):
    """セキュリティインシデントの対応"""
    
    # 1. ログに記録
    audit_logger.error(f"Security incident: {incident_type}, Details: {details}")
    
    # 2. 管理者に通知
    notify_admin(incident_type, details)
    
    # 3. 必要に応じてアクセスを制限
    if incident_type == 'xss_attempt':
        block_user_ip(get_client_ip())
    
    # 4. インシデントレポートを作成
    create_incident_report(incident_type, details)
```

## セキュリティ設定例

### 本番環境での設定

```python
# 本番環境用のセキュリティ設定
PRODUCTION_SECURITY_CONFIG = {
    'enable_xss_protection': True,
    'enable_csrf_protection': True,
    'content_security_policy': "default-src 'self'; script-src 'self' 'unsafe-inline'",
    'strict_transport_security': True,
    'x_content_type_options': 'nosniff',
    'x_frame_options': 'DENY',
    'max_data_size': 50000,
    'session_timeout': 15,
    'require_authentication': True,
    'enable_audit_log': True,
    'log_level': 'INFO'
}
```

### 開発環境での設定

```python
# 開発環境用のセキュリティ設定
DEVELOPMENT_SECURITY_CONFIG = {
    'enable_xss_protection': True,
    'enable_csrf_protection': False,  # 開発時は無効化
    'content_security_policy': "default-src 'self' 'unsafe-inline'",
    'max_data_size': 1000,
    'session_timeout': 60,
    'require_authentication': False,  # 開発時は無効化
    'enable_audit_log': True,
    'log_level': 'DEBUG'
}
```

## セキュリティ監査

### 定期的な監査

```python
import pytest
import logging
from datetime import datetime

# 監査ログの設定
audit_logger = logging.getLogger('audit')
audit_logger.setLevel(logging.INFO)

def test_xss_protection():
    """XSS攻撃の防止テスト"""
    malicious_data = pd.DataFrame({
        'x': [1, 2, 3],
        'y': [1, 4, 9],
        'label': ['<script>alert("XSS")</script>', 'Normal', 'Data']
    })
    
    chart = ChartComponent(data=malicious_data, chart_type='scatter')
    html_output = chart.render()
    
    # スクリプトタグがエスケープされていることを確認
    assert '<script>' not in html_output
    assert '&lt;script&gt;' in html_output

def test_sql_injection_protection():
    """SQLインジェクション攻撃の防止テスト"""
    malicious_input = "'; DROP TABLE users; --"
    
    # パラメータ化クエリを使用
    safe_query = "SELECT * FROM users WHERE name = %s"
    # この実装では、パラメータ化クエリが使用されることを確認
```

## サポート

セキュリティに関する質問や問題がある場合は、以下をご確認ください：

1. [セキュリティFAQ](../troubleshooting/faq.md#セキュリティ関連)
2. [エラーリファレンス](../troubleshooting/errors.md)
3. [GitHub Issues](https://github.com/y-nishizaki/db-ui-components/issues)

セキュリティインシデントの報告は、[GitHub Issues](https://github.com/y-nishizaki/db-ui-components/issues)で行ってください。