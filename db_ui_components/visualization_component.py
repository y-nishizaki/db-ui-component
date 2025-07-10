"""
高度な可視化コンポーネント

このモジュールには、サンキーチャート、ヒートマップ、ネットワークグラフなどの
高度な可視化コンポーネントが含まれています。
"""

import json
import pandas as pd
from typing import Dict, List, Optional, Any
from .base_component import BaseComponent
from .exceptions import ComponentError


class SankeyChartComponent(BaseComponent):
    """
    サンキーチャートコンポーネント

    データフローやプロセスフローを可視化するためのサンキーチャートを生成します。
    """

    def __init__(
        self,
        source_column: str,
        target_column: str,
        value_column: str,
        title: str = "Sankey Chart",
        height: int = 600,
        **kwargs,
    ):
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
        super().__init__(**kwargs)
        self.source_column = source_column
        self.target_column = target_column
        self.value_column = value_column
        self.title = title
        self.height = height
        self._data: Optional[pd.DataFrame] = None

    def set_data(self, data: pd.DataFrame) -> None:
        """データを設定"""
        self._data = data

    def render(self) -> str:
        """
        サンキーチャートをレンダリング

        Returns:
            レンダリングされたHTML
        """
        if self._data is None:
            return "<div>データが設定されていません</div>"

        try:
            # データの前処理
            sankey_data = self._prepare_sankey_data(self._data)

            # HTMLテンプレートの生成
            html = f"""
            <div id="sankey-chart-{self.component_id}"
                 style="width: 100%; height: {self.height}px;"></div>
            <script>
                // Plotly.jsを使用したサンキーチャート
                const data = {json.dumps(sankey_data)};
                const layout = {{
                    title: '{self.title}',
                    font: {{
                        size: 10
                    }},
                    height: {self.height}
                }};

                Plotly.newPlot('sankey-chart-{self.component_id}', data, layout);
            </script>
            """

            return html

        except Exception as e:
            raise ComponentError(f"サンキーチャートのレンダリングに失敗しました: {str(e)}")

    def _prepare_sankey_data(self, data: pd.DataFrame) -> Dict:
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

            links.append({"source": source_idx, "target": target_idx, "value": value})

        return {
            "type": "sankey",
            "node": {"label": all_nodes, "color": ["#1f77b4"] * len(all_nodes)},
            "link": links,
        }


class HeatmapComponent(BaseComponent):
    """
    ヒートマップコンポーネント

    2次元データの相関や分布を可視化するためのヒートマップを生成します。
    """

    def __init__(
        self,
        x_column: str,
        y_column: str,
        value_column: str,
        title: str = "Heatmap",
        height: int = 500,
        color_scale: str = "Viridis",
        **kwargs,
    ):
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
        super().__init__(**kwargs)
        self.x_column = x_column
        self.y_column = y_column
        self.value_column = value_column
        self.title = title
        self.height = height
        self.color_scale = color_scale
        self._data: Optional[pd.DataFrame] = None

    def set_data(self, data: pd.DataFrame) -> None:
        """データを設定"""
        self._data = data

    def render(self) -> str:
        """
        ヒートマップをレンダリング

        Returns:
            レンダリングされたHTML
        """
        if self._data is None:
            return "<div>データが設定されていません</div>"

        try:
            # データの前処理
            heatmap_data = self._prepare_heatmap_data(self._data)

            # HTMLテンプレートの生成
            html = f"""
            <div id="heatmap-{self.component_id}"
                 style="width: 100%; height: {self.height}px;"></div>
            <script>
                const data = {json.dumps(heatmap_data)};

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

                Plotly.newPlot('heatmap-{self.component_id}', data, layout);
            </script>
            """

            return html

        except Exception as e:
            raise ComponentError(f"ヒートマップのレンダリングに失敗しました: {str(e)}")

    def _prepare_heatmap_data(self, data: pd.DataFrame) -> Dict:
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
            aggfunc="mean",
        )

        return {
            "type": "heatmap",
            "z": pivot_data.values.tolist(),
            "x": pivot_data.columns.tolist(),
            "y": pivot_data.index.tolist(),
            "colorscale": self.color_scale.lower(),
        }


