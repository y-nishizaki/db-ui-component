# 高度な可視化コンポーネント API リファレンス

このドキュメントでは、Databricks UI Component Libraryの高度な可視化コンポーネントについて説明します。これらのコンポーネントは、複雑なデータ関係や特殊な可視化ニーズに対応します。

## 📋 概要

高度な可視化コンポーネントには以下が含まれます：

- **SankeyChartComponent**: データフローの可視化
- **HeatmapComponent**: 相関分析・密度表示
- **NetworkGraphComponent**: 関係性の可視化
- **TreemapComponent**: 階層データの可視化
- **BubbleChartComponent**: 3次元データの可視化

## 🔄 SankeyChartComponent

### 概要

データフローやプロセスの流れを可視化するためのコンポーネントです。

```python
from db_ui_components import SankeyChartComponent

sankey = SankeyChartComponent(
    data=flow_data,
    source_column='source',
    target_column='target',
    value_column='value',
    title='データフロー'
)
```

### パラメータ

| パラメータ | 型 | 説明 | 例 |
|-----------|----|------|-----|
| `data` | pandas.DataFrame | フローデータ | `flow_df` |
| `source_column` | str | ソース列名 | `'source'` |
| `target_column` | str | ターゲット列名 | `'target'` |
| `value_column` | str | 値列名 | `'value'` |
| `title` | str | チャートタイトル | `'データフロー'` |

### 使用例

```python
import pandas as pd
import numpy as np
from db_ui_components import SankeyChartComponent

# サンプルフローデータ
flow_data = pd.DataFrame({
    'source': ['A', 'A', 'B', 'B', 'C'],
    'target': ['B', 'C', 'D', 'E', 'D'],
    'value': [100, 50, 80, 20, 30]
})

# サンキーチャートの作成
sankey = SankeyChartComponent(
    data=flow_data,
    source_column='source',
    target_column='target',
    value_column='value',
    title='顧客ジャーニー'
)

displayHTML(sankey.render())
```

## 🔥 HeatmapComponent

### 概要

相関行列や時系列ヒートマップなどの密度データを可視化するコンポーネントです。

```python
from db_ui_components import HeatmapComponent

heatmap = HeatmapComponent(
    data=correlation_data,
    x_column='x_category',
    y_column='y_category',
    z_column='value',
    title='相関ヒートマップ'
)
```

### パラメータ

| パラメータ | 型 | 説明 | 例 |
|-----------|----|------|-----|
| `data` | pandas.DataFrame | ヒートマップデータ | `corr_df` |
| `x_column` | str | X軸列名 | `'x_category'` |
| `y_column` | str | Y軸列名 | `'y_category'` |
| `z_column` | str | 値列名 | `'value'` |
| `color_scale` | str | カラースケール | `'Viridis'` |

### 使用例

```python
# 相関行列の作成
correlation_data = df.corr().reset_index()
correlation_data = correlation_data.melt(
    id_vars='index',
    var_name='variable',
    value_name='correlation'
)

# ヒートマップの作成
heatmap = HeatmapComponent(
    data=correlation_data,
    x_column='index',
    y_column='variable',
    z_column='correlation',
    title='相関ヒートマップ',
    color_scale='RdBu'
)

displayHTML(heatmap.render())
```

## 🌐 NetworkGraphComponent

### 概要

ソーシャルネットワークや依存関係などの関係性データを可視化するコンポーネントです。

```python
from db_ui_components import NetworkGraphComponent

network = NetworkGraphComponent(
    nodes=node_data,
    edges=edge_data,
    title='ネットワークグラフ'
)
```

### パラメータ

| パラメータ | 型 | 説明 | 例 |
|-----------|----|------|-----|
| `nodes` | pandas.DataFrame | ノードデータ | `node_df` |
| `edges` | pandas.DataFrame | エッジデータ | `edge_df` |
| `node_size_column` | str | ノードサイズ列 | `'size'` |
| `edge_weight_column` | str | エッジ重み列 | `'weight'` |

### 使用例

