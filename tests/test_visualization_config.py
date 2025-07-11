"""
可視化コンポーネント設定のテスト

このモジュールには、visualization/config.pyのテストが含まれています。
"""

import pytest
from db_ui_components.visualization.config import (
    VisualizationConfig,
    SankeyConfig,
    HeatmapConfig,
    NetworkConfig,
    BubbleConfig,
)


class TestVisualizationConfig:
    """VisualizationConfigのテスト"""

    def setup_method(self):
        """テスト前のセットアップ"""
        self.config = VisualizationConfig()

    def test_default_initialization(self):
        """デフォルト初期化テスト"""
        assert self.config.title == "Chart"
        assert self.config.height == 500
        assert self.config.width is None
        assert self.config.background_color == "#ffffff"
        assert self.config.border_color == "#e0e0e0"
        assert self.config.border_width == 1
        assert self.config.margin == {"top": 50, "bottom": 50, "left": 50, "right": 50}

    def test_custom_initialization(self):
        """カスタム初期化テスト"""
        config = VisualizationConfig(
            title="カスタムチャート",
            height=600,
            width=800,
            background_color="#f0f0f0",
            border_color="#000000",
            border_width=2,
            margin={"top": 100, "bottom": 100, "left": 100, "right": 100},
        )

        assert config.title == "カスタムチャート"
        assert config.height == 600
        assert config.width == 800
        assert config.background_color == "#f0f0f0"
        assert config.border_color == "#000000"
        assert config.border_width == 2
        assert config.margin == {"top": 100, "bottom": 100, "left": 100, "right": 100}

    def test_to_dict(self):
        """辞書変換テスト"""
        config = VisualizationConfig(title="テストチャート", height=400, width=600)

        config_dict = config.to_dict()

        assert config_dict["title"] == "テストチャート"
        assert config_dict["height"] == 400
        assert config_dict["width"] == 600
        assert config_dict["background_color"] == "#ffffff"
        assert config_dict["border_color"] == "#e0e0e0"
        assert config_dict["border_width"] == 1
        assert config_dict["margin"] == {
            "top": 50,
            "bottom": 50,
            "left": 50,
            "right": 50,
        }

    def test_validate_valid_config(self):
        """有効な設定の検証テスト"""
        config = VisualizationConfig(height=500, width=800)

        assert config.validate() is True

    def test_validate_invalid_height(self):
        """無効な高さでの検証テスト"""
        config = VisualizationConfig(height=0)
        assert config.validate() is False

        config = VisualizationConfig(height=-100)
        assert config.validate() is False

    def test_validate_invalid_width(self):
        """無効な幅での検証テスト"""
        config = VisualizationConfig(width=0)
        assert config.validate() is False

        config = VisualizationConfig(width=-100)
        assert config.validate() is False

    def test_validate_invalid_margin(self):
        """無効なマージンでの検証テスト"""
        config = VisualizationConfig()
        config.margin = {"invalid": 100}
        assert config.validate() is False

        config.margin = {"top": 50, "bottom": 50, "left": 50, "right": 50, "extra": 100}
        assert config.validate() is False


class TestSankeyConfig:
    """SankeyConfigのテスト"""

    def setup_method(self):
        """テスト前のセットアップ"""
        self.config = SankeyConfig()

    def test_default_initialization(self):
        """デフォルト初期化テスト"""
        assert self.config.title == "Chart"
        assert self.config.height == 500
        assert self.config.node_color == "#1f77b4"
        assert self.config.link_color == "#888888"
        assert self.config.font_size == 10

    def test_custom_initialization(self):
        """カスタム初期化テスト"""
        config = SankeyConfig(
            title="サンキーチャート",
            height=600,
            node_color="#ff0000",
            link_color="#00ff00",
            font_size=12,
        )

        assert config.title == "サンキーチャート"
        assert config.height == 600
        assert config.node_color == "#ff0000"
        assert config.link_color == "#00ff00"
        assert config.font_size == 12

    def test_to_dict(self):
        """辞書変換テスト"""
        config = SankeyConfig(
            title="サンキー", node_color="#ff0000", link_color="#00ff00", font_size=14
        )

        config_dict = config.to_dict()

        # 基底クラスの属性
        assert config_dict["title"] == "サンキー"
        assert config_dict["height"] == 500

        # サンキー固有の属性
        assert config_dict["node_color"] == "#ff0000"
        assert config_dict["link_color"] == "#00ff00"
        assert config_dict["font_size"] == 14

    def test_inheritance(self):
        """継承テスト"""
        config = SankeyConfig()

        # 基底クラスのメソッドが利用できることを確認
        assert hasattr(config, "validate")
        assert hasattr(config, "to_dict")

        # 基底クラスの属性が利用できることを確認
        assert hasattr(config, "title")
        assert hasattr(config, "height")
        assert hasattr(config, "width")

        # サンキー固有の属性が利用できることを確認
        assert hasattr(config, "node_color")
        assert hasattr(config, "link_color")
        assert hasattr(config, "font_size")


