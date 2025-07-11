"""
データ変換モジュールの改善されたテスト

このモジュールには、data_transformer.pyの未カバー部分のテストが含まれています。
"""

import pytest
import pandas as pd
import numpy as np
from typing import Dict, Any
from db_ui_components.visualization.data_transformer import (
    DataTransformer,
    SankeyDataTransformer,
    HeatmapDataTransformer,
    NetworkDataTransformer,
)


class TestDataTransformerConcrete(DataTransformer):
    """テスト用の具体的なDataTransformer実装"""

    def transform(self, data: pd.DataFrame) -> Dict[str, Any]:
        """ダミーの変換実装"""
        return {"data": data.to_dict()}


class TestDataTransformerUncovered:
    """DataTransformerの未カバー部分のテスト"""

    def setup_method(self):
        """テスト前のセットアップ"""
        self.transformer = TestDataTransformerConcrete()

    def test_validate_data_empty_dataframe(self):
        """空のデータフレームでの検証テスト"""
        data = pd.DataFrame()
        required_columns = ["col1", "col2"]

        result = self.transformer.validate_data(data, required_columns)
        assert result is False

    def test_validate_data_missing_columns(self):
        """不足列での検証テスト"""
        data = pd.DataFrame({"col1": [1, 2, 3]})
        required_columns = ["col1", "col2"]

        result = self.transformer.validate_data(data, required_columns)
        assert result is False

    def test_validate_data_valid_data(self):
        """有効なデータでの検証テスト"""
        data = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
        required_columns = ["col1", "col2"]

        result = self.transformer.validate_data(data, required_columns)
        assert result is True

    def test_validate_data_partial_columns(self):
        """部分的な列での検証テスト"""
        data = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6], "col3": [7, 8, 9]})
        required_columns = ["col1", "col2"]

        result = self.transformer.validate_data(data, required_columns)
        assert result is True


class TestSankeyDataTransformerUncovered:
    """SankeyDataTransformerの未カバー部分のテスト"""

    def setup_method(self):
        """テスト前のセットアップ"""
        self.transformer = SankeyDataTransformer(
            source_column="source", target_column="target", value_column="value"
        )

    def test_transform_with_duplicate_links(self):
        """重複リンクでの変換テスト"""
        data = pd.DataFrame(
            {
                "source": ["A", "A", "B", "B", "C"],
                "target": ["B", "C", "D", "E", "D"],
                "value": [10, 5, 8, 12, 15],
            }
        )

        result = self.transformer.transform(data)

        assert "type" in result
        assert result["type"] == "sankey"
        assert "node" in result
        assert "link" in result
        assert len(result["node"]["label"]) > 0
        assert len(result["link"]) > 0

    def test_transform_with_single_node(self):
        """単一ノードでの変換テスト"""
        data = pd.DataFrame({"source": ["A"], "target": ["A"], "value": [10]})

        result = self.transformer.transform(data)

        assert "type" in result
        assert result["type"] == "sankey"
        assert "node" in result
        assert "link" in result
        assert len(result["node"]["label"]) == 1
        assert len(result["link"]) == 1

    def test_transform_with_large_dataset(self):
        """大規模データセットでの変換テスト"""
        # 大規模データセットを作成
        sources = [f"Node{i}" for i in range(100)]
        targets = [f"Node{i+1}" for i in range(100)]
        values = np.random.randint(1, 100, 100)

        data = pd.DataFrame({"source": sources, "target": targets, "value": values})

        result = self.transformer.transform(data)

        assert "type" in result
        assert result["type"] == "sankey"
        assert "node" in result
        assert "link" in result
        assert len(result["node"]["label"]) > 0
        assert len(result["link"]) > 0

    def test_transform_with_numeric_nodes(self):
        """数値ノードでの変換テスト"""
        data = pd.DataFrame(
            {
                "source": [1, 1, 2, 2, 3],
                "target": [2, 3, 4, 5, 4],
                "value": [10, 5, 8, 12, 15],
            }
        )

        result = self.transformer.transform(data)

        assert "type" in result
        assert result["type"] == "sankey"
        assert "node" in result
        assert "link" in result
        assert len(result["node"]["label"]) > 0
        assert len(result["link"]) > 0

    def test_transform_with_mixed_data_types(self):
        """混合データ型での変換テスト"""
        data = pd.DataFrame(
            {
                "source": ["A", 1, "B", 2, "C"],
                "target": ["B", 2, "C", 3, "D"],
                "value": [10.5, 5.2, 8.7, 12.1, 15.9],
            }
        )

        result = self.transformer.transform(data)

        assert "type" in result
        assert result["type"] == "sankey"
        assert "node" in result
        assert "link" in result
        assert len(result["node"]["label"]) > 0
        assert len(result["link"]) > 0


