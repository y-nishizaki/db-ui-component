# Databricks Database Access Component

Databricksノートブック内で直接使用できるデータベースアクセスコンポーネントです。

## 特徴

- **Databricks環境専用**: SparkSessionを直接利用
- **シンプルなAPI**: 直感的な関数呼び出し
- **HTMLウィジェット**: インタラクティブな操作
- **キャッシュ機能**: パフォーマンス最適化
- **エラーハンドリング**: 堅牢なエラー処理

## インストール

Databricksノートブック内で以下のコマンドを実行：

```python
# パッケージのインストール
!pip install db-ui-components

# または、Databricksライブラリとして追加
# Databricks UI > Libraries > Install New > PyPI
# Package: db-ui-components
```

## 基本的な使用方法

### 1. インポート

```python
from db_ui_components.databricks_database import (
    DatabricksDatabaseComponent,
    create_databricks_database_component,
    execute_sql,
    get_tables,
    preview_table,
    get_table_stats
)
```

### 2. コンポーネントの作成

```python
# 基本的なコンポーネント作成
db = create_databricks_database_component("my-db")

# カタログとスキーマを指定
db = create_databricks_database_component(
    "my-db", 
    catalog="hive_metastore", 
    schema="default"
)
```

### 3. SQLクエリの実行

```python
# 簡単なクエリ
result = execute_sql("SELECT current_timestamp() as current_time")
print(result)

# 複雑なクエリ
result = execute_sql("""
    SELECT 
        current_date() as today,
        current_timestamp() as now,
        version() as spark_version
""")
display(result)  # Databricksのdisplay関数を使用
```

### 4. テーブル一覧の取得

```python
# デフォルトスキーマのテーブル一覧
tables = get_tables()
print(f"Found {len(tables)} tables")

# 特定のカタログ・スキーマのテーブル一覧
tables = get_tables(catalog="hive_metastore", schema="default")
for _, table in tables.iterrows():
    print(f"- {table['table_name']} ({table['table_type']})")
```

### 5. テーブルプレビュー

```python
# テーブルの最初の5行をプレビュー
preview = preview_table("your_table_name", limit=5)
display(preview)

# 特定のカタログ・スキーマのテーブルをプレビュー
preview = preview_table(
    "your_table_name", 
    limit=10,
    catalog="hive_metastore", 
    schema="default"
)
display(preview)
```

### 6. テーブル統計情報の取得

```python
# テーブルの統計情報を取得
stats = get_table_stats("your_table_name")
print(f"Row count: {stats['row_count']}")
print(f"Column count: {stats['column_count']}")
print(f"Catalog: {stats['catalog']}")
print(f"Schema: {stats['schema']}")

# 列情報の表示
for col in stats['columns']:
    print(f"- {col['column_name']}: {col['data_type']}")
```

## 高度な使用方法

### 1. コンポーネントインスタンスの使用

```python
# コンポーネントを作成
db = create_databricks_database_component("advanced-db")

# メソッドを使用
result = db.execute_sql("SELECT * FROM your_table LIMIT 10")
tables = db.get_tables()
schema = db.get_table_schema("your_table")
stats = db.get_table_stats("your_table")

# テーブルを直接読み込み
df = db.read_table("your_table")
display(df)
```

### 2. HTMLウィジェットの表示

```python
# HTMLウィジェットを生成
widget_html = db.render()
print("Widget HTML generated")

# Databricks環境で表示
from IPython.display import HTML, display
display(HTML(widget_html))
```

### 3. 並行処理

```python
import concurrent.futures

def run_query(query):
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

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(run_query, queries))

for i, result in enumerate(results):
    print(f"Query {i+1} result:")
    display(result)
```

### 4. エラーハンドリング

```python
try:
    result = execute_sql("SELECT * FROM non_existent_table")
    display(result)
except Exception as e:
    print(f"Query failed: {e}")

try:
    result = execute_sql("INVALID SQL QUERY")
    display(result)
except Exception as e:
    print(f"Invalid SQL: {e}")
```

## パフォーマンス最適化

### 1. キャッシュの活用

