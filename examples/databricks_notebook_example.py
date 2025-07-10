"""
Databricksノートブックでの使用例

このファイルはDatabricksノートブック内で実行することを想定しています。
"""

# Databricks環境でのインポート
from db_ui_components.databricks_database import (
    DatabricksDatabaseComponent,
    create_databricks_database_component,
    execute_sql,
    get_tables,
    preview_table,
    get_table_stats
)

# 1. 基本的な使用例
print("=== Databricks Database Component Example ===")

# コンポーネントの作成
db = create_databricks_database_component("my-db", catalog="hive_metastore", schema="default")

# 2. SQLクエリの実行
print("\n--- SQL Query Execution ---")
try:
    # 現在時刻を取得
    result = execute_sql("SELECT current_timestamp() as current_time")
    print("Current time query result:")
    print(result)
    
    # より複雑なクエリ
    result = execute_sql("""
        SELECT 
            current_date() as today,
            current_timestamp() as now,
            version() as spark_version
    """)
    print("\nSystem info query result:")
    print(result)
    
except Exception as e:
    print(f"Query execution failed: {e}")

# 3. テーブル一覧の取得
print("\n--- Table Listing ---")
try:
    tables = get_tables(catalog="hive_metastore", schema="default")
    print("Available tables:")
    print(tables)
    
    # テーブルが存在する場合の処理
    if not tables.empty:
        print(f"\nFound {len(tables)} tables")
        for _, table in tables.iterrows():
            print(f"- {table['table_name']} ({table['table_type']})")
    else:
        print("No tables found in the specified schema")
        
except Exception as e:
    print(f"Table listing failed: {e}")

# 4. テーブルプレビュー
print("\n--- Table Preview ---")
try:
    # サンプルテーブルが存在する場合のプレビュー
    sample_tables = ["sample_table", "users", "orders"]
    
    for table_name in sample_tables:
        try:
            preview = preview_table(table_name, limit=5)
            print(f"\nPreview of {table_name}:")
            print(preview)
        except Exception as e:
            print(f"Could not preview {table_name}: {e}")
            
except Exception as e:
    print(f"Table preview failed: {e}")

# 5. テーブル統計情報の取得
print("\n--- Table Statistics ---")
try:
    for table_name in sample_tables:
        try:
            stats = get_table_stats(table_name)
            print(f"\nStatistics for {table_name}:")
            print(f"- Row count: {stats['row_count']}")
            print(f"- Column count: {stats['column_count']}")
            print(f"- Catalog: {stats['catalog']}")
            print(f"- Schema: {stats['schema']}")
        except Exception as e:
            print(f"Could not get stats for {table_name}: {e}")
            
except Exception as e:
    print(f"Statistics retrieval failed: {e}")

# 6. コンポーネントのHTMLウィジェット表示
print("\n--- HTML Widget Display ---")
try:
    # HTMLウィジェットを生成
    widget_html = db.render()
    print("Widget HTML generated successfully")
    
    # Databricks環境での表示
    try:
        from IPython.display import HTML, display
        display(HTML(widget_html))
        print("Widget displayed in notebook")
    except ImportError:
        print("IPython not available, HTML widget not displayed")
        print("Widget HTML:")
        print(widget_html[:500] + "..." if len(widget_html) > 500 else widget_html)
        
except Exception as e:
    print(f"Widget generation failed: {e}")

# 7. 高度な使用例
print("\n--- Advanced Usage ---")

# 複数のコンポーネントインスタンス
db1 = create_databricks_database_component("db1", catalog="hive_metastore", schema="default")
db2 = create_databricks_database_component("db2", catalog="hive_metastore", schema="default")

# 並行処理の例
import concurrent.futures

def run_query(query):
    """クエリを実行する関数"""
    try:
        return execute_sql(query)
    except Exception as e:
        return f"Error: {e}"

# 複数のクエリを並行実行
queries = [
    "SELECT current_timestamp() as time1",
    "SELECT current_date() as date1",
    "SELECT version() as version1"
]

print("Running parallel queries...")
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(run_query, queries))

for i, result in enumerate(results):
    print(f"Query {i+1} result:")
    print(result)
    print()

# 8. エラーハンドリングの例
print("\n--- Error Handling Examples ---")

# 存在しないテーブルへのアクセス
try:
    result = execute_sql("SELECT * FROM non_existent_table LIMIT 1")
    print("Non-existent table query result:", result)
except Exception as e:
    print(f"Expected error for non-existent table: {e}")

# 無効なSQLクエリ
try:
    result = execute_sql("INVALID SQL QUERY")
    print("Invalid SQL query result:", result)
except Exception as e:
    print(f"Expected error for invalid SQL: {e}")

# 9. パフォーマンステスト
print("\n--- Performance Test ---")
import time

# クエリ実行時間の測定
start_time = time.time()
try:
    result = execute_sql("SELECT current_timestamp() as test_time")
    execution_time = time.time() - start_time
    print(f"Query execution time: {execution_time:.3f} seconds")
    print("Result:", result)
except Exception as e:
    print(f"Performance test failed: {e}")

print("\n=== Example completed ===")