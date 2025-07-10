"""
Database API Server

HTMLからデータベースにアクセスするためのAPIサーバーです。
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import pandas as pd
import os
import logging
from typing import Dict, Any, Optional
from .database_component import DatabaseComponent, SparkComponent

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseAPIServer:
    """
    データベースアクセス用APIサーバー
    
    HTMLからデータベースにアクセスするためのRESTful APIを提供します。
    """
    
    def __init__(self, workspace_url: Optional[str] = None, token: Optional[str] = None):
        """
        初期化
        
        Args:
            workspace_url: DatabricksワークスペースURL
            token: Databricksアクセストークン
        """
        self.app = Flask(__name__)
        CORS(self.app)  # CORSを有効化
        
        # データベースコンポーネントの初期化
        self.db_component = None
        self.spark_component = None
        
        if workspace_url and token:
            try:
                self.db_component = DatabaseComponent(
                    component_id="api-db",
                    workspace_url=workspace_url,
                    token=token
                )
                logger.info("Database component initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize database component: {e}")
        
        # APIルートの設定
        self._setup_routes()
    
    def _setup_routes(self):
        """APIルートを設定"""
        
        @self.app.route('/')
        def index():
            """メインページ"""
            return self._get_html_template()
        
        @self.app.route('/api/tables', methods=['GET'])
        def get_tables():
            """テーブル一覧を取得"""
            try:
                if not self.db_component:
                    return jsonify({'error': 'Database component not initialized'}), 500
                
                catalog = request.args.get('catalog')
                schema = request.args.get('schema')
                
                tables = self.db_component.get_tables(catalog, schema)
                return jsonify({
                    'success': True,
                    'data': tables.to_dict('records')
                })
            except Exception as e:
                logger.error(f"Error getting tables: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/query', methods=['POST'])
        def execute_query():
            """SQLクエリを実行"""
            try:
                if not self.db_component:
                    return jsonify({'error': 'Database component not initialized'}), 500
                
                data = request.get_json()
                query = data.get('query')
                params = data.get('params')
                
                if not query:
                    return jsonify({'error': 'Query is required'}), 400
                
                result = self.db_component.execute_query(query, params)
                return jsonify({
                    'success': True,
                    'data': result.to_dict('records'),
                    'columns': list(result.columns)
                })
            except Exception as e:
                logger.error(f"Error executing query: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/schema/<table_name>', methods=['GET'])
        def get_table_schema(table_name):
            """テーブルスキーマを取得"""
            try:
                if not self.db_component:
                    return jsonify({'error': 'Database component not initialized'}), 500
                
                catalog = request.args.get('catalog')
                schema = request.args.get('schema')
                
                schema_info = self.db_component.get_table_schema(table_name, catalog, schema)
                return jsonify({
                    'success': True,
                    'data': schema_info.to_dict('records')
                })
            except Exception as e:
                logger.error(f"Error getting schema: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/stats/<table_name>', methods=['GET'])
        def get_table_stats(table_name):
            """テーブル統計情報を取得"""
            try:
                if not self.db_component:
                    return jsonify({'error': 'Database component not initialized'}), 500
                
                catalog = request.args.get('catalog')
                schema = request.args.get('schema')
                
                stats = self.db_component.get_table_stats(table_name, catalog, schema)
                return jsonify({
                    'success': True,
                    'data': stats
                })
            except Exception as e:
                logger.error(f"Error getting stats: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/preview/<table_name>', methods=['GET'])
        def preview_table(table_name):
            """テーブルプレビューを取得"""
            try:
                if not self.db_component:
                    return jsonify({'error': 'Database component not initialized'}), 500
                
                limit = request.args.get('limit', 100, type=int)
                catalog = request.args.get('catalog')
                schema = request.args.get('schema')
                
                preview = self.db_component.preview_table(table_name, limit, catalog, schema)
                return jsonify({
                    'success': True,
                    'data': preview.to_dict('records'),
                    'columns': list(preview.columns)
                })
            except Exception as e:
                logger.error(f"Error getting preview: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/status', methods=['GET'])
        def get_status():
            """接続状態を取得"""
            try:
                if not self.db_component:
                    return jsonify({
                        'connected': False,
                        'message': 'Database component not initialized'
                    })
                
                # 簡単なテストクエリを実行
                test_result = self.db_component.execute_query("SELECT 1 as test")
                
                return jsonify({
                    'connected': True,
                    'message': 'Connected to Databricks',
                    'test_result': test_result.to_dict('records')
                })
            except Exception as e:
                return jsonify({
                    'connected': False,
                    'message': f'Connection failed: {str(e)}'
                })
    
    def _get_html_template(self):
        """HTMLテンプレートを取得"""
        return render_template_string('''
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Databricks Database Access</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #007bff;
        }
        .section {
            margin-bottom: 30px;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .section h3 {
            margin-top: 0;
            color: #333;
        }
        .status {
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .status.connected {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .status.disconnected {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .query-section {
            margin-bottom: 20px;
        }
        .query-input {
            width: 100%;
            height: 100px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-family: monospace;
            resize: vertical;
        }
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            margin-right: 10px;
        }
        .btn-primary {
            background-color: #007bff;
            color: white;
        }
        .btn-secondary {
            background-color: #6c757d;
            color: white;
        }
        .btn-info {
            background-color: #17a2b8;
            color: white;
        }
        .results {
            margin-top: 20px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 4px;
            border: 1px solid #dee2e6;
        }
        .table-container {
            overflow-x: auto;
            margin-top: 15px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        th, td {
            padding: 8px 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f8f9fa;
            font-weight: bold;
        }
        .error {
            color: #dc3545;
            background-color: #f8d7da;
            padding: 10px;
            border-radius: 4px;
            margin-top: 10px;
        }
        .loading {
            text-align: center;
            padding: 20px;
            color: #666;
        }
        .tables-list {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 15px;
        }
        .table-btn {
            padding: 8px 16px;
            background-color: #e9ecef;
            border: 1px solid #dee2e6;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
        }
        .table-btn:hover {
            background-color: #007bff;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Databricks Database Access</h1>
            <p>HTMLからDatabricksデータベースにアクセス</p>
        </div>
        
        <!-- 接続状態 -->
        <div class="section">
            <h3>接続状態</h3>
            <div id="connection-status" class="status disconnected">
                接続状態を確認中...
            </div>
            <button class="btn btn-info" onclick="checkStatus()">状態を確認</button>
        </div>
        
        <!-- クエリ実行 -->
        <div class="section">
            <h3>SQLクエリ実行</h3>
            <div class="query-section">
                <textarea id="query-input" class="query-input" placeholder="SQLクエリを入力してください...">SELECT current_timestamp() as current_time</textarea>
                <br><br>
                <button class="btn btn-primary" onclick="executeQuery()">クエリ実行</button>
                <button class="btn btn-secondary" onclick="clearQuery()">クリア</button>
            </div>
            <div id="query-results" class="results" style="display: none;"></div>
        </div>
        
        <!-- テーブル一覧 -->
        <div class="section">
            <h3>テーブル一覧</h3>
            <button class="btn btn-info" onclick="loadTables()">テーブル一覧を取得</button>
            <div id="tables-list" class="tables-list"></div>
        </div>
        
        <!-- テーブル情報 -->
        <div class="section">
            <h3>テーブル情報</h3>
            <div id="table-info"></div>
        </div>
    </div>

    <script>
        // 接続状態を確認
        async function checkStatus() {
            const statusDiv = document.getElementById('connection-status');
            statusDiv.className = 'status';
            statusDiv.textContent = '接続状態を確認中...';
            
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                
                if (data.connected) {
                    statusDiv.className = 'status connected';
                    statusDiv.textContent = '✅ ' + data.message;
                } else {
                    statusDiv.className = 'status disconnected';
                    statusDiv.textContent = '❌ ' + data.message;
                }
            } catch (error) {
                statusDiv.className = 'status disconnected';
                statusDiv.textContent = '❌ 接続エラー: ' + error.message;
            }
        }
        
        // SQLクエリを実行
        async function executeQuery() {
            const queryInput = document.getElementById('query-input');
            const resultsDiv = document.getElementById('query-results');
            
            const query = queryInput.value.trim();
            if (!query) {
                alert('クエリを入力してください');
                return;
            }
            
            resultsDiv.innerHTML = '<div class="loading">クエリを実行中...</div>';
            resultsDiv.style.display = 'block';
            
            try {
                const response = await fetch('/api/query', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: query })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    displayResults(data.data, data.columns);
                } else {
                    resultsDiv.innerHTML = '<div class="error">エラー: ' + data.error + '</div>';
                }
            } catch (error) {
                resultsDiv.innerHTML = '<div class="error">エラー: ' + error.message + '</div>';
            }
        }
        
        // 結果を表示
        function displayResults(data, columns) {
            const resultsDiv = document.getElementById('query-results');
            
            if (!data || data.length === 0) {
                resultsDiv.innerHTML = '<div>結果がありません</div>';
                return;
            }
            
            let html = '<h4>クエリ結果 (' + data.length + ' 行)</h4>';
            html += '<div class="table-container"><table>';
            
            // ヘッダー
            html += '<thead><tr>';
            columns.forEach(col => {
                html += '<th>' + col + '</th>';
            });
            html += '</tr></thead>';
            
            // データ
            html += '<tbody>';
            data.forEach(row => {
                html += '<tr>';
                columns.forEach(col => {
                    html += '<td>' + (row[col] || '') + '</td>';
                });
                html += '</tr>';
            });
            html += '</tbody></table></div>';
            
            resultsDiv.innerHTML = html;
        }
        
        // クエリをクリア
        function clearQuery() {
            document.getElementById('query-input').value = '';
            document.getElementById('query-results').style.display = 'none';
        }
        
        // テーブル一覧を取得
        async function loadTables() {
            const tablesDiv = document.getElementById('tables-list');
            tablesDiv.innerHTML = '<div class="loading">テーブル一覧を取得中...</div>';
            
            try {
                const response = await fetch('/api/tables');
                const data = await response.json();
                
                if (data.success) {
                    displayTables(data.data);
                } else {
                    tablesDiv.innerHTML = '<div class="error">エラー: ' + data.error + '</div>';
                }
            } catch (error) {
                tablesDiv.innerHTML = '<div class="error">エラー: ' + error.message + '</div>';
            }
        }
        
        // テーブル一覧を表示
        function displayTables(tables) {
            const tablesDiv = document.getElementById('tables-list');
            
            if (!tables || tables.length === 0) {
                tablesDiv.innerHTML = '<div>テーブルが見つかりません</div>';
                return;
            }
            
            let html = '';
            tables.forEach(table => {
                html += '<button class="table-btn" onclick="showTableInfo(\'' + table.table_name + '\')">';
                html += table.table_name + ' (' + table.table_type + ')';
                html += '</button>';
            });
            
            tablesDiv.innerHTML = html;
        }
        
        // テーブル情報を表示
        async function showTableInfo(tableName) {
            const infoDiv = document.getElementById('table-info');
            infoDiv.innerHTML = '<div class="loading">テーブル情報を取得中...</div>';
            
            try {
                // スキーマ情報を取得
                const schemaResponse = await fetch('/api/schema/' + tableName);
                const schemaData = await schemaResponse.json();
                
                // 統計情報を取得
                const statsResponse = await fetch('/api/stats/' + tableName);
                const statsData = await statsResponse.json();
                
                let html = '<h4>テーブル: ' + tableName + '</h4>';
                
                if (schemaData.success && statsData.success) {
                    const stats = statsData.data;
                    html += '<p><strong>行数:</strong> ' + stats.row_count.toLocaleString() + '</p>';
                    html += '<p><strong>列数:</strong> ' + stats.column_count + '</p>';
                    
                    html += '<h5>スキーマ:</h5>';
                    html += '<div class="table-container"><table>';
                    html += '<thead><tr><th>列名</th><th>データ型</th><th>NULL許可</th><th>コメント</th></tr></thead>';
                    html += '<tbody>';
                    
                    schemaData.data.forEach(col => {
                        html += '<tr>';
                        html += '<td>' + col.column_name + '</td>';
                        html += '<td>' + col.data_type + '</td>';
                        html += '<td>' + col.is_nullable + '</td>';
                        html += '<td>' + (col.column_comment || '') + '</td>';
                        html += '</tr>';
                    });
                    
                    html += '</tbody></table></div>';
                } else {
                    html += '<div class="error">テーブル情報の取得に失敗しました</div>';
                }
                
                infoDiv.innerHTML = html;
            } catch (error) {
                infoDiv.innerHTML = '<div class="error">エラー: ' + error.message + '</div>';
            }
        }
        
        // ページ読み込み時に接続状態を確認
        window.onload = function() {
            checkStatus();
        };
    </script>
</body>
</html>
        ''')
    
    def run(self, host: str = '0.0.0.0', port: int = 5000, debug: bool = False):
        """
        APIサーバーを起動
        
        Args:
            host: ホストアドレス
            port: ポート番号
            debug: デバッグモード
        """
        logger.info(f"Starting API server on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)


def create_api_server(workspace_url: Optional[str] = None, token: Optional[str] = None) -> DatabaseAPIServer:
    """
    APIサーバーを作成
    
    Args:
        workspace_url: DatabricksワークスペースURL
        token: Databricksアクセストークン
        
    Returns:
        DatabaseAPIServerインスタンス
    """
    # 環境変数から認証情報を取得（指定されていない場合）
    if not workspace_url:
        workspace_url = os.getenv('DATABRICKS_WORKSPACE_URL')
    if not token:
        token = os.getenv('DATABRICKS_TOKEN')
    
    return DatabaseAPIServer(workspace_url, token)


if __name__ == '__main__':
    # 環境変数から認証情報を取得
    workspace_url = os.getenv('DATABRICKS_WORKSPACE_URL')
    token = os.getenv('DATABRICKS_TOKEN')
    
    if not workspace_url or not token:
        print("Error: DATABRICKS_WORKSPACE_URL and DATABRICKS_TOKEN environment variables are required")
        print("Example:")
        print("export DATABRICKS_WORKSPACE_URL='https://your-workspace.cloud.databricks.com'")
        print("export DATABRICKS_TOKEN='your-access-token'")
        exit(1)
    
    # APIサーバーを作成して起動
    server = create_api_server(workspace_url, token)
    server.run(debug=True)