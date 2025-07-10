# セキュリティガイド

このガイドでは、Databricks UI Component Libraryを使用する際のセキュリティのベストプラクティスを説明します。

## 🎯 概要

データの可視化において、セキュリティは重要な要素です。このガイドでは、データの保護、アクセス制御、安全なデプロイメントについて説明します。

## 🔒 データセキュリティ

### 1. 機密データの保護

```python
# 機密データのマスキング
def mask_sensitive_data(df, sensitive_columns):
    """機密データをマスキング"""
    masked_df = df.copy()
    for col in sensitive_columns:
        if col in masked_df.columns:
            # 個人情報のマスキング
            if col in ['email', 'phone', 'ssn']:
                masked_df[col] = masked_df[col].apply(lambda x: f"{str(x)[:3]}***")
            # 金額情報のマスキング
            elif col in ['salary', 'credit_card']:
                masked_df[col] = masked_df[col].apply(lambda x: "***")
    return masked_df

# 使用例
sensitive_columns = ['email', 'phone', 'salary']
masked_df = mask_sensitive_data(df, sensitive_columns)

chart = ChartComponent(
    data=masked_df,
    chart_type='bar',
    x_column='category',
    y_column='sales',
    title='マスキングされた売上データ'
)
```

### 2. データの暗号化

```python
import hashlib
import base64

# データの暗号化
def encrypt_sensitive_data(data, key):
    """機密データを暗号化"""
    import cryptography.fernet as Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    
    # キーの生成
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'salt_',
        iterations=100000,
    )
    key_bytes = base64.urlsafe_b64encode(kdf.derive(key.encode()))
    
    # 暗号化
    f = Fernet(key_bytes)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data

# データの復号化
def decrypt_sensitive_data(encrypted_data, key):
    """暗号化されたデータを復号化"""
    import cryptography.fernet as Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'salt_',
        iterations=100000,
    )
    key_bytes = base64.urlsafe_b64encode(kdf.derive(key.encode()))
    
    f = Fernet(key_bytes)
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data.decode()
```

### 3. データアクセス制御

```python
# ロールベースのアクセス制御
class DataAccessControl:
    def __init__(self):
        self.user_roles = {
            'admin': ['read', 'write', 'delete'],
            'analyst': ['read'],
            'viewer': ['read']
        }
    
    def check_permission(self, user, action, data_type):
        """ユーザーの権限をチェック"""
        if user not in self.user_roles:
            return False
        
        user_permissions = self.user_roles[user]
        return action in user_permissions
    
    def filter_data_by_role(self, df, user, sensitive_columns):
        """ロールに基づいてデータをフィルタリング"""
        if self.check_permission(user, 'read', 'sensitive'):
            return df
        else:
            # 機密列を除外
            safe_columns = [col for col in df.columns if col not in sensitive_columns]
            return df[safe_columns]

# 使用例
access_control = DataAccessControl()
user = 'analyst'
sensitive_columns = ['email', 'phone', 'salary']

if access_control.check_permission(user, 'read', 'sales'):
    filtered_df = access_control.filter_data_by_role(df, user, sensitive_columns)
    chart = ChartComponent(data=filtered_df, chart_type='line', x_column='date', y_column='sales')
    displayHTML(chart.render())
else:
    print("アクセス権限がありません")
```

## 🛡️ 入力検証

### 1. データの検証

```python
import re
from typing import Dict, Any

# データ検証クラス
class DataValidator:
    def __init__(self):
        self.validation_rules = {
            'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'phone': r'^\+?1?\d{9,15}$',
            'date': r'^\d{4}-\d{2}-\d{2}$',
            'numeric': r'^\d+(\.\d+)?$'
        }
    
    def validate_data(self, df, column_rules):
        """データフレームの検証"""
        validation_results = {}
        
        for column, rule in column_rules.items():
            if column in df.columns:
                if rule in self.validation_rules:
                    pattern = self.validation_rules[rule]
                    valid_mask = df[column].astype(str).str.match(pattern, na=False)
                    validation_results[column] = {
                        'valid_count': valid_mask.sum(),
                        'invalid_count': (~valid_mask).sum(),
                        'valid_percentage': (valid_mask.sum() / len(df)) * 100
                    }
        
        return validation_results
    
    def clean_invalid_data(self, df, column_rules):
        """無効なデータをクリーンアップ"""
        cleaned_df = df.copy()
        
        for column, rule in column_rules.items():
            if column in cleaned_df.columns:
                if rule in self.validation_rules:
                    pattern = self.validation_rules[rule]
                    valid_mask = cleaned_df[column].astype(str).str.match(pattern, na=False)
                    cleaned_df = cleaned_df[valid_mask]
        
        return cleaned_df

# 使用例
validator = DataValidator()
column_rules = {
    'email': 'email',
    'phone': 'phone',
    'date': 'date',
    'sales': 'numeric'
}

# データの検証
validation_results = validator.validate_data(df, column_rules)
print("検証結果:", validation_results)

# 無効なデータのクリーンアップ
cleaned_df = validator.clean_invalid_data(df, column_rules)
```