class NetworkGraphComponent(BaseComponent):
    """
    ネットワークグラフコンポーネント

    ノードとエッジの関係を可視化するためのネットワークグラフを生成します。
    """

    def __init__(
        self,
        source_column: str,
        target_column: str,
        weight_column: Optional[str] = None,
        title: str = "Network Graph",
        height: int = 600,
        **kwargs,
    ):
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
        super().__init__(**kwargs)
        self.source_column = source_column
        self.target_column = target_column
        self.weight_column = weight_column
        self.title = title
        self.height = height
        self._data: Optional[pd.DataFrame] = None

    def set_data(self, data: pd.DataFrame) -> None:
        """データを設定"""
        self._data = data

    def render(self) -> str:
        """
        ネットワークグラフをレンダリング

        Returns:
            レンダリングされたHTML
        """
        if self._data is None:
            return "<div>データが設定されていません</div>"

        try:
            # データの前処理
            network_data = self._prepare_network_data(self._data)

            # HTMLテンプレートの生成
            html = f"""
            <div id="network-graph-{self.component_id}"
                 style="width: 100%; height: {self.height}px;"></div>
            <script>
                const data = {json.dumps(network_data)};

                const layout = {{
                    title: '{self.title}',
                    showlegend: false,
                    height: {self.height},
                    hovermode: 'closest'
                }};

                Plotly.newPlot('network-graph-{self.component_id}', data, layout);
            </script>
            """

            return html

        except Exception as e:
            raise ComponentError(f"ネットワークグラフのレンダリングに失敗しました: {str(e)}")

    def _prepare_network_data(self, data: pd.DataFrame) -> List[Dict]:
        """
        ネットワークグラフ用のデータを準備

        Args:
            data: 元のデータフレーム

        Returns:
            ネットワークグラフ用のデータリスト
        """
        # ノードのリストを作成
        all_nodes = list(
            set(
                list(data[self.source_column].unique())
                + list(data[self.target_column].unique())
            )
        )

        # ノードの座標を計算（簡易的な円形配置）
        import math

        node_positions = {}
        for i, node in enumerate(all_nodes):
            angle = 2 * math.pi * i / len(all_nodes)
            x = math.cos(angle)
            y = math.sin(angle)
            node_positions[node] = {"x": x, "y": y}

        # ノードのトレース
        node_trace = {
            "type": "scatter",
            "x": [node_positions[node]["x"] for node in all_nodes],
            "y": [node_positions[node]["y"] for node in all_nodes],
            "mode": "markers+text",
            "text": all_nodes,
            "textposition": "middle center",
            "marker": {"size": 20, "color": ["#1f77b4"] * len(all_nodes)},
            "name": "Nodes",
        }

        # エッジのトレース
        edge_x = []
        edge_y = []

        for _, row in data.iterrows():
            source = row[self.source_column]
            target = row[self.target_column]

            if source in node_positions and target in node_positions:
                edge_x.extend(
                    [node_positions[source]["x"], node_positions[target]["x"], None]
                )
                edge_y.extend(
                    [node_positions[source]["y"], node_positions[target]["y"], None]
                )

        edge_trace = {
            "type": "scatter",
            "x": edge_x,
            "y": edge_y,
            "mode": "lines",
            "line": {"width": 1, "color": "#888"},
            "name": "Edges",
        }

        return [edge_trace, node_trace]


