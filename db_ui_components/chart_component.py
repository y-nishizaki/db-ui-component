"""
グラフ・チャートコンポーネント

Databricksダッシュボードで使用するグラフ・チャートを表示するコンポーネントです。
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Optional, Dict, Any, Callable, List


class ChartComponent:
    """
    Databricksダッシュボード用のグラフ・チャートコンポーネント

    サポートするグラフタイプ:
    - line: 折れ線グラフ
    - bar: 棒グラフ
    - pie: 円グラフ
    - scatter: 散布図
    - heatmap: ヒートマップ
    """

    def __init__(
        self,
        data: pd.DataFrame,
        chart_type: str = "line",
        x_column: Optional[str] = None,
        y_column: Optional[str] = None,
        title: Optional[str] = None,
        height: int = 400,
        **kwargs,
    ):
        """
        初期化

        Args:
            data: データフレーム
            chart_type: グラフタイプ ('line', 'bar', 'pie', 'scatter', 'heatmap')
            x_column: X軸の列名
            y_column: Y軸の列名
            title: グラフのタイトル
            height: グラフの高さ（ピクセル）
            **kwargs: その他のパラメータ
        """
        self.data = data
        self.chart_type = chart_type
        self.x_column = x_column
        self.y_column = y_column
        self.title = title
        self.height = height
        self.kwargs = kwargs
        self._click_handlers: List[Callable] = []

    def render(self) -> str:
        """
        グラフをHTMLとしてレンダリング

        Returns:
            HTML文字列
        """
        fig = self._create_figure()

        # カスタムスタイルの適用
        if hasattr(self, "_custom_style"):
            fig.update_layout(**self._custom_style)

        return str(fig.to_html(
            include_plotlyjs=True, full_html=False, config={"displayModeBar": True}
        ))

    def _create_figure(self) -> go.Figure:
        """グラフを作成"""
        if self.chart_type == "line":
            return self._create_line_chart()
        elif self.chart_type == "bar":
            return self._create_bar_chart()
        elif self.chart_type == "pie":
            return self._create_pie_chart()
        elif self.chart_type == "scatter":
            return self._create_scatter_chart()
        elif self.chart_type == "heatmap":
            return self._create_heatmap()
        else:
            raise ValueError(f"Unsupported chart type: {self.chart_type}")

    def _create_line_chart(self) -> go.Figure:
        """折れ線グラフを作成"""
        fig = px.line(
            self.data, x=self.x_column, y=self.y_column, title=self.title, **self.kwargs
        )
        fig.update_layout(height=self.height)
        return fig

    def _create_bar_chart(self) -> go.Figure:
        """棒グラフを作成"""
        fig = px.bar(
            self.data, x=self.x_column, y=self.y_column, title=self.title, **self.kwargs
        )
        fig.update_layout(height=self.height)
        return fig

    def _create_pie_chart(self) -> go.Figure:
        """円グラフを作成"""
        fig = px.pie(
            self.data,
            values=self.y_column,
            names=self.x_column,
            title=self.title,
            **self.kwargs,
        )
        fig.update_layout(height=self.height)
        return fig

    def _create_scatter_chart(self) -> go.Figure:
        """散布図を作成"""
        fig = px.scatter(
            self.data, x=self.x_column, y=self.y_column, title=self.title, **self.kwargs
        )
        fig.update_layout(height=self.height)
        return fig

    def _create_heatmap(self) -> go.Figure:
        """ヒートマップを作成"""
        # ヒートマップ用のデータ整形
        pivot_data = self.data.pivot_table(
            values=self.y_column,
            index=self.data.columns[0],
            columns=self.data.columns[1],
            aggfunc="mean",
        )

        fig = px.imshow(pivot_data, title=self.title, **self.kwargs)
        fig.update_layout(height=self.height)
        return fig

    def set_style(self, style: Dict[str, Any]) -> None:
        """
        カスタムスタイルを設定

        Args:
            style: スタイル設定の辞書
        """
        self._custom_style = style

    def on_click(self, handler: Callable) -> None:
        """
        クリックイベントハンドラーを追加

        Args:
            handler: クリック時の処理関数
        """
        self._click_handlers.append(handler)

    def update_data(self, new_data: pd.DataFrame) -> None:
        """
        データを更新

        Args:
            new_data: 新しいデータフレーム
        """
        self.data = new_data

    def to_dict(self) -> Dict[str, Any]:
        """
        コンポーネントの設定を辞書として取得

        Returns:
            設定辞書
        """
        return {
            "type": "chart",
            "chart_type": self.chart_type,
            "x_column": self.x_column,
            "y_column": self.y_column,
            "title": self.title,
            "height": self.height,
            "kwargs": self.kwargs,
        }