```python
# ノードデータ
nodes = pd.DataFrame({
    'id': ['A', 'B', 'C', 'D', 'E'],
    'label': ['Node A', 'Node B', 'Node C', 'Node D', 'Node E'],
    'size': [10, 15, 8, 12, 6]
})

# エッジデータ
edges = pd.DataFrame({
    'source': ['A', 'A', 'B', 'C', 'D'],
    'target': ['B', 'C', 'D', 'E', 'E'],
    'weight': [5, 3, 7, 2, 4]
})

# ネットワークグラフの作成
network = NetworkGraphComponent(
    nodes=nodes,
    edges=edges,
    node_size_column='size',
    edge_weight_column='weight',
    title='関係性ネットワーク'
)

displayHTML(network.render())
```

## 🌳 TreemapComponent

### 概要

階層データやファイル構造などを可視化するコンポーネントです。

```python
from db_ui_components import TreemapComponent

treemap = TreemapComponent(
    data=hierarchy_data,
    path_column='path',
    value_column='size',
    title='階層データ'
)
```

### パラメータ

| パラメータ | 型 | 説明 | 例 |
|-----------|----|------|-----|
| `data` | pandas.DataFrame | 階層データ | `hierarchy_df` |
| `path_column` | str | パス列名 | `'path'` |
| `value_column` | str | 値列名 | `'size'` |
| `color_column` | str | 色分け列名 | `'category'` |

### 使用例

```python
# 階層データの作成
hierarchy_data = pd.DataFrame({
    'path': ['Root/A', 'Root/B', 'Root/A/1', 'Root/A/2', 'Root/B/1'],
    'size': [100, 80, 30, 70, 80],
    'category': ['A', 'B', 'A1', 'A2', 'B1']
})

# ツリーマップの作成
treemap = TreemapComponent(
    data=hierarchy_data,
    path_column='path',
    value_column='size',
    color_column='category',
    title='ファイル構造'
)

displayHTML(treemap.render())
```

## 🫧 BubbleChartComponent

### 概要

3次元データ（X軸、Y軸、サイズ）を可視化するコンポーネントです。

```python
from db_ui_components import BubbleChartComponent

bubble = BubbleChartComponent(
    data=bubble_data,
    x_column='x_value',
    y_column='y_value',
    size_column='size',
    color_column='category',
    title='バブルチャート'
)
```

### パラメータ

| パラメータ | 型 | 説明 | 例 |
|-----------|----|------|-----|
| `data` | pandas.DataFrame | バブルデータ | `bubble_df` |
| `x_column` | str | X軸列名 | `'x_value'` |
| `y_column` | str | Y軸列名 | `'y_value'` |
| `size_column` | str | サイズ列名 | `'size'` |
| `color_column` | str | 色分け列名 | `'category'` |

### 使用例

```python
# バブルデータの作成
bubble_data = pd.DataFrame({
    'x_value': np.random.randn(50),
    'y_value': np.random.randn(50),
    'size': np.random.randint(10, 100, 50),
    'category': np.random.choice(['A', 'B', 'C'], 50)
})

# バブルチャートの作成
bubble = BubbleChartComponent(
    data=bubble_data,
    x_column='x_value',
    y_column='y_value',
    size_column='size',
    color_column='category',
    title='多変量分析'
)

displayHTML(bubble.render())
```

## 🎨 スタイリング

### 共通スタイリング

```python
# 高度な可視化コンポーネントのスタイリング
advanced_chart = SankeyChartComponent(
    data=flow_data,
    source_column='source',
    target_column='target',
    value_column='value'
)

# スタイルを設定
advanced_chart.set_style({
    'backgroundColor': '#f8f9fa',
    'borderRadius': '8px',
    'padding': '16px',
    'fontFamily': 'Arial, sans-serif',
    'fontSize': '14px'
})

displayHTML(advanced_chart.render())
```

### カスタムカラースケール

```python
# カスタムカラースケールの設定
heatmap = HeatmapComponent(
    data=correlation_data,
    x_column='x_category',
    y_column='y_category',
    z_column='value',
    color_scale='Viridis'  # カラースケールを指定
)

displayHTML(heatmap.render())
```

## 🔄 データ更新

### 動的データ更新

```python
# 初期データでチャートを作成
sankey = SankeyChartComponent(
    data=flow_data,
    source_column='source',
    target_column='target',
    value_column='value'
)

displayHTML(sankey.render())

# データを更新
new_flow_data = pd.DataFrame({
    'source': ['X', 'X', 'Y'],
    'target': ['Y', 'Z', 'Z'],
    'value': [60, 40, 30]
})

sankey.update_data(new_flow_data)
displayHTML(sankey.render())
```

