"""
Databricks Notebook Example

Databricksノートブック内でのデータベースアクセス機能の使用例です。
"""

# Databricksノートブック内で実行する例

def databricks_notebook_example():
    """
    Databricksノートブック内での使用例
    """
    print("=== Databricks Database Access Example ===")
    
    # 1. 基本的なSQLクエリ実行
    print("\n1. 基本的なSQLクエリ実行")
    try:
        from db_ui_components.databricks_database import execute_sql
        
        # 簡単なクエリを実行
        result = execute_sql("SELECT current_timestamp() as current_time, version() as spark_version")
        print("クエリ結果:")
        print(result)
        
    except Exception as e:
        print(f"エラー: {e}")
    
    # 2. テーブル一覧の取得
    print("\n2. テーブル一覧の取得")
    try:
        from db_ui_components.databricks_database import get_tables
        
        # デフォルトスキーマのテーブル一覧を取得
        tables = get_tables()
        print(f"テーブル数: {len(tables)}")
        if len(tables) > 0:
            print("テーブル一覧:")
            for _, row in tables.iterrows():
                print(f"  - {row['table_name']} ({row['table_type']})")
        
    except Exception as e:
        print(f"エラー: {e}")
    
    # 3. テーブルプレビュー
    print("\n3. テーブルプレビュー")
    try:
        from db_ui_components.databricks_database import preview_table
        
        # 最初のテーブルをプレビュー
        if len(tables) > 0:
            first_table = tables.iloc[0]['table_name']
            preview = preview_table(first_table, limit=5)
            print(f"テーブル '{first_table}' のプレビュー:")
            print(preview.head())
        
    except Exception as e:
        print(f"エラー: {e}")
    
    # 4. コンポーネントを使用したインタラクティブな操作
    print("\n4. インタラクティブなコンポーネント")
    try:
        from db_ui_components.databricks_database import DatabricksDatabaseComponent
        
        # データベースコンポーネントを作成
        db_component = DatabricksDatabaseComponent(
            component_id="notebook-db",
            catalog="hive_metastore",
            schema="default"
        )
        
        # ノートブックで表示
        display(db_component.display())
        
    except Exception as e:
        print(f"エラー: {e}")


def databricks_sql_magic_example():
    """
    Databricks SQLマジックコマンドの使用例
    """
    print("=== Databricks SQL Magic Example ===")
    
    # Databricksノートブック内でのSQLマジックコマンドの使用例
    
    # 1. 基本的なSQLクエリ
    print("\n1. 基本的なSQLクエリ")
    sql_query = """
    SELECT 
        current_timestamp() as current_time,
        version() as spark_version,
        current_user() as current_user
    """
    print("実行するクエリ:")
    print(sql_query)
    
    # 2. テーブル情報の取得
    print("\n2. テーブル情報の取得")
    table_info_query = """
    SELECT 
        table_catalog,
        table_schema,
        table_name,
        table_type
    FROM information_schema.tables 
    WHERE table_schema = 'default'
    ORDER BY table_name
    LIMIT 10
    """
    print("実行するクエリ:")
    print(table_info_query)
    
    # 3. データサンプルの取得
    print("\n3. データサンプルの取得")
    sample_query = """
    SELECT * 
    FROM your_table_name 
    LIMIT 10
    """
    print("実行するクエリ:")
    print(sample_query)


