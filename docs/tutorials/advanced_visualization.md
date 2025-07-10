# 高度な可視化チュートリアル

このチュートリアルでは、Databricks UI Component Libraryの高度な可視化コンポーネントを使用して、複雑なデータ関係を可視化する方法を説明します。

## 🎯 概要

高度な可視化コンポーネントは、標準的なグラフでは表現できない複雑なデータ関係を可視化するために設計されています。

## 📊 SankeyChartComponent（サンキーチャート）

### 概要
データフローやプロセスの流れを可視化するためのコンポーネントです。

### 基本的な使用例

```python
import pandas as pd
import numpy as np
from db_ui_components import SankeyChartComponent

# サンプルフローデータの作成
flow_data = pd.DataFrame({
    'source': ['Website', 'Website', 'Social Media', 'Social Media', 'Email'],
    'target': ['Product Page', 'Blog', 'Product Page', 'Blog', 'Product Page'],
    'value': [1000, 500, 800, 300, 600]
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

### 高度な設定

```python
# カスタムスタイル付きサンキーチャート
sankey = SankeyChartComponent(
    data=flow_data,
    source_column='source',
    target_column='target',
    value_column='value',
    title='顧客ジャーニー',
    node_color='category',
    link_color='source',
    height=600
)

# スタイルの設定
sankey.set_style({
    'backgroundColor': '#ffffff',
    'borderRadius': '8px',
    'padding': '16px'
})

displayHTML(sankey.render())
```

## 🔥 HeatmapComponent（ヒートマップ）

### 概要
相関行列や時系列ヒートマップなどの密度データを可視化するコンポーネントです。

### 相関分析の例

```python
import pandas as pd
import numpy as np
from db_ui_components import HeatmapComponent

# サンプルデータの作成
np.random.seed(42)
data = {
    'sales': np.random.normal(1000, 200, 100),
    'profit': np.random.normal(200, 50, 100),
    'customers': np.random.normal(500, 100, 100),
    'reviews': np.random.normal(4.5, 0.5, 100),
    'returns': np.random.normal(50, 20, 100)
}
df = pd.DataFrame(data)

# 相関行列の計算
correlation_matrix = df.corr()

# ヒートマップの作成
heatmap = HeatmapComponent(
    data=correlation_matrix,
    title='相関ヒートマップ',
    color_scale='RdBu',
    show_values=True
)

displayHTML(heatmap.render())
```

### 時系列ヒートマップ

```python
# 時系列データの準備
dates = pd.date_range('2024-01-01', periods=365, freq='D')
hourly_data = []
for date in dates:
    for hour in range(24):
        hourly_data.append({
            'date': date,
            'hour': hour,
            'value': np.random.normal(100, 30)
        })

hourly_df = pd.DataFrame(hourly_data)
hourly_df['day_of_week'] = hourly_df['date'].dt.day_name()
hourly_df['month'] = hourly_df['date'].dt.month

# ピボットテーブルでヒートマップ用データを作成
heatmap_data = hourly_df.pivot_table(
    values='value',
    index='day_of_week',
    columns='hour',
    aggfunc='mean'
)

# 時系列ヒートマップの作成
time_heatmap = HeatmapComponent(
    data=heatmap_data,
    title='時間別アクティビティ',
    color_scale='Viridis',
    x_label='時間',
    y_label='曜日'
)

displayHTML(time_heatmap.render())
```

## 🌐 NetworkGraphComponent（ネットワークグラフ）

### 概要
ソーシャルネットワークや依存関係などの関係性データを可視化するコンポーネントです。

### 基本的なネットワークグラフ

```python
from db_ui_components import NetworkGraphComponent

# ノードデータ
nodes = pd.DataFrame({
    'id': ['A', 'B', 'C', 'D', 'E', 'F'],
    'label': ['Node A', 'Node B', 'Node C', 'Node D', 'Node E', 'Node F'],
    'size': [20, 15, 10, 25, 12, 18],
    'color': ['red', 'blue', 'green', 'orange', 'purple', 'brown']
})

# エッジデータ
edges = pd.DataFrame({
    'source': ['A', 'A', 'B', 'C', 'D', 'E'],
    'target': ['B', 'C', 'D', 'E', 'F', 'F'],
    'weight': [5, 3, 7, 2, 4, 6],
    'color': ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff']
})

# ネットワークグラフの作成
network = NetworkGraphComponent(
    nodes=nodes,
    edges=edges,
    node_size_column='size',
    node_color_column='color',
    edge_weight_column='weight',
    edge_color_column='color',
    title='関係性ネットワーク'
)

displayHTML(network.render())
```

### ソーシャルネットワーク分析

```python
# ソーシャルネットワークデータの作成
users = pd.DataFrame({
    'id': range(1, 21),
    'name': [f'User_{i}' for i in range(1, 21)],
    'followers': np.random.poisson(100, 20),
    'category': np.random.choice(['Influencer', 'Regular', 'Brand'], 20)
})

