"""
可視化データ変換管理

責任:
- 可視化用データの変換
- データの前処理
- データの検証
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List
from abc import ABC, abstractmethod


class DataTransformer(ABC):
    """
    データ変換の基底クラス

    責任: データ変換の共通インターフェース
    """

    @abstractmethod
    def transform(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        データを変換

        Args:
            data: 元のデータフレーム

        Returns:
            変換されたデータ
        """
        pass

    def validate_data(self, data: pd.DataFrame, required_columns: List[str]) -> bool:
        """
        データの妥当性を検証

        Args:
            data: 検証するデータフレーム
            required_columns: 必要な列名のリスト

        Returns:
            妥当性の結果
        """
        if data.empty:
            return False

        missing_columns = [col for col in required_columns if col not in data.columns]
        return len(missing_columns) == 0


class SankeyDataTransformer(DataTransformer):
    """
    サンキーチャート用データ変換クラス

    責任: サンキーチャート用のデータ変換
    """

    def __init__(self, source_column: str, target_column: str, value_column: str):
        """
        初期化

        Args:
            source_column: ソースノードの列名
            target_column: ターゲットノードの列名
            value_column: フロー値の列名
        """
        self.source_column = source_column
        self.target_column = target_column
        self.value_column = value_column

    def transform(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        サンキーチャート用のデータを変換

        Args:
            data: 元のデータフレーム

        Returns:
            サンキーチャート用のデータ辞書
        """
        required_columns = [self.source_column, self.target_column, self.value_column]
        if not self.validate_data(data, required_columns):
            raise ValueError(f"必要な列が見つかりません: {required_columns}")

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


class HeatmapDataTransformer(DataTransformer):
    """
    ヒートマップ用データ変換クラス

    責任: ヒートマップ用のデータ変換
    """

    def __init__(self, x_column: str, y_column: str, value_column: str):
        """
        初期化

        Args:
            x_column: X軸の列名
            y_column: Y軸の列名
            value_column: 値の列名
        """
        self.x_column = x_column
        self.y_column = y_column
        self.value_column = value_column

    def transform(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        ヒートマップ用のデータを変換

        Args:
            data: 元のデータフレーム

        Returns:
            ヒートマップ用のデータ辞書
        """
        required_columns = [self.x_column, self.y_column, self.value_column]
        if not self.validate_data(data, required_columns):
            raise ValueError(f"必要な列が見つかりません: {required_columns}")

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
            "colorscale": "viridis",
        }


class NetworkDataTransformer(DataTransformer):
    """
    ネットワークグラフ用データ変換クラス

    責任: ネットワークグラフ用のデータ変換
    """

    def __init__(self, source_column: str, target_column: str):
        """
        初期化

        Args:
            source_column: ソースノードの列名
            target_column: ターゲットノードの列名
        """
        self.source_column = source_column
        self.target_column = target_column

    def transform(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        ネットワークグラフ用のデータを変換

        Args:
            data: 元のデータフレーム

        Returns:
            ネットワークグラフ用のデータリスト
        """
        required_columns = [self.source_column, self.target_column]
        if not self.validate_data(data, required_columns):
            raise ValueError(f"必要な列が見つかりません: {required_columns}")

        # ノードのリストを作成
        all_nodes = list(
            set(
                list(data[self.source_column].unique())
                + list(data[self.target_column].unique())
            )
        )

        # ノードの座標を計算（簡易的な円形配置）
        node_positions = {}
        for i, node in enumerate(all_nodes):
            angle = 2 * np.pi * i / len(all_nodes)
            x = np.cos(angle)
            y = np.sin(angle)
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

        return {"traces": [edge_trace, node_trace]}
