"""
Databricks Database Access Component

Databricksノートブック内で直接使用できるデータベースアクセスコンポーネントです。
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Optional, Dict, List, Any, Union
import logging
from .base_component import BaseComponent
from .exceptions import ComponentError

try:
    from pyspark.sql import SparkSession
    from pyspark.sql.types import *
    PYSPARK_AVAILABLE = True
except ImportError:
    PYSPARK_AVAILABLE = False
    logging.warning("PySpark not available. Install with: pip install pyspark")


class DatabricksDatabaseComponent(BaseComponent):
    """
    Databricksノートブック専用データベースアクセスコンポーネント
    
    Databricksノートブック内で直接使用できるデータベース操作を提供します。
    """
    
    def __init__(
        self,
        component_id: str,
        catalog: Optional[str] = None,
        schema: Optional[str] = None,
        **kwargs
    ):
        """
        DatabricksDatabaseComponentの初期化
        
        Args:
            component_id: コンポーネントID
            catalog: カタログ名
            schema: スキーマ名
            **kwargs: その他のパラメータ
        """
        super().__init__(component_id, **kwargs)
        
        self.catalog = catalog
        self.schema = schema
        self.spark_session = None
        
        # デフォルトの設定
        self.default_config = {
            'max_rows': 10000,
            'enable_cache': True,
            'cache_ttl': 300  # 5分
        }
        
        # キャッシュ
        self._query_cache = {}
        self._cache_timestamps = {}
        
        # 初期化
        self._initialize_spark()
    
    def _initialize_spark(self):
        """Sparkセッションの初期化"""
        if not PYSPARK_AVAILABLE:
            raise ComponentError("PySpark is not available")
        
        try:
            # Databricks環境でSparkSessionを取得
            self.spark_session = SparkSession.builder.getOrCreate()
            logging.info("Spark session initialized in Databricks")
            
        except Exception as e:
            logging.error(f"Failed to initialize Spark session: {e}")
            raise ComponentError(f"Spark initialization failed: {e}")
    
    def execute_sql(self, query: str) -> pd.DataFrame:
        """
        SQLクエリを実行
        
        Args:
            query: 実行するSQLクエリ
            
        Returns:
            pandas DataFrame
        """
        if not self.spark_session:
            raise ComponentError("No Spark session available")
        
        try:
            # キャッシュキーの生成
            cache_key = query
            
            # キャッシュチェック
            if self.default_config['enable_cache'] and cache_key in self._query_cache:
                cache_age = pd.Timestamp.now().timestamp() - self._cache_timestamps[cache_key]
                if cache_age < self.default_config['cache_ttl']:
                    logging.info(f"Returning cached result for query: {query[:50]}...")
                    return self._query_cache[cache_key]
            
            # クエリ実行
            spark_df = self.spark_session.sql(query)
            df = spark_df.toPandas()
            
            # 行数制限
            if len(df) > self.default_config['max_rows']:
                df = df.head(self.default_config['max_rows'])
                logging.warning(f"Query result limited to {self.default_config['max_rows']} rows")
            
            # キャッシュに保存
            if self.default_config['enable_cache']:
                self._query_cache[cache_key] = df
                self._cache_timestamps[cache_key] = pd.Timestamp.now().timestamp()
            
            return df
            
        except Exception as e:
            logging.error(f"Query execution failed: {e}")
            raise ComponentError(f"Query execution failed: {e}")
    
    def get_tables(self, catalog: Optional[str] = None, schema: Optional[str] = None) -> pd.DataFrame:
        """
        テーブル一覧を取得
        
        Args:
            catalog: カタログ名
            schema: スキーマ名
            
        Returns:
            テーブル一覧のDataFrame
        """
        catalog = catalog or self.catalog
        schema = schema or self.schema
        
        if catalog and schema:
            query = f"""
            SELECT table_name, table_type, table_comment
            FROM {catalog}.information_schema.tables 
            WHERE table_schema = '{schema}'
            ORDER BY table_name
            """
        else:
            query = """
            SELECT table_catalog, table_schema, table_name, table_type, table_comment
            FROM information_schema.tables 
            ORDER BY table_catalog, table_schema, table_name
            """
        
        return self.execute_sql(query)
    
    def get_table_schema(self, table_name: str, catalog: Optional[str] = None, schema: Optional[str] = None) -> pd.DataFrame:
        """
        テーブルスキーマを取得
        
        Args:
            table_name: テーブル名
            catalog: カタログ名
            schema: スキーマ名
            
        Returns:
            スキーマ情報のDataFrame
        """
        catalog = catalog or self.catalog
        schema = schema or self.schema
        
        if catalog and schema:
            query = f"""
            SELECT column_name, data_type, is_nullable, column_default, column_comment
            FROM {catalog}.information_schema.columns 
            WHERE table_schema = '{schema}' AND table_name = '{table_name}'
            ORDER BY ordinal_position
            """
        else:
            query = f"""
            SELECT column_name, data_type, is_nullable, column_default, column_comment
            FROM information_schema.columns 
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position
            """
        
        return self.execute_sql(query)
    
    def preview_table(self, table_name: str, limit: int = 100, catalog: Optional[str] = None, schema: Optional[str] = None) -> pd.DataFrame:
        """
        テーブルのプレビューを取得
        
        Args:
            table_name: テーブル名
            limit: 取得行数
            catalog: カタログ名
            schema: スキーマ名
            
        Returns:
            プレビューデータのDataFrame
        """
        catalog = catalog or self.catalog
        schema = schema or self.schema
        
        if catalog and schema:
            query = f"SELECT * FROM {catalog}.{schema}.{table_name} LIMIT {limit}"
        else:
            query = f"SELECT * FROM {table_name} LIMIT {limit}"
        
        return self.execute_sql(query)
    
    def get_table_stats(self, table_name: str, catalog: Optional[str] = None, schema: Optional[str] = None) -> Dict[str, Any]:
        """
        テーブル統計情報を取得
        
        Args:
            table_name: テーブル名
            catalog: カタログ名
            schema: スキーマ名
            
        Returns:
            統計情報の辞書
        """
        catalog = catalog or self.catalog
        schema = schema or self.schema
        
        # 行数取得
        if catalog and schema:
            count_query = f"SELECT COUNT(*) as row_count FROM {catalog}.{schema}.{table_name}"
        else:
            count_query = f"SELECT COUNT(*) as row_count FROM {table_name}"
        
        count_df = self.execute_sql(count_query)
        row_count = count_df.iloc[0]['row_count']
        
        # スキーマ情報取得
        schema_df = self.get_table_schema(table_name, catalog, schema)
        
        stats = {
            'table_name': table_name,
            'row_count': row_count,
            'column_count': len(schema_df),
            'columns': schema_df.to_dict('records'),
            'catalog': catalog,
            'schema': schema
        }
        
        return stats
    
    def read_table(self, table_name: str, catalog: Optional[str] = None, schema: Optional[str] = None) -> pd.DataFrame:
        """
        テーブルを読み込み
        
        Args:
            table_name: テーブル名
            catalog: カタログ名
            schema: スキーマ名
            
        Returns:
            pandas DataFrame
        """
        if not self.spark_session:
            raise ComponentError("No Spark session available")
        
        try:
            if catalog and schema:
                full_table_name = f"{catalog}.{schema}.{table_name}"
            else:
                full_table_name = table_name
            
            spark_df = self.spark_session.table(full_table_name)
            return spark_df.toPandas()
            
        except Exception as e:
            logging.error(f"Failed to read table {table_name}: {e}")
            raise ComponentError(f"Table read failed: {e}")
    
    def create_notebook_widget(self) -> str:
        """
        Databricksノートブック用のウィジェットHTMLを生成
        
        Returns:
            HTML文字列
        """
        widget_id = self.component_id.replace('-', '_')
        
        html = f'''
        <div id="{widget_id}_container" style="padding: 20px; border: 1px solid #ddd; border-radius: 8px; margin: 10px 0;">
            <h3>Databricks Database Access: {self.component_id}</h3>
            
            <!-- 接続状態 -->
            <div style="margin-bottom: 20px;">
                <h4>接続状態</h4>
                <div id="{widget_id}_status" style="padding: 10px; background-color: #d4edda; color: #155724; border-radius: 5px;">
                    ✅ Spark session initialized
                </div>
            </div>
            
            <!-- クエリ実行 -->
            <div style="margin-bottom: 20px;">
                <h4>SQLクエリ実行</h4>
                <textarea id="{widget_id}_query" style="width: 100%; height: 100px; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-family: monospace;" placeholder="SQLクエリを入力してください...">SELECT current_timestamp() as current_time</textarea>
                <br><br>
                <button onclick="executeQuery_{widget_id}()" style="padding: 10px 20px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer;">クエリ実行</button>
                <button onclick="clearQuery_{widget_id}()" style="padding: 10px 20px; background-color: #6c757d; color: white; border: none; border-radius: 4px; cursor: pointer; margin-left: 10px;">クリア</button>
            </div>
            
            <!-- テーブル一覧 -->
            <div style="margin-bottom: 20px;">
                <h4>テーブル一覧</h4>
                <button onclick="loadTables_{widget_id}()" style="padding: 10px 20px; background-color: #17a2b8; color: white; border: none; border-radius: 4px; cursor: pointer;">テーブル一覧を取得</button>
                <div id="{widget_id}_tables" style="margin-top: 10px;"></div>
            </div>
            
            <!-- 結果表示 -->
            <div style="margin-bottom: 20px;">
                <h4>クエリ結果</h4>
                <div id="{widget_id}_results" style="padding: 15px; background-color: #f8f9fa; border-radius: 4px; border: 1px solid #dee2e6;"></div>
            </div>
            
            <!-- テーブル情報 -->
            <div style="margin-bottom: 20px;">
                <h4>テーブル情報</h4>
                <div id="{widget_id}_table_info"></div>
            </div>
        </div>
        
        <script>
            // クエリ実行
            async function executeQuery_{widget_id}() {{
                const query = document.getElementById('{widget_id}_query').value.trim();
                if (!query) {{
                    alert('クエリを入力してください');
                    return;
                }}
                
                const resultsDiv = document.getElementById('{widget_id}_results');
                resultsDiv.innerHTML = '<div style="text-align: center; padding: 20px; color: #666;">クエリを実行中...</div>';
                
                try {{
                    // Databricksノートブック内でのクエリ実行
                    const result = await executeSQL_{widget_id}(query);
                    displayResults_{widget_id}(result);
                }} catch (error) {{
                    resultsDiv.innerHTML = '<div style="color: #dc3545; background-color: #f8d7da; padding: 10px; border-radius: 4px;">エラー: ' + error.message + '</div>';
                }}
            }}
            
            // SQL実行（Databricks環境用）
            async function executeSQL_{widget_id}(query) {{
                // ここでDatabricksのSQL実行機能を使用
                // 実際の実装はDatabricks環境に依存
                return new Promise((resolve, reject) => {{
                    // 仮の実装 - 実際はDatabricksのAPIを使用
                    setTimeout(() => {{
                        resolve([{{'current_time': new Date().toISOString()}}]);
                    }}, 1000);
                }});
            }}
            
            // 結果表示
            function displayResults_{widget_id}(data) {{
                const resultsDiv = document.getElementById('{widget_id}_results');
                
                if (!data || data.length === 0) {{
                    resultsDiv.innerHTML = '<div>結果がありません</div>';
                    return;
                }}
                
                let html = '<h5>クエリ結果 (' + data.length + ' 行)</h5>';
                html += '<div style="overflow-x: auto;"><table style="width: 100%; border-collapse: collapse;">';
                
                // ヘッダー
                const columns = Object.keys(data[0]);
                html += '<thead><tr style="background-color: #f8f9fa;">';
                columns.forEach(col => {{
                    html += '<th style="padding: 8px 12px; text-align: left; border-bottom: 1px solid #ddd;">' + col + '</th>';
                }});
                html += '</tr></thead>';
                
                // データ
                html += '<tbody>';
                data.forEach(row => {{
                    html += '<tr>';
                    columns.forEach(col => {{
                        html += '<td style="padding: 8px 12px; text-align: left; border-bottom: 1px solid #ddd;">' + (row[col] || '') + '</td>';
                    }});
                    html += '</tr>';
                }});
                html += '</tbody></table></div>';
                
                resultsDiv.innerHTML = html;
            }}
            
            // クエリをクリア
            function clearQuery_{widget_id}() {{
                document.getElementById('{widget_id}_query').value = '';
                document.getElementById('{widget_id}_results').innerHTML = '';
            }}
            
            // テーブル一覧を取得
            async function loadTables_{widget_id}() {{
                const tablesDiv = document.getElementById('{widget_id}_tables');
                tablesDiv.innerHTML = '<div style="text-align: center; padding: 20px; color: #666;">テーブル一覧を取得中...</div>';
                
                try {{
                    // 実際の実装ではDatabricksのAPIを使用
                    const tables = await getTables_{widget_id}();
                    displayTables_{widget_id}(tables);
                }} catch (error) {{
                    tablesDiv.innerHTML = '<div style="color: #dc3545; background-color: #f8d7da; padding: 10px; border-radius: 4px;">エラー: ' + error.message + '</div>';
                }}
            }}
            
            // テーブル一覧を取得（仮の実装）
            async function getTables_{widget_id}() {{
                return new Promise((resolve) => {{
                    setTimeout(() => {{
                        resolve([
                            {{'table_name': 'sample_table', 'table_type': 'BASE TABLE'}},
                            {{'table_name': 'users', 'table_type': 'BASE TABLE'}},
                            {{'table_name': 'orders', 'table_type': 'BASE TABLE'}}
                        ]);
                    }}, 1000);
                }});
            }}
            
            // テーブル一覧を表示
            function displayTables_{widget_id}(tables) {{
                const tablesDiv = document.getElementById('{widget_id}_tables');
                
                if (!tables || tables.length === 0) {{
                    tablesDiv.innerHTML = '<div>テーブルが見つかりません</div>';
                    return;
                }}
                
                let html = '<div style="margin-top: 10px;">';
                tables.forEach(table => {{
                    html += '<button onclick="showTableInfo_{widget_id}(\\'' + table.table_name + '\\')" style="padding: 8px 16px; background-color: #e9ecef; border: 1px solid #dee2e6; border-radius: 4px; cursor: pointer; margin: 2px;">';
                    html += table.table_name + ' (' + table.table_type + ')';
                    html += '</button>';
                }});
                html += '</div>';
                
                tablesDiv.innerHTML = html;
            }}
            
            // テーブル情報を表示
            async function showTableInfo_{widget_id}(tableName) {{
                const infoDiv = document.getElementById('{widget_id}_table_info');
                infoDiv.innerHTML = '<div style="text-align: center; padding: 20px; color: #666;">テーブル情報を取得中...</div>';
                
                try {{
                    // 実際の実装ではDatabricksのAPIを使用
                    const info = await getTableInfo_{widget_id}(tableName);
                    displayTableInfo_{widget_id}(tableName, info);
                }} catch (error) {{
                    infoDiv.innerHTML = '<div style="color: #dc3545; background-color: #f8d7da; padding: 10px; border-radius: 4px;">エラー: ' + error.message + '</div>';
                }}
            }}
            
            // テーブル情報を取得（仮の実装）
            async function getTableInfo_{widget_id}(tableName) {{
                return new Promise((resolve) => {{
                    setTimeout(() => {{
                        resolve({{
                            row_count: 1000,
                            column_count: 5,
                            columns: [
                                {{'column_name': 'id', 'data_type': 'INT', 'is_nullable': 'NO'}},
                                {{'column_name': 'name', 'data_type': 'VARCHAR(255)', 'is_nullable': 'YES'}},
                                {{'column_name': 'email', 'data_type': 'VARCHAR(255)', 'is_nullable': 'YES'}}
                            ]
                        }});
                    }}, 1000);
                }});
            }}
            
            // テーブル情報を表示
            function displayTableInfo_{widget_id}(tableName, info) {{
                const infoDiv = document.getElementById('{widget_id}_table_info');
                
                let html = '<h5>テーブル: ' + tableName + '</h5>';
                html += '<p><strong>行数:</strong> ' + info.row_count.toLocaleString() + '</p>';
                html += '<p><strong>列数:</strong> ' + info.column_count + '</p>';
                
                html += '<h6>スキーマ:</h6>';
                html += '<div style="overflow-x: auto;"><table style="width: 100%; border-collapse: collapse;">';
                html += '<thead><tr style="background-color: #f8f9fa;"><th style="padding: 8px 12px; text-align: left;">列名</th><th style="padding: 8px 12px; text-align: left;">データ型</th><th style="padding: 8px 12px; text-align: left;">NULL許可</th></tr></thead>';
                html += '<tbody>';
                
                info.columns.forEach(col => {{
                    html += '<tr>';
                    html += '<td style="padding: 8px 12px; text-align: left; border-bottom: 1px solid #ddd;">' + col.column_name + '</td>';
                    html += '<td style="padding: 8px 12px; text-align: left; border-bottom: 1px solid #ddd;">' + col.data_type + '</td>';
                    html += '<td style="padding: 8px 12px; text-align: left; border-bottom: 1px solid #ddd;">' + col.is_nullable + '</td>';
                    html += '</tr>';
                }});
                
                html += '</tbody></table></div>';
                
                infoDiv.innerHTML = html;
            }}
        </script>
        '''
        
        return html
    
    def render(self) -> str:
        """
        コンポーネントをHTMLとしてレンダリング
        
        Returns:
            HTML文字列
        """
        return self.create_notebook_widget()
    
    def display(self):
        """
        Databricksノートブックで表示
        """
        try:
            # Databricks環境での表示
            from IPython.display import HTML
            return HTML(self.render())
        except ImportError:
            # 通常の環境での表示
            return self.render()


def create_databricks_database_component(component_id: str, catalog: Optional[str] = None, schema: Optional[str] = None) -> DatabricksDatabaseComponent:
    """
    Databricksデータベースコンポーネントを作成
    
    Args:
        component_id: コンポーネントID
        catalog: カタログ名
        schema: スキーマ名
        
    Returns:
        DatabricksDatabaseComponentインスタンス
    """
    return DatabricksDatabaseComponent(component_id, catalog, schema)


# 便利な関数
def execute_sql(query: str) -> pd.DataFrame:
    """
    SQLクエリを実行（便利関数）
    
    Args:
        query: SQLクエリ
        
    Returns:
        pandas DataFrame
    """
    db = DatabricksDatabaseComponent("temp-db")
    return db.execute_sql(query)


def get_tables(catalog: Optional[str] = None, schema: Optional[str] = None) -> pd.DataFrame:
    """
    テーブル一覧を取得（便利関数）
    
    Args:
        catalog: カタログ名
        schema: スキーマ名
        
    Returns:
        テーブル一覧のDataFrame
    """
    db = DatabricksDatabaseComponent("temp-db", catalog, schema)
    return db.get_tables()


def preview_table(table_name: str, limit: int = 100, catalog: Optional[str] = None, schema: Optional[str] = None) -> pd.DataFrame:
    """
    テーブルプレビューを取得（便利関数）
    
    Args:
        table_name: テーブル名
        limit: 取得行数
        catalog: カタログ名
        schema: スキーマ名
        
    Returns:
        プレビューデータのDataFrame
    """
    db = DatabricksDatabaseComponent("temp-db", catalog, schema)
    return db.preview_table(table_name, limit)