class TestHeatmapDataTransformerUncovered:
    """HeatmapDataTransformerの未カバー部分のテスト"""

    def setup_method(self):
        """テスト前のセットアップ"""
        self.transformer = HeatmapDataTransformer(
            x_column="x", y_column="y", value_column="value"
        )

    def test_transform_with_duplicate_coordinates(self):
        """重複座標での変換テスト"""
        data = pd.DataFrame(
            {
                "x": ["A", "A", "B", "B", "C"],
                "y": ["X", "Y", "X", "Y", "X"],
                "value": [10, 5, 8, 12, 15],
            }
        )

        result = self.transformer.transform(data)

        assert "type" in result
        assert result["type"] == "heatmap"
        assert "z" in result
        assert "x" in result
        assert "y" in result
        assert "colorscale" in result

    def test_transform_with_single_value(self):
        """単一値での変換テスト"""
        data = pd.DataFrame({"x": ["A"], "y": ["X"], "value": [10]})

        result = self.transformer.transform(data)

        assert "type" in result
        assert result["type"] == "heatmap"
        assert "z" in result
        assert "x" in result
        assert "y" in result
        assert "colorscale" in result

    def test_transform_with_large_dataset(self):
        """大規模データセットでの変換テスト"""
        # 大規模データセットを作成
        x_values = [f"X{i}" for i in range(50)]
        y_values = [f"Y{i}" for i in range(50)]
        values = np.random.rand(2500)

        data = pd.DataFrame({"x": x_values * 50, "y": y_values * 50, "value": values})

        result = self.transformer.transform(data)

        assert "type" in result
        assert result["type"] == "heatmap"
        assert "z" in result
        assert "x" in result
        assert "y" in result
        assert "colorscale" in result

    def test_transform_with_numeric_coordinates(self):
        """数値座標での変換テスト"""
        data = pd.DataFrame(
            {
                "x": [1, 1, 2, 2, 3],
                "y": [1, 2, 1, 2, 1],
                "value": [10.5, 5.2, 8.7, 12.1, 15.9],
            }
        )

        result = self.transformer.transform(data)

        assert "type" in result
        assert result["type"] == "heatmap"
        assert "z" in result
        assert "x" in result
        assert "y" in result
        assert "colorscale" in result

    def test_transform_with_missing_values(self):
        """欠損値での変換テスト"""
        data = pd.DataFrame(
            {
                "x": ["A", "A", "B", "B", "C"],
                "y": ["X", "Y", "X", "Y", "X"],
                "value": [10, np.nan, 8, 12, np.nan],
            }
        )

        result = self.transformer.transform(data)

        assert "type" in result
        assert result["type"] == "heatmap"
        assert "z" in result
        assert "x" in result
        assert "y" in result
        assert "colorscale" in result


