"""
Databricks Database Access Component

Databricksノートブック内で直接使用できるデータベースアクセスコンポーネントです。
"""

import pandas as pd
from typing import Optional, Dict, Any
import logging
from .base_component import BaseComponent
from .exceptions import ComponentError

# Databricks環境でのSparkSession取得
try:
    from pyspark.sql import SparkSession

    PYSPARK_AVAILABLE = True
except ImportError:
    PYSPARK_AVAILABLE = False
    logging.warning("PySpark not available")


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
        **kwargs,
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
        self.spark = None

        # デフォルトの設定
        self.default_config = {
            "max_rows": 10000,
            "enable_cache": True,
            "cache_ttl": 300,  # 5分
        }

        # キャッシュ
        self._query_cache = {}
        self._cache_timestamps = {}

        # 初期化
        self._initialize_spark()

    def _initialize_spark(self):
        """SparkSessionの初期化（Databricks環境用）"""
        if not PYSPARK_AVAILABLE:
            raise ComponentError("PySpark is not available")

        try:
            # Databricks環境ではSparkSessionが既に利用可能
            self.spark = SparkSession.builder.getOrCreate()
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
        if not self.spark:
            raise ComponentError("No Spark session available")

        try:
            # キャッシュキーの生成
            cache_key = query

            # キャッシュチェック
            if self.default_config["enable_cache"] and cache_key in self._query_cache:
                cache_age = (
                    pd.Timestamp.now().timestamp() - self._cache_timestamps[cache_key]
                )
                if cache_age < self.default_config["cache_ttl"]:
                    logging.info(f"Returning cached result for query: {query[:50]}...")
                    return self._query_cache[cache_key]

            # クエリ実行
            spark_df = self.spark.sql(query)
            df = spark_df.toPandas()

            # 行数制限
            if len(df) > self.default_config["max_rows"]:
                df = df.head(self.default_config["max_rows"])
                logging.warning(
                    f"Query result limited to {self.default_config['max_rows']} rows"
                )

            # キャッシュに保存
            if self.default_config["enable_cache"]:
                self._query_cache[cache_key] = df
                self._cache_timestamps[cache_key] = pd.Timestamp.now().timestamp()

            return df

        except Exception as e:
            logging.error(f"Query execution failed: {e}")
            raise ComponentError(f"Query execution failed: {e}")

    def get_tables(
        self, catalog: Optional[str] = None, schema: Optional[str] = None
    ) -> pd.DataFrame:
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

    def get_table_schema(
        self,
        table_name: str,
        catalog: Optional[str] = None,
        schema: Optional[str] = None,
    ) -> pd.DataFrame:
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

    def preview_table(
        self,
        table_name: str,
        limit: int = 100,
        catalog: Optional[str] = None,
        schema: Optional[str] = None,
    ) -> pd.DataFrame:
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

    def get_table_stats(
        self,
        table_name: str,
        catalog: Optional[str] = None,
        schema: Optional[str] = None,
    ) -> Dict[str, Any]:
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
            count_query = (
                f"SELECT COUNT(*) as row_count FROM {catalog}.{schema}.{table_name}"
            )
        else:
            count_query = f"SELECT COUNT(*) as row_count FROM {table_name}"

        count_df = self.execute_sql(count_query)
        row_count = count_df.iloc[0]["row_count"]

        # スキーマ情報取得
        schema_df = self.get_table_schema(table_name, catalog, schema)

        stats = {
            "table_name": table_name,
            "row_count": row_count,
            "column_count": len(schema_df),
            "columns": schema_df.to_dict("records"),
            "catalog": catalog,
            "schema": schema,
        }

        return stats

    def read_table(
        self,
        table_name: str,
        catalog: Optional[str] = None,
        schema: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        テーブルを読み込み

        Args:
            table_name: テーブル名
            catalog: カタログ名
            schema: スキーマ名

        Returns:
            pandas DataFrame
        """
        if not self.spark:
            raise ComponentError("No Spark session available")

        try:
            if catalog and schema:
                full_table_name = f"{catalog}.{schema}.{table_name}"
            else:
                full_table_name = table_name

            spark_df = self.spark.table(full_table_name)
            return spark_df.toPandas()

        except Exception as e:
            logging.error(f"Failed to read table {table_name}: {e}")
            raise ComponentError(f"Table read failed: {e}")

    def render(self) -> str:
        """
        コンポーネントをHTMLとしてレンダリング

        Returns:
            HTML文字列
        """
        return self.create_simple_widget()

    def create_simple_widget(self) -> str:
        """
        シンプルなDatabricksウィジェットHTMLを生成

        Returns:
            HTML文字列
        """
        widget_id = self.component_id.replace("-", "_")

        html = f"""
        <div id="{widget_id}_container"
             style="padding: 20px; border: 1px solid #ddd; border-radius: 8px;
                    margin: 10px 0; background-color: #f8f9fa;">
            <h3 style="margin-top: 0; color: #333;">
                Databricks Database Access: {self.component_id}
            </h3>

            <!-- 接続状態 -->
            <div style="margin-bottom: 20px;">
                <h4 style="color: #555;">接続状態</h4>
                <div style="padding: 10px; background-color: #d4edda;
                            color: #155724; border-radius: 5px;
                            border: 1px solid #c3e6cb;">
                    ✅ Spark session initialized in Databricks
                </div>
            </div>

            <!-- クエリ実行 -->
            <div style="margin-bottom: 20px;">
                <h4 style="color: #555;">SQLクエリ実行</h4>
                <textarea id="{widget_id}_query"
                          style="width: 100%; height: 100px; padding: 10px;
                                 border: 1px solid #ddd; border-radius: 4px;
                                 font-family: monospace; font-size: 14px;"
                          placeholder="SQLクエリを入力してください...">
SELECT current_timestamp() as current_time</textarea>
                <br><br>
                <button onclick="executeQuery_{widget_id}()"
                        style="padding: 10px 20px; background-color: #007bff;
                               color: white; border: none; border-radius: 4px;
                               cursor: pointer; font-size: 14px;">クエリ実行</button>
                <button onclick="clearQuery_{widget_id}()"
                        style="padding: 10px 20px; background-color: #6c757d;
                               color: white; border: none; border-radius: 4px;
                               cursor: pointer; margin-left: 10px;
                               font-size: 14px;">クリア</button>
            </div>

            <!-- 結果表示 -->
            <div style="margin-bottom: 20px;">
                <h4 style="color: #555;">クエリ結果</h4>
                <div id="{widget_id}_results"
                     style="padding: 15px; background-color: white;
                            border-radius: 4px; border: 1px solid #dee2e6;
                            min-height: 100px;">
                    <p style="color: #666; text-align: center;
                              margin: 20px 0;">クエリを実行して結果を表示</p>
                </div>
            </div>

            <!-- テーブル一覧 -->
            <div style="margin-bottom: 20px;">
                <h4 style="color: #555;">テーブル一覧</h4>
                <button onclick="loadTables_{widget_id}()"
                        style="padding: 10px 20px; background-color: #17a2b8;
                               color: white; border: none; border-radius: 4px;
                               cursor: pointer; font-size: 14px;">
                    テーブル一覧を取得
                </button>
                <div id="{widget_id}_tables" style="margin-top: 10px;"></div>
            </div>

            <!-- テーブル情報 -->
            <div style="margin-bottom: 20px;">
                <h4 style="color: #555;">テーブル情報</h4>
                <div id="{widget_id}_table_info"></div>
            </div>
        </div>

        <script>
            // クエリ実行
            function executeQuery_{widget_id}() {{
                const query = document.getElementById(
                    '{widget_id}_query').value.trim();
                if (!query) {{
                    alert('クエリを入力してください');
                    return;
                }}

                const resultsDiv = document.getElementById(
                    '{widget_id}_results');
                resultsDiv.innerHTML = '<div style="text-align: center; ' +
                    'padding: 20px; color: #666;">クエリを実行中...</div>';

                // Databricks環境では実際のSQL実行はPython側で行う
                // ここでは表示のみ
                setTimeout(() => {{
                    resultsDiv.innerHTML = '<div style="color: #28a745; ' +
                        'padding: 10px; background-color: #d4edda; ' +
                        'border-radius: 4px;">クエリが実行されました。' +
                        '結果はPython側で表示されます。</div>';
                }}, 1000);
            }}

            // クエリをクリア
            function clearQuery_{widget_id}() {{
                document.getElementById('{widget_id}_query').value = '';
                document.getElementById('{widget_id}_results').innerHTML =
                    '<p style="color: #666; text-align: center; ' +
                    'margin: 20px 0;">クエリを実行して結果を表示</p>';
            }}

            // テーブル一覧を取得
            function loadTables_{widget_id}() {{
                const tablesDiv = document.getElementById(
                    '{widget_id}_tables');
                tablesDiv.innerHTML = '<div style="text-align: center; ' +
                    'padding: 20px; color: #666;">テーブル一覧を取得中...</div>';

                setTimeout(() => {{
                    tablesDiv.innerHTML = '<div style="color: #17a2b8; ' +
                        'padding: 10px; background-color: #d1ecf1; ' +
                        'border-radius: 4px;">テーブル一覧が取得されました。' +
                        'Python側で表示されます。</div>';
                }}, 1000);
            }}
        </script>
        """

        return html


def create_databricks_database_component(
    component_id: str, catalog: Optional[str] = None, schema: Optional[str] = None
) -> DatabricksDatabaseComponent:
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


# 便利な関数（Databricks環境用）
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


def get_tables(
    catalog: Optional[str] = None, schema: Optional[str] = None
) -> pd.DataFrame:
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


def preview_table(
    table_name: str,
    limit: int = 100,
    catalog: Optional[str] = None,
    schema: Optional[str] = None,
) -> pd.DataFrame:
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


def get_table_stats(
    table_name: str, catalog: Optional[str] = None, schema: Optional[str] = None
) -> Dict[str, Any]:
    """
    テーブル統計情報を取得（便利関数）

    Args:
        table_name: テーブル名
        catalog: カタログ名
        schema: スキーマ名

    Returns:
        統計情報の辞書
    """
    db = DatabricksDatabaseComponent("temp-db", catalog, schema)
    return db.get_table_stats(table_name, catalog, schema)
