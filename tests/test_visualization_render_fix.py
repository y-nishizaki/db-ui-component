"""
render()メソッドの修正に対応したテスト

visualization_component.pyとbase_visualization.pyのrender()メソッドが
引数を取らないように変更されたため、set_data()を使用するテストを作成
"""

import pytest
import pandas as pd
from db_ui_components.visualization_component import (
    SankeyChartComponent,
    HeatmapComponent,
    NetworkGraphComponent,
    TreemapComponent,
    BubbleChartComponent,
)
from db_ui_components.visualization.base_visualization import BaseVisualizationComponent


class TestVisualizationRenderFix:
    """render()メソッド修正後のテスト"""

    @pytest.fixture
    def sample_data(self):
        """テスト用サンプルデータ"""
        return pd.DataFrame(
            {
                "source": ["A", "A", "B", "B", "C"],
                "target": ["B", "C", "C", "D", "D"],
                "value": [10, 20, 15, 25, 30],
                "x": [1, 2, 3, 4, 5],
                "y": [10, 20, 30, 40, 50],
                "size": [100, 200, 150, 250, 300],
                "category": ["cat1", "cat1", "cat2", "cat2", "cat3"],
                "label": ["Node1", "Node2", "Node3", "Node4", "Node5"],
                "parent": ["", "Node1", "Node1", "Node2", "Node2"],
            }
        )

    def test_sankey_chart_with_set_data(self, sample_data):
        """SankeyChartComponentのset_data()とrender()のテスト"""
        component = SankeyChartComponent(
            source_column="source",
            target_column="target",
            value_column="value",
            title="Test Sankey",
        )

        # データ未設定時のレンダリング
        html = component.render()
        assert "データが設定されていません" in html

        # データ設定後のレンダリング
        component.set_data(sample_data)
        html = component.render()
        assert "sankey" in html.lower()
        assert "Test Sankey" in html

    def test_heatmap_with_set_data(self, sample_data):
        """HeatmapComponentのset_data()とrender()のテスト"""
        component = HeatmapComponent(
            x_column="source",
            y_column="target",
            value_column="value",
            title="Test Heatmap",
        )

        # データ未設定時のレンダリング
        html = component.render()
        assert "データが設定されていません" in html

        # データ設定後のレンダリング
        component.set_data(sample_data)
        html = component.render()
        assert "heatmap" in html.lower()
        assert "Test Heatmap" in html

    def test_network_graph_with_set_data(self, sample_data):
        """NetworkGraphComponentのset_data()とrender()のテスト"""
        component = NetworkGraphComponent(
            source_column="source",
            target_column="target",
            weight_column="value",
            title="Test Network",
        )

        # データ未設定時のレンダリング
        html = component.render()
        assert "データが設定されていません" in html

        # データ設定後のレンダリング
        component.set_data(sample_data)
        html = component.render()
        assert "network" in html.lower()
        assert "Test Network" in html

    def test_treemap_with_set_data(self, sample_data):
        """TreemapComponentのset_data()とrender()のテスト"""
        component = TreemapComponent(
            labels_column="label",
            parents_column="parent",
            values_column="value",
            title="Test Treemap",
        )

        # データ未設定時のレンダリング
        html = component.render()
        assert "データが設定されていません" in html

        # データ設定後のレンダリング
        component.set_data(sample_data)
        html = component.render()
        assert "treemap" in html.lower()
        assert "Test Treemap" in html

    def test_bubble_chart_with_set_data(self, sample_data):
        """BubbleChartComponentのset_data()とrender()のテスト"""
        component = BubbleChartComponent(
            x_column="x",
            y_column="y",
            size_column="size",
            color_column="category",
            title="Test Bubble",
        )

        # データ未設定時のレンダリング
        html = component.render()
        assert "データが設定されていません" in html

        # データ設定後のレンダリング
        component.set_data(sample_data)
        html = component.render()
        assert "bubble" in html.lower()
        assert "Test Bubble" in html

    def test_base_visualization_error_handling(self):
        """BaseVisualizationComponentのエラーハンドリングテスト"""
        # BaseVisualizationComponentを直接使うことはできないが、
        # 継承クラスでエラーが適切に処理されることを確認
        component = SankeyChartComponent(
            source_column="invalid", target_column="invalid", value_column="invalid"
        )

        # 無効なデータでComponentErrorが発生することを確認
        invalid_data = pd.DataFrame({"col1": [1, 2, 3]})
        component.set_data(invalid_data)

        from db_ui_components.exceptions import ComponentError

        with pytest.raises(
            ComponentError, match="サンキーチャートのレンダリングに失敗しました"
        ):
            component.render()