# フォロー関係の作成
follows = []
for i in range(1, 21):
    num_follows = np.random.poisson(5)
    followed = np.random.choice([j for j in range(1, 21) if j != i], num_follows, replace=False)
    for target in followed:
        follows.append({
            'source': i,
            'target': target,
            'strength': np.random.uniform(0.1, 1.0)
        })

follows_df = pd.DataFrame(follows)

# ソーシャルネットワークの可視化
social_network = NetworkGraphComponent(
    nodes=users,
    edges=follows_df,
    node_id_column='id',
    node_label_column='name',
    node_size_column='followers',
    node_color_column='category',
    edge_weight_column='strength',
    title='ソーシャルネットワーク',
    layout='force'
)

displayHTML(social_network.render())
```

## 🌳 TreemapComponent（ツリーマップ）

### 概要
階層データやファイル構造などを可視化するコンポーネントです。

### 基本的なツリーマップ

```python
from db_ui_components import TreemapComponent

# 階層データの作成
hierarchy_data = pd.DataFrame({
    'path': [
        'Electronics/Computers/Laptops',
        'Electronics/Computers/Desktops',
        'Electronics/Phones/Smartphones',
        'Electronics/Phones/Accessories',
        'Clothing/Men/Shirts',
        'Clothing/Men/Pants',
        'Clothing/Women/Dresses',
        'Clothing/Women/Shoes',
        'Books/Fiction/Novels',
        'Books/Non-fiction/Technical'
    ],
    'size': [500, 300, 800, 200, 400, 350, 600, 450, 250, 180],
    'color': ['red', 'red', 'blue', 'blue', 'green', 'green', 'purple', 'purple', 'orange', 'orange']
})

# ツリーマップの作成
treemap = TreemapComponent(
    data=hierarchy_data,
    path_column='path',
    value_column='size',
    color_column='color',
    title='商品カテゴリ別売上'
)

displayHTML(treemap.render())
```

### ファイル構造の可視化

```python
# ファイル構造データの作成
file_structure = pd.DataFrame({
    'path': [
        'src/components/ChartComponent.py',
        'src/components/TableComponent.py',
        'src/components/FilterComponent.py',
        'src/utils/helpers.py',
        'src/utils/validators.py',
        'tests/test_chart.py',
        'tests/test_table.py',
        'docs/api/chart_component.md',
        'docs/api/table_component.md',
        'docs/tutorials/quickstart.md'
    ],
    'size': [5000, 3000, 2500, 1500, 1200, 2000, 1800, 800, 600, 400],
    'type': ['code', 'code', 'code', 'code', 'code', 'test', 'test', 'doc', 'doc', 'doc']
})

# ファイル構造の可視化
file_treemap = TreemapComponent(
    data=file_structure,
    path_column='path',
    value_column='size',
    color_column='type',
    title='プロジェクトファイル構造'
)

displayHTML(file_treemap.render())
```

## 🎈 BubbleChartComponent（バブルチャート）

### 概要
3次元データを可視化するコンポーネントです。

### 基本的なバブルチャート

```python
from db_ui_components import BubbleChartComponent

# 3次元データの作成
bubble_data = pd.DataFrame({
    'x': np.random.normal(0, 1, 50),
    'y': np.random.normal(0, 1, 50),
    'size': np.random.uniform(10, 100, 50),
    'color': np.random.choice(['A', 'B', 'C'], 50),
    'label': [f'Point_{i}' for i in range(50)]
})

# バブルチャートの作成
bubble_chart = BubbleChartComponent(
    data=bubble_data,
    x_column='x',
    y_column='y',
    size_column='size',
    color_column='color',
    label_column='label',
    title='3次元データ可視化'
)

displayHTML(bubble_chart.render())
```

### マーケティング分析の例

```python
# マーケティングデータの作成
marketing_data = pd.DataFrame({
    'ad_spend': np.random.uniform(1000, 10000, 30),
    'conversions': np.random.uniform(50, 500, 30),
    'roi': np.random.uniform(1.5, 4.0, 30),
    'channel': np.random.choice(['Facebook', 'Google', 'Instagram', 'Twitter'], 30),
    'campaign': [f'Campaign_{i}' for i in range(30)]
})

# バブルチャートでマーケティング分析
marketing_bubble = BubbleChartComponent(
    data=marketing_data,
    x_column='ad_spend',
    y_column='conversions',
    size_column='roi',
    color_column='channel',
    label_column='campaign',
    title='マーケティングキャンペーン分析',
    x_label='広告費',
    y_label='コンバージョン数'
)