class TreemapComponent(BaseComponent):
    """
    ツリーマップコンポーネント

    階層構造を持つデータを可視化するためのツリーマップを生成します。
    """

    def __init__(
        self,
        labels_column: str,
        parents_column: str,
        values_column: str,
        title: str = "Treemap",
        height: int = 500,
        **kwargs,
    ):
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
        super().__init__(**kwargs)
        self.labels_column = labels_column
        self.parents_column = parents_column
        self.values_column = values_column
        self.title = title
        self.height = height
        self._data: Optional[pd.DataFrame] = None

    def set_data(self, data: pd.DataFrame) -> None:
        """データを設定"""
        self._data = data

    def render(self) -> str:
        """
        ツリーマップをレンダリング

        Returns:
            レンダリングされたHTML
        """
        if self._data is None:
            return "<div>データが設定されていません</div>"

        try:
            # データの前処理
            treemap_data = self._prepare_treemap_data(self._data)

            # HTMLテンプレートの生成
            html = f"""
            <div id="treemap-{self.component_id}"
                 style="width: 100%; height: {self.height}px;"></div>
            <script>
                const data = {json.dumps(treemap_data)};

                const layout = {{
                    title: '{self.title}',
                    height: {self.height}
                }};

                Plotly.newPlot('treemap-{self.component_id}', data, layout);
            </script>
            """

            return html

        except Exception as e:
            raise ComponentError(f"ツリーマップのレンダリングに失敗しました: {str(e)}")

    def _prepare_treemap_data(self, data: pd.DataFrame) -> Dict:
        """
        ツリーマップ用のデータを準備

        Args:
            data: 元のデータフレーム

        Returns:
            ツリーマップ用のデータ辞書
        """
        return {
            "type": "treemap",
            "labels": data[self.labels_column].tolist(),
            "parents": data[self.parents_column].tolist(),
            "values": data[self.values_column].tolist(),
            "textinfo": "label+value",
        }


class BubbleChartComponent(BaseComponent):
    """
    バブルチャートコンポーネント

    3次元データを可視化するためのバブルチャートを生成します。
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
        super().__init__(**kwargs)
        self.x_column = x_column
        self.y_column = y_column
        self.size_column = size_column
        self.color_column = color_column
        self.title = title
        self.height = height
        self._data: Optional[pd.DataFrame] = None

    def set_data(self, data: pd.DataFrame) -> None:
        """データを設定"""
        self._data = data

    def render(self) -> str:
        """
        バブルチャートをレンダリング

        Returns:
            レンダリングされたHTML
        """
        if self._data is None:
            return "<div>データが設定されていません</div>"

        try:
            # データの前処理
            bubble_data = self._prepare_bubble_data(self._data)

            # HTMLテンプレートの生成
            html = f"""
            <div id="bubble-chart-{self.component_id}"
                 style="width: 100%; height: {self.height}px;"></div>
            <script>
                const data = {json.dumps(bubble_data)};

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

                Plotly.newPlot('bubble-chart-{self.component_id}', data, layout);
            </script>
            """

            return html

        except Exception as e:
            raise ComponentError(f"バブルチャートのレンダリングに失敗しました: {str(e)}")

    def _prepare_bubble_data(self, data: pd.DataFrame) -> Dict:
        """
        バブルチャート用のデータを準備

        Args:
            data: 元のデータフレーム

        Returns:
            バブルチャート用のデータ辞書
        """
        # サイズの正規化
        import numpy as np

        sizes = np.array(data[self.size_column].values)
        sizes_min = float(np.min(sizes))
        sizes_max = float(np.max(sizes))
        normalized_sizes = (sizes - sizes_min) / (sizes_max - sizes_min) * 50 + 10

        bubble_data: Dict[str, Any] = {
            "type": "scatter",
            "x": data[self.x_column].tolist(),
            "y": data[self.y_column].tolist(),
            "mode": "markers",
            "marker": {
                "size": normalized_sizes.tolist(),
                "sizemode": "area",
                "sizeref": 2 * float(np.max(normalized_sizes)) / (40**2),
                "sizemin": 4,
            },
            "text": data[self.size_column].tolist(),
            "hovertemplate": (
                f"{self.x_column}: %{{x}}<br>{self.y_column}: %{{y}}<br>"
                f"{self.size_column}: %{{text}}<extra></extra>"
            ),
        }

        # カラー分けがある場合
        if self.color_column:
            marker = bubble_data["marker"]
            assert isinstance(marker, dict)  # type guard
            marker["color"] = data[self.color_column].tolist()
            marker["colorscale"] = "Viridis"
            marker["showscale"] = True
            marker["colorbar"] = {"title": self.color_column}

        return bubble_data
