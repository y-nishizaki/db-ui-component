"""
Databricks Database Access Example

Databricksデータベースアクセス機能の使用例です。
"""

import os
import pandas as pd
from dash import Dash, html, dcc
from db_ui_components import DatabaseComponent, SparkComponent, Dashboard

def create_database_dashboard():
    """
    Databricksデータベースアクセス機能を含むダッシュボードを作成
    """
    
    # 環境変数からDatabricks認証情報を取得
    workspace_url = os.getenv('DATABRICKS_WORKSPACE_URL')
    token = os.getenv('DATABRICKS_TOKEN')
    catalog = os.getenv('DATABRICKS_CATALOG', 'hive_metastore')
    schema = os.getenv('DATABRICKS_SCHEMA', 'default')
    
    # データベースコンポーネントの作成
    db_component = DatabaseComponent(
        component_id="databricks-db",
        workspace_url=workspace_url,
        token=token,
        catalog=catalog,
        schema=schema
    )
    
    # Sparkコンポーネントの作成（オプション）
    spark_component = SparkComponent(
        component_id="spark-component",
        spark_config={
            "spark.sql.warehouse.dir": "/tmp/spark-warehouse",
            "spark.sql.adaptive.enabled": "true"
        }
    )
    
    # ダッシュボードの作成
    dashboard = Dashboard(
        title="Databricks Database Dashboard"
    )
    
    # コンポーネントをダッシュボードに追加
    dashboard.add_component(db_component, position=(0, 0), size=(6, 1))
    dashboard.add_component(spark_component, position=(6, 0), size=(6, 1))
    
    return dashboard

def create_simple_database_app():
    """
    シンプルなデータベースアプリケーションを作成
    """
    app = Dash(__name__)
    
    # データベースコンポーネント
    db_component = DatabaseComponent(
        component_id="simple-db",
        workspace_url="https://your-workspace.cloud.databricks.com",
        token="your-token-here"
    )
    
    app.layout = html.Div([
        html.H1("Databricks Database Access"),
        html.Div([
            db_component.create_layout()
        ])
    ])
    
    # コールバックを登録
    db_component.register_callbacks(app)
    
    return app

def database_usage_example():
    """
    データベースコンポーネントの使用例
    """
    print("=== Databricks Database Access Example ===")
    
    # データベースコンポーネントの作成
    db = DatabaseComponent(
        component_id="example-db",
        workspace_url="https://your-workspace.cloud.databricks.com",
        token="your-token-here",
        catalog="hive_metastore",
        schema="default"
    )
    
    try:
        # テーブル一覧の取得
        print("\n1. Getting tables...")
        tables = db.get_tables()
        print(f"Found {len(tables)} tables:")
        for _, row in tables.iterrows():
            print(f"  - {row['table_name']} ({row['table_type']})")
        
        # 特定のテーブルのスキーマ取得
        if len(tables) > 0:
            table_name = tables.iloc[0]['table_name']
            print(f"\n2. Getting schema for table '{table_name}'...")
            schema = db.get_table_schema(table_name)
            print(f"Schema for {table_name}:")
            for _, col in schema.iterrows():
                print(f"  - {col['column_name']}: {col['data_type']}")
            
            # テーブルのプレビュー
            print(f"\n3. Previewing table '{table_name}'...")
            preview = db.preview_table(table_name, limit=5)
            print(f"Preview data ({len(preview)} rows):")
            print(preview.head())
            
            # テーブル統計情報
            print(f"\n4. Getting statistics for table '{table_name}'...")
            stats = db.get_table_stats(table_name)
            print(f"Table statistics:")
            print(f"  - Rows: {stats['row_count']:,}")
            print(f"  - Columns: {stats['column_count']}")
        
        # カスタムクエリの実行
        print("\n5. Executing custom query...")
        query = "SELECT current_timestamp() as current_time, version() as spark_version"
        result = db.execute_query(query)
        print("Query result:")
        print(result)
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # 接続を閉じる
        db.close_connection()

def spark_usage_example():
    """
    Sparkコンポーネントの使用例
    """
    print("\n=== Spark Component Example ===")
    
    # Sparkコンポーネントの作成
    spark = SparkComponent(
        component_id="example-spark",
        spark_config={
            "spark.sql.adaptive.enabled": "true",
            "spark.sql.adaptive.coalescePartitions.enabled": "true"
        }
    )
    
    try:
        # セッション情報の取得
        print("1. Getting Spark session info...")
        version = spark.spark_session.version
        print(f"Spark version: {version}")
        
        # テーブルの読み込み
        print("\n2. Reading table...")
        # 例: sample_tableというテーブルが存在する場合
        try:
            df = spark.read_table("sample_table")
            print(f"Table loaded: {df.count()} rows, {len(df.columns)} columns")
            print(f"Columns: {df.columns}")
        except Exception as e:
            print(f"Table read failed: {e}")
        
        # SQLクエリの実行
        print("\n3. Executing SQL query...")
        sql_result = spark.execute_sql("SELECT current_timestamp() as time")
        print("SQL result:")
        print(sql_result)
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # セッションを停止
        spark.stop_session()

def create_advanced_database_dashboard():
    """
    高度なデータベースダッシュボードの作成例
    """
    from db_ui_components import ChartComponent, TableComponent
    
    # ダッシュボードの作成
    dashboard = Dashboard(
        title="Advanced Database Dashboard"
    )
    
    # データベースコンポーネント
    db_component = DatabaseComponent(
        component_id="advanced-db",
        workspace_url=os.getenv('DATABRICKS_WORKSPACE_URL'),
        token=os.getenv('DATABRICKS_TOKEN')
    )
    
    # サンプルデータの作成
    sample_data = pd.DataFrame({
        'category': ['A', 'B', 'C', 'D'],
        'value': [10, 20, 15, 25]
    })
    
    # テーブルコンポーネント（データベースの結果を表示）
    table_component = TableComponent(
        data=sample_data,
        component_id="db-results-table"
    )
    
    # チャートコンポーネント（データベースの結果を可視化）
    chart_component = ChartComponent(
        data=sample_data,
        chart_type="bar",
        x_column="category",
        y_column="value",
        component_id="db-results-chart"
    )
    
    # コンポーネントをダッシュボードに追加
    dashboard.add_component(db_component, position=(0, 0), size=(12, 1))
    dashboard.add_component(table_component, position=(0, 1), size=(6, 1))
    dashboard.add_component(chart_component, position=(6, 1), size=(6, 1))
    
    return dashboard

if __name__ == "__main__":
    # 使用例の実行
    database_usage_example()
    spark_usage_example()
    
    print("\n=== Example completed ===")
    print("To run the dashboard, use:")
    print("python -c \"from examples.database_example import create_database_dashboard; app = create_database_dashboard().create_app(); app.run_server(debug=True)\"")