displayHTML(marketing_bubble.render())
```

## 🔄 インタラクティブな高度な可視化

### フィルターとの連動

```python
from db_ui_components import FilterComponent

# フィルターコンポーネント
channel_filter = FilterComponent(
    filter_type='multiselect',
    column='channel',
    options=['Facebook', 'Google', 'Instagram', 'Twitter'],
    title='チャンネル'
)

# フィルターされたデータでバブルチャートを更新
def update_bubble_chart(filtered_data):
    marketing_bubble.update_data(filtered_data)

# フィルターイベントの設定
channel_filter.on_change(update_bubble_chart)

# ダッシュボードでの表示
from db_ui_components import Dashboard

dashboard = Dashboard(title='高度な可視化ダッシュボード')
dashboard.add_component(channel_filter, position=(0, 0))
dashboard.add_component(marketing_bubble, position=(1, 0))

displayHTML(dashboard.render())
```

## 🎨 カスタマイズとスタイリング

### カスタムカラーパレット

```python
# カスタムカラーパレットの設定
custom_colors = {
    'Facebook': '#1877f2',
    'Google': '#4285f4',
    'Instagram': '#e4405f',
    'Twitter': '#1da1f2'
}

marketing_bubble.set_color_palette(custom_colors)
```

### アニメーション効果

```python
# アニメーション効果の追加
sankey.enable_animation(True)
heatmap.enable_animation(True)
network.enable_animation(True)
```

## 🚀 実践的な例

### 完全な分析ダッシュボード

```python
import pandas as pd
import numpy as np
from db_ui_components import (
    Dashboard, SankeyChartComponent, HeatmapComponent,
    NetworkGraphComponent, TreemapComponent, BubbleChartComponent,
    FilterComponent
)

# データの準備
def create_analysis_data():
    # 顧客ジャーニーデータ
    journey_data = pd.DataFrame({
        'source': ['Website', 'Social Media', 'Email', 'Referral'],
        'target': ['Product Page', 'Product Page', 'Product Page', 'Product Page'],
        'value': [1000, 800, 600, 400]
    })
    
    # 相関データ
    correlation_data = pd.DataFrame({
        'feature1': [1.0, 0.8, 0.3, 0.5],
        'feature2': [0.8, 1.0, 0.4, 0.6],
        'feature3': [0.3, 0.4, 1.0, 0.2],
        'feature4': [0.5, 0.6, 0.2, 1.0]
    }, index=['feature1', 'feature2', 'feature3', 'feature4'])
    
    # ネットワークデータ
    nodes = pd.DataFrame({
        'id': range(1, 11),
        'name': [f'Node_{i}' for i in range(1, 11)],
        'size': np.random.poisson(50, 10),
        'category': np.random.choice(['A', 'B', 'C'], 10)
    })
    
    edges = pd.DataFrame({
        'source': np.random.randint(1, 11, 20),
        'target': np.random.randint(1, 11, 20),
        'weight': np.random.uniform(0.1, 1.0, 20)
    })
    
    return journey_data, correlation_data, nodes, edges

# データの作成
journey_data, correlation_data, nodes, edges = create_analysis_data()

# ダッシュボードの作成
dashboard = Dashboard(
    title='高度な可視化分析ダッシュボード',
    layout='grid',
    grid_size=(2, 2)
)

# コンポーネントの作成
sankey = SankeyChartComponent(
    data=journey_data,
    source_column='source',
    target_column='target',
    value_column='value',
    title='顧客ジャーニー'
)

heatmap = HeatmapComponent(
    data=correlation_data,
    title='相関ヒートマップ',
    color_scale='RdBu'
)

network = NetworkGraphComponent(
    nodes=nodes,
    edges=edges,
    node_size_column='size',
    node_color_column='category',
    edge_weight_column='weight',
    title='関係性ネットワーク'
)

# ダッシュボードにコンポーネントを追加
dashboard.add_component(sankey, position=(0, 0))
dashboard.add_component(heatmap, position=(0, 1))
dashboard.add_component(network, position=(1, 0), size=(1, 2))

# 表示
displayHTML(dashboard.render())
```

## 🚀 次のステップ

- [カスタマイズ](./customization.md) - スタイルとカスタマイズ
- [API リファレンス](../api/advanced_visualization.md) - 高度な可視化APIの詳細
- [パフォーマンス最適化](../guides/performance.md) - パフォーマンスの最適化

## ❓ よくある質問

**Q: 大量のデータでパフォーマンスが悪い場合はどうすればよいですか？**
A: データのサンプリングや集約を行い、表示するデータ量を制限してください。

**Q: カスタムカラーパレットを設定できますか？**
A: はい、`set_color_palette`メソッドでカスタムカラーパレットを設定できます。

**Q: アニメーション効果を無効にできますか？**
A: はい、`enable_animation(False)`でアニメーション効果を無効にできます。