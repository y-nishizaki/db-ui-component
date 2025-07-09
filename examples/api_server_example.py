"""
API Server Example

HTMLからデータベースにアクセスするためのAPIサーバーの使用例です。
"""

import os
import sys
from db_ui_components.api_server import create_api_server

def run_api_server():
    """
    APIサーバーを起動する例
    """
    print("=== Databricks Database API Server ===")
    
    # 環境変数から認証情報を取得
    workspace_url = os.getenv('DATABRICKS_WORKSPACE_URL')
    token = os.getenv('DATABRICKS_TOKEN')
    
    if not workspace_url or not token:
        print("Error: 環境変数が設定されていません")
        print("以下の環境変数を設定してください:")
        print("export DATABRICKS_WORKSPACE_URL='https://your-workspace.cloud.databricks.com'")
        print("export DATABRICKS_TOKEN='your-access-token'")
        return
    
    print(f"Workspace URL: {workspace_url}")
    print("Token: [設定済み]")
    print("\nAPIサーバーを起動しています...")
    print("ブラウザで http://localhost:5000 にアクセスしてください")
    print("Ctrl+C で停止")
    
    try:
        # APIサーバーを作成して起動
        server = create_api_server(workspace_url, token)
        server.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        print("\nサーバーを停止しました")
    except Exception as e:
        print(f"エラー: {e}")

def create_standalone_html():
    """
    スタンドアロンHTMLファイルを作成する例
    """
    html_content = '''
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Databricks Database Access (Standalone)</title>
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
        .config-section {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .input-group {
            margin-bottom: 15px;
        }
        .input-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        .input-group input {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
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
        .note {
            background-color: #fff3cd;
            color: #856404;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 20px;
            border: 1px solid #ffeaa7;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Databricks Database Access</h1>
            <p>HTMLからDatabricksデータベースにアクセス（スタンドアロン版）</p>
        </div>
        
        <div class="note">
            <strong>注意:</strong> このHTMLファイルを使用するには、APIサーバーが起動している必要があります。
            <br>APIサーバーを起動するには: <code>python -m db_ui_components.api_server</code>
        </div>
        
        <!-- 設定 -->
        <div class="section">
            <h3>API設定</h3>
            <div class="config-section">
                <div class="input-group">
                    <label for="api-url">API URL:</label>
                    <input type="text" id="api-url" value="http://localhost:5000" placeholder="http://localhost:5000">
                </div>
                <button class="btn btn-primary" onclick="testConnection()">接続テスト</button>
            </div>
            <div id="connection-status" class="status disconnected">
                接続状態を確認してください
            </div>
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
            <button class="btn btn-primary" onclick="loadTables()">テーブル一覧を取得</button>
            <div id="tables-list"></div>
        </div>
        
        <!-- テーブル情報 -->
        <div class="section">
            <h3>テーブル情報</h3>
            <div id="table-info"></div>
        </div>
    </div>

    <script>
        // API URLを取得
        function getApiUrl() {
            return document.getElementById('api-url').value.trim();
        }
        
        // 接続テスト
        async function testConnection() {
            const statusDiv = document.getElementById('connection-status');
            statusDiv.className = 'status';
            statusDiv.textContent = '接続状態を確認中...';
            
            try {
                const apiUrl = getApiUrl();
                const response = await fetch(apiUrl + '/api/status');
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
                const apiUrl = getApiUrl();
                const response = await fetch(apiUrl + '/api/query', {
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
                const apiUrl = getApiUrl();
                const response = await fetch(apiUrl + '/api/tables');
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
            
            let html = '<div style="margin-top: 15px;">';
            tables.forEach(table => {
                html += '<button class="btn btn-secondary" style="margin: 5px;" onclick="showTableInfo(\'' + table.table_name + '\')">';
                html += table.table_name + ' (' + table.table_type + ')';
                html += '</button>';
            });
            html += '</div>';
            
            tablesDiv.innerHTML = html;
        }
        
        // テーブル情報を表示
        async function showTableInfo(tableName) {
            const infoDiv = document.getElementById('table-info');
            infoDiv.innerHTML = '<div class="loading">テーブル情報を取得中...</div>';
            
            try {
                const apiUrl = getApiUrl();
                
                // スキーマ情報を取得
                const schemaResponse = await fetch(apiUrl + '/api/schema/' + tableName);
                const schemaData = await schemaResponse.json();
                
                // 統計情報を取得
                const statsResponse = await fetch(apiUrl + '/api/stats/' + tableName);
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
        
        // ページ読み込み時に接続テストを実行
        window.onload = function() {
            testConnection();
        };
    </script>
</body>
</html>
    '''
    
    # HTMLファイルを保存
    with open('databricks_database_access.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("スタンドアロンHTMLファイルを作成しました: databricks_database_access.html")
    print("このファイルをブラウザで開いて使用できます")

def main():
    """メイン関数"""
    if len(sys.argv) > 1 and sys.argv[1] == 'html':
        create_standalone_html()
    else:
        run_api_server()

if __name__ == '__main__':
    main()