class TestHeatmapConfig:
    """HeatmapConfigのテスト"""

    def setup_method(self):
        """テスト前のセットアップ"""
        self.config = HeatmapConfig()

    def test_default_initialization(self):
        """デフォルト初期化テスト"""
        assert self.config.title == "Chart"
        assert self.config.height == 500
        assert self.config.color_scale == "Viridis"
        assert self.config.show_colorbar is True
        assert self.config.colorbar_title is None

    def test_custom_initialization(self):
        """カスタム初期化テスト"""
        config = HeatmapConfig(
            title="ヒートマップ",
            height=600,
            color_scale="Plasma",
            show_colorbar=False,
            colorbar_title="値",
        )

        assert config.title == "ヒートマップ"
        assert config.height == 600
        assert config.color_scale == "Plasma"
        assert config.show_colorbar is False
        assert config.colorbar_title == "値"

    def test_to_dict(self):
        """辞書変換テスト"""
        config = HeatmapConfig(
            title="ヒートマップ",
            color_scale="Inferno",
            show_colorbar=True,
            colorbar_title="温度",
        )

        config_dict = config.to_dict()

        # 基底クラスの属性
        assert config_dict["title"] == "ヒートマップ"
        assert config_dict["height"] == 500

        # ヒートマップ固有の属性
        assert config_dict["color_scale"] == "Inferno"
        assert config_dict["show_colorbar"] is True
        assert config_dict["colorbar_title"] == "温度"

    def test_inheritance(self):
        """継承テスト"""
        config = HeatmapConfig()

        # 基底クラスのメソッドが利用できることを確認
        assert hasattr(config, "validate")
        assert hasattr(config, "to_dict")

        # ヒートマップ固有の属性が利用できることを確認
        assert hasattr(config, "color_scale")
        assert hasattr(config, "show_colorbar")
        assert hasattr(config, "colorbar_title")


class TestNetworkConfig:
    """NetworkConfigのテスト"""

    def setup_method(self):
        """テスト前のセットアップ"""
        self.config = NetworkConfig()

    def test_default_initialization(self):
        """デフォルト初期化テスト"""
        assert self.config.title == "Chart"
        assert self.config.height == 500
        assert self.config.node_size == 20
        assert self.config.node_color == "#1f77b4"
        assert self.config.edge_color == "#888888"
        assert self.config.edge_width == 1
        assert self.config.show_legend is False

    def test_custom_initialization(self):
        """カスタム初期化テスト"""
        config = NetworkConfig(
            title="ネットワークグラフ",
            height=600,
            node_size=30,
            node_color="#ff0000",
            edge_color="#00ff00",
            edge_width=2,
            show_legend=True,
        )

        assert config.title == "ネットワークグラフ"
        assert config.height == 600
        assert config.node_size == 30
        assert config.node_color == "#ff0000"
        assert config.edge_color == "#00ff00"
        assert config.edge_width == 2
        assert config.show_legend is True

    def test_to_dict(self):
        """辞書変換テスト"""
        config = NetworkConfig(
            title="ネットワーク",
            node_size=25,
            node_color="#ff0000",
            edge_color="#00ff00",
            edge_width=3,
            show_legend=True,
        )

        config_dict = config.to_dict()

        # 基底クラスの属性
        assert config_dict["title"] == "ネットワーク"
        assert config_dict["height"] == 500

        # ネットワーク固有の属性
        assert config_dict["node_size"] == 25
        assert config_dict["node_color"] == "#ff0000"
        assert config_dict["edge_color"] == "#00ff00"
        assert config_dict["edge_width"] == 3
        assert config_dict["show_legend"] is True

    def test_inheritance(self):
        """継承テスト"""
        config = NetworkConfig()

        # 基底クラスのメソッドが利用できることを確認
        assert hasattr(config, "validate")
        assert hasattr(config, "to_dict")

        # ネットワーク固有の属性が利用できることを確認
        assert hasattr(config, "node_size")
        assert hasattr(config, "node_color")
        assert hasattr(config, "edge_color")
        assert hasattr(config, "edge_width")
        assert hasattr(config, "show_legend")


