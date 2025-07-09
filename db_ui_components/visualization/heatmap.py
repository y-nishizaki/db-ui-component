"""
ヒートマップコンポーネント

責任:
- ヒートマップ用のデータ変換
- ヒートマップ固有の設定管理
"""

import pandas as pd
from typing import Dict, Any
from .base_visualization import BaseVisualizationComponent


class HeatmapComponent(BaseVisualizationComponent):
    """
    ヒートマップコンポーネント
    
    責任: ヒートマップのデータ変換と設定管理
    """
    
    def __init__(self,
                 x_column: str,
                 y_column: str,
                 value_column: str,
                 title: str = "Heatmap",
                 height: int = 500,
                 color_scale: str = "Viridis",
                 **kwargs):
        """
        ヒートマップコンポーネントを初期化
        
        Args:
            x_column: X軸の列名
            y_column: Y軸の列名
            value_column: 値の列名
            title: チャートのタイトル
            height: チャートの高さ
            color_scale: カラースケール
            **kwargs: その他のパラメータ
        """
        super().__init__(title=title, height=height, **kwargs)
        self.x_column = x_column
        self.y_column = y_column
        self.value_column = value_column
        self.color_scale = color_scale
    
    def _prepare_chart_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        ヒートマップ用のデータを準備
        
        Args:
            data: 元のデータフレーム
            
        Returns:
            ヒートマップ用のデータ辞書
        """
        # ピボットテーブルを作成
        pivot_data = data.pivot_table(
            values=self.value_column,
            index=self.y_column,
            columns=self.x_column,
            aggfunc='mean'
        )
        
        return {
            'type': 'heatmap',
            'z': pivot_data.values.tolist(),
            'x': pivot_data.columns.tolist(),
            'y': pivot_data.index.tolist(),
            'colorscale': self.color_scale.lower()
        }
    
    def _get_chart_type(self) -> str:
        """
        チャートタイプを取得
        
        Returns:
            チャートタイプ
        """
        return "heatmap"
    
    def _generate_html_template(self, chart_data: Dict[str, Any]) -> str:
        """
        ヒートマップ用のHTMLテンプレートを生成
        
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
                xaxis: {{
                    title: '{self.x_column}'
                }},
                yaxis: {{
                    title: '{self.y_column}'
                }},
                height: {self.height}
            }};
            
            Plotly.newPlot('{div_id}', data, layout);
        </script>
        """
        
        return html