def databricks_widget_example():
    """
    Databricksウィジェットの使用例
    """
    print("=== Databricks Widget Example ===")
    
    # Databricksノートブック内でのウィジェット使用例
    
    # 1. パラメータウィジェットの作成
    print("\n1. パラメータウィジェットの作成")
    
    # カタログ選択ウィジェット
    catalog_widget_code = """
    dbutils.widgets.text("catalog", "hive_metastore", "Catalog")
    dbutils.widgets.text("schema", "default", "Schema")
    dbutils.widgets.text("table_name", "", "Table Name")
    dbutils.widgets.text("limit", "100", "Limit")
    """
    print("ウィジェット作成コード:")
    print(catalog_widget_code)
    
    # 2. ウィジェット値の取得
    print("\n2. ウィジェット値の取得")
    get_widget_values_code = """
    catalog = dbutils.widgets.get("catalog")
    schema = dbutils.widgets.get("schema")
    table_name = dbutils.widgets.get("table_name")
    limit = int(dbutils.widgets.get("limit"))
    
    print(f"Catalog: {catalog}")
    print(f"Schema: {schema}")
    print(f"Table: {table_name}")
    print(f"Limit: {limit}")
    """
    print("ウィジェット値取得コード:")
    print(get_widget_values_code)
    
    # 3. 動的クエリの実行
    print("\n3. 動的クエリの実行")
    dynamic_query_code = """
    if table_name:
        query = f"SELECT * FROM {catalog}.{schema}.{table_name} LIMIT {limit}"
        result = spark.sql(query)
        display(result)
    else:
        print("テーブル名を指定してください")
    """
    print("動的クエリ実行コード:")
    print(dynamic_query_code)


def databricks_display_example():
    """
    Databricks display関数の使用例
    """
    print("=== Databricks Display Example ===")
    
    # 1. 基本的なdisplay関数の使用
    print("\n1. 基本的なdisplay関数の使用")
    display_code = """
    # データフレームを表示
    df = spark.sql("SELECT * FROM your_table LIMIT 10")
    display(df)
    
    # グラフを表示
    import plotly.express as px
    fig = px.line(df.toPandas(), x='date_column', y='value_column')
    display(fig)
    """
    print("display関数使用例:")
    print(display_code)
    
    # 2. HTMLコンテンツの表示
    print("\n2. HTMLコンテンツの表示")
    html_display_code = """
    from IPython.display import HTML
    
    html_content = '''
    <div style="padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
        <h3>Databricks Database Access</h3>
        <p>このHTMLはDatabricksノートブック内で表示されます。</p>
        <button onclick="alert('Hello from Databricks!')">クリック</button>
    </div>
    '''
    
    display(HTML(html_content))
    """
    print("HTML表示例:")
    print(html_display_code)


def databricks_complete_example():
    """
    Databricksでの完全な使用例
    """
    print("=== Complete Databricks Example ===")
    
    # 完全なDatabricksノートブック例
    
    complete_example = """
    # Databricksノートブック内での完全な使用例
    
    # 1. ライブラリのインポート
    from db_ui_components.databricks_database import DatabricksDatabaseComponent, execute_sql, get_tables, preview_table
    
    # 2. データベースコンポーネントの作成
    db = DatabricksDatabaseComponent(
        component_id="my-database",
        catalog="hive_metastore",
        schema="default"
    )
    
    # 3. テーブル一覧の取得
    print("テーブル一覧を取得中...")
    tables = get_tables()
    print(f"テーブル数: {len(tables)}")
    
    # 4. 最初のテーブルをプレビュー
    if len(tables) > 0:
        first_table = tables.iloc[0]['table_name']
        print(f"テーブル '{first_table}' をプレビュー中...")
        preview = preview_table(first_table, limit=5)
        display(preview)
    
    # 5. カスタムクエリの実行
    print("カスタムクエリを実行中...")
    custom_result = execute_sql("""
        SELECT 
            current_timestamp() as current_time,
            version() as spark_version,
            current_user() as current_user
    """)
    display(custom_result)
    
    # 6. インタラクティブなウィジェットを表示
    print("インタラクティブなウィジェットを表示中...")
    display(db.display())
    
    # 7. テーブル統計情報の取得
    if len(tables) > 0:
        first_table = tables.iloc[0]['table_name']
        print(f"テーブル '{first_table}' の統計情報を取得中...")
        stats = db.get_table_stats(first_table)
        print(f"行数: {stats['row_count']:,}")
        print(f"列数: {stats['column_count']}")
        print("列情報:")
        for col in stats['columns']:
            print(f"  - {col['column_name']}: {col['data_type']}")
    """
    
    print("完全な使用例:")
    print(complete_example)


if __name__ == "__main__":
    # 各例を実行
    databricks_notebook_example()
    databricks_sql_magic_example()
    databricks_widget_example()
    databricks_display_example()
    databricks_complete_example()
    
    print("\n=== 使用例完了 ===")
    print("Databricksノートブック内でこれらの例を実行してください。")