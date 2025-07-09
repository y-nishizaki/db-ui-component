# Dashboard API リファレンス

`Dashboard`は、複数のコンポーネントを統合して美しいダッシュボードを作成するためのクラスです。グリッドベースのレイアウトシステムとスタイリング機能を提供します。

## 📋 概要

```python
from db_ui_components import Dashboard, ChartComponent, TableComponent

dashboard = Dashboard(title='売上ダッシュボード')

# コンポーネントを追加
chart = ChartComponent(data=df, chart_type='line', x_column='date', y_column='sales')
table = TableComponent(data=df, enable_csv_download=True)

dashboard.add_component(chart, position=(0, 0))
dashboard.add_component(table, position=(1, 0))

# 表示
displayHTML(dashboard.render())
```

## 🔧 パラメータ

### オプションパラメータ

| パラメータ | 型 | デフォルト | 説明 |
|-----------|----|-----------|------|
| `title` | str | `'Dashboard'` | ダッシュボードのタイトル |
| `theme` | str | `'light'` | テーマ（'light', 'dark'） |
| `layout` | str | `'grid'` | レイアウトタイプ（'grid', 'flex'） |
| `columns` | int | `2` | グリッドの列数 |
| `spacing` | int | `16` | コンポーネント間の間隔（ピクセル） |
| `padding` | int | `20` | ダッシュボードの内側の余白（ピクセル） |
| `height` | int | `None` | ダッシュボードの高さ（ピクセル） |
| `width` | int | `None` | ダッシュボードの幅（ピクセル） |

## 📊 機能

### 1. 基本的なダッシュボード作成

```python
# 基本的なダッシュボード
dashboard = Dashboard(title='売上ダッシュボード')

# コンポーネントを追加
chart = ChartComponent(data=df, chart_type='line', x_column='date', y_column='sales')
table = TableComponent(data=df, enable_csv_download=True)

dashboard.add_component(chart, position=(0, 0))
dashboard.add_component(table, position=(1, 0))

displayHTML(dashboard.render())
```

### 2. グリッドレイアウト

```python
# 2x2グリッドレイアウト
dashboard = Dashboard(title='売上分析ダッシュボード', columns=2)

# コンポーネントを配置
sales_chart = ChartComponent(data=df, chart_type='line', x_column='date', y_column='sales')
profit_chart = ChartComponent(data=df, chart_type='bar', x_column='date', y_column='profit')
category_chart = ChartComponent(data=category_df, chart_type='pie', x_column='category', y_column='sales')
data_table = TableComponent(data=df, enable_csv_download=True)

dashboard.add_component(sales_chart, position=(0, 0))
dashboard.add_component(profit_chart, position=(0, 1))
dashboard.add_component(category_chart, position=(1, 0))
dashboard.add_component(data_table, position=(1, 1))

displayHTML(dashboard.render())
```

### 3. テーマ設定

```python
# ダークテーマのダッシュボード
dark_dashboard = Dashboard(
    title='ダークテーマダッシュボード',
    theme='dark'
)

# コンポーネントを追加
chart = ChartComponent(data=df, chart_type='line', x_column='date', y_column='sales')
dark_dashboard.add_component(chart, position=(0, 0))

displayHTML(dark_dashboard.render())
```

### 4. カスタムレイアウト

```python
# カスタムレイアウト設定
custom_dashboard = Dashboard(
    title='カスタムレイアウトダッシュボード',
    layout='flex',
    spacing=24,
    padding=32
)

# コンポーネントを追加
chart1 = ChartComponent(data=df, chart_type='line', x_column='date', y_column='sales')
chart2 = ChartComponent(data=df, chart_type='bar', x_column='date', y_column='profit')

custom_dashboard.add_component(chart1, position=(0, 0))
custom_dashboard.add_component(chart2, position=(0, 1))

displayHTML(custom_dashboard.render())
```

## 🎨 スタイリング

### カスタムスタイルの適用

```python
dashboard = Dashboard(title='カスタムスタイルダッシュボード')

# コンポーネントを追加
chart = ChartComponent(data=df, chart_type='line', x_column='date', y_column='sales')
dashboard.add_component(chart, position=(0, 0))

# スタイルを設定
dashboard.set_style({
    'backgroundColor': '#f8f9fa',
    'borderRadius': '12px',
    'padding': '24px',
    'fontFamily': 'Roboto, sans-serif',
    'fontSize': '16px',
    'boxShadow': '0 8px 16px rgba(0, 0, 0, 0.1)'
})

displayHTML(dashboard.render())
```

### 利用可能なスタイルプロパティ

| プロパティ | 型 | 説明 |
|-----------|----|------|
| `backgroundColor` | str | 背景色 |
| `borderRadius` | str | 角丸の半径 |
| `padding` | str | 内側の余白 |
| `margin` | str | 外側の余白 |
| `fontFamily` | str | フォントファミリー |
| `fontSize` | str | フォントサイズ |
| `color` | str | テキスト色 |
| `border` | str | ボーダー |
| `boxShadow` | str | ボックスシャドウ |
| `gridGap` | str | グリッド間隔 |

## 🔄 コンポーネント管理

### コンポーネントの追加

```python
dashboard = Dashboard(title='コンポーネント管理ダッシュボード')

# コンポーネントを追加
chart = ChartComponent(data=df, chart_type='line', x_column='date', y_column='sales')
table = TableComponent(data=df, enable_csv_download=True)
filter_comp = FilterComponent(filter_type='dropdown', column='category', options=['A', 'B', 'C'])

dashboard.add_component(chart, position=(0, 0))
dashboard.add_component(table, position=(1, 0))
dashboard.add_component(filter_comp, position=(2, 0))

displayHTML(dashboard.render())
```

