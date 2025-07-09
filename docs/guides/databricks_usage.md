# Databricksでの使用ガイド

このガイドでは、Databricks環境でDatabricks UI Component Libraryを使用する方法を詳しく説明します。

## 🚀 Databricks環境でのセットアップ

### 1. インストール

#### Databricks Runtime 10.4以上

```python
# ノートブックの最初のセルで実行
!pip install db-ui-components

# インストール確認
import db_ui_components
print(f"バージョン: {db_ui_components.__version__}")
```

#### Databricks Runtime 10.4未満

```python
# 依存関係を個別にインストール
!pip install pandas>=1.5.0
!pip install numpy>=1.21.0
!pip install plotly>=5.0.0
!pip install dash>=2.0.0
!pip install db-ui-components
```

### 2. 基本的な使用例

```python
# 必要なライブラリをインポート
import pandas as pd
import numpy as np
from db_ui_components import ChartComponent, TableComponent, Dashboard

# サンプルデータの作成
np.random.seed(42)
df = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=30, freq='D'),
    'sales': np.random.normal(1000, 200, 30),
    'profit': np.random.normal(200, 50, 30)
})

# グラフコンポーネントの作成
chart = ChartComponent(
    data=df,
    chart_type='line',
    x_column='date',
    y_column='sales',
    title='売上推移'
)

# Databricksで表示
displayHTML(chart.render())
```

## 📊 Databricksでのデータ処理

### 1. Delta Lakeからのデータ読み込み

```python
# Deltaテーブルからデータを読み込み
df = spark.read.format("delta").load("/path/to/your/table").toPandas()

# データの前処理
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

# グラフコンポーネントで表示
chart = ChartComponent(
    data=df,
    chart_type='line',
    x_column='date',
    y_column='sales',
    title='Delta Lakeからの売上データ'
)

displayHTML(chart.render())
```

### 2. Spark DataFrameの変換

```python
# Spark DataFrameをPandas DataFrameに変換
spark_df = spark.sql("SELECT * FROM sales_table WHERE date >= '2024-01-01'")
df = spark_df.toPandas()

# データの集約
daily_sales = df.groupby('date')['sales'].sum().reset_index()

# グラフで表示
chart = ChartComponent(
    data=daily_sales,
    chart_type='bar',
    x_column='date',
    y_column='sales',
    title='日次売上集計'
)

displayHTML(chart.render())
```

### 3. 大量データの処理

```python
# 大量データのサンプリング
large_df = spark.read.format("delta").load("/path/to/large/table")

# サンプリングしてからPandasに変換
sampled_df = large_df.sample(fraction=0.1, seed=42).toPandas()

# または、特定の期間のデータのみを取得
recent_df = large_df.filter("date >= '2024-01-01'").toPandas()

# グラフで表示
chart = ChartComponent(
    data=sampled_df,
    chart_type='line',
    x_column='date',
    y_column='sales',
    title='大量データのサンプリング結果'
)

displayHTML(chart.render())
```

## 🎛️ Databricksでのダッシュボード作成

### 1. 基本的なダッシュボード

```python
from db_ui_components import Dashboard, ChartComponent, TableComponent

# データの準備
sales_data = spark.sql("""
    SELECT 
        date,
        SUM(sales) as total_sales,
        SUM(profit) as total_profit,
        COUNT(*) as transaction_count
    FROM sales_table 
    WHERE date >= '2024-01-01'
    GROUP BY date
    ORDER BY date
""").toPandas()

# ダッシュボードの作成
dashboard = Dashboard(title='Databricks売上ダッシュボード')

# 売上推移グラフ
sales_chart = ChartComponent(
    data=sales_data,
    chart_type='line',
    x_column='date',
    y_column='total_sales',
    title='売上推移'
)
dashboard.add_component(sales_chart, position=(0, 0))

# 利益推移グラフ
profit_chart = ChartComponent(
    data=sales_data,
    chart_type='line',
    x_column='date',
    y_column='total_profit',
    title='利益推移'
)
dashboard.add_component(profit_chart, position=(0, 1))

# 詳細テーブル
detail_table = TableComponent(
    data=sales_data,
    enable_csv_download=True,
    sortable=True,
    searchable=True,
    title='売上詳細'
)
dashboard.add_component(detail_table, position=(1, 0))

# 表示
displayHTML(dashboard.render())
```