class TestBubbleConfig:
    """BubbleConfigのテスト"""

    def setup_method(self):
        """テスト前のセットアップ"""
        self.config = BubbleConfig()

    def test_default_initialization(self):
        """デフォルト初期化テスト"""
        assert self.config.title == "Chart"
        assert self.config.height == 500
        assert self.config.min_bubble_size == 4
        assert self.config.max_bubble_size == 50
        assert self.config.color_scale == "Viridis"
        assert self.config.show_colorbar is True

    def test_custom_initialization(self):
        """カスタム初期化テスト"""
        config = BubbleConfig(
            title="バブルチャート",
            height=600,
            min_bubble_size=8,
            max_bubble_size=60,
            color_scale="Plasma",
            show_colorbar=False,
        )

        assert config.title == "バブルチャート"
        assert config.height == 600
        assert config.min_bubble_size == 8
        assert config.max_bubble_size == 60
        assert config.color_scale == "Plasma"
        assert config.show_colorbar is False

    def test_to_dict(self):
        """辞書変換テスト"""
        config = BubbleConfig(
            title="バブル",
            min_bubble_size=10,
            max_bubble_size=80,
            color_scale="Inferno",
            show_colorbar=True,
        )

        config_dict = config.to_dict()

        # 基底クラスの属性
        assert config_dict["title"] == "バブル"
        assert config_dict["height"] == 500

        # バブル固有の属性
        assert config_dict["min_bubble_size"] == 10
        assert config_dict["max_bubble_size"] == 80
        assert config_dict["color_scale"] == "Inferno"
        assert config_dict["show_colorbar"] is True

    def test_inheritance(self):
        """継承テスト"""
        config = BubbleConfig()

        # 基底クラスのメソッドが利用できることを確認
        assert hasattr(config, "validate")
        assert hasattr(config, "to_dict")

        # バブル固有の属性が利用できることを確認
        assert hasattr(config, "min_bubble_size")
        assert hasattr(config, "max_bubble_size")
        assert hasattr(config, "color_scale")
        assert hasattr(config, "show_colorbar")


class TestVisualizationConfigEdgeCases:
    """VisualizationConfigのエッジケーステスト"""

    def test_margin_copy(self):
        """マージンのコピーテスト"""
        config = VisualizationConfig()
        original_margin = config.margin.copy()

        # マージンを変更
        config.margin["top"] = 100

        # to_dictで返されるマージンが元のマージンと異なることを確認
        config_dict = config.to_dict()
        assert config_dict["margin"] != original_margin
        assert config_dict["margin"]["top"] == 100
        assert original_margin["top"] == 50

    def test_none_width(self):
        """None幅のテスト"""
        config = VisualizationConfig(width=None)
        config_dict = config.to_dict()
        assert config_dict["width"] is None

    def test_zero_values(self):
        """ゼロ値のテスト"""
        config = VisualizationConfig(height=0, width=0, border_width=0)

        config_dict = config.to_dict()
        assert config_dict["height"] == 0
        assert config_dict["width"] == 0
        assert config_dict["border_width"] == 0

    def test_large_values(self):
        """大きな値のテスト"""
        config = VisualizationConfig(height=9999, width=9999, border_width=9999)

        config_dict = config.to_dict()
        assert config_dict["height"] == 9999
        assert config_dict["width"] == 9999
        assert config_dict["border_width"] == 9999

    def test_special_characters_in_title(self):
        """タイトルに特殊文字を含むテスト"""
        config = VisualizationConfig(title='特殊文字: "クォート" & <タグ>')
        config_dict = config.to_dict()
        assert config_dict["title"] == '特殊文字: "クォート" & <タグ>'