```python
# コンポーネントは自動的にキャッシュを使用
db = create_databricks_database_component("cached-db")

# 同じクエリを複数回実行（キャッシュが使用される）
result1 = db.execute_sql("SELECT current_timestamp()")
result2 = db.execute_sql("SELECT current_timestamp()")  # キャッシュから取得
```

### 2. 行数制限

```python
# 大量データの場合は行数制限を使用
result = execute_sql("SELECT * FROM large_table LIMIT 1000")
```

## 実際の使用例

### 1. データ探索

```python
# 1. 利用可能なテーブルを確認
tables = get_tables()
print("Available tables:")
for _, table in tables.iterrows():
    print(f"- {table['table_name']}")

# 2. テーブルの構造を確認
if not tables.empty:
    first_table = tables.iloc[0]['table_name']
    schema = db.get_table_schema(first_table)
    print(f"\nSchema for {first_table}:")
    display(schema)

# 3. データをプレビュー
if not tables.empty:
    preview = preview_table(first_table, limit=10)
    print(f"\nPreview of {first_table}:")
    display(preview)
```

### 2. データ分析

```python
# 基本的な統計分析
result = execute_sql("""
    SELECT 
        COUNT(*) as total_rows,
        COUNT(DISTINCT column_name) as unique_values,
        AVG(numeric_column) as average_value,
        MIN(numeric_column) as min_value,
        MAX(numeric_column) as max_value
    FROM your_table
""")
display(result)

# 時系列分析
result = execute_sql("""
    SELECT 
        DATE(date_column) as date,
        COUNT(*) as daily_count,
        SUM(amount) as daily_total
    FROM your_table
    WHERE date_column >= DATE_SUB(CURRENT_DATE, 30)
    GROUP BY DATE(date_column)
    ORDER BY date
""")
display(result)
```

### 3. データ品質チェック

```python
# NULL値のチェック
result = execute_sql("""
    SELECT 
        column_name,
        COUNT(*) as total_rows,
        COUNT(CASE WHEN column_name IS NULL THEN 1 END) as null_count,
        ROUND(COUNT(CASE WHEN column_name IS NULL THEN 1 END) * 100.0 / COUNT(*), 2) as null_percentage
    FROM your_table
    GROUP BY column_name
    ORDER BY null_percentage DESC
""")
display(result)

# 重複チェック
result = execute_sql("""
    SELECT 
        column_name,
        COUNT(*) as duplicate_count
    FROM your_table
    GROUP BY column_name
    HAVING COUNT(*) > 1
    ORDER BY duplicate_count DESC
""")
display(result)
```

## トラブルシューティング

### よくある問題

1. **SparkSessionが見つからない**
   ```python
   # 解決方法: Databricks環境で実行していることを確認
   from pyspark.sql import SparkSession
   spark = SparkSession.builder.getOrCreate()
   ```

2. **テーブルが見つからない**
   ```python
   # 解決方法: 正しいカタログ・スキーマを指定
   tables = get_tables(catalog="your_catalog", schema="your_schema")
   ```

3. **権限エラー**
   ```python
   # 解決方法: 適切な権限を持つユーザーで実行
   # または、テーブルへのアクセス権限を確認
   ```

### デバッグ方法

```python
# 1. 接続状態を確認
db = create_databricks_database_component("debug-db")
print("Component created successfully")

# 2. 簡単なクエリでテスト
try:
    result = execute_sql("SELECT current_timestamp()")
    print("Basic query works")
except Exception as e:
    print(f"Basic query failed: {e}")

# 3. テーブル一覧でテスト
try:
    tables = get_tables()
    print(f"Found {len(tables)} tables")
except Exception as e:
    print(f"Table listing failed: {e}")
```

## 制限事項

1. **Databricks環境専用**: このコンポーネントはDatabricksノートブック環境でのみ動作します
2. **SparkSession依存**: SparkSessionが利用可能である必要があります
3. **権限制限**: データベースへのアクセス権限が必要です
4. **メモリ制限**: 大量データの場合はメモリ使用量に注意してください

## サポート

問題が発生した場合は、以下を確認してください：

1. Databricks環境で実行しているか
2. 必要な権限があるか
3. 正しいカタログ・スキーマを指定しているか
4. SQLクエリの構文が正しいか

詳細なログを確認するには：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```