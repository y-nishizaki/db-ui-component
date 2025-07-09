"""
ネットワークグラフコンポーネント

責任:
- ネットワークグラフ用のデータ変換
- ネットワークグラフ固有の設定管理
"""

import pandas as pd
import math
from typing import Dict, Any, List, Optional
from .base_visualization import BaseVisualizationComponent


class NetworkGraphComponent(BaseVisualizationComponent):
    """
    ネットワークグラフコンポーネント
    
    責任: ネットワークグラフのデータ変換と設定管理
    """
    
    def __init__(self,
                 source_column: str,
                 target_column: str,
                 weight_column: Optional[str] = None,
                 title: str = "Network Graph",
                 height: int = 600,
                 **kwargs):
        """
        ネットワークグラフコンポーネントを初期化
        
        Args:
            source_column: ソースノードの列名
            target_column: ターゲットノードの列名
            weight_column: エッジの重みの列名（オプション）
            title: チャートのタイトル
            height: チャートの高さ
            **kwargs: その他のパラメータ
        """
        super().__init__(title=title, height=height, **kwargs)
        self.source_column = source_column
        self.target_column = target_column
        self.weight_column = weight_column
    
    def _prepare_chart_data(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        ネットワークグラフ用のデータを準備
        
        Args:
            data: 元のデータフレーム
            
        Returns:
            ネットワークグラフ用のデータリスト
        """
        # ノードのリストを作成
        all_nodes = list(set(list(data[self.source_column].unique()) + 
                           list(data[self.target_column].unique())))
        
        # ノードの座標を計算（簡易的な円形配置）
        node_positions = {}
        for i, node in enumerate(all_nodes):
            angle = 2 * math.pi * i / len(all_nodes)
            x = math.cos(angle)
            y = math.sin(angle)
            node_positions[node] = {'x': x, 'y': y}
        
        # ノードのトレース
        node_trace = {
            'type': 'scatter',
            'x': [node_positions[node]['x'] for node in all_nodes],
            'y': [node_positions[node]['y'] for node in all_nodes],
            'mode': 'markers+text',
            'text': all_nodes,
            'textposition': 'middle center',
            'marker': {
                'size': 20,
                'color': ['#1f77b4'] * len(all_nodes)
            },
            'name': 'Nodes'
        }
        
        # エッジのトレース
        edge_x = []
        edge_y = []
        
        for _, row in data.iterrows():
            source = row[self.source_column]
            target = row[self.target_column]
            
            if source in node_positions and target in node_positions:
                edge_x.extend([node_positions[source]['x'], node_positions[target]['x'], None])
                edge_y.extend([node_positions[source]['y'], node_positions[target]['y'], None])
        
        edge_trace = {
            'type': 'scatter',
            'x': edge_x,
            'y': edge_y,
            'mode': 'lines',
            'line': {
                'width': 1,
                'color': '#888'
            },
            'name': 'Edges'
        }
        
        return [edge_trace, node_trace]
    
    def _get_chart_type(self) -> str:
        """
        チャートタイプを取得
        
        Returns:
            チャートタイプ
        """
        return "network-graph"
    
    def _generate_html_template(self, chart_data: List[Dict[str, Any]]) -> str:
        """
        ネットワークグラフ用のHTMLテンプレートを生成
        
        Args:
            chart_data: チャートデータ
            
        Returns:
            HTMLテンプレート
        """
        chart_type = self._get_chart_type()
        div_id = f"{chart_type}-{self.component_id}"
        
        html = f"""
        <div id="{div_id}" style="width: 100%; height: {self.height}px;"></div>
        <script>
            const data = {chart_data};
            
            const layout = {{
                title: '{self.title}',
                showlegend: false,
                height: {self.height},
                hovermode: 'closest'
            }};
            
            Plotly.newPlot('{div_id}', data, layout);
        </script>
        """
        
        return html