### コンポーネントの削除

```python
# 特定のコンポーネントを削除
dashboard.remove_component(position=(0, 0))

# 全コンポーネントを削除
dashboard.clear_components()
```

### コンポーネントの取得

```python
# 特定位置のコンポーネントを取得
component = dashboard.get_component(position=(0, 0))

# 全コンポーネントを取得
all_components = dashboard.get_all_components()
```

## 📱 レスポンシブ対応

```python
# レスポンシブ対応ダッシュボード
responsive_dashboard = Dashboard(
    title='レスポンシブダッシュボード',
    responsive=True
)

# コンポーネントを追加
chart = ChartComponent(data=df, chart_type='line', x_column='date', y_column='sales')
table = TableComponent(data=df, enable_csv_download=True)

responsive_dashboard.add_component(chart, position=(0, 0))
responsive_dashboard.add_component(table, position=(1, 0))

displayHTML(responsive_dashboard.render())
```

## 🎯 使用例

### 基本的な使用例

```python
import pandas as pd
import numpy as np
from db_ui_components import Dashboard, ChartComponent, TableComponent

# サンプルデータ
df = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=30, freq='D'),
    'sales': np.random.normal(1000, 200, 30),
    'profit': np.random.normal(200, 50, 30),
    'category': np.random.choice(['A', 'B', 'C'], 30)
})

# ダッシュボードの作成
dashboard = Dashboard(title='売上ダッシュボード')

# グラフコンポーネント
sales_chart = ChartComponent(
    data=df,
    chart_type='line',
    x_column='date',
    y_column='sales',
    title='売上推移'
)

# テーブルコンポーネント
data_table = TableComponent(
    data=df,
    enable_csv_download=True,
    sortable=True,
    searchable=True,
    title='売上データ'
)

# コンポーネントを追加
dashboard.add_component(sales_chart, position=(0, 0))
dashboard.add_component(data_table, position=(1, 0))

# 表示
displayHTML(dashboard.render())
```

### 複雑なダッシュボード

```python
# 複雑なダッシュボードの作成
complex_dashboard = Dashboard(
    title='包括的売上分析ダッシュボード',
    theme='light',
    columns=3,
    spacing=20
)

# データの準備
sales_summary = df.groupby('category')['sales'].sum().reset_index()
profit_summary = df.groupby('category')['profit'].sum().reset_index()

# 複数のコンポーネントを作成
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

category_chart = ChartComponent(
    data=sales_summary,
    chart_type='bar',
    x_column='category',
    y_column='sales',
    title='カテゴリ別売上'
)

profit_pie = ChartComponent(
    data=profit_summary,
    chart_type='pie',
    x_column='category',
    y_column='profit',
    title='カテゴリ別利益'
)

data_table = TableComponent(
    data=df,
    enable_csv_download=True,
    sortable=True,
    searchable=True,
    title='詳細データ'
)

# コンポーネントを配置
complex_dashboard.add_component(sales_chart, position=(0, 0))
complex_dashboard.add_component(profit_chart, position=(0, 1))
complex_dashboard.add_component(category_chart, position=(0, 2))
complex_dashboard.add_component(profit_pie, position=(1, 0))
complex_dashboard.add_component(data_table, position=(1, 1))

# スタイルを設定
complex_dashboard.set_style({
    'backgroundColor': '#f8f9fa',
    'borderRadius': '12px',
    'padding': '24px',
    'fontFamily': 'Roboto, sans-serif',
    'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
})

displayHTML(complex_dashboard.render())
```

### 動的ダッシュボード

```python
# 動的ダッシュボードの作成
def create_dynamic_dashboard(data_dict):
    """データ辞書から動的にダッシュボードを作成"""
    dashboard = Dashboard(title='動的ダッシュボード')
    
    row = 0
    for title, data in data_dict.items():
        if isinstance(data, pd.DataFrame):
            # データフレームの場合、テーブルとして表示
            table = TableComponent(
                data=data,
                title=title,
                enable_csv_download=True
            )
            dashboard.add_component(table, position=(row, 0))
            row += 1
        elif isinstance(data, dict) and 'chart_type' in data:
            # チャートデータの場合、グラフとして表示
            chart = ChartComponent(**data)
            dashboard.add_component(chart, position=(row, 0))
            row += 1
    
    return dashboard

# 動的ダッシュボードの使用
data_dict = {
    '売上データ': df,
    '売上推移': {
        'data': df,
        'chart_type': 'line',
        'x_column': 'date',
        'y_column': 'sales',
        'title': '売上推移'
    }
}

dynamic_dashboard = create_dynamic_dashboard(data_dict)
displayHTML(dynamic_dashboard.render())
```

## ⚠️ 制限事項

- **コンポーネント数**: 推奨最大50個
- **グリッドサイズ**: 推奨最大10x10
- **メモリ使用量**: 大量コンポーネントの場合は注意が必要
- **ブラウザ互換性**: モダンブラウザが必要

## 🔗 関連リンク

- [ChartComponent](./chart_component.md) - グラフ・チャートコンポーネント
- [TableComponent](./table_component.md) - テーブルコンポーネント
- [FilterComponent](./filter_component.md) - フィルターコンポーネント
- [トラブルシューティング](../troubleshooting/faq.md) - よくある問題