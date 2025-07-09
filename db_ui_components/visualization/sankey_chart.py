"""
サンキーチャートコンポーネント

責任:
- サンキーチャート用のデータ変換
- サンキーチャート固有の設定管理
"""

import pandas as pd
from typing import Dict, Any
from .base_visualization import BaseVisualizationComponent


class SankeyChartComponent(BaseVisualizationComponent):
    """
    サンキーチャートコンポーネント
    
    責任: サンキーチャートのデータ変換と設定管理
    """
    
    def __init__(self, 
                 source_column: str,
                 target_column: str, 
                 value_column: str,
                 title: str = "Sankey Chart",
                 height: int = 600,
                 **kwargs):
        """
        サンキーチャートコンポーネントを初期化
        
        Args:
            source_column: ソースノードの列名
            target_column: ターゲットノードの列名
            value_column: フロー値の列名
            title: チャートのタイトル
            height: チャートの高さ
            **kwargs: その他のパラメータ
        """
        super().__init__(title=title, height=height, **kwargs)
        self.source_column = source_column
        self.target_column = target_column
        self.value_column = value_column
    
    def _prepare_chart_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        サンキーチャート用のデータを準備
        
        Args:
            data: 元のデータフレーム
            
        Returns:
            サンキーチャート用のデータ辞書
        """
        # ユニークなノードのリストを作成
        sources = data[self.source_column].unique()
        targets = data[self.target_column].unique()
        all_nodes = list(set(list(sources) + list(targets)))
        
        # ノードのインデックスマッピング
        node_to_index = {node: i for i, node in enumerate(all_nodes)}
        
        # リンクデータの作成
        links = []
        for _, row in data.iterrows():
            source_idx = node_to_index[row[self.source_column]]
            target_idx = node_to_index[row[self.target_column]]
            value = float(row[self.value_column])
            
            links.append({
                'source': source_idx,
                'target': target_idx,
                'value': value
            })
        
        return {
            'type': 'sankey',
            'node': {
                'label': all_nodes,
                'color': ['#1f77b4'] * len(all_nodes)
            },
            'link': links
        }
    
    def _get_chart_type(self) -> str:
        """
        チャートタイプを取得
        
        Returns:
            チャートタイプ
        """
        return "sankey-chart"