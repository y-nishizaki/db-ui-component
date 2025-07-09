"""
ツリーマップコンポーネント

責任:
- ツリーマップ用のデータ変換
- ツリーマップ固有の設定管理
"""

import pandas as pd
from typing import Dict, Any
from .base_visualization import BaseVisualizationComponent


class TreemapComponent(BaseVisualizationComponent):
    """
    ツリーマップコンポーネント
    
    責任: ツリーマップのデータ変換と設定管理
    """
    
    def __init__(self,
                 labels_column: str,
                 parents_column: str,
                 values_column: str,
                 title: str = "Treemap",
                 height: int = 500,
                 **kwargs):
        """
        ツリーマップコンポーネントを初期化
        
        Args:
            labels_column: ラベルの列名
            parents_column: 親要素の列名
            values_column: 値の列名
            title: チャートのタイトル
            height: チャートの高さ
            **kwargs: その他のパラメータ
        """
        super().__init__(title=title, height=height, **kwargs)
        self.labels_column = labels_column
        self.parents_column = parents_column
        self.values_column = values_column
    
    def _prepare_chart_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        ツリーマップ用のデータを準備
        
        Args:
            data: 元のデータフレーム
            
        Returns:
            ツリーマップ用のデータ辞書
        """
        return {
            'type': 'treemap',
            'labels': data[self.labels_column].tolist(),
            'parents': data[self.parents_column].tolist(),
            'values': data[self.values_column].tolist(),
            'textinfo': 'label+value'
        }
    
    def _get_chart_type(self) -> str:
        """
        チャートタイプを取得
        
        Returns:
            チャートタイプ
        """
        return "treemap"