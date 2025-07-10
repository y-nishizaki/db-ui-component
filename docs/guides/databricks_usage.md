# Databricksでの使用ガイド

このガイドでは、Databricks環境でDatabricks UI Component Libraryを使用する方法を詳しく説明します。

## 🎯 概要

Databricks UI Component Libraryは、Databricksの`displayHTML`関数と完全に互換性があり、ノートブック内で美しいダッシュボードを作成できます。

## 🚀 基本的な使用方法

### 1. ライブラリのインポート

```python
# 必要なライブラリをインポート
from db_ui_components import ChartComponent, TableComponent, Dashboard
import pandas as pd
import numpy as np
```

### 2. サンプルデータの作成

```python
# サンプルデータの作成
np.random.seed(42)
dates = pd.date_range('2024-01-01', periods=30, freq='D')
data = {
    'date': dates,
    'sales': np.random.normal(1000, 200, 30),
    'profit': np.random.normal(200, 50, 30),
    'category': np.random.choice(['A', 'B', 'C'], 30)
}
df = pd.DataFrame(data)
```

### 3. コンポーネントの作成と表示

```python
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

## 📊 実践的な例

### 売上ダッシュボード

```python
import pandas as pd
import numpy as np
from db_ui_components import ChartComponent, TableComponent, Dashboard

# データの準備
np.random.seed(42)
dates = pd.date_range('2024-01-01', periods=100, freq='D')
data = {
    'date': dates,
    'sales': np.random.normal(1000, 200, 100),
    'profit': np.random.normal(200, 50, 100),
    'category': np.random.choice(['Electronics', 'Clothing', 'Books'], 100),
    'region': np.random.choice(['North', 'South', 'East', 'West'], 100)
}
df = pd.DataFrame(data)

# コンポーネントの作成
sales_chart = ChartComponent(
    data=df,
    chart_type='line',
    x_column='date',
    y_column='sales',
    title='売上推移'
)

profit_chart = ChartComponent(
    data=df,
    chart_type='line',
    x_column='date',
    y_column='profit',
    title='利益推移'
)

category_sales = df.groupby('category')['sales'].sum().reset_index()
category_chart = ChartComponent(
    data=category_sales,
    chart_type='pie',
    x_column='category',
    y_column='sales',
    title='カテゴリ別売上'
)

data_table = TableComponent(
    data=df.head(20),
    enable_csv_download=True,
    sortable=True,
    searchable=True
)

# ダッシュボードの作成
dashboard = Dashboard(title='売上ダッシュボード')
dashboard.add_component(sales_chart, position=(0, 0))
dashboard.add_component(profit_chart, position=(0, 1))
dashboard.add_component(category_chart, position=(1, 0))
dashboard.add_component(data_table, position=(1, 1))

# 表示
displayHTML(dashboard.render())
```

## 🔄 インタラクティブなダッシュボード

### フィルター機能

```python
from db_ui_components import FilterComponent

# フィルターコンポーネントの作成
date_filter = FilterComponent(
    filter_type='date',
    column='date',
    title='日付範囲'
)

category_filter = FilterComponent(
    filter_type='dropdown',
    column='category',
    options=['Electronics', 'Clothing', 'Books'],
    title='カテゴリ'
)

region_filter = FilterComponent(
    filter_type='multiselect',
    column='region',
    options=['North', 'South', 'East', 'West'],
    title='地域'
)

# フィルターされたデータでグラフを更新する関数
def update_charts(filtered_data):
    sales_chart.update_data(filtered_data)
    profit_chart.update_data(filtered_data)
    data_table.update_data(filtered_data.head(20))

# フィルターイベントの設定
date_filter.on_change(update_charts)
category_filter.on_change(update_charts)
region_filter.on_change(update_charts)

# ダッシュボードにフィルターを追加
dashboard.add_component(date_filter, position=(0, 0))
dashboard.add_component(category_filter, position=(0, 1))
dashboard.add_component(region_filter, position=(0, 2))

displayHTML(dashboard.render())
```

## 🗄️ データベースとの連携

### Databricks SQLとの連携

```python
from db_ui_components import DatabaseComponent

# データベースコンポーネントの作成
db_component = DatabaseComponent(
    connection_string="your_databricks_sql_connection",
    query="SELECT * FROM sales_data WHERE date >= '2024-01-01'"
)

# データの取得
sales_data = db_component.execute_query()

# グラフの作成
chart = ChartComponent(
    data=sales_data,
    chart_type='line',
    x_column='date',
    y_column='sales',
    title='データベースからの売上データ'
)

displayHTML(chart.render())
```

### Spark DataFrameとの連携

```python
# Spark DataFrameからPandas DataFrameへの変換
spark_df = spark.sql("SELECT * FROM sales_data")
pandas_df = spark_df.toPandas()

# グラフの作成
chart = ChartComponent(
    data=pandas_df,
    chart_type='bar',
    x_column='category',
    y_column='sales',
    title='Sparkデータからの売上'
)

displayHTML(chart.render())
```

## 🎨 カスタマイズとスタイリング

### テーマの適用

```python
# ダークテーマの適用
dashboard.set_theme('dark')

