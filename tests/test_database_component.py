"""
データベースコンポーネントのテスト

Databricksデータベースアクセス機能のテストを実行します。
"""

import unittest
import pandas as pd
import os
from unittest.mock import Mock, patch, MagicMock
from db_ui_components.database_component import DatabaseComponent, SparkComponent

# PySparkモジュールをモック
import sys
from unittest.mock import MagicMock

# pysparkモジュールをモック
sys.modules["pyspark"] = MagicMock()
sys.modules["pyspark.sql"] = MagicMock()


class TestDatabaseComponent(unittest.TestCase):
    """DatabaseComponentのテストクラス"""

    def setUp(self):
        """テストの前準備"""
        self.component_id = "test-db"
        self.workspace_url = "https://test-workspace.cloud.databricks.com"
        self.token = "test-token"
        self.catalog = "test_catalog"
        self.schema = "test_schema"

        # モックデータ
        self.sample_data = pd.DataFrame(
            {
                "id": [1, 2, 3, 4, 5],
                "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
                "age": [25, 30, 35, 40, 45],
                "city": ["Tokyo", "Osaka", "Kyoto", "Nagoya", "Fukuoka"],
            }
        )

    @patch("db_ui_components.database_component.DATABRICKS_AVAILABLE", False)
    def test_databricks_not_available(self):
        """Databricks SDKが利用できない場合のテスト"""
        with self.assertRaises(Exception):
            DatabaseComponent(self.component_id)

    @patch("db_ui_components.database_component.DATABRICKS_AVAILABLE", True)
    @patch("db_ui_components.database_component.Config")
    @patch("db_ui_components.database_component.sql_connect")
    @patch("db_ui_components.database_component.WorkspaceClient")
    def test_initialization_with_credentials(
        self, mock_workspace_client, mock_sql_connect, mock_config
    ):
        """認証情報付きでの初期化テスト"""
        # モックの設定
        mock_config.return_value = Mock()
        mock_workspace_client.return_value = Mock()
        mock_sql_connect.return_value = Mock()

        # コンポーネントの作成
        db = DatabaseComponent(
            self.component_id,
            workspace_url=self.workspace_url,
            token=self.token,
            catalog=self.catalog,
            schema=self.schema,
        )

        # 検証
        self.assertEqual(db.component_id, self.component_id)
        self.assertEqual(db.workspace_url, self.workspace_url)
        self.assertEqual(db.token, self.token)
        self.assertEqual(db.catalog, self.catalog)
        self.assertEqual(db.schema, self.schema)

    @patch("db_ui_components.database_component.DATABRICKS_AVAILABLE", True)
    @patch("db_ui_components.database_component.Config")
    @patch("db_ui_components.database_component.sql_connect")
    @patch("db_ui_components.database_component.WorkspaceClient")
    def test_execute_query(self, mock_workspace_client, mock_sql_connect, mock_config):
        """クエリ実行のテスト"""
        # モックの設定
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            (1, "Alice", 25, "Tokyo"),
            (2, "Bob", 30, "Osaka"),
        ]
        mock_cursor.description = [("id",), ("name",), ("age",), ("city",)]
        # cursor()がコンテキストマネージャーとして使われるため
        mock_cursor_context = MagicMock()
        mock_cursor_context.__enter__.return_value = mock_cursor
        mock_cursor_context.__exit__.return_value = None
        mock_connection.cursor.return_value = mock_cursor_context

        mock_sql_connect.return_value = mock_connection
        mock_workspace_client.return_value = Mock()
        mock_config.return_value = Mock()

        # コンポーネントの作成
        db = DatabaseComponent(
            self.component_id, workspace_url=self.workspace_url, token=self.token
        )

        # クエリ実行
        result = db.execute_query("SELECT * FROM users LIMIT 2")

        # 検証
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)
        self.assertEqual(list(result.columns), ["id", "name", "age", "city"])

    @patch("db_ui_components.database_component.DATABRICKS_AVAILABLE", True)
    @patch("db_ui_components.database_component.Config")
    @patch("db_ui_components.database_component.sql_connect")
    @patch("db_ui_components.database_component.WorkspaceClient")
    def test_get_tables(self, mock_workspace_client, mock_sql_connect, mock_config):
        """テーブル一覧取得のテスト"""
        # モックの設定
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            ("users", "BASE TABLE", "User information"),
            ("orders", "BASE TABLE", "Order data"),
            ("products", "BASE TABLE", "Product catalog"),
        ]
        mock_cursor.description = [("table_name",), ("table_type",), ("table_comment",)]
        # cursor()がコンテキストマネージャーとして使われるため
        mock_cursor_context = MagicMock()
        mock_cursor_context.__enter__.return_value = mock_cursor
        mock_cursor_context.__exit__.return_value = None
        mock_connection.cursor.return_value = mock_cursor_context

        mock_sql_connect.return_value = mock_connection
        mock_workspace_client.return_value = Mock()
        mock_config.return_value = Mock()

        # コンポーネントの作成
        db = DatabaseComponent(
            self.component_id,
            workspace_url=self.workspace_url,
            token=self.token,
            catalog=self.catalog,
            schema=self.schema,
        )

        # テーブル一覧取得
        tables = db.get_tables()

        # 検証
        self.assertIsInstance(tables, pd.DataFrame)
        self.assertEqual(len(tables), 3)
        self.assertIn("users", tables["table_name"].values)
        self.assertIn("orders", tables["table_name"].values)
        self.assertIn("products", tables["table_name"].values)

    @patch("db_ui_components.database_component.DATABRICKS_AVAILABLE", True)
    @patch("db_ui_components.database_component.Config")
    @patch("db_ui_components.database_component.sql_connect")
    @patch("db_ui_components.database_component.WorkspaceClient")
    def test_get_table_schema(
        self, mock_workspace_client, mock_sql_connect, mock_config
    ):
        """テーブルスキーマ取得のテスト"""
        # モックの設定
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            ("id", "INT", "NO", None, "Primary key"),
            ("name", "VARCHAR(255)", "YES", None, "User name"),
            ("age", "INT", "YES", None, "User age"),
            ("city", "VARCHAR(100)", "YES", None, "User city"),
        ]
        mock_cursor.description = [
            ("column_name",),
            ("data_type",),
            ("is_nullable",),
            ("column_default",),
            ("column_comment",),
        ]
        # cursor()がコンテキストマネージャーとして使われるため
        mock_cursor_context = MagicMock()
        mock_cursor_context.__enter__.return_value = mock_cursor
        mock_cursor_context.__exit__.return_value = None
        mock_connection.cursor.return_value = mock_cursor_context

        mock_sql_connect.return_value = mock_connection
        mock_workspace_client.return_value = Mock()
        mock_config.return_value = Mock()

        # コンポーネントの作成
        db = DatabaseComponent(
            self.component_id,
            workspace_url=self.workspace_url,
            token=self.token,
            catalog=self.catalog,
            schema=self.schema,
        )

        # スキーマ取得
        schema = db.get_table_schema("users")

        # 検証
        self.assertIsInstance(schema, pd.DataFrame)
        self.assertEqual(len(schema), 4)
        self.assertIn("id", schema["column_name"].values)
        self.assertIn("name", schema["column_name"].values)
        self.assertIn("age", schema["column_name"].values)
        self.assertIn("city", schema["column_name"].values)

    @patch("db_ui_components.database_component.DATABRICKS_AVAILABLE", True)
    @patch("db_ui_components.database_component.Config")
    @patch("db_ui_components.database_component.sql_connect")
    @patch("db_ui_components.database_component.WorkspaceClient")
    def test_get_table_stats(
        self, mock_workspace_client, mock_sql_connect, mock_config
    ):
        """テーブル統計情報取得のテスト"""
        # モックの設定
        mock_workspace_client.return_value = Mock()
        mock_config.return_value = Mock()

        # 1つの接続で、cursorが呼ばれるたびに違う結果を返すように設定
        mock_connection = Mock()

        # COUNTクエリ用のカーソル
        mock_cursor1 = Mock()
        mock_cursor1.fetchall.return_value = [(1000,)]  # COUNT(*) の結果
        mock_cursor1.description = [("row_count",)]

        # スキーマクエリ用のカーソル
        mock_cursor2 = Mock()
        mock_cursor2.fetchall.return_value = [  # スキーマ情報
            ("id", "INT", "NO", None, "Primary key"),
            ("name", "VARCHAR(255)", "YES", None, "User name"),
            ("age", "INT", "YES", None, "User age"),
        ]
        mock_cursor2.description = [
            ("column_name",),
            ("data_type",),
            ("is_nullable",),
            ("column_default",),
            ("column_comment",),
        ]

        # cursor()がコンテキストマネージャーとして使われるため
        mock_cursor_context1 = MagicMock()
        mock_cursor_context1.__enter__.return_value = mock_cursor1
        mock_cursor_context1.__exit__.return_value = None

        mock_cursor_context2 = MagicMock()
        mock_cursor_context2.__enter__.return_value = mock_cursor2
        mock_cursor_context2.__exit__.return_value = None

        # cursor()が呼ばれるたびに違うコンテキストを返す
        mock_connection.cursor.side_effect = [
            mock_cursor_context1,
            mock_cursor_context2,
        ]

        # sql_connectは常に同じ接続を返す
        mock_sql_connect.return_value = mock_connection

        # コンポーネントの作成
        db = DatabaseComponent(
            self.component_id,
            workspace_url=self.workspace_url,
            token=self.token,
            catalog=self.catalog,
            schema=self.schema,
        )

        # 統計情報取得
        stats = db.get_table_stats("users")

        # 検証
        self.assertIsInstance(stats, dict)
        self.assertEqual(stats["table_name"], "users")
        self.assertEqual(stats["row_count"], 1000)
        self.assertEqual(stats["column_count"], 3)
        self.assertEqual(len(stats["columns"]), 3)

    def test_render_method(self):
        """renderメソッドのテスト"""
        with patch("db_ui_components.database_component.DATABRICKS_AVAILABLE", True):
            with patch("db_ui_components.database_component.Config"):
                with patch("db_ui_components.database_component.sql_connect"):
                    with patch("db_ui_components.database_component.WorkspaceClient"):
                        db = DatabaseComponent(self.component_id)

                        # renderメソッドの実行
                        html_output = db.render()

                        # 検証
                        self.assertIsInstance(html_output, str)
                        self.assertIn("Database Component", html_output)

    def test_close_connection(self):
        """接続終了のテスト"""
        with patch("db_ui_components.database_component.DATABRICKS_AVAILABLE", True):
            with patch("db_ui_components.database_component.Config"):
                with patch(
                    "db_ui_components.database_component.sql_connect"
                ) as mock_sql_connect:
                    with patch("db_ui_components.database_component.WorkspaceClient"):
                        # モック接続を設定
                        mock_connection = Mock()
                        mock_sql_connect.return_value = mock_connection

                        db = DatabaseComponent(
                            self.component_id,
                            workspace_url=self.workspace_url,
                            token=self.token,
                        )

                        # 接続終了
                        db.close_connection()

                        # 検証 - close()が呼ばれたことを確認
                        mock_connection.close.assert_called_once()


