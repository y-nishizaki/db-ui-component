"""
高度な可視化コンポーネントの使用例

このファイルには、サンキーチャート、ヒートマップ、ネットワークグラフなどの
高度な可視化コンポーネントの使用例が含まれています。
"""

import pandas as pd
import numpy as np
from db_ui_components import (
    SankeyChartComponent,
    HeatmapComponent,
    NetworkGraphComponent,
    TreemapComponent,
    BubbleChartComponent,
    Dashboard
)


def create_sample_data():
    """サンプルデータを作成"""
    
    # サンキーチャート用データ
    sankey_data = pd.DataFrame({
        'source': ['A', 'A', 'B', 'B', 'C', 'C'],
        'target': ['X', 'Y', 'X', 'Z', 'Y', 'Z'],
        'value': [10, 5, 8, 12, 6, 9]
    })
    
    # ヒートマップ用データ
    np.random.seed(42)
    heatmap_data = pd.DataFrame({
        'x': np.repeat(['A', 'B', 'C'], 4),
        'y': np.tile(['X', 'Y', 'Z', 'W'], 3),
        'value': np.random.rand(12) * 100
    })
    
    # ネットワークグラフ用データ
    network_data = pd.DataFrame({
        'source': ['Node1', 'Node1', 'Node2', 'Node2', 'Node3'],
        'target': ['Node2', 'Node3', 'Node3', 'Node4', 'Node4']
    })
    
    # ツリーマップ用データ
    treemap_data = pd.DataFrame({
        'labels': ['A', 'B', 'C', 'D', 'E'],
        'parents': ['', '', '', '', ''],
        'values': [20, 30, 15, 25, 10]
    })
    
    # バブルチャート用データ
    bubble_data = pd.DataFrame({
        'x': np.random.rand(20) * 100,
        'y': np.random.rand(20) * 100,
        'size': np.random.rand(20) * 50 + 10,
        'color': np.random.choice(['Red', 'Blue', 'Green'], 20)
    })
    
    return {
        'sankey': sankey_data,
        'heatmap': heatmap_data,
        'network': network_data,
        'treemap': treemap_data,
        'bubble': bubble_data
    }


def sankey_chart_example():
    """サンキーチャートの使用例"""
    print("=== サンキーチャートの使用例 ===")
    
    data = create_sample_data()
    
    # サンキーチャートコンポーネントを作成
    sankey = SankeyChartComponent(
        source_column='source',
        target_column='target',
        value_column='value',
        title='データフロー図',
        height=400
    )
    
    # HTMLを生成
    html = sankey.render(data['sankey'])
    print("サンキーチャートHTMLが生成されました")
    print(f"HTML長: {len(html)} 文字")
    
    return html


def heatmap_example():
    """ヒートマップの使用例"""
    print("=== ヒートマップの使用例 ===")
    
    data = create_sample_data()
    
    # ヒートマップコンポーネントを作成
    heatmap = HeatmapComponent(
        x_column='x',
        y_column='y',
        value_column='value',
        title='相関ヒートマップ',
        height=400,
        color_scale='Viridis'
    )
    
    # HTMLを生成
    html = heatmap.render(data['heatmap'])
    print("ヒートマップHTMLが生成されました")
    print(f"HTML長: {len(html)} 文字")
    
    return html


def network_graph_example():
    """ネットワークグラフの使用例"""
    print("=== ネットワークグラフの使用例 ===")
    
    data = create_sample_data()
    
    # ネットワークグラフコンポーネントを作成
    network = NetworkGraphComponent(
        source_column='source',
        target_column='target',
        title='ネットワーク関係図',
        height=500
    )
    
    # HTMLを生成
    html = network.render(data['network'])
    print("ネットワークグラフHTMLが生成されました")
    print(f"HTML長: {len(html)} 文字")
    
    return html


def treemap_example():
    """ツリーマップの使用例"""
    print("=== ツリーマップの使用例 ===")
    
    data = create_sample_data()
    
    # ツリーマップコンポーネントを作成
    treemap = TreemapComponent(
        labels_column='labels',
        parents_column='parents',
        values_column='values',
        title='階層データ可視化',
        height=400
    )
    
    # HTMLを生成
    html = treemap.render(data['treemap'])
    print("ツリーマップHTMLが生成されました")
    print(f"HTML長: {len(html)} 文字")
    
    return html


def bubble_chart_example():
    """バブルチャートの使用例"""
    print("=== バブルチャートの使用例 ===")
    
    data = create_sample_data()
    
    # バブルチャートコンポーネントを作成
    bubble = BubbleChartComponent(
        x_column='x',
        y_column='y',
        size_column='size',
        color_column='color',
        title='3次元データ可視化',
        height=500
    )
    
    # HTMLを生成
    html = bubble.render(data['bubble'])
    print("バブルチャートHTMLが生成されました")
    print(f"HTML長: {len(html)} 文字")
    
    return html


def dashboard_with_visualizations():
    """可視化コンポーネントを含むダッシュボードの例"""
    print("=== 可視化コンポーネントを含むダッシュボード ===")
    
    data = create_sample_data()
    
    # ダッシュボードを作成
    dashboard = Dashboard(title="高度な可視化ダッシュボード")
    
    # 各種可視化コンポーネントを追加
    sankey = SankeyChartComponent(
        source_column='source',
        target_column='target',
        value_column='value',
        title='データフロー'
    )
    
    heatmap = HeatmapComponent(
        x_column='x',
        y_column='y',
        value_column='value',
        title='相関分析'
    )
    
    network = NetworkGraphComponent(
        source_column='source',
        target_column='target',
        title='ネットワーク関係'
    )
    
    bubble = BubbleChartComponent(
        x_column='x',
        y_column='y',
        size_column='size',
        color_column='color',
        title='3次元データ'
    )
    
    # コンポーネントをダッシュボードに追加
    dashboard.add_component(sankey, data['sankey'], row=0, col=0)
    dashboard.add_component(heatmap, data['heatmap'], row=0, col=1)
    dashboard.add_component(network, data['network'], row=1, col=0)
    dashboard.add_component(bubble, data['bubble'], row=1, col=1)
    
    # HTMLを生成
    html = dashboard.render()
    print("ダッシュボードHTMLが生成されました")
    print(f"HTML長: {len(html)} 文字")
    
    return html


def main():
    """メイン関数"""
    print("高度な可視化コンポーネントの使用例を実行します...")
    
    # 各可視化コンポーネントの例を実行
    sankey_html = sankey_chart_example()
    heatmap_html = heatmap_example()
    network_html = network_graph_example()
    treemap_html = treemap_example()
    bubble_html = bubble_chart_example()
    
    # ダッシュボードの例を実行
    dashboard_html = dashboard_with_visualizations()
    
    print("\n=== 実行完了 ===")
    print("すべての可視化コンポーネントの例が正常に実行されました。")


if __name__ == "__main__":
    main()