class TestVisualizationConfigIntegration:
    """VisualizationConfigの統合テスト"""

    def test_all_config_types(self):
        """すべての設定タイプのテスト"""
        configs = [
            VisualizationConfig(title="基本"),
            SankeyConfig(title="サンキー"),
            HeatmapConfig(title="ヒートマップ"),
            NetworkConfig(title="ネットワーク"),
            BubbleConfig(title="バブル"),
        ]

        for config in configs:
            # すべての設定が辞書に変換できることを確認
            config_dict = config.to_dict()
            assert "title" in config_dict
            assert "height" in config_dict
            assert config_dict["title"] in [
                "基本",
                "サンキー",
                "ヒートマップ",
                "ネットワーク",
                "バブル",
            ]

    def test_config_validation_integration(self):
        """設定検証の統合テスト"""
        # 有効な設定
        valid_config = VisualizationConfig(height=500, width=800)
        assert valid_config.validate() is True

        # 無効な設定
        invalid_config = VisualizationConfig(height=0)
        assert invalid_config.validate() is False

        # 無効なマージン
        invalid_margin_config = VisualizationConfig()
        invalid_margin_config.margin = {"invalid": 100}
        assert invalid_margin_config.validate() is False

    def test_inheritance_chain(self):
        """継承チェーンのテスト"""
        sankey_config = SankeyConfig()

        # VisualizationConfigの属性が利用できることを確認
        assert hasattr(sankey_config, "title")
        assert hasattr(sankey_config, "height")
        assert hasattr(sankey_config, "width")
        assert hasattr(sankey_config, "background_color")
        assert hasattr(sankey_config, "border_color")
        assert hasattr(sankey_config, "border_width")
        assert hasattr(sankey_config, "margin")

        # VisualizationConfigのメソッドが利用できることを確認
        assert hasattr(sankey_config, "to_dict")
        assert hasattr(sankey_config, "validate")

        # SankeyConfig固有の属性が利用できることを確認
        assert hasattr(sankey_config, "node_color")
        assert hasattr(sankey_config, "link_color")
        assert hasattr(sankey_config, "font_size")

    def test_config_serialization(self):
        """設定のシリアライゼーションテスト"""
        configs = [
            VisualizationConfig(title="基本設定"),
            SankeyConfig(title="サンキー設定", node_color="#ff0000"),
            HeatmapConfig(title="ヒートマップ設定", color_scale="Plasma"),
            NetworkConfig(title="ネットワーク設定", node_size=30),
            BubbleConfig(title="バブル設定", min_bubble_size=10),
        ]

        for config in configs:
            # 辞書に変換
            config_dict = config.to_dict()

            # 辞書から再構築（実際のfrom_dictメソッドはないが、構造を確認）
            assert isinstance(config_dict, dict)
            assert "title" in config_dict
            assert "height" in config_dict

            # 各設定タイプ固有の属性が含まれていることを確認
            if isinstance(config, SankeyConfig):
                assert "node_color" in config_dict
                assert "link_color" in config_dict
                assert "font_size" in config_dict
            elif isinstance(config, HeatmapConfig):
                assert "color_scale" in config_dict
                assert "show_colorbar" in config_dict
                assert "colorbar_title" in config_dict
            elif isinstance(config, NetworkConfig):
                assert "node_size" in config_dict
                assert "node_color" in config_dict
                assert "edge_color" in config_dict
                assert "edge_width" in config_dict
                assert "show_legend" in config_dict
            elif isinstance(config, BubbleConfig):
                assert "min_bubble_size" in config_dict
                assert "max_bubble_size" in config_dict
                assert "color_scale" in config_dict
                assert "show_colorbar" in config_dict
