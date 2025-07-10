"""
バブルチャートコンポーネント

責任:
- バブルチャート用のデータ変換
- バブルチャート固有の設定管理
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from .base_visualization import BaseVisualizationComponent


class BubbleChartComponent(BaseVisualizationComponent):
    """
    バブルチャートコンポーネント

    責任: バブルチャートのデータ変換と設定管理
    """

    def __init__(
        self,
        x_column: str,
        y_column: str,
        size_column: str,
        color_column: Optional[str] = None,
        title: str = "Bubble Chart",
        height: int = 500,
        **kwargs,
    ):
        """
        バブルチャートコンポーネントを初期化

        Args:
            x_column: X軸の列名
            y_column: Y軸の列名
            size_column: バブルサイズの列名
            color_column: カラー分けの列名（オプション）
            title: チャートのタイトル
            height: チャートの高さ
            **kwargs: その他のパラメータ
        """
        super().__init__(title=title, height=height, **kwargs)
        self.x_column = x_column
        self.y_column = y_column
        self.size_column = size_column
        self.color_column = color_column

    def _prepare_chart_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        バブルチャート用のデータを準備

        Args:
            data: 元のデータフレーム

        Returns:
            バブルチャート用のデータ辞書
        """
        # サイズの正規化
        sizes = data[self.size_column].values
        normalized_sizes = np.array(sizes) * 10 + 10  # 簡易的な正規化

        bubble_data = {
            "type": "scatter",
            "x": data[self.x_column].tolist(),
            "y": data[self.y_column].tolist(),
            "mode": "markers",
            "marker": {
                "size": normalized_sizes.tolist(),
                "sizemode": "area",
                "sizeref": 2 * max(normalized_sizes) / (40**2),
                "sizemin": 4,
            },
            "text": data[self.size_column].tolist(),
            "hovertemplate": f"{self.x_column}: %{{x}}<br>{self.y_column}: %{{y}}<br>{self.size_column}: %{{text}}<extra></extra>",
        }

        # カラー分けがある場合
        if self.color_column:
            bubble_data["marker"]["color"] = data[self.color_column].tolist()
            bubble_data["marker"]["colorscale"] = "Viridis"
            bubble_data["marker"]["showscale"] = True
            bubble_data["marker"]["colorbar"] = {"title": self.color_column}

        return bubble_data

    def _get_chart_type(self) -> str:
        """
        チャートタイプを取得

        Returns:
            チャートタイプ
        """
        return "bubble-chart"

    def _generate_html_template(self, chart_data: Dict[str, Any]) -> str:
        """
        バブルチャート用のHTMLテンプレートを生成

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