### 2. リアルタイムデータ更新

```python
# 定期的なデータ更新
import time
from datetime import datetime

def update_dashboard():
    """ダッシュボードを定期的に更新"""
    while True:
        # 最新データを取得
        latest_data = spark.sql("""
            SELECT 
                date,
                SUM(sales) as total_sales
            FROM sales_table 
            WHERE date >= DATE_SUB(CURRENT_DATE(), 30)
            GROUP BY date
            ORDER BY date
        """).toPandas()
        
        # グラフを更新
        chart = ChartComponent(
            data=latest_data,
            chart_type='line',
            x_column='date',
            y_column='total_sales',
            title=f'リアルタイム売上推移 (更新: {datetime.now().strftime("%H:%M:%S")})'
        )
        
        # 表示
        displayHTML(chart.render())
        
        # 5分待機
        time.sleep(300)

# バックグラウンドで実行（注意: 実際の使用では適切なスケジューリングを使用）
# update_dashboard()
```

## 🔍 Databricksでのフィルター機能

### 1. 動的フィルター

```python
from db_ui_components import FilterComponent

# 利用可能なカテゴリを取得
categories = spark.sql("SELECT DISTINCT category FROM sales_table").toPandas()['category'].tolist()

# カテゴリフィルター
category_filter = FilterComponent(
    filter_type='dropdown',
    column='category',
    options=categories,
    placeholder='カテゴリを選択',
    title='カテゴリフィルター'
)

displayHTML(category_filter.render())

# フィルター結果を表示
def show_filtered_data(selected_category):
    """選択されたカテゴリのデータを表示"""
    filtered_data = spark.sql(f"""
        SELECT * FROM sales_table 
        WHERE category = '{selected_category}'
        ORDER BY date
    """).toPandas()
    
    chart = ChartComponent(
        data=filtered_data,
        chart_type='line',
        x_column='date',
        y_column='sales',
        title=f'{selected_category}カテゴリの売上'
    )
    
    displayHTML(chart.render())
```

### 2. 日付範囲フィルター

```python
# 日付範囲の取得
date_range = spark.sql("""
    SELECT 
        MIN(date) as min_date,
        MAX(date) as max_date
    FROM sales_table
""").toPandas()

# 日付範囲フィルター
date_filter = FilterComponent(
    filter_type='date',
    column='date',
    start_date=date_range['min_date'].iloc[0],
    end_date=date_range['max_date'].iloc[0],
    title='日付範囲フィルター'
)

displayHTML(date_filter.render())
```

## 📈 パフォーマンス最適化

### 1. データキャッシュ

```python
# 頻繁に使用するデータをキャッシュ
frequently_used_data = spark.sql("""
    SELECT 
        date,
        category,
        region,
        SUM(sales) as total_sales,
        SUM(profit) as total_profit
    FROM sales_table 
    WHERE date >= '2024-01-01'
    GROUP BY date, category, region
""").cache()

# Pandas DataFrameに変換
df = frequently_used_data.toPandas()

# グラフで表示
chart = ChartComponent(
    data=df,
    chart_type='line',
    x_column='date',
    y_column='total_sales',
    title='キャッシュされた売上データ'
)

displayHTML(chart.render())
```

### 2. データサンプリング

```python
# 大量データのサンプリング
def get_sampled_data(table_path, sample_fraction=0.1):
    """大量データからサンプリング"""
    df = spark.read.format("delta").load(table_path)
    sampled_df = df.sample(fraction=sample_fraction, seed=42)
    return sampled_df.toPandas()

# サンプリングしたデータでグラフ作成
sampled_data = get_sampled_data("/path/to/large/table", 0.05)

chart = ChartComponent(
    data=sampled_data,
    chart_type='scatter',
    x_column='sales',
    y_column='profit',
    title='サンプリングされた売上・利益データ'
)

displayHTML(chart.render())
```

## 🔧 トラブルシューティング

### 1. メモリ不足の対処

