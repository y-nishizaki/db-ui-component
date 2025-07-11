"""
高度な可視化コンポーネントのテスト

このモジュールには、サンキーチャート、ヒートマップ、ネットワークグラフなどの
高度な可視化コンポーネントのテストが含まれています。
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
from db_ui_components.visualization_component import (
    SankeyChartComponent,
    HeatmapComponent,
    NetworkGraphComponent,
    TreemapComponent,
    BubbleChartComponent,
)
from db_ui_components.exceptions import ComponentError


class TestSankeyChartComponent:
    """サンキーチャートコンポーネントのテスト"""

    def setup_method(self):
        """テスト前のセットアップ"""
        self.data = pd.DataFrame(
            {
                "source": ["A", "A", "B", "B", "C"],
                "target": ["B", "C", "D", "E", "D"],
                "value": [10, 5, 8, 12, 15],
            }
        )

        self.component = SankeyChartComponent(
            source_column="source",
            target_column="target",
            value_column="value",
            title="テストサンキー",
        )

    def test_sankey_chart_initialization(self):
        """初期化テスト"""
        assert self.component.source_column == "source"
        assert self.component.target_column == "target"
        assert self.component.value_column == "value"
        assert self.component.title == "テストサンキー"
        assert self.component.height == 600

    def test_sankey_chart_render(self):
        """レンダリングテスト"""
        self.component.set_data(self.data)
        html = self.component.render()

        assert isinstance(html, str)
        assert "sankey-chart-" in html
        assert "テストサンキー" in html
        assert "Plotly.newPlot" in html

    def test_sankey_chart_prepare_data(self):
        """データ準備テスト"""
        sankey_data = self.component._prepare_sankey_data(self.data)

        assert "type" in sankey_data
        assert sankey_data["type"] == "sankey"
        assert "node" in sankey_data
        assert "link" in sankey_data
        assert len(sankey_data["node"]["label"]) > 0
        assert len(sankey_data["link"]) > 0

    def test_sankey_chart_render_error(self):
        """エラーハンドリングテスト"""
        invalid_data = pd.DataFrame({"wrong_column": ["A", "B"]})

        self.component.set_data(invalid_data)
        with pytest.raises(ComponentError):
            self.component.render()


class TestHeatmapComponent:
    """ヒートマップコンポーネントのテスト"""

    def setup_method(self):
        """テスト前のセットアップ"""
        # テスト用のヒートマップデータを作成
        x_values = ["A", "B", "C"]
        y_values = ["X", "Y", "Z"]
        values = np.random.rand(9)

        self.data = pd.DataFrame(
            {"x": x_values * 3, "y": y_values * 3, "value": values}
        )

        self.component = HeatmapComponent(
            x_column="x", y_column="y", value_column="value", title="テストヒートマップ"
        )

    def test_heatmap_initialization(self):
        """初期化テスト"""
        assert self.component.x_column == "x"
        assert self.component.y_column == "y"
        assert self.component.value_column == "value"
        assert self.component.title == "テストヒートマップ"
        assert self.component.height == 500
        assert self.component.color_scale == "Viridis"

    def test_heatmap_render(self):
        """レンダリングテスト"""
        self.component.set_data(self.data)
        html = self.component.render()

        assert isinstance(html, str)
        assert "heatmap-" in html
        assert "テストヒートマップ" in html
        assert "Plotly.newPlot" in html

    def test_heatmap_prepare_data(self):
        """データ準備テスト"""
        heatmap_data = self.component._prepare_heatmap_data(self.data)

        assert "type" in heatmap_data
        assert heatmap_data["type"] == "heatmap"
        assert "x" in heatmap_data
        assert "y" in heatmap_data
        assert "z" in heatmap_data

    def test_heatmap_render_error(self):
        """エラーハンドリングテスト"""
        invalid_data = pd.DataFrame({"wrong_column": ["A", "B"]})

        self.component.set_data(invalid_data)
        with pytest.raises(ComponentError):
            self.component.render()


class TestNetworkGraphComponent:
    """ネットワークグラフコンポーネントのテスト"""

    def setup_method(self):
        """テスト前のセットアップ"""
        self.data = pd.DataFrame(
            {
                "source": ["A", "A", "B", "C"],
                "target": ["B", "C", "D", "D"],
                "weight": [1, 2, 3, 4],
            }
        )

        self.component = NetworkGraphComponent(
            source_column="source",
            target_column="target",
            weight_column="weight",
            title="テストネットワーク",
        )

    def test_network_graph_initialization(self):
        """初期化テスト"""
        assert self.component.source_column == "source"
        assert self.component.target_column == "target"
        assert self.component.weight_column == "weight"
        assert self.component.title == "テストネットワーク"
        assert self.component.height == 600

    def test_network_graph_render(self):
        """レンダリングテスト"""
        self.component.set_data(self.data)
        html = self.component.render()

        assert isinstance(html, str)
        assert "network-graph-" in html
        assert "テストネットワーク" in html
        assert "Plotly.newPlot" in html

    def test_network_graph_prepare_data(self):
        """データ準備テスト"""
        result = self.component._prepare_network_data(self.data)

        assert isinstance(result, list)
        assert len(result) == 2  # edge_trace, node_trace
        assert result[0]["name"] == "Edges"
        assert result[1]["name"] == "Nodes"

    def test_network_graph_render_error(self):
        """エラーハンドリングテスト"""
        invalid_data = pd.DataFrame({"wrong_column": ["A", "B"]})

        self.component.set_data(invalid_data)
        with pytest.raises(ComponentError):
            self.component.render()


class TestTreemapComponent:
    """トレーマップコンポーネントのテスト"""

    def setup_method(self):
        """テスト前のセットアップ"""
        self.data = pd.DataFrame(
            {
                "labels": ["A", "B", "C", "D"],
                "parents": ["", "A", "A", "B"],
                "values": [10, 5, 8, 12],
            }
        )

        self.component = TreemapComponent(
            labels_column="labels",
            parents_column="parents",
            values_column="values",
            title="テストトレーマップ",
        )

    def test_treemap_initialization(self):
        """初期化テスト"""
        assert self.component.labels_column == "labels"
        assert self.component.parents_column == "parents"
        assert self.component.values_column == "values"
        assert self.component.title == "テストトレーマップ"
        assert self.component.height == 500

    def test_treemap_render(self):
        """レンダリングテスト"""
        self.component.set_data(self.data)
        html = self.component.render()

        assert isinstance(html, str)
        assert "treemap-" in html
        assert "テストトレーマップ" in html
        assert "Plotly.newPlot" in html

    def test_treemap_prepare_data(self):
        """データ準備テスト"""
        treemap_data = self.component._prepare_treemap_data(self.data)

        assert "type" in treemap_data
        assert treemap_data["type"] == "treemap"
        assert "labels" in treemap_data
        assert "parents" in treemap_data
        assert "values" in treemap_data

    def test_treemap_render_error(self):
        """エラーハンドリングテスト"""
        invalid_data = pd.DataFrame({"wrong_column": ["A", "B"]})

        self.component.set_data(invalid_data)
        with pytest.raises(ComponentError):
            self.component.render()


class TestBubbleChartComponent:
    """バブルチャートコンポーネントのテスト"""

    def setup_method(self):
        """テスト前のセットアップ"""
        self.data = pd.DataFrame(
            {
                "x": [1, 2, 3, 4, 5],
                "y": [10, 20, 30, 40, 50],
                "size": [5, 10, 15, 20, 25],
                "color": ["A", "B", "A", "B", "A"],
            }
        )

        self.component = BubbleChartComponent(
            x_column="x",
            y_column="y",
            size_column="size",
            color_column="color",
            title="テストバブルチャート",
        )

    def test_bubble_chart_initialization(self):
        """初期化テスト"""
        assert self.component.x_column == "x"
        assert self.component.y_column == "y"
        assert self.component.size_column == "size"
        assert self.component.color_column == "color"
        assert self.component.title == "テストバブルチャート"
        assert self.component.height == 500

    def test_bubble_chart_render(self):
        """レンダリングテスト"""
        self.component.set_data(self.data)
        html = self.component.render()

        assert isinstance(html, str)
        assert "bubble-chart-" in html
        assert "テストバブルチャート" in html
        assert "Plotly.newPlot" in html

    def test_bubble_chart_prepare_data(self):
        """データ準備テスト"""
        bubble_data = self.component._prepare_bubble_data(self.data)

        assert "type" in bubble_data
        assert bubble_data["type"] == "scatter"
        assert "x" in bubble_data
        assert "y" in bubble_data
        assert "mode" in bubble_data
        assert bubble_data["mode"] == "markers"

    def test_bubble_chart_render_error(self):
        """エラーハンドリングテスト"""
        invalid_data = pd.DataFrame({"wrong_column": ["A", "B"]})

        self.component.set_data(invalid_data)
        with pytest.raises(ComponentError):
            self.component.render()

    def test_bubble_chart_without_color(self):
        """色なしバブルチャートテスト"""
        component_no_color = BubbleChartComponent(
            x_column="x", y_column="y", size_column="size", title="テストバブルチャート"
        )

        component_no_color.set_data(self.data)
        html = component_no_color.render()
        assert isinstance(html, str)
        assert "bubble-chart-" in html


class TestVisualizationComponentEdgeCases:
    """可視化コンポーネントのエッジケーステスト"""

    def test_sankey_empty_data(self):
        """空データのサンキーチャートテスト"""
        empty_data = pd.DataFrame(columns=["source", "target", "value"])
        component = SankeyChartComponent(
            source_column="source", target_column="target", value_column="value"
        )

        component.set_data(empty_data)
        # 空データでもレンダリングされるが、空のグラフが表示される
        html = component.render()
        assert isinstance(html, str)
        assert "sankey-chart-" in html

    def test_heatmap_single_value(self):
        """単一値のヒートマップテスト"""
        single_data = pd.DataFrame({"x": ["A"], "y": ["X"], "value": [1.0]})

        component = HeatmapComponent(x_column="x", y_column="y", value_column="value")

        component.set_data(single_data)
        html = component.render()
        assert isinstance(html, str)

    def test_network_graph_no_weight(self):
        """重みなしネットワークグラフテスト"""
        data = pd.DataFrame({"source": ["A", "B"], "target": ["B", "C"]})

        component = NetworkGraphComponent(
            source_column="source", target_column="target"
        )

        component.set_data(data)
        html = component.render()
        assert isinstance(html, str)

    def test_treemap_flat_structure(self):
        """フラット構造のトレーマップテスト"""
        flat_data = pd.DataFrame(
            {"labels": ["A", "B", "C"], "parents": ["", "", ""], "values": [10, 20, 30]}
        )

        component = TreemapComponent(
            labels_column="labels", parents_column="parents", values_column="values"
        )

        component.set_data(flat_data)
        html = component.render()
        assert isinstance(html, str)

    def test_bubble_chart_large_data(self):
        """大規模データのバブルチャートテスト"""
        large_data = pd.DataFrame(
            {
                "x": np.random.randn(1000),
                "y": np.random.randn(1000),
                "size": np.random.randint(1, 100, 1000),
                "color": np.random.choice(["A", "B", "C"], 1000),
            }
        )

        component = BubbleChartComponent(
            x_column="x", y_column="y", size_column="size", color_column="color"
        )

        component.set_data(large_data)
        html = component.render()
        assert isinstance(html, str)
        assert len(html) > 0


class TestVisualizationComponentIntegration:
    """可視化コンポーネントの統合テスト"""

    def test_multiple_components_same_page(self):
        """同一ページでの複数コンポーネントテスト"""
        data = pd.DataFrame(
            {
                "source": ["A", "B"],
                "target": ["B", "C"],
                "value": [10, 20],
                "x": ["A", "B"],
                "y": ["X", "Y"],
                "z": [1, 2],
            }
        )

        sankey = SankeyChartComponent(
            source_column="source", target_column="target", value_column="value"
        )

        heatmap = HeatmapComponent(x_column="x", y_column="y", value_column="z")

        sankey.set_data(data)
        heatmap.set_data(data)
        sankey_html = sankey.render()
        heatmap_html = heatmap.render()

        assert isinstance(sankey_html, str)
        assert isinstance(heatmap_html, str)
        assert sankey.component_id != heatmap.component_id

    def test_component_id_uniqueness(self):
        """コンポーネントIDの一意性テスト"""
        component1 = SankeyChartComponent(
            source_column="source", target_column="target", value_column="value"
        )

        component2 = HeatmapComponent(x_column="x", y_column="y", value_column="z")

        assert component1.component_id != component2.component_id

    def test_custom_height_and_title(self):
        """カスタム高さとタイトルのテスト"""
        component = SankeyChartComponent(
            source_column="source",
            target_column="target",
            value_column="value",
            title="カスタムタイトル",
            height=800,
        )

        assert component.title == "カスタムタイトル"
        assert component.height == 800

    def test_json_serialization(self):
        """JSONシリアライゼーションテスト"""
        data = pd.DataFrame(
            {"source": ["A", "B"], "target": ["B", "C"], "value": [10, 20]}
        )

        component = SankeyChartComponent(
            source_column="source", target_column="target", value_column="value"
        )

        # JSONシリアライゼーションが正常に動作することを確認
        sankey_data = component._prepare_sankey_data(data)
        import json

        json_str = json.dumps(sankey_data)
        assert isinstance(json_str, str)
        assert len(json_str) > 0