class TestNetworkDataTransformerUncovered:
    """NetworkDataTransformerの未カバー部分のテスト"""

    def setup_method(self):
        """テスト前のセットアップ"""
        self.transformer = NetworkDataTransformer(
            source_column="source", target_column="target"
        )

    def test_transform_with_duplicate_edges(self):
        """重複エッジでの変換テスト"""
        data = pd.DataFrame(
            {"source": ["A", "A", "B", "B", "C"], "target": ["B", "C", "D", "E", "D"]}
        )

        result = self.transformer.transform(data)

        assert isinstance(result, dict)
        assert "traces" in result
        assert len(result["traces"]) == 2  # エッジとノードのトレース
        assert result["traces"][0]["name"] == "Edges"
        assert result["traces"][1]["name"] == "Nodes"

    def test_transform_with_single_edge(self):
        """単一エッジでの変換テスト"""
        data = pd.DataFrame({"source": ["A"], "target": ["B"]})

        result = self.transformer.transform(data)

        assert isinstance(result, dict)
        assert "traces" in result
        assert len(result["traces"]) == 2
        # ノードが2つあることを確認
        assert len(result["traces"][1]["text"]) == 2

    def test_transform_with_large_dataset(self):
        """大規模データセットでの変換テスト"""
        # 大規模データセットを作成
        sources = [f"Node{i}" for i in range(100)]
        targets = [f"Node{i+1}" for i in range(100)]

        data = pd.DataFrame({"source": sources, "target": targets})

        result = self.transformer.transform(data)

        assert isinstance(result, dict)
        assert "traces" in result
        assert len(result["traces"]) == 2  # エッジとノードのトレース
        assert result["traces"][0]["name"] == "Edges"
        assert result["traces"][1]["name"] == "Nodes"

    def test_transform_with_numeric_nodes(self):
        """数値ノードでの変換テスト"""
        data = pd.DataFrame({"source": [1, 1, 2, 2, 3], "target": [2, 3, 4, 5, 4]})

        result = self.transformer.transform(data)

        assert isinstance(result, dict)
        assert "traces" in result
        assert len(result["traces"]) == 2  # エッジとノードのトレース
        assert result["traces"][0]["name"] == "Edges"
        assert result["traces"][1]["name"] == "Nodes"

    def test_transform_with_mixed_data_types(self):
        """混合データ型での変換テスト"""
        data = pd.DataFrame(
            {"source": ["A", 1, "B", 2, "C"], "target": ["B", 2, "C", 3, "D"]}
        )

        result = self.transformer.transform(data)

        assert isinstance(result, dict)
        assert "traces" in result
        assert len(result["traces"]) == 2  # エッジとノードのトレース
        assert result["traces"][0]["name"] == "Edges"
        assert result["traces"][1]["name"] == "Nodes"


class TestDataTransformerEdgeCases:
    """データ変換のエッジケーステスト"""

    def test_sankey_transformer_with_empty_data(self):
        """空データでのサンキー変換テスト"""
        transformer = SankeyDataTransformer(
            source_column="source", target_column="target", value_column="value"
        )

        empty_data = pd.DataFrame(columns=["source", "target", "value"])

        with pytest.raises(ValueError):
            transformer.transform(empty_data)

    def test_heatmap_transformer_with_empty_data(self):
        """空データでのヒートマップ変換テスト"""
        transformer = HeatmapDataTransformer(
            x_column="x", y_column="y", value_column="value"
        )

        empty_data = pd.DataFrame(columns=["x", "y", "value"])

        with pytest.raises(ValueError):
            transformer.transform(empty_data)

    def test_network_transformer_with_empty_data(self):
        """空データでのネットワーク変換テスト"""
        transformer = NetworkDataTransformer(
            source_column="source", target_column="target"
        )

        empty_data = pd.DataFrame(columns=["source", "target"])

        with pytest.raises(ValueError):
            transformer.transform(empty_data)

    def test_sankey_transformer_with_missing_columns(self):
        """不足列でのサンキー変換テスト"""
        transformer = SankeyDataTransformer(
            source_column="source", target_column="target", value_column="value"
        )

        data = pd.DataFrame({"wrong_column": ["A", "B"], "target": ["B", "C"]})

        with pytest.raises(ValueError):
            transformer.transform(data)

    def test_heatmap_transformer_with_missing_columns(self):
        """不足列でのヒートマップ変換テスト"""
        transformer = HeatmapDataTransformer(
            x_column="x", y_column="y", value_column="value"
        )

        data = pd.DataFrame({"wrong_column": ["A", "B"], "y": ["X", "Y"]})

        with pytest.raises(ValueError):
            transformer.transform(data)

    def test_network_transformer_with_missing_columns(self):
        """不足列でのネットワーク変換テスト"""
        transformer = NetworkDataTransformer(
            source_column="source", target_column="target"
        )

        data = pd.DataFrame({"wrong_column": ["A", "B"]})

        with pytest.raises(ValueError):
            transformer.transform(data)