### 2. SQLインジェクション対策

```python
# 安全なSQLクエリの構築
class SafeSQLBuilder:
    def __init__(self):
        self.allowed_tables = ['sales_data', 'customer_data', 'product_data']
        self.allowed_columns = ['date', 'sales', 'category', 'region']
    
    def build_safe_query(self, table, columns, conditions=None):
        """安全なSQLクエリを構築"""
        # テーブル名の検証
        if table not in self.allowed_tables:
            raise ValueError(f"許可されていないテーブル: {table}")
        
        # カラム名の検証
        for col in columns:
            if col not in self.allowed_columns:
                raise ValueError(f"許可されていないカラム: {col}")
        
        # 安全なクエリの構築
        query = f"SELECT {', '.join(columns)} FROM {table}"
        
        if conditions:
            # 条件の検証と追加
            safe_conditions = self._validate_conditions(conditions)
            query += f" WHERE {safe_conditions}"
        
        return query
    
    def _validate_conditions(self, conditions):
        """条件の検証"""
        # 基本的な条件の検証（実際の実装ではより厳密に）
        allowed_operators = ['=', '>', '<', '>=', '<=', 'LIKE']
        
        for condition in conditions:
            if not any(op in condition for op in allowed_operators):
                raise ValueError(f"許可されていない演算子: {condition}")
        
        return ' AND '.join(conditions)

# 使用例
sql_builder = SafeSQLBuilder()
try:
    safe_query = sql_builder.build_safe_query(
        table='sales_data',
        columns=['date', 'sales', 'category'],
        conditions=['category = "Electronics"', 'sales > 1000']
    )
    print(f"安全なクエリ: {safe_query}")
except ValueError as e:
    print(f"エラー: {e}")
```

## 🔐 認証と認可

### 1. ユーザー認証

```python
import hashlib
import secrets
import jwt
from datetime import datetime, timedelta

# 認証システム
class AuthenticationSystem:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.users = {}  # 実際の実装ではデータベースを使用
    
    def hash_password(self, password):
        """パスワードのハッシュ化"""
        salt = secrets.token_hex(16)
        hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return salt + hash_obj.hex()
    
    def verify_password(self, password, hashed_password):
        """パスワードの検証"""
        salt = hashed_password[:32]
        stored_hash = hashed_password[32:]
        hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return hash_obj.hex() == stored_hash
    
    def create_token(self, user_id, role):
        """JWTトークンの作成"""
        payload = {
            'user_id': user_id,
            'role': role,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token):
        """JWTトークンの検証"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

# 使用例
auth_system = AuthenticationSystem('your-secret-key')

# ユーザー登録
password = "secure_password_123"
hashed_password = auth_system.hash_password(password)
auth_system.users['user1'] = {
    'password': hashed_password,
    'role': 'analyst'
}

# ログイン
if auth_system.verify_password(password, hashed_password):
    token = auth_system.create_token('user1', 'analyst')
    print(f"認証トークン: {token}")
    
    # トークンの検証
    payload = auth_system.verify_token(token)
    if payload:
        print(f"認証成功: {payload}")
    else:
        print("認証失敗")
```

### 2. セッション管理

```python
import time
from collections import defaultdict

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

# 使用例
session_manager = SessionManager()

# セッションの作成
session_id = session_manager.create_session('user1', token)

# セッションの検証
if session_manager.validate_session(session_id):
    print("セッション有効")
else:
    print("セッション無効")
```

## 🌐 HTTPSとセキュア通信

### 1. HTTPSの強制

