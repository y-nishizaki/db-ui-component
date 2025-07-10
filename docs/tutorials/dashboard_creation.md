# ダッシュボード作成チュートリアル

このチュートリアルでは、Databricks UI Component Libraryを使用して複雑なダッシュボードを作成する方法を説明します。

## 🎯 概要

ダッシュボードは、複数のコンポーネントを組み合わせて、包括的なデータビューを作成するための機能です。

## 📊 基本的なダッシュボード

### 1. ダッシュボードの初期化

```python
from db_ui_components import Dashboard, ChartComponent, TableComponent
import pandas as pd
import numpy as np

# サンプルデータの作成
np.random.seed(42)
dates = pd.date_range('2024-01-01', periods=100, freq='D')
data = {
    'date': dates,
    'sales': np.random.normal(1000, 200, 100),
    'profit': np.random.normal(200, 50, 100),
    'category': np.random.choice(['A', 'B', 'C'], 100),
    'region': np.random.choice(['North', 'South', 'East', 'West'], 100)
}
df = pd.DataFrame(data)

# ダッシュボードの作成
dashboard = Dashboard(title='売上ダッシュボード')
```

### 2. コンポーネントの追加

```python
# 売上推移グラフ
sales_chart = ChartComponent(
    data=df,
    chart_type='line',
    x_column='date',
    y_column='sales',
    title='売上推移'
)

# 利益推移グラフ
profit_chart = ChartComponent(
    data=df,
    chart_type='line',
    x_column='date',
    y_column='profit',
    title='利益推移'
)

# カテゴリ別売上（棒グラフ）
category_sales = df.groupby('category')['sales'].sum().reset_index()
category_chart = ChartComponent(
    data=category_sales,
    chart_type='bar',
    x_column='category',
    y_column='sales',
    title='カテゴリ別売上'
)

# データテーブル
data_table = TableComponent(
    data=df.head(20),
    enable_csv_download=True,
    sortable=True,
    searchable=True
)

# ダッシュボードにコンポーネントを追加
dashboard.add_component(sales_chart, position=(0, 0))
dashboard.add_component(profit_chart, position=(0, 1))
dashboard.add_component(category_chart, position=(1, 0))
dashboard.add_component(data_table, position=(1, 1))
```

### 3. ダッシュボードの表示

```python
# ダッシュボードを表示
displayHTML(dashboard.render())
```

## 🎨 レイアウトのカスタマイズ

### グリッドレイアウト

```python
# 3x3のグリッドレイアウト
dashboard = Dashboard(
    title='売上ダッシュボード',
    layout='grid',
    grid_size=(3, 3)
)

# コンポーネントを配置
dashboard.add_component(sales_chart, position=(0, 0), size=(1, 2))  # 2列分の幅
dashboard.add_component(profit_chart, position=(0, 2))
dashboard.add_component(category_chart, position=(1, 0), size=(2, 1))  # 2行分の高さ
dashboard.add_component(data_table, position=(2, 0), size=(1, 3))  # 3列分の幅
```

### レスポンシブレイアウト

```python
# レスポンシブ対応のダッシュボード
dashboard = Dashboard(
    title='売上ダッシュボード',
    layout='responsive',
    responsive_breakpoints={
        'mobile': 768,
        'tablet': 1024,
        'desktop': 1200
    }
)
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
    options=['A', 'B', 'C'],
    title='カテゴリ'
)

region_filter = FilterComponent(
    filter_type='multiselect',
    column='region',
    options=['North', 'South', 'East', 'West'],
    title='地域'
)

# フィルターをダッシュボードに追加
dashboard.add_component(date_filter, position=(0, 0))
dashboard.add_component(category_filter, position=(0, 1))
dashboard.add_component(region_filter, position=(0, 2))
```

### フィルターとグラフの連動

```python
# フィルターされたデータでグラフを更新
def update_charts(filtered_data):
    sales_chart.update_data(filtered_data)
    profit_chart.update_data(filtered_data)
    data_table.update_data(filtered_data.head(20))

# フィルターイベントの設定
date_filter.on_change(update_charts)
category_filter.on_change(update_charts)
region_filter.on_change(update_charts)
```