# カスタムスタイルの設定
dashboard.set_style({
    'backgroundColor': '#1e1e1e',
    'color': '#ffffff',
    'fontFamily': 'Arial, sans-serif',
    'borderRadius': '8px',
    'padding': '16px'
})

displayHTML(dashboard.render())
```

### レスポンシブデザイン

```python
# レスポンシブ対応のダッシュボード
dashboard = Dashboard(
    title='レスポンシブダッシュボード',
    layout='responsive',
    responsive_breakpoints={
        'mobile': 768,
        'tablet': 1024,
        'desktop': 1200
    }
)
```

## 📈 パフォーマンス最適化

### 大量データの処理

```python
# データのサンプリング
large_df = spark.sql("SELECT * FROM large_table").toPandas()
sampled_df = large_df.sample(n=10000, random_state=42)

# 集約データの使用
aggregated_df = large_df.groupby(['category', 'region']).agg({
    'sales': 'sum',
    'profit': 'sum'
}).reset_index()

# グラフの作成
chart = ChartComponent(
    data=aggregated_df,
    chart_type='bar',
    x_column='category',
    y_column='sales',
    title='集約された売上データ'
)
```

### キャッシュの活用

```python
# データのキャッシュ
@cache
def get_sales_data():
    return spark.sql("SELECT * FROM sales_data").toPandas()

# キャッシュされたデータを使用
sales_data = get_sales_data()
chart = ChartComponent(data=sales_data, chart_type='line', x_column='date', y_column='sales')
```

## 🔧 高度な機能

### リアルタイム更新

```python
import time
from IPython.display import clear_output

# リアルタイム更新の例
for i in range(10):
    # 新しいデータの生成
    new_data = pd.DataFrame({
        'timestamp': pd.date_range('2024-01-01', periods=30, freq='D'),
        'value': np.random.normal(100, 20, 30)
    })
    
    # グラフの更新
    chart.update_data(new_data)
    
    # 表示の更新
    clear_output(wait=True)
    displayHTML(chart.render())
    
    time.sleep(2)  # 2秒待機
```

### 条件付き表示

```python
# 条件に基づいてコンポーネントを表示
if len(df) > 100:
    # 大量データの場合は集約グラフ
    aggregated_df = df.groupby('category')['sales'].sum().reset_index()
    chart = ChartComponent(
        data=aggregated_df,
        chart_type='pie',
        x_column='category',
        y_column='sales',
        title='カテゴリ別売上（集約）'
    )
else:
    # 少量データの場合は詳細グラフ
    chart = ChartComponent(
        data=df,
        chart_type='line',
        x_column='date',
        y_column='sales',
        title='売上推移（詳細）'
    )

displayHTML(chart.render())
```

## 🛠️ トラブルシューティング

### よくある問題と解決方法

#### 1. メモリ不足エラー

```python
# データサイズの制限
df_limited = df.head(1000)  # 最初の1000行のみ使用

# または、データの集約
df_aggregated = df.groupby('category').agg({
    'sales': 'sum',
    'profit': 'sum'
}).reset_index()
```

#### 2. 表示エラー

```python
# HTMLの確認
html_output = chart.render()
print(f"HTML長さ: {len(html_output)}")

# エラーハンドリング
try:
    displayHTML(chart.render())
except Exception as e:
    print(f"表示エラー: {e}")
    # フォールバック表示
    display(df.head())
```

#### 3. パフォーマンス問題

```python
# プロファイリング
import time

start_time = time.time()
chart = ChartComponent(data=df, chart_type='line', x_column='date', y_column='sales')
render_time = time.time() - start_time
print(f"レンダリング時間: {render_time:.2f}秒")
```

## 📚 ベストプラクティス

### 1. データの前処理

```python
# データのクリーニング
df_clean = df.dropna()  # 欠損値の削除
df_clean = df_clean[df_clean['sales'] > 0]  # 異常値の除去

# データ型の最適化
df_clean['date'] = pd.to_datetime(df_clean['date'])
df_clean['category'] = df_clean['category'].astype('category')
```

### 2. エラーハンドリング

```python
def safe_render(component, fallback_html=""):
    """安全なレンダリング関数"""
    try:
        return component.render()
    except Exception as e:
        print(f"レンダリングエラー: {e}")
        return fallback_html

# 使用例
html_output = safe_render(chart, "<p>グラフの表示に失敗しました</p>")
displayHTML(html_output)
```

### 3. ログ出力

```python
import logging

# ログの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ログ付きのコンポーネント作成
def create_chart_with_logging(data, **kwargs):
    logger.info(f"グラフの作成開始: {kwargs}")
    try:
        chart = ChartComponent(data=data, **kwargs)
        logger.info("グラフの作成完了")
        return chart
    except Exception as e:
        logger.error(f"グラフの作成失敗: {e}")
        raise
```

## � 次のステップ

- [パフォーマンス最適化](./performance.md) - パフォーマンスの最適化
- [セキュリティ](./security.md) - セキュリティのベストプラクティス
- [デプロイメント](./deployment.md) - 本番環境へのデプロイ

## ❓ サポート

問題が発生した場合は、以下を確認してください：

- [よくある問題](../troubleshooting/faq.md)
- [エラーリファレンス](../troubleshooting/errors.md)
- [GitHub Issues](https://github.com/databricks/db-ui-components/issues)