class TestSparkComponent(unittest.TestCase):
    """SparkComponentのテストクラス"""

    def setUp(self):
        """テストの前準備"""
        self.component_id = "test-spark"
        self.spark_config = {
            "spark.sql.adaptive.enabled": "true",
            "spark.sql.adaptive.coalescePartitions.enabled": "true",
        }

    @patch("db_ui_components.database_component.PYSPARK_AVAILABLE", False)
    def test_pyspark_not_available(self):
        """PySparkが利用できない場合のテスト"""
        with self.assertRaises(Exception):
            SparkComponent(self.component_id)

    @patch("db_ui_components.database_component.PYSPARK_AVAILABLE", True)
    def test_initialization(self):
        """初期化のテスト"""
        # モックの設定
        from db_ui_components import database_component

        # database_componentモジュールをリロードしてモックされたPySparkを認識させる
        import importlib

        importlib.reload(database_component)

        with patch(
            "db_ui_components.database_component.SparkSession"
        ) as mock_spark_session:
            mock_session = Mock()
            mock_builder = Mock()
            mock_builder.config.return_value = mock_builder
            mock_builder.getOrCreate.return_value = mock_session
            mock_spark_session.builder = mock_builder

            # コンポーネントの作成
            spark = SparkComponent(self.component_id, spark_config=self.spark_config)

            # 検証
            self.assertEqual(spark.component_id, self.component_id)
            self.assertEqual(spark.spark_config, self.spark_config)

    @patch("db_ui_components.database_component.PYSPARK_AVAILABLE", True)
    def test_read_table(self):
        """テーブル読み込みのテスト"""
        # モックの設定
        from db_ui_components import database_component

        # database_componentモジュールをリロードしてモックされたPySparkを認識させる
        import importlib

        importlib.reload(database_component)

        with patch(
            "db_ui_components.database_component.SparkSession"
        ) as mock_spark_session:
            mock_session = Mock()
            mock_builder = Mock()
            mock_builder.config.return_value = mock_builder
            mock_builder.getOrCreate.return_value = mock_session
            mock_spark_session.builder = mock_builder

            # コンポーネントの作成
            spark = SparkComponent(self.component_id)

            # テーブル読み込み
            result = spark.read_table("test_table")

            # 検証
            mock_session.table.assert_called_once_with("test_table")

    @patch("db_ui_components.database_component.PYSPARK_AVAILABLE", True)
    def test_execute_sql(self):
        """SQL実行のテスト"""
        # モックの設定
        from db_ui_components import database_component

        # database_componentモジュールをリロードしてモックされたPySparkを認識させる
        import importlib

        importlib.reload(database_component)

        with patch(
            "db_ui_components.database_component.SparkSession"
        ) as mock_spark_session:
            mock_session = Mock()
            mock_builder = Mock()
            mock_builder.config.return_value = mock_builder
            mock_builder.getOrCreate.return_value = mock_session
            mock_spark_session.builder = mock_builder

            # モックDataFrame
            mock_df = Mock()
            mock_df.toPandas.return_value = pd.DataFrame({"col1": [1, 2, 3]})
            mock_session.sql.return_value = mock_df

            # コンポーネントの作成
            spark = SparkComponent(self.component_id)

            # SQL実行
            result = spark.execute_sql("SELECT * FROM test_table")

            # 検証
            self.assertIsInstance(result, pd.DataFrame)
            mock_session.sql.assert_called_once_with("SELECT * FROM test_table")

    def test_render_method(self):
        """renderメソッドのテスト"""
        with patch("db_ui_components.database_component.PYSPARK_AVAILABLE", True):
            with patch(
                "db_ui_components.database_component.SparkSession"
            ) as mock_spark_session:
                # モックの設定
                mock_session = Mock()
                mock_builder = Mock()
                mock_builder.config.return_value = mock_builder
                mock_builder.getOrCreate.return_value = mock_session
                mock_spark_session.builder = mock_builder

                spark = SparkComponent(self.component_id)

                # renderメソッドの実行
                html_output = spark.render()

                # 検証
                self.assertIsInstance(html_output, str)
                self.assertIn("Spark Component", html_output)

    def test_stop_session(self):
        """セッション停止のテスト"""
        with patch("db_ui_components.database_component.PYSPARK_AVAILABLE", True):
            with patch(
                "db_ui_components.database_component.SparkSession"
            ) as mock_spark_session:
                # モックの設定
                mock_session = Mock()
                mock_builder = Mock()
                mock_builder.config.return_value = mock_builder
                mock_builder.getOrCreate.return_value = mock_session
                mock_spark_session.builder = mock_builder

                spark = SparkComponent(self.component_id)

                # セッション停止
                spark.stop_session()

                # 検証 - stop()が呼ばれたことを確認
                mock_session.stop.assert_called_once()


if __name__ == "__main__":
    unittest.main()