## 📈 高度なダッシュボード

### 複数のデータソース

```python
from db_ui_components import DatabaseComponent

# データベースコンポーネント
db_component = DatabaseComponent(
    connection_string="your_connection_string",
    query="SELECT * FROM sales_data WHERE date >= '2024-01-01'"
)

# リアルタイムデータ更新
def refresh_data():
    new_data = db_component.execute_query()
    sales_chart.update_data(new_data)
    profit_chart.update_data(new_data)

# 自動更新の設定（5分間隔）
dashboard.set_auto_refresh(refresh_data, interval=300)
```

### カスタムスタイリング

```python
# ダッシュボードのスタイル設定
dashboard.set_style({
    'backgroundColor': '#f8f9fa',
    'borderRadius': '12px',
    'padding': '20px',
    'fontFamily': 'Arial, sans-serif',
    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
})

# 個別コンポーネントのスタイル設定
sales_chart.set_style({
    'backgroundColor': '#ffffff',
    'borderRadius': '8px',
    'padding': '16px',
    'border': '1px solid #e9ecef'
})
```

## 🎯 実践的な例

### 完全な売上ダッシュボード

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from db_ui_components import (
    Dashboard, ChartComponent, TableComponent, 
    FilterComponent, DatabaseComponent
)

# データの準備
def create_sample_data():
    np.random.seed(42)
    dates = pd.date_range('2024-01-01', periods=365, freq='D')
    data = {
        'date': dates,
        'sales': np.random.normal(1000, 200, 365),
        'profit': np.random.normal(200, 50, 365),
        'category': np.random.choice(['Electronics', 'Clothing', 'Books'], 365),
        'region': np.random.choice(['North', 'South', 'East', 'West'], 365),
        'customer_type': np.random.choice(['New', 'Returning', 'VIP'], 365)
    }
    return pd.DataFrame(data)

df = create_sample_data()

# ダッシュボードの作成
dashboard = Dashboard(
    title='売上分析ダッシュボード',
    layout='grid',
    grid_size=(4, 4)
)

# コンポーネントの作成
sales_trend = ChartComponent(
    data=df,
    chart_type='line',
    x_column='date',
    y_column='sales',
    title='売上推移'
)

profit_trend = ChartComponent(
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

region_sales = df.groupby('region')['sales'].sum().reset_index()
region_chart = ChartComponent(
    data=region_sales,
    chart_type='bar',
    x_column='region',
    y_column='sales',
    title='地域別売上'
)

# フィルター
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

# テーブル
summary_table = TableComponent(
    data=df.groupby(['category', 'region']).agg({
        'sales': 'sum',
        'profit': 'sum'
    }).reset_index(),
    enable_csv_download=True,
    sortable=True,
    searchable=True
)

# ダッシュボードにコンポーネントを追加
dashboard.add_component(date_filter, position=(0, 0), size=(1, 2))
dashboard.add_component(category_filter, position=(0, 2), size=(1, 2))
dashboard.add_component(sales_trend, position=(1, 0), size=(1, 2))
dashboard.add_component(profit_trend, position=(1, 2), size=(1, 2))
dashboard.add_component(category_chart, position=(2, 0))
dashboard.add_component(region_chart, position=(2, 1))
dashboard.add_component(summary_table, position=(3, 0), size=(1, 4))

# 表示
displayHTML(dashboard.render())
```

## 🚀 次のステップ

- [高度な可視化](./advanced_visualization.md) - 高度な可視化コンポーネントの使用
- [カスタマイズ](./customization.md) - スタイルとカスタマイズ
- [API リファレンス](../api/dashboard.md) - ダッシュボードAPIの詳細

## ❓ よくある質問

**Q: ダッシュボードのサイズを変更できますか？**
A: はい、`grid_size`パラメータでグリッドサイズを設定できます。

**Q: コンポーネントの位置を動的に変更できますか？**
A: はい、`move_component`メソッドを使用してコンポーネントの位置を変更できます。

**Q: ダッシュボードを保存できますか？**
A: はい、`save_layout`メソッドでレイアウトを保存し、`load_layout`で読み込めます。