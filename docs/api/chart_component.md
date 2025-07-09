# ChartComponent API リファレンス

`ChartComponent`は、データをグラフ・チャートとして可視化するためのコンポーネントです。

## 📋 概要

```python
from db_ui_components import ChartComponent

chart = ChartComponent(
    data=df,
    chart_type='line',
    x_column='date',
    y_column='value',
    title='グラフタイトル'
)
```

## 🔧 パラメータ

### 必須パラメータ

| パラメータ | 型 | 説明 | 例 |
|-----------|----|------|-----|
| `data` | pandas.DataFrame | グラフに表示するデータ | `df` |
| `chart_type` | str | グラフのタイプ | `'line'`, `'bar'`, `'pie'`, `'scatter'`, `'heatmap'` |
| `x_column` | str | X軸に使用する列名 | `'date'`, `'category'` |
| `y_column` | str | Y軸に使用する列名 | `'value'`, `'sales'` |

### オプションパラメータ

| パラメータ | 型 | デフォルト | 説明 |
|-----------|----|-----------|------|
| `title` | str | `None` | グラフのタイトル |
| `height` | int | `400` | グラフの高さ（ピクセル） |
| `width` | int | `None` | グラフの幅（ピクセル） |
| `color` | str | `'#1f77b4'` | グラフの色 |
| `show_legend` | bool | `True` | 凡例の表示 |
| `show_grid` | bool | `True` | グリッドの表示 |
| `animate` | bool | `False` | アニメーション効果 |

## 📊 サポートされているグラフタイプ

### 1. 折れ線グラフ (`'line'`)

```python
chart = ChartComponent(
    data=df,
    chart_type='line',
    x_column='date',
    y_column='sales',
    title='売上推移'
)
```

**特徴:**
- 時系列データの表示に最適
- トレンドの可視化
- 複数系列の比較

### 2. 棒グラフ (`'bar'`)

```python
chart = ChartComponent(
    data=df,
    chart_type='bar',
    x_column='category',
    y_column='sales',
    title='カテゴリ別売上'
)
```

**特徴:**
- カテゴリ別の比較
- 数値の大小関係の可視化
- 水平・垂直両方に対応

### 3. 円グラフ (`'pie'`)

```python
chart = ChartComponent(
    data=df,
    chart_type='pie',
    x_column='category',
    y_column='sales',
    title='売上構成比'
)
```

**特徴:**
- 構成比の表示
- パーセンテージの可視化
- 全体に対する割合の理解

### 4. 散布図 (`'scatter'`)

```python
chart = ChartComponent(
    data=df,
    chart_type='scatter',
    x_column='x_value',
    y_column='y_value',
    title='相関分析'
)
```

**特徴:**
- 2変数の相関関係
- クラスタリングの可視化
- 外れ値の検出

### 5. ヒートマップ (`'heatmap'`)

```python
chart = ChartComponent(
    data=df,
    chart_type='heatmap',
    x_column='x_category',
    y_column='y_category',
    z_column='value',
    title='相関ヒートマップ'
)
```

**特徴:**
- 相関行列の可視化
- 密度の表示
- パターンの発見

## 🎨 スタイリング

### カスタムスタイルの適用

```python
chart = ChartComponent(
    data=df,
    chart_type='line',
    x_column='date',
    y_column='sales'
)

# スタイルを設定
chart.set_style({
    'backgroundColor': '#f5f5f5',
    'borderRadius': '8px',
    'padding': '16px',
    'fontFamily': 'Arial, sans-serif'
})
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

## 🔄 データ更新

### 動的データ更新

```python
# 初期データでグラフを作成
chart = ChartComponent(data=df, chart_type='line', x_column='date', y_column='sales')

# データを更新
new_df = pd.DataFrame({
    'date': pd.date_range('2024-02-01', periods=30, freq='D'),
    'sales': np.random.normal(1200, 250, 30)
})

# グラフを更新
chart.update_data(new_df)
displayHTML(chart.render())
```

## 📱 レスポンシブ対応

```python
chart = ChartComponent(
    data=df,
    chart_type='line',
    x_column='date',
    y_column='sales',
    responsive=True  # レスポンシブ対応を有効化
)
```

## 🎯 使用例

### 基本的な使用例

```python
import pandas as pd
import numpy as np
from db_ui_components import ChartComponent

# サンプルデータ
df = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=30, freq='D'),
    'sales': np.random.normal(1000, 200, 30),
    'profit': np.random.normal(200, 50, 30)
})

# 売上グラフ
sales_chart = ChartComponent(
    data=df,
    chart_type='line',
    x_column='date',
    y_column='sales',
    title='売上推移',
    height=400
)

# 利益グラフ
profit_chart = ChartComponent(
    data=df,
    chart_type='bar',
    x_column='date',
    y_column='profit',
    title='利益推移',
    height=300
)

# 表示
displayHTML(sales_chart.render())
displayHTML(profit_chart.render())
```

### 複数系列のグラフ

```python
# 複数系列のデータ
df_multi = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=30, freq='D'),
    'sales_A': np.random.normal(1000, 200, 30),
    'sales_B': np.random.normal(800, 150, 30),
    'sales_C': np.random.normal(1200, 250, 30)
})

# 複数系列のグラフ
multi_chart = ChartComponent(
    data=df_multi,
    chart_type='line',
    x_column='date',
    y_columns=['sales_A', 'sales_B', 'sales_C'],
    title='部門別売上推移'
)
```

## ⚠️ 制限事項

- データサイズ: 推奨最大10,000行
- メモリ使用量: 大量データの場合は注意が必要
- ブラウザ互換性: モダンブラウザが必要

## 🔗 関連リンク

- [TableComponent](./table_component.md) - テーブルコンポーネント
- [FilterComponent](./filter_component.md) - フィルターコンポーネント
- [Dashboard](./dashboard.md) - ダッシュボードクラス
- [トラブルシューティング](../troubleshooting/faq.md) - よくある問題