```python
# データサイズを制限
def limit_data_size(df, max_rows=10000):
    """データサイズを制限"""
    if len(df) > max_rows:
        return df.sample(n=max_rows, random_state=42)
    return df

# 制限されたデータでグラフ作成
limited_data = limit_data_size(df, 5000)

chart = ChartComponent(
    data=limited_data,
    chart_type='line',
    x_column='date',
    y_column='sales',
    title='制限された売上データ'
)

displayHTML(chart.render())
```

### 2. データ型の問題

```python
# データ型の確認と修正
def fix_data_types(df):
    """データ型を修正"""
    # 日付列の修正
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    # 数値列の修正
    numeric_columns = ['sales', 'profit']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

# データ型を修正してからグラフ作成
fixed_data = fix_data_types(df)

chart = ChartComponent(
    data=fixed_data,
    chart_type='line',
    x_column='date',
    y_column='sales',
    title='データ型修正済み売上データ'
)

displayHTML(chart.render())
```

## 🎯 実践的な例

### 完全なDatabricks分析ダッシュボード

```python
# 包括的な分析ダッシュボード
def create_comprehensive_dashboard():
    """包括的な分析ダッシュボードを作成"""
    
    # 1. 売上サマリー
    sales_summary = spark.sql("""
        SELECT 
            DATE_TRUNC('month', date) as month,
            SUM(sales) as total_sales,
            SUM(profit) as total_profit,
            COUNT(*) as transaction_count
        FROM sales_table 
        WHERE date >= '2024-01-01'
        GROUP BY DATE_TRUNC('month', date)
        ORDER BY month
    """).toPandas()
    
    # 2. カテゴリ別分析
    category_analysis = spark.sql("""
        SELECT 
            category,
            SUM(sales) as total_sales,
            AVG(sales) as avg_sales,
            COUNT(*) as transaction_count
        FROM sales_table 
        WHERE date >= '2024-01-01'
        GROUP BY category
        ORDER BY total_sales DESC
    """).toPandas()
    
    # 3. 地域別分析
    region_analysis = spark.sql("""
        SELECT 
            region,
            SUM(sales) as total_sales,
            SUM(profit) as total_profit
        FROM sales_table 
        WHERE date >= '2024-01-01'
        GROUP BY region
        ORDER BY total_sales DESC
    """).toPandas()
    
    # ダッシュボードの作成
    dashboard = Dashboard(title='Databricks包括的分析ダッシュボード')
    
    # 月次売上推移
    monthly_chart = ChartComponent(
        data=sales_summary,
        chart_type='line',
        x_column='month',
        y_column='total_sales',
        title='月次売上推移'
    )
    dashboard.add_component(monthly_chart, position=(0, 0))
    
    # カテゴリ別売上
    category_chart = ChartComponent(
        data=category_analysis,
        chart_type='bar',
        x_column='category',
        y_column='total_sales',
        title='カテゴリ別売上'
    )
    dashboard.add_component(category_chart, position=(0, 1))
    
    # 地域別売上
    region_chart = ChartComponent(
        data=region_analysis,
        chart_type='pie',
        x_column='region',
        y_column='total_sales',
        title='地域別売上構成'
    )
    dashboard.add_component(region_chart, position=(1, 0))
    
    # 詳細テーブル
    detail_table = TableComponent(
        data=sales_summary,
        enable_csv_download=True,
        sortable=True,
        searchable=True,
        title='月次売上詳細'
    )
    dashboard.add_component(detail_table, position=(1, 1))
    
    return dashboard

# ダッシュボードの作成と表示
dashboard = create_comprehensive_dashboard()
displayHTML(dashboard.render())
```

## 📚 次のステップ

- [パフォーマンス最適化](./performance.md) - Databricksでのパフォーマンス改善
- [セキュリティ](./security.md) - セキュリティのベストプラクティス
- [トラブルシューティング](../troubleshooting/faq.md) - よくある問題と解決方法

## ❓ サポート

Databricksでの使用で問題が発生した場合は：

1. **クラスター設定**の確認
2. **メモリ使用量**の監視
3. **データサイズ**の確認
4. **エラーログ**の確認

**関連リンク:**
- [インストールガイド](./installation.md) - 詳細なインストール手順
- [よくある問題](../troubleshooting/faq.md) - Databricks関連のFAQ