class TestDataTransformerIntegration:
    """データ変換の統合テスト"""

    def test_multiple_transformers_same_data(self):
        """同一データでの複数変換テスト"""
        data = pd.DataFrame(
            {
                "source": ["A", "B", "C"],
                "target": ["B", "C", "D"],
                "value": [10, 20, 30],
                "x": ["A", "B", "C"],
                "y": ["X", "Y", "Z"],
                "z": [1, 2, 3],
            }
        )

        # サンキー変換
        sankey_transformer = SankeyDataTransformer(
            source_column="source", target_column="target", value_column="value"
        )
        sankey_result = sankey_transformer.transform(data)

        # ヒートマップ変換
        heatmap_transformer = HeatmapDataTransformer(
            x_column="x", y_column="y", value_column="z"
        )
        heatmap_result = heatmap_transformer.transform(data)

        # ネットワーク変換
        network_transformer = NetworkDataTransformer(
            source_column="source", target_column="target"
        )
        network_result = network_transformer.transform(data)

        # 結果の検証
        assert sankey_result["type"] == "sankey"
        assert heatmap_result["type"] == "heatmap"
        assert isinstance(network_result, dict)
        assert "traces" in network_result
        assert len(network_result["traces"]) == 2

    def test_transformer_validation_integration(self):
        """変換器検証の統合テスト"""
        # 有効なデータ
        valid_data = pd.DataFrame(
            {"source": ["A", "B"], "target": ["B", "C"], "value": [10, 20]}
        )

        transformer = SankeyDataTransformer(
            source_column="source", target_column="target", value_column="value"
        )

        # 検証が成功することを確認
        assert (
            transformer.validate_data(valid_data, ["source", "target", "value"]) is True
        )

        # 変換が成功することを確認
        result = transformer.transform(valid_data)
        assert result["type"] == "sankey"

    def test_large_scale_integration(self):
        """大規模統合テスト"""
        # 大規模データセットを作成
        n_nodes = 1000
        sources = [f"Node{i}" for i in range(n_nodes)]
        targets = [f"Node{i+1}" for i in range(n_nodes)]
        values = np.random.randint(1, 100, n_nodes)

        data = pd.DataFrame({"source": sources, "target": targets, "value": values})

        # 各変換器でテスト
        transformers = [
            SankeyDataTransformer("source", "target", "value"),
            NetworkDataTransformer("source", "target"),
        ]

        for transformer in transformers:
            if isinstance(transformer, SankeyDataTransformer):
                result = transformer.transform(data)
                assert result["type"] == "sankey"
                assert len(result["node"]["label"]) > 0
                assert len(result["link"]) > 0
            else:
                result = transformer.transform(data)
                assert isinstance(result, dict)
                assert "traces" in result
                assert len(result["traces"]) == 2

    def test_data_type_handling(self):
        """データ型処理のテスト"""
        # 様々なデータ型を含むデータセット
        data = pd.DataFrame(
            {
                "source": ["A", 1, True, None, "B"],
                "target": ["B", 2, False, "C", "C"],
                "value": [10.5, 20, 30.7, 40, 50.2],
            }
        )

        transformer = SankeyDataTransformer(
            source_column="source", target_column="target", value_column="value"
        )

        # 変換が成功することを確認（None値は適切に処理される）
        result = transformer.transform(data)
        assert result["type"] == "sankey"
        assert len(result["node"]["label"]) > 0
        assert len(result["link"]) > 0
