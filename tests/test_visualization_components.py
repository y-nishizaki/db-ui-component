"""
可視化コンポーネントのテスト

SRPに準拠した可視化コンポーネントの動作をテストします。
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from db_ui_components.visualization import (
    SankeyChartComponent,
    HeatmapComponent,
    NetworkGraphComponent,
    TreemapComponent,
    BubbleChartComponent
)
from db_ui_components.visualization.config import (
    VisualizationConfig,
    SankeyConfig,
    HeatmapConfig,
    NetworkConfig,
    BubbleConfig
)
from db_ui_components.visualization.data_transformer import (
    DataTransformer,
    SankeyDataTransformer,
    HeatmapDataTransformer,
    NetworkDataTransformer
)


class TestVisualizationConfig:
    """可視化設定クラスのテスト"""
    
    def test_visualization_config_default_values(self):
        """デフォルト値のテスト"""
        config = VisualizationConfig()
        
        assert config.title == "Chart"
        assert config.height == 500
        assert config.width is None
        assert config.background_color == "#ffffff"
        assert config.border_color == "#e0e0e0"
        assert config.border_width == 1
        assert config.margin == {"top": 50, "bottom": 50, "left": 50, "right": 50}
    
    def test_visualization_config_custom_values(self):
        """カスタム値のテスト"""
        config = VisualizationConfig(
            title="Custom Chart",
            height=600,
            width=800,
            background_color="#f0f0f0"
        )
        
        assert config.title == "Custom Chart"
        assert config.height == 600
        assert config.width == 800
        assert config.background_color == "#f0f0f0"
    
    def test_visualization_config_validation(self):
        """設定の妥当性検証テスト"""
        # 正常な設定
        config = VisualizationConfig(height=500)
        assert config.validate() is True
        
        # 無効な設定（高さが負の値）
        config = VisualizationConfig(height=-100)
        assert config.validate() is False
        
        # 無効な設定（幅が負の値）
        config = VisualizationConfig(width=-100)
        assert config.validate() is False
    
    def test_visualization_config_to_dict(self):
        """設定の辞書変換テスト"""
        config = VisualizationConfig(title="Test Chart", height=400)
        config_dict = config.to_dict()
        
        assert config_dict["title"] == "Test Chart"
        assert config_dict["height"] == 400
        assert "width" in config_dict
        assert "background_color" in config_dict


class TestSankeyConfig:
    """サンキーチャート設定クラスのテスト"""
    
    def test_sankey_config_default_values(self):
        """デフォルト値のテスト"""
        config = SankeyConfig()
        
        assert config.node_color == "#1f77b4"
        assert config.link_color == "#888888"
        assert config.font_size == 10
    
    def test_sankey_config_to_dict(self):
        """設定の辞書変換テスト"""
        config = SankeyConfig(
            title="Sankey Test",
            node_color="#ff0000",
            link_color="#00ff00"
        )
        config_dict = config.to_dict()
        
        assert config_dict["title"] == "Sankey Test"
        assert config_dict["node_color"] == "#ff0000"
        assert config_dict["link_color"] == "#00ff00"
        assert config_dict["font_size"] == 10


class TestHeatmapConfig:
    """ヒートマップ設定クラスのテスト"""
    
    def test_heatmap_config_default_values(self):
        """デフォルト値のテスト"""
        config = HeatmapConfig()
        
        assert config.color_scale == "Viridis"
        assert config.show_colorbar is True
        assert config.colorbar_title is None
    
    def test_heatmap_config_custom_values(self):
        """カスタム値のテスト"""
        config = HeatmapConfig(
            color_scale="Plasma",
            show_colorbar=False,
            colorbar_title="Custom Scale"
        )
        
        assert config.color_scale == "Plasma"
        assert config.show_colorbar is False
        assert config.colorbar_title == "Custom Scale"


class TestDataTransformer:
    """データ変換クラスのテスト"""
    
    def test_data_transformer_validate_data_empty(self):
        """空データの検証テスト"""
        transformer = Mock(spec=DataTransformer)
        data = pd.DataFrame()
        
        result = transformer.validate_data(data, ["col1", "col2"])
        assert result is False
    
    def test_data_transformer_validate_data_missing_columns(self):
        """不足列の検証テスト"""
        transformer = Mock(spec=DataTransformer)
        data = pd.DataFrame({"col1": [1, 2, 3]})
        
        result = transformer.validate_data(data, ["col1", "col2"])
        assert result is False
    
    def test_data_transformer_validate_data_valid(self):
        """正常データの検証テスト"""
        transformer = Mock(spec=DataTransformer)
        data = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
        
        result = transformer.validate_data(data, ["col1", "col2"])
        assert result is True


class TestSankeyDataTransformer:
    """サンキーチャートデータ変換クラスのテスト"""
    
    def setup_method(self):
        """テスト前のセットアップ"""
        self.transformer = SankeyDataTransformer(
            source_column="source",
            target_column="target",
            value_column="value"
        )
        self.test_data = pd.DataFrame({
            "source": ["A", "A", "B"],
            "target": ["X", "Y", "X"],
            "value": [10, 5, 8]
        })
    
    def test_sankey_data_transformer_transform(self):
        """データ変換テスト"""
        result = self.transformer.transform(self.test_data)
        
        assert result["type"] == "sankey"
        assert "node" in result
        assert "link" in result
        assert len(result["node"]["label"]) == 4  # A, B, X, Y
        assert len(result["link"]) == 3
    
    def test_sankey_data_transformer_missing_columns(self):
        """不足列のエラーテスト"""
        invalid_data = pd.DataFrame({"source": ["A"], "target": ["X"]})
        
        with pytest.raises(ValueError, match="必要な列が見つかりません"):
            self.transformer.transform(invalid_data)
    
    def test_sankey_data_transformer_empty_data(self):
        """空データのエラーテスト"""
        empty_data = pd.DataFrame()
        
        with pytest.raises(ValueError, match="必要な列が見つかりません"):
            self.transformer.transform(empty_data)


class TestHeatmapDataTransformer:
    """ヒートマップデータ変換クラスのテスト"""
    
    def setup_method(self):
        """テスト前のセットアップ"""
        self.transformer = HeatmapDataTransformer(
            x_column="x",
            y_column="y",
            value_column="value"
        )
        self.test_data = pd.DataFrame({
            "x": ["A", "A", "B", "B"],
            "y": ["X", "Y", "X", "Y"],
            "value": [1, 2, 3, 4]
        })
    
    def test_heatmap_data_transformer_transform(self):
        """データ変換テスト"""
        result = self.transformer.transform(self.test_data)
        
        assert result["type"] == "heatmap"
        assert "z" in result
        assert "x" in result
        assert "y" in result
        assert result["colorscale"] == "viridis"
    
    def test_heatmap_data_transformer_missing_columns(self):
        """不足列のエラーテスト"""
        invalid_data = pd.DataFrame({"x": ["A"], "y": ["X"]})
        
        with pytest.raises(ValueError, match="必要な列が見つかりません"):
            self.transformer.transform(invalid_data)


class TestNetworkDataTransformer:
    """ネットワークグラフデータ変換クラスのテスト"""
    
    def setup_method(self):
        """テスト前のセットアップ"""
        self.transformer = NetworkDataTransformer(
            source_column="source",
            target_column="target"
        )
        self.test_data = pd.DataFrame({
            "source": ["Node1", "Node1", "Node2"],
            "target": ["Node2", "Node3", "Node3"]
        })
    
    def test_network_data_transformer_transform(self):
        """データ変換テスト"""
        result = self.transformer.transform(self.test_data)
        
        assert isinstance(result, list)
        assert len(result) == 2  # edge_trace, node_trace
        assert result[0]["name"] == "Edges"
        assert result[1]["name"] == "Nodes"
    
    def test_network_data_transformer_missing_columns(self):
        """不足列のエラーテスト"""
        invalid_data = pd.DataFrame({"source": ["Node1"]})
        
        with pytest.raises(ValueError, match="必要な列が見つかりません"):
            self.transformer.transform(invalid_data)


class TestSankeyChartComponent:
    """サンキーチャートコンポーネントのテスト"""
    
    def setup_method(self):
        """テスト前のセットアップ"""
        self.component = SankeyChartComponent(
            source_column="source",
            target_column="target",
            value_column="value",
            title="Test Sankey"
        )
        self.test_data = pd.DataFrame({
            "source": ["A", "A", "B"],
            "target": ["X", "Y", "X"],
            "value": [10, 5, 8]
        })
    
    def test_sankey_chart_component_initialization(self):
        """初期化テスト"""
        assert self.component.source_column == "source"
        assert self.component.target_column == "target"
        assert self.component.value_column == "value"
        assert self.component.title == "Test Sankey"
        assert self.component.height == 600
    
    def test_sankey_chart_component_prepare_chart_data(self):
        """データ準備テスト"""
        result = self.component._prepare_chart_data(self.test_data)
        
        assert result["type"] == "sankey"
        assert "node" in result
        assert "link" in result
        assert len(result["node"]["label"]) == 4
    
    def test_sankey_chart_component_get_chart_type(self):
        """チャートタイプ取得テスト"""
        chart_type = self.component._get_chart_type()
        assert chart_type == "sankey-chart"
    
    def test_sankey_chart_component_render(self):
        """レンダリングテスト"""
        html = self.component.render(self.test_data)
        
        assert isinstance(html, str)
        assert "sankey-chart" in html
        assert "Plotly.newPlot" in html
        assert "Test Sankey" in html


class TestHeatmapComponent:
    """ヒートマップコンポーネントのテスト"""
    
    def setup_method(self):
        """テスト前のセットアップ"""
        self.component = HeatmapComponent(
            x_column="x",
            y_column="y",
            value_column="value",
            title="Test Heatmap",
            color_scale="Viridis"
        )
        self.test_data = pd.DataFrame({
            "x": ["A", "A", "B", "B"],
            "y": ["X", "Y", "X", "Y"],
            "value": [1, 2, 3, 4]
        })
    
    def test_heatmap_component_initialization(self):
        """初期化テスト"""
        assert self.component.x_column == "x"
        assert self.component.y_column == "y"
        assert self.component.value_column == "value"
        assert self.component.title == "Test Heatmap"
        assert self.component.color_scale == "Viridis"
    
    def test_heatmap_component_prepare_chart_data(self):
        """データ準備テスト"""
        result = self.component._prepare_chart_data(self.test_data)
        
        assert result["type"] == "heatmap"
        assert "z" in result
        assert "x" in result
        assert "y" in result
        assert result["colorscale"] == "viridis"
    
    def test_heatmap_component_get_chart_type(self):
        """チャートタイプ取得テスト"""
        chart_type = self.component._get_chart_type()
        assert chart_type == "heatmap"
    
    def test_heatmap_component_render(self):
        """レンダリングテスト"""
        html = self.component.render(self.test_data)
        
        assert isinstance(html, str)
        assert "heatmap" in html
        assert "Plotly.newPlot" in html
        assert "Test Heatmap" in html


class TestNetworkGraphComponent:
    """ネットワークグラフコンポーネントのテスト"""
    
    def setup_method(self):
        """テスト前のセットアップ"""
        self.component = NetworkGraphComponent(
            source_column="source",
            target_column="target",
            title="Test Network"
        )
        self.test_data = pd.DataFrame({
            "source": ["Node1", "Node1", "Node2"],
            "target": ["Node2", "Node3", "Node3"]
        })
    
    def test_network_graph_component_initialization(self):
        """初期化テスト"""
        assert self.component.source_column == "source"
        assert self.component.target_column == "target"
        assert self.component.title == "Test Network"
        assert self.component.height == 600
    
    def test_network_graph_component_prepare_chart_data(self):
        """データ準備テスト"""
        result = self.component._prepare_chart_data(self.test_data)
        
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["name"] == "Edges"
        assert result[1]["name"] == "Nodes"
    
    def test_network_graph_component_get_chart_type(self):
        """チャートタイプ取得テスト"""
        chart_type = self.component._get_chart_type()
        assert chart_type == "network-graph"
    
    def test_network_graph_component_render(self):
        """レンダリングテスト"""
        html = self.component.render(self.test_data)
        
        assert isinstance(html, str)
        assert "network-graph" in html
        assert "Plotly.newPlot" in html
        assert "Test Network" in html


class TestTreemapComponent:
    """ツリーマップコンポーネントのテスト"""
    
    def setup_method(self):
        """テスト前のセットアップ"""
        self.component = TreemapComponent(
            labels_column="labels",
            parents_column="parents",
            values_column="values",
            title="Test Treemap"
        )
        self.test_data = pd.DataFrame({
            "labels": ["A", "B", "C"],
            "parents": ["", "", ""],
            "values": [20, 30, 15]
        })
    
    def test_treemap_component_initialization(self):
        """初期化テスト"""
        assert self.component.labels_column == "labels"
        assert self.component.parents_column == "parents"
        assert self.component.values_column == "values"
        assert self.component.title == "Test Treemap"
    
    def test_treemap_component_prepare_chart_data(self):
        """データ準備テスト"""
        result = self.component._prepare_chart_data(self.test_data)
        
        assert result["type"] == "treemap"
        assert "labels" in result
        assert "parents" in result
        assert "values" in result
        assert result["textinfo"] == "label+value"
    
    def test_treemap_component_get_chart_type(self):
        """チャートタイプ取得テスト"""
        chart_type = self.component._get_chart_type()
        assert chart_type == "treemap"
    
    def test_treemap_component_render(self):
        """レンダリングテスト"""
        html = self.component.render(self.test_data)
        
        assert isinstance(html, str)
        assert "treemap" in html
        assert "Plotly.newPlot" in html
        assert "Test Treemap" in html


class TestBubbleChartComponent:
    """バブルチャートコンポーネントのテスト"""
    
    def setup_method(self):
        """テスト前のセットアップ"""
        self.component = BubbleChartComponent(
            x_column="x",
            y_column="y",
            size_column="size",
            color_column="color",
            title="Test Bubble"
        )
        self.test_data = pd.DataFrame({
            "x": [1, 2, 3],
            "y": [4, 5, 6],
            "size": [10, 20, 30],
            "color": ["Red", "Blue", "Green"]
        })
    
    def test_bubble_chart_component_initialization(self):
        """初期化テスト"""
        assert self.component.x_column == "x"
        assert self.component.y_column == "y"
        assert self.component.size_column == "size"
        assert self.component.color_column == "color"
        assert self.component.title == "Test Bubble"
    
    def test_bubble_chart_component_prepare_chart_data(self):
        """データ準備テスト"""
        result = self.component._prepare_chart_data(self.test_data)
        
        assert result["type"] == "scatter"
        assert "x" in result
        assert "y" in result
        assert "marker" in result
        assert "color" in result["marker"]
    
    def test_bubble_chart_component_get_chart_type(self):
        """チャートタイプ取得テスト"""
        chart_type = self.component._get_chart_type()
        assert chart_type == "bubble-chart"
    
    def test_bubble_chart_component_render(self):
        """レンダリングテスト"""
        html = self.component.render(self.test_data)
        
        assert isinstance(html, str)
        assert "bubble-chart" in html
        assert "Plotly.newPlot" in html
        assert "Test Bubble" in html


class TestIntegration:
    """統合テスト"""
    
    def test_all_components_with_same_data(self):
        """全コンポーネントの統合テスト"""
        # テストデータ
        data = pd.DataFrame({
            "source": ["A", "A", "B"],
            "target": ["X", "Y", "X"],
            "value": [10, 5, 8],
            "x": ["A", "A", "B"],
            "y": ["X", "Y", "X"],
            "labels": ["A", "B", "C"],
            "parents": ["", "", ""],
            "values": [20, 30, 15]
        })
        
        # 各コンポーネントのテスト
        components = [
            SankeyChartComponent("source", "target", "value"),
            HeatmapComponent("x", "y", "value"),
            NetworkGraphComponent("source", "target"),
            TreemapComponent("labels", "parents", "values"),
            BubbleChartComponent("source", "target", "value")
        ]
        
        for component in components:
            html = component.render(data)
            assert isinstance(html, str)
            assert "Plotly.newPlot" in html


if __name__ == "__main__":
    pytest.main([__file__])