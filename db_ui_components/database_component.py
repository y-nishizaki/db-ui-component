"""
Databricks Database Access Component

Databricksへの接続とデータベース操作を提供するコンポーネントです。
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import html, dcc, Input, Output, State, callback_context, dash_table
import dash
from typing import Optional, Dict, List, Any, Union
import logging
from .base_component import BaseComponent
from .exceptions import ComponentError

try:
    from databricks import sql
    from databricks.sdk import WorkspaceClient
    from databricks.sdk.core import Config
    DATABRICKS_AVAILABLE = True
except ImportError:
    DATABRICKS_AVAILABLE = False
    logging.warning("Databricks SDK not available. Install with: pip install databricks-sdk")

try:
    from pyspark.sql import SparkSession
    from pyspark.sql.types import *
    PYSPARK_AVAILABLE = True
except ImportError:
    PYSPARK_AVAILABLE = False
    logging.warning("PySpark not available. Install with: pip install pyspark")


class DatabaseComponent(BaseComponent):
    """
    Databricksデータベースアクセスコンポーネント
    
    Databricksへの接続とデータベース操作を提供します。
    """
    
    def __init__(
        self,
        component_id: str,
        workspace_url: Optional[str] = None,
        token: Optional[str] = None,
        catalog: Optional[str] = None,
        schema: Optional[str] = None,
        **kwargs
    ):
        """
        DatabaseComponentの初期化
        
        Args:
            component_id: コンポーネントID
            workspace_url: DatabricksワークスペースURL
            token: Databricksアクセストークン
            catalog: カタログ名
            schema: スキーマ名
            **kwargs: その他のパラメータ
        """
        super().__init__(component_id, **kwargs)
        
        self.workspace_url = workspace_url
        self.token = token
        self.catalog = catalog
        self.schema = schema
        self.connection = None
        self.workspace_client = None
        
        # デフォルトの設定
        self.default_config = {
            'connection_timeout': 30,
            'query_timeout': 300,
            'max_rows': 10000,
            'enable_cache': True,
            'cache_ttl': 300  # 5分
        }
        
        # キャッシュ
        self._query_cache = {}
        self._cache_timestamps = {}
        
        # 初期化
        self._initialize_connection()
    
    def _initialize_connection(self):
        """Databricks接続の初期化"""
        if not DATABRICKS_AVAILABLE:
            raise ComponentError("Databricks SDK is not available")
        
        try:
            # ワークスペースクライアントの初期化
            if self.workspace_url and self.token:
                config = Config(
                    host=self.workspace_url,
                    token=self.token
                )
                self.workspace_client = WorkspaceClient(config=config)
                
                # SQL接続の初期化
                self.connection = sql.connect(
                    server_hostname=self.workspace_url.replace('https://', ''),
                    http_path="/sql/1.0/warehouses/your-warehouse-id",  # 実際のウェアハウスIDに変更
                    access_token=self.token
                )
                
                logging.info(f"Databricks connection established to {self.workspace_url}")
            else:
                logging.warning("Databricks credentials not provided. Using default connection.")
                
        except Exception as e:
            logging.error(f"Failed to initialize Databricks connection: {e}")
            raise ComponentError(f"Connection initialization failed: {e}")
    
    def execute_query(self, query: str, params: Optional[Dict] = None) -> pd.DataFrame:
        """
        SQLクエリを実行
        
        Args:
            query: 実行するSQLクエリ
            params: クエリパラメータ
            
        Returns:
            pandas DataFrame
        """
        if not self.connection:
            raise ComponentError("No database connection available")
        
        try:
            # キャッシュキーの生成
            cache_key = f"{query}_{str(params)}"
            
            # キャッシュチェック
            if self.default_config['enable_cache'] and cache_key in self._query_cache:
                cache_age = pd.Timestamp.now().timestamp() - self._cache_timestamps[cache_key]
                if cache_age < self.default_config['cache_ttl']:
                    logging.info(f"Returning cached result for query: {query[:50]}...")
                    return self._query_cache[cache_key]
            
            # クエリ実行
            with self.connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                # 結果の取得
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                
                df = pd.DataFrame(results, columns=columns)
                
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
        
        return self.execute_query(query)
    
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
        
        return self.execute_query(query)
    
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
        
        return self.execute_query(query)
    
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
        
        count_df = self.execute_query(count_query)
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
    
    def render(self) -> str:
        """
        コンポーネントをHTMLとしてレンダリング
        
        Returns:
            HTML文字列
        """
        layout = self.create_layout()
        return str(layout)
    
    def create_layout(self) -> html.Div:
        """
        コンポーネントのレイアウトを作成
        
        Returns:
            Dash HTMLコンポーネント
        """
        return html.Div([
            html.H3(f"Database Component: {self.component_id}"),
            
            # 接続状態
            html.Div([
                html.H4("Connection Status"),
                html.Div(id=f"{self.component_id}-connection-status", className="status-indicator"),
            ]),
            
            # クエリ実行セクション
            html.Div([
                html.H4("Query Execution"),
                dcc.Textarea(
                    id=f"{self.component_id}-query-input",
                    placeholder="Enter SQL query here...",
                    style={'width': '100%', 'height': '100px'}
                ),
                html.Button(
                    "Execute Query",
                    id=f"{self.component_id}-execute-btn",
                    className="btn btn-primary"
                ),
                html.Button(
                    "Clear",
                    id=f"{self.component_id}-clear-btn",
                    className="btn btn-secondary"
                ),
            ]),
            
            # テーブル一覧セクション
            html.Div([
                html.H4("Tables"),
                html.Button(
                    "Refresh Tables",
                    id=f"{self.component_id}-refresh-tables-btn",
                    className="btn btn-info"
                ),
                html.Div(id=f"{self.component_id}-tables-list"),
            ]),
            
            # 結果表示セクション
            html.Div([
                html.H4("Query Results"),
                html.Div(id=f"{self.component_id}-query-results"),
                html.Div(id=f"{self.component_id}-query-error"),
            ]),
            
            # 統計情報セクション
            html.Div([
                html.H4("Table Statistics"),
                html.Div(id=f"{self.component_id}-table-stats"),
            ]),
            
            # スタイル
            html.Style("""
                .status-indicator {
                    padding: 10px;
                    margin: 10px 0;
                    border-radius: 5px;
                }
                .status-connected {
                    background-color: #d4edda;
                    color: #155724;
                    border: 1px solid #c3e6cb;
                }
                .status-disconnected {
                    background-color: #f8d7da;
                    color: #721c24;
                    border: 1px solid #f5c6cb;
                }
            """)
        ])
    
    def register_callbacks(self, app):
        """
        コールバック関数を登録
        
        Args:
            app: Dashアプリケーション
        """
        @app.callback(
            Output(f"{self.component_id}-connection-status", "children"),
            Output(f"{self.component_id}-connection-status", "className"),
            Input(f"{self.component_id}-execute-btn", "n_clicks"),
            Input(f"{self.component_id}-refresh-tables-btn", "n_clicks")
        )
        def update_connection_status(execute_clicks, refresh_clicks):
            if self.connection:
                return "Connected to Databricks", "status-indicator status-connected"
            else:
                return "Not connected to Databricks", "status-indicator status-disconnected"
        
        @app.callback(
            Output(f"{self.component_id}-query-results", "children"),
            Output(f"{self.component_id}-query-error", "children"),
            Input(f"{self.component_id}-execute-btn", "n_clicks"),
            State(f"{self.component_id}-query-input", "value")
        )
        def execute_query(execute_clicks, query_text):
            if not execute_clicks or not query_text:
                return "", ""
            
            try:
                df = self.execute_query(query_text)
                
                # 結果をテーブルとして表示
                table = html.Div([
                    html.H5(f"Results ({len(df)} rows)"),
                    dash_table.DataTable(
                        data=df.to_dict('records'),
                        columns=[{"name": i, "id": i} for i in df.columns],
                        page_size=10,
                        style_table={'overflowX': 'auto'},
                        style_cell={'textAlign': 'left', 'padding': '10px'},
                        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
                    )
                ])
                
                return table, ""
                
            except Exception as e:
                return "", html.Div(f"Error: {str(e)}", style={'color': 'red'})
        
        @app.callback(
            Output(f"{self.component_id}-tables-list", "children"),
            Input(f"{self.component_id}-refresh-tables-btn", "n_clicks")
        )
        def refresh_tables(refresh_clicks):
            if not refresh_clicks:
                return ""
            
            try:
                tables_df = self.get_tables()
                
                if len(tables_df) == 0:
                    return html.Div("No tables found")
                
                # テーブル一覧を表示
                table_list = []
                for _, row in tables_df.iterrows():
                    table_name = row.get('table_name', 'Unknown')
                    table_type = row.get('table_type', 'Unknown')
                    
                    table_item = html.Div([
                        html.Button(
                            f"{table_name} ({table_type})",
                            id=f"{self.component_id}-table-{table_name}",
                            className="btn btn-outline-primary btn-sm",
                            style={'margin': '2px'}
                        )
                    ])
                    table_list.append(table_item)
                
                return html.Div(table_list)
                
            except Exception as e:
                return html.Div(f"Error loading tables: {str(e)}", style={'color': 'red'})
        
        @app.callback(
            Output(f"{self.component_id}-table-stats", "children"),
            [Input(f"{self.component_id}-table-{i}", "n_clicks") for i in range(100)]  # 最大100テーブル
        )
        def show_table_stats(*table_clicks):
            ctx = callback_context
            if not ctx.triggered:
                return ""
            
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            table_name = button_id.replace(f"{self.component_id}-table-", "")
            
            try:
                stats = self.get_table_stats(table_name)
                
                stats_display = html.Div([
                    html.H5(f"Statistics for {table_name}"),
                    html.P(f"Rows: {stats['row_count']:,}"),
                    html.P(f"Columns: {stats['column_count']}"),
                    html.H6("Columns:"),
                    html.Ul([
                        html.Li(f"{col['column_name']} ({col['data_type']})")
                        for col in stats['columns']
                    ])
                ])
                
                return stats_display
                
            except Exception as e:
                return html.Div(f"Error loading table stats: {str(e)}", style={'color': 'red'})
        
        @app.callback(
            Output(f"{self.component_id}-query-input", "value"),
            Input(f"{self.component_id}-clear-btn", "n_clicks")
        )
        def clear_query(clear_clicks):
            if clear_clicks:
                return ""
            return dash.no_update
    
    def close_connection(self):
        """データベース接続を閉じる"""
        if self.connection:
            self.connection.close()
            logging.info("Database connection closed")
    
    def __del__(self):
        """デストラクタで接続を閉じる"""
        self.close_connection()


class SparkComponent(BaseComponent):
    """
    PySparkを使用したDatabricks接続コンポーネント
    """
    
    def __init__(
        self,
        component_id: str,
        spark_config: Optional[Dict] = None,
        **kwargs
    ):
        """
        SparkComponentの初期化
        
        Args:
            component_id: コンポーネントID
            spark_config: Spark設定
            **kwargs: その他のパラメータ
        """
        super().__init__(component_id, **kwargs)
        
        if not PYSPARK_AVAILABLE:
            raise ComponentError("PySpark is not available")
        
        self.spark_config = spark_config or {}
        self.spark_session = None
        
        self._initialize_spark()
    
    def _initialize_spark(self):
        """Sparkセッションの初期化"""
        try:
            builder = SparkSession.builder
            
            # 設定の適用
            for key, value in self.spark_config.items():
                builder = builder.config(key, value)
            
            self.spark_session = builder.getOrCreate()
            logging.info("Spark session initialized")
            
        except Exception as e:
            logging.error(f"Failed to initialize Spark session: {e}")
            raise ComponentError(f"Spark initialization failed: {e}")
    
    def read_table(self, table_name: str, catalog: Optional[str] = None, schema: Optional[str] = None):
        """
        テーブルを読み込み
        
        Args:
            table_name: テーブル名
            catalog: カタログ名
            schema: スキーマ名
            
        Returns:
            Spark DataFrame
        """
        if not self.spark_session:
            raise ComponentError("No Spark session available")
        
        try:
            if catalog and schema:
                full_table_name = f"{catalog}.{schema}.{table_name}"
            else:
                full_table_name = table_name
            
            return self.spark_session.table(full_table_name)
            
        except Exception as e:
            logging.error(f"Failed to read table {table_name}: {e}")
            raise ComponentError(f"Table read failed: {e}")
    
    def execute_sql(self, query: str) -> pd.DataFrame:
        """
        SQLクエリを実行
        
        Args:
            query: SQLクエリ
            
        Returns:
            pandas DataFrame
        """
        if not self.spark_session:
            raise ComponentError("No Spark session available")
        
        try:
            spark_df = self.spark_session.sql(query)
            return spark_df.toPandas()
            
        except Exception as e:
            logging.error(f"SQL execution failed: {e}")
            raise ComponentError(f"SQL execution failed: {e}")
    
    def get_table_info(self, table_name: str, catalog: Optional[str] = None, schema: Optional[str] = None) -> Dict[str, Any]:
        """
        テーブル情報を取得
        
        Args:
            table_name: テーブル名
            catalog: カタログ名
            schema: スキーマ名
            
        Returns:
            テーブル情報の辞書
        """
        try:
            spark_df = self.read_table(table_name, catalog, schema)
            
            info = {
                'table_name': table_name,
                'row_count': spark_df.count(),
                'column_count': len(spark_df.columns),
                'columns': spark_df.columns,
                'schema': spark_df.schema.json()
            }
            
            return info
            
        except Exception as e:
            logging.error(f"Failed to get table info: {e}")
            raise ComponentError(f"Table info retrieval failed: {e}")
    
    def render(self) -> str:
        """
        コンポーネントをHTMLとしてレンダリング
        
        Returns:
            HTML文字列
        """
        layout = self.create_layout()
        return str(layout)
    
    def create_layout(self) -> html.Div:
        """Sparkコンポーネントのレイアウトを作成"""
        return html.Div([
            html.H3(f"Spark Component: {self.component_id}"),
            html.Div([
                html.H4("Spark Session Status"),
                html.Div(
                    "Spark session initialized" if self.spark_session else "No Spark session",
                    className="status-indicator status-connected" if self.spark_session else "status-indicator status-disconnected"
                ),
            ]),
            html.Div([
                html.H4("Spark Operations"),
                html.Button(
                    "Get Session Info",
                    id=f"{self.component_id}-session-info-btn",
                    className="btn btn-info"
                ),
                html.Div(id=f"{self.component_id}-session-info"),
            ])
        ])
    
    def register_callbacks(self, app):
        """Sparkコンポーネントのコールバックを登録"""
        @app.callback(
            Output(f"{self.component_id}-session-info", "children"),
            Input(f"{self.component_id}-session-info-btn", "n_clicks")
        )
        def get_session_info(n_clicks):
            if not n_clicks:
                return ""
            
            if not self.spark_session:
                return html.Div("No Spark session available", style={'color': 'red'})
            
            try:
                version = self.spark_session.version
                conf = self.spark_session.conf.get("spark.sql.warehouse.dir", "Not set")
                
                return html.Div([
                    html.H5("Spark Session Information"),
                    html.P(f"Spark Version: {version}"),
                    html.P(f"Warehouse Directory: {conf}"),
                ])
                
            except Exception as e:
                return html.Div(f"Error getting session info: {str(e)}", style={'color': 'red'})
    
    def stop_session(self):
        """Sparkセッションを停止"""
        if self.spark_session:
            self.spark_session.stop()
            logging.info("Spark session stopped")
    
    def __del__(self):
        """デストラクタでセッションを停止"""
        self.stop_session()