## 📱 レスポンシブ対応

```python
# レスポンシブ対応の高度な可視化
responsive_chart = HeatmapComponent(
    data=correlation_data,
    x_column='x_category',
    y_column='y_category',
    z_column='value',
    responsive=True  # レスポンシブ対応を有効化
)

displayHTML(responsive_chart.render())
```

## 🎯 実践的な使用例

### 顧客ジャーニー分析

```python
# 顧客ジャーニーデータ
journey_data = pd.DataFrame({
    'source': ['Homepage', 'Homepage', 'Search', 'Search', 'Product', 'Product'],
    'target': ['Search', 'Product', 'Product', 'Cart', 'Cart', 'Purchase'],
    'value': [1000, 300, 800, 200, 150, 100]
})

# サンキーチャートで可視化
journey_chart = SankeyChartComponent(
    data=journey_data,
    source_column='source',
    target_column='target',
    value_column='value',
    title='顧客ジャーニー分析'
)

displayHTML(journey_chart.render())
```

### 相関分析ダッシュボード

```python
# 相関分析ダッシュボード
correlation_dashboard = Dashboard(title='相関分析ダッシュボード')

# 相関行列の作成
corr_matrix = df.corr()
correlation_data = corr_matrix.reset_index().melt(
    id_vars='index',
    var_name='variable',
    value_name='correlation'
)

# ヒートマップの作成
correlation_heatmap = HeatmapComponent(
    data=correlation_data,
    x_column='index',
    y_column='variable',
    z_column='correlation',
    title='相関ヒートマップ',
    color_scale='RdBu'
)

# 散布図の作成（相関の高い変数ペア）
high_corr_pairs = []
for i in range(len(corr_matrix.columns)):
    for j in range(i+1, len(corr_matrix.columns)):
        corr_value = corr_matrix.iloc[i, j]
        if abs(corr_value) > 0.5:
            high_corr_pairs.append({
                'var1': corr_matrix.columns[i],
                'var2': corr_matrix.columns[j],
                'correlation': corr_value
            })

scatter_data = pd.DataFrame(high_corr_pairs)
scatter_chart = ChartComponent(
    data=scatter_data,
    chart_type='scatter',
    x_column='var1',
    y_column='correlation',
    title='高相関変数'
)

# ダッシュボードに追加
correlation_dashboard.add_component(correlation_heatmap, position=(0, 0))
correlation_dashboard.add_component(scatter_chart, position=(0, 1))

displayHTML(correlation_dashboard.render())
```

### ソーシャルネットワーク分析

```python
# ソーシャルネットワークデータ
network_nodes = pd.DataFrame({
    'id': ['User1', 'User2', 'User3', 'User4', 'User5'],
    'label': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
    'size': [20, 15, 25, 10, 18],
    'group': ['A', 'A', 'B', 'B', 'A']
})

network_edges = pd.DataFrame({
    'source': ['User1', 'User1', 'User2', 'User3', 'User4'],
    'target': ['User2', 'User3', 'User3', 'User4', 'User5'],
    'weight': [5, 3, 7, 2, 4]
})

# ネットワークグラフの作成
network_graph = NetworkGraphComponent(
    nodes=network_nodes,
    edges=network_edges,
    node_size_column='size',
    edge_weight_column='weight',
    title='ソーシャルネットワーク'
)

displayHTML(network_graph.render())
```

## ⚠️ 制限事項

- **データサイズ**: 推奨最大10,000ノード（ネットワークグラフ）
- **階層レベル**: 推奨最大10レベル（ツリーマップ）
- **フロー数**: 推奨最大1,000フロー（サンキーチャート）
- **メモリ使用量**: 大量データの場合は注意が必要

## 🔗 関連リンク

- [ChartComponent](./chart_component.md) - 基本グラフコンポーネント
- [TableComponent](./table_component.md) - テーブルコンポーネント
- [Dashboard](./dashboard.md) - ダッシュボードクラス
- [トラブルシューティング](../troubleshooting/faq.md) - よくある問題