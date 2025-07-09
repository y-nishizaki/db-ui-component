# 基本使用法チュートリアル

このチュートリアルでは、Databricks UI Component Libraryの基本的な使用方法を段階的に説明します。

## 📋 目次

1. [準備](#準備)
2. [ChartComponentの基本](#chartcomponentの基本)
3. [TableComponentの基本](#tablecomponentの基本)
4. [FilterComponentの基本](#filtercomponentの基本)
5. [Dashboardの基本](#dashboardの基本)
6. [実践的な例](#実践的な例)

## 🚀 準備

### 必要なライブラリのインポート

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from db_ui_components import ChartComponent, TableComponent, FilterComponent, Dashboard
```

### サンプルデータの作成

```python
# サンプルデータを作成
np.random.seed(42)
dates = pd.date_range('2024-01-01', periods=100, freq='D')

data = {
    'date': dates,
    'sales': np.random.normal(1000, 200, 100),
    'profit': np.random.normal(200, 50, 100),
    'category': np.random.choice(['A', 'B', 'C'], 100),
    'region': np.random.choice(['North', 'South', 'East', 'West'], 100),
    'customer_count': np.random.randint(50, 200, 100)
}

df = pd.DataFrame(data)
print(f"データ形状: {df.shape}")
print(f"データ列: {df.columns.tolist()}")
```

## 📊 ChartComponentの基本

### 1. 基本的な折れ線グラフ

```python
# 基本的な折れ線グラフ
sales_chart = ChartComponent(
    data=df,
    chart_type='line',
    x_column='date',
    y_column='sales',
    title='売上推移'
)

# 表示
displayHTML(sales_chart.render())
```

### 2. 棒グラフの作成

```python
# カテゴリ別売上の棒グラフ
category_sales = df.groupby('category')['sales'].sum().reset_index()

category_chart = ChartComponent(
    data=category_sales,
    chart_type='bar',
    x_column='category',
    y_column='sales',
    title='カテゴリ別売上',
    height=400
)

displayHTML(category_chart.render())
```

### 3. 円グラフの作成

```python
# 地域別売上の円グラフ
region_sales = df.groupby('region')['sales'].sum().reset_index()

region_chart = ChartComponent(
    data=region_sales,
    chart_type='pie',
    x_column='region',
    y_column='sales',
    title='地域別売上構成'
)

displayHTML(region_chart.render())
```

### 4. 散布図の作成

```python
# 売上と利益の相関関係
correlation_chart = ChartComponent(
    data=df,
    chart_type='scatter',
    x_column='sales',
    y_column='profit',
    title='売上と利益の相関'
)

displayHTML(correlation_chart.render())
```

## 📋 TableComponentの基本

### 1. 基本的なテーブル

```python
# 基本的なテーブル
basic_table = TableComponent(
    data=df.head(20),
    title='売上データ'
)

displayHTML(basic_table.render())
```

### 2. 機能付きテーブル

```python
# CSVダウンロード、ソート、検索機能付きテーブル
advanced_table = TableComponent(
    data=df,
    enable_csv_download=True,
    sortable=True,
    searchable=True,
    page_size=10,
    title='売上データ（機能付き）'
)

displayHTML(advanced_table.render())
```

### 3. カスタム列設定

```python
# 特定の列のみを表示
custom_table = TableComponent(
    data=df,
    columns=['date', 'sales', 'profit', 'category'],
    enable_csv_download=True,
    sortable=True,
    title='売上・利益データ'
)

displayHTML(custom_table.render())
```

## 🔍 FilterComponentの基本

### 1. ドロップダウンフィルター

```python
# カテゴリフィルター
category_filter = FilterComponent(
    filter_type='dropdown',
    column='category',
    options=df['category'].unique().tolist(),
    placeholder='カテゴリを選択',
    title='カテゴリフィルター'
)

displayHTML(category_filter.render())
```

### 2. マルチセレクトフィルター

```python
# 地域マルチセレクトフィルター
region_filter = FilterComponent(
    filter_type='multiselect',
    column='region',
    options=df['region'].unique().tolist(),
    placeholder='地域を選択',
    title='地域フィルター'
)

displayHTML(region_filter.render())
```

### 3. 日付範囲フィルター

```python
# 日付範囲フィルター
date_filter = FilterComponent(
    filter_type='date',
    column='date',
    start_date=df['date'].min(),
    end_date=df['date'].max(),
    title='日付範囲フィルター'
)

displayHTML(date_filter.render())
```

### 4. テキスト検索フィルター

```python
# テキスト検索フィルター
search_filter = FilterComponent(
    filter_type='text',
    column='category',
    placeholder='カテゴリを検索',
    title='検索フィルター'
)

displayHTML(search_filter.render())
```

## 🎛️ Dashboardの基本

### 1. 基本的なダッシュボード

```python
# ダッシュボードを作成
dashboard = Dashboard(title='売上ダッシュボード')

# コンポーネントを追加
dashboard.add_component(sales_chart, position=(0, 0))
dashboard.add_component(advanced_table, position=(1, 0))

# 表示
displayHTML(dashboard.render())
```

### 2. 複数コンポーネントのダッシュボード

```python
# より複雑なダッシュボード
complex_dashboard = Dashboard(title='総合売上ダッシュボード')

# グラフを追加
complex_dashboard.add_component(sales_chart, position=(0, 0))
complex_dashboard.add_component(category_chart, position=(0, 1))
complex_dashboard.add_component(region_chart, position=(1, 0))

# テーブルを追加
complex_dashboard.add_component(advanced_table, position=(1, 1))

# フィルターを追加
complex_dashboard.add_component(category_filter, position=(2, 0))
complex_dashboard.add_component(region_filter, position=(2, 1))

# 表示
displayHTML(complex_dashboard.render())
```

## 🎨 スタイリングとカスタマイズ

### 1. グラフのスタイリング

```python
# カスタムスタイルを適用
styled_chart = ChartComponent(
    data=df,
    chart_type='line',
    x_column='date',
    y_column='sales',
    title='カスタムスタイルのグラフ',
    height=500,
    color='#ff6b6b'
)

# スタイルを設定
styled_chart.set_style({
    'backgroundColor': '#f8f9fa',
    'borderRadius': '10px',
    'padding': '20px',
    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
})

displayHTML(styled_chart.render())
```

### 2. ダッシュボードのスタイリング

```python
# スタイル付きダッシュボード
styled_dashboard = Dashboard(
    title='スタイル付きダッシュボード',
    theme='dark'  # ダークテーマ
)

styled_dashboard.add_component(styled_chart, position=(0, 0))
styled_dashboard.add_component(advanced_table, position=(1, 0))

# ダッシュボードのスタイルを設定
styled_dashboard.set_style({
    'backgroundColor': '#2c3e50',
    'color': '#ecf0f1',
    'padding': '20px'
})

displayHTML(styled_dashboard.render())
```

## 🔄 データ更新とインタラクティブ機能

### 1. 動的データ更新

```python
# 初期データでグラフを作成
dynamic_chart = ChartComponent(
    data=df.head(50),
    chart_type='line',
    x_column='date',
    y_column='sales',
    title='動的更新グラフ'
)

displayHTML(dynamic_chart.render())

# データを更新
new_data = df.tail(50)
dynamic_chart.update_data(new_data)
displayHTML(dynamic_chart.render())
```

### 2. フィルターとグラフの連動

```python
# フィルター付きグラフ
filtered_chart = ChartComponent(
    data=df[df['category'] == 'A'],  # フィルター済みデータ
    chart_type='line',
    x_column='date',
    y_column='sales',
    title='カテゴリAの売上推移'
)

displayHTML(filtered_chart.render())
```

## 🎯 実践的な例

### 完全な売上分析ダッシュボード

```python
# データの準備
sales_summary = df.groupby(['category', 'region']).agg({
    'sales': 'sum',
    'profit': 'sum',
    'customer_count': 'sum'
}).reset_index()

# ダッシュボードの作成
analysis_dashboard = Dashboard(title='売上分析ダッシュボード')

# 1. 売上推移グラフ
trend_chart = ChartComponent(
    data=df.groupby('date')['sales'].sum().reset_index(),
    chart_type='line',
    x_column='date',
    y_column='sales',
    title='日次売上推移'
)
analysis_dashboard.add_component(trend_chart, position=(0, 0))

# 2. カテゴリ別売上
category_chart = ChartComponent(
    data=df.groupby('category')['sales'].sum().reset_index(),
    chart_type='bar',
    x_column='category',
    y_column='sales',
    title='カテゴリ別売上'
)
analysis_dashboard.add_component(category_chart, position=(0, 1))

# 3. 地域別売上
region_chart = ChartComponent(
    data=df.groupby('region')['sales'].sum().reset_index(),
    chart_type='pie',
    x_column='region',
    y_column='sales',
    title='地域別売上'
)
analysis_dashboard.add_component(region_chart, position=(1, 0))

# 4. 詳細テーブル
detail_table = TableComponent(
    data=sales_summary,
    enable_csv_download=True,
    sortable=True,
    searchable=True,
    title='カテゴリ・地域別売上詳細'
)
analysis_dashboard.add_component(detail_table, position=(1, 1))

# 5. フィルター
date_filter = FilterComponent(
    filter_type='date',
    column='date',
    start_date=df['date'].min(),
    end_date=df['date'].max(),
    title='日付フィルター'
)
analysis_dashboard.add_component(date_filter, position=(2, 0))

category_filter = FilterComponent(
    filter_type='dropdown',
    column='category',
    options=df['category'].unique().tolist(),
    title='カテゴリフィルター'
)
analysis_dashboard.add_component(category_filter, position=(2, 1))

# 表示
displayHTML(analysis_dashboard.render())
```

## 📚 次のステップ

このチュートリアルを完了したら、以下のドキュメントを参照してください：

- [高度な可視化](./advanced_visualization.md) - 高度な可視化コンポーネント
- [カスタマイズ](./customization.md) - 詳細なカスタマイズ方法
- [API リファレンス](../api/) - 全APIの詳細
- [パフォーマンス最適化](../guides/performance.md) - パフォーマンスの改善

## ❓ 問題が発生した場合

- [よくある問題](../troubleshooting/faq.md) - よくある問題と解決方法
- [エラーリファレンス](../troubleshooting/errors.md) - エラーメッセージの説明
- [デバッグガイド](../troubleshooting/debugging.md) - デバッグの方法