```python
# HTTPS強制の実装
def enforce_https(request):
    """HTTPSを強制"""
    if not request.is_secure():
        # HTTPリクエストをHTTPSにリダイレクト
        secure_url = request.build_absolute_uri().replace('http://', 'https://')
        return redirect(secure_url)
    return None

# セキュリティヘッダーの設定
def set_security_headers(response):
    """セキュリティヘッダーを設定"""
    response['X-Content-Type-Options'] = 'nosniff'
    response['X-Frame-Options'] = 'DENY'
    response['X-XSS-Protection'] = '1; mode=block'
    response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'"
    return response
```

### 2. CORS設定

```python
# CORS設定
def configure_cors(app):
    """CORS設定を構成"""
    from flask_cors import CORS
    
    CORS(app, resources={
        r"/api/*": {
            "origins": ["https://your-domain.com"],
            "methods": ["GET", "POST"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
```

## 📊 ログと監査

### 1. セキュリティログ

```python
import logging
from datetime import datetime

# セキュリティログシステム
class SecurityLogger:
    def __init__(self, log_file='security.log'):
        self.logger = logging.getLogger('security')
        self.logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_access(self, user_id, action, resource, success=True):
        """アクセスログを記録"""
        status = "SUCCESS" if success else "FAILED"
        message = f"ACCESS: User={user_id}, Action={action}, Resource={resource}, Status={status}"
        self.logger.info(message)
    
    def log_security_event(self, event_type, details):
        """セキュリティイベントを記録"""
        message = f"SECURITY_EVENT: Type={event_type}, Details={details}"
        self.logger.warning(message)
    
    def log_data_access(self, user_id, data_type, record_count):
        """データアクセスを記録"""
        message = f"DATA_ACCESS: User={user_id}, DataType={data_type}, Records={record_count}"
        self.logger.info(message)

# 使用例
security_logger = SecurityLogger()

# アクセスログの記録
security_logger.log_access('user1', 'READ', 'sales_data', True)
security_logger.log_data_access('user1', 'customer_data', 1000)
security_logger.log_security_event('UNAUTHORIZED_ACCESS', 'Invalid token provided')
```

### 2. 監査トレイル

```python
# 監査トレイルシステム
class AuditTrail:
    def __init__(self):
        self.audit_events = []
    
    def add_event(self, user_id, action, resource, details=None):
        """監査イベントを追加"""
        event = {
            'timestamp': datetime.utcnow(),
            'user_id': user_id,
            'action': action,
            'resource': resource,
            'details': details,
            'ip_address': self._get_client_ip(),
            'user_agent': self._get_user_agent()
        }
        self.audit_events.append(event)
    
    def get_audit_report(self, user_id=None, start_date=None, end_date=None):
        """監査レポートを取得"""
        filtered_events = self.audit_events
        
        if user_id:
            filtered_events = [e for e in filtered_events if e['user_id'] == user_id]
        
        if start_date:
            filtered_events = [e for e in filtered_events if e['timestamp'] >= start_date]
        
        if end_date:
            filtered_events = [e for e in filtered_events if e['timestamp'] <= end_date]
        
        return filtered_events
    
    def _get_client_ip(self):
        """クライアントIPを取得（実際の実装では適切な方法を使用）"""
        return "192.168.1.1"  # プレースホルダー
    
    def _get_user_agent(self):
        """ユーザーエージェントを取得（実際の実装では適切な方法を使用）"""
        return "Mozilla/5.0"  # プレースホルダー

# 使用例
audit_trail = AuditTrail()

# 監査イベントの記録
audit_trail.add_event('user1', 'CREATE_CHART', 'sales_data', {'chart_type': 'line'})
audit_trail.add_event('user1', 'EXPORT_DATA', 'customer_data', {'format': 'csv'})

# 監査レポートの取得
user_events = audit_trail.get_audit_report(user_id='user1')
for event in user_events:
    print(f"{event['timestamp']}: {event['action']} on {event['resource']}")
```

## 🚀 次のステップ

- [デプロイメント](./deployment.md) - 本番環境へのデプロイ
- [パフォーマンス最適化](./performance.md) - パフォーマンスの最適化
- [トラブルシューティング](../troubleshooting/faq.md) - セキュリティ関連のFAQ

## ❓ サポート

セキュリティで問題が発生した場合は、以下を確認してください：

- [よくある問題](../troubleshooting/faq.md)
- [エラーリファレンス](../troubleshooting/errors.md)
- [GitHub Issues](https://github.com/databricks/db-ui-components/issues)