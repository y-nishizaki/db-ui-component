"""
設定管理のテスト

ConfigManagerと各種設定クラスの全機能をテストします。
"""

import pytest
import json
import tempfile
import os
from unittest.mock import patch, MagicMock
from db_ui_components.config import (
    LayoutType, ChartType, FilterType,
    ComponentConfig, DashboardConfig, TableConfig, ChartConfig, FilterConfig,
    ConfigManager
)


class TestEnums:
    """列挙型のテスト"""
    
    def test_layout_type(self):
        """LayoutTypeのテスト"""
        assert LayoutType.GRID.value == "grid"
        assert LayoutType.FLEX.value == "flex"
        assert LayoutType.CUSTOM.value == "custom"
    
    def test_chart_type(self):
        """ChartTypeのテスト"""
        assert ChartType.LINE.value == "line"
        assert ChartType.BAR.value == "bar"
        assert ChartType.PIE.value == "pie"
        assert ChartType.SCATTER.value == "scatter"
        assert ChartType.HEATMAP.value == "heatmap"
    
    def test_filter_type(self):
        """FilterTypeのテスト"""
        assert FilterType.DATE.value == "date"
        assert FilterType.DROPDOWN.value == "dropdown"
        assert FilterType.MULTISELECT.value == "multiselect"
        assert FilterType.TEXT.value == "text"


class TestComponentConfig:
    """ComponentConfigのテスト"""
    
    def test_default_values(self):
        """デフォルト値のテスト"""
        config = ComponentConfig()
        assert config.component_id is None
        assert config.title is None
        assert config.height == 400
        assert config.width is None
        assert config.background_color == "white"
        assert config.border_color == "#ddd"
        assert config.border_radius == 8
        assert config.padding == 16
        assert config.margin == 10
        assert config.responsive is True
        assert config.min_width is None
        assert config.max_width is None
    
    def test_custom_values(self):
        """カスタム値のテスト"""
        config = ComponentConfig(
            component_id="test-id",
            title="Test Title",
            height=500,
            width=300,
            background_color="blue",
            border_color="red",
            border_radius=10,
            padding=20,
            margin=15,
            responsive=False,
            min_width=200,
            max_width=800
        )
        assert config.component_id == "test-id"
        assert config.title == "Test Title"
        assert config.height == 500
        assert config.width == 300
        assert config.background_color == "blue"
        assert config.border_color == "red"
        assert config.border_radius == 10
        assert config.padding == 20
        assert config.margin == 15
        assert config.responsive is False
        assert config.min_width == 200
        assert config.max_width == 800
    
    def test_to_dict(self):
        """辞書形式への変換テスト"""
        config = ComponentConfig(
            component_id="test-id",
            title="Test Title",
            height=500
        )
        result = config.to_dict()
        expected = {
            "component_id": "test-id",
            "title": "Test Title",
            "height": 500,
            "width": None,
            "background_color": "white",
            "border_color": "#ddd",
            "border_radius": 8,
            "padding": 16,
            "margin": 10,
            "responsive": True,
            "min_width": None,
            "max_width": None
        }
        assert result == expected
    
    def test_from_dict(self):
        """辞書形式からの作成テスト"""
        data = {
            "component_id": "test-id",
            "title": "Test Title",
            "height": 500,
            "width": 300,
            "background_color": "blue"
        }
        config = ComponentConfig.from_dict(data)
        assert config.component_id == "test-id"
        assert config.title == "Test Title"
        assert config.height == 500
        assert config.width == 300
        assert config.background_color == "blue"


class TestDashboardConfig:
    """DashboardConfigのテスト"""
    
    def test_default_values(self):
        """デフォルト値のテスト"""
        config = DashboardConfig()
        assert config.title is None
        assert config.layout == LayoutType.GRID
        assert config.grid_columns == 12
        assert config.gap == 20
        assert config.padding == 20
        assert config.show_header is True
        assert config.header_background == "#f8f9fa"
        assert config.header_padding == 20
        assert config.container_background == "transparent"
        assert config.container_border_radius == 8
    
    def test_custom_values(self):
        """カスタム値のテスト"""
        config = DashboardConfig(
            title="Test Dashboard",
            layout=LayoutType.FLEX,
            grid_columns=6,
            gap=30,
            padding=25,
            show_header=False,
            header_background="blue",
            header_padding=25,
            container_background="white",
            container_border_radius=10
        )
        assert config.title == "Test Dashboard"
        assert config.layout == LayoutType.FLEX
        assert config.grid_columns == 6
        assert config.gap == 30
        assert config.padding == 25
        assert config.show_header is False
        assert config.header_background == "blue"
        assert config.header_padding == 25
        assert config.container_background == "white"
        assert config.container_border_radius == 10
    
    def test_to_dict(self):
        """辞書形式への変換テスト"""
        config = DashboardConfig(title="Test Dashboard")
        result = config.to_dict()
        expected = {
            "title": "Test Dashboard",
            "layout": "grid",
            "grid_columns": 12,
            "gap": 20,
            "padding": 20,
            "show_header": True,
            "header_background": "#f8f9fa",
            "header_padding": 20,
            "container_background": "transparent",
            "container_border_radius": 8
        }
        assert result == expected
    
    def test_from_dict(self):
        """辞書形式からの作成テスト"""
        data = {
            "title": "Test Dashboard",
            "layout": "flex",
            "grid_columns": 6
        }
        config = DashboardConfig.from_dict(data)
        assert config.title == "Test Dashboard"
        assert config.layout == LayoutType.FLEX
        assert config.grid_columns == 6


class TestTableConfig:
    """TableConfigのテスト"""
    
    def test_default_values(self):
        """デフォルト値のテスト"""
        config = TableConfig()
        assert config.enable_csv_download is True
        assert config.sortable is True
        assert config.searchable is True
        assert config.page_size == 10
        assert config.show_pagination is True
        assert config.header_background == "#f8f9fa"
        assert config.row_hover is True
        assert config.striped_rows is False
        assert config.columns is None
        assert config.column_widths is None
    
    def test_custom_values(self):
        """カスタム値のテスト"""
        config = TableConfig(
            enable_csv_download=False,
            sortable=False,
            searchable=False,
            page_size=20,
            show_pagination=False,
            header_background="blue",
            row_hover=False,
            striped_rows=True,
            columns=["col1", "col2"],
            column_widths={"col1": 100, "col2": 200}
        )
        assert config.enable_csv_download is False
        assert config.sortable is False
        assert config.searchable is False
        assert config.page_size == 20
        assert config.show_pagination is False
        assert config.header_background == "blue"
        assert config.row_hover is False
        assert config.striped_rows is True
        assert config.columns == ["col1", "col2"]
        assert config.column_widths == {"col1": 100, "col2": 200}
    
    def test_to_dict(self):
        """辞書形式への変換テスト"""
        config = TableConfig(enable_csv_download=False)
        result = config.to_dict()
        assert "enable_csv_download" in result
        assert result["enable_csv_download"] is False
        assert "sortable" in result
        assert "searchable" in result
        assert "page_size" in result
        assert "show_pagination" in result


class TestChartConfig:
    """ChartConfigのテスト"""
    
    def test_default_values(self):
        """デフォルト値のテスト"""
        config = ChartConfig()
        assert config.chart_type == ChartType.LINE
        assert config.x_column is None
        assert config.y_column is None
        assert config.show_legend is True
        assert config.show_grid is True
        assert config.color_scheme == "plotly"
        assert config.enable_zoom is True
        assert config.enable_pan is True
        assert config.enable_hover is True
    
    def test_custom_values(self):
        """カスタム値のテスト"""
        config = ChartConfig(
            chart_type=ChartType.BAR,
            x_column="x",
            y_column="y",
            show_legend=False,
            show_grid=False,
            color_scheme="custom",
            enable_zoom=False,
            enable_pan=False,
            enable_hover=False
        )
        assert config.chart_type == ChartType.BAR
        assert config.x_column == "x"
        assert config.y_column == "y"
        assert config.show_legend is False
        assert config.show_grid is False
        assert config.color_scheme == "custom"
        assert config.enable_zoom is False
        assert config.enable_pan is False
        assert config.enable_hover is False
    
    def test_to_dict(self):
        """辞書形式への変換テスト"""
        config = ChartConfig(chart_type=ChartType.BAR)
        result = config.to_dict()
        assert "chart_type" in result
        assert result["chart_type"] == "bar"
        assert "x_column" in result
        assert "y_column" in result
        assert "show_legend" in result
        assert "show_grid" in result
        assert "color_scheme" in result


class TestFilterConfig:
    """FilterConfigのテスト"""
    
    def test_default_values(self):
        """デフォルト値のテスト"""
        config = FilterConfig()
        assert config.filter_type == FilterType.DROPDOWN
        assert config.column is None
        assert config.options == []
        assert config.placeholder is None
        assert config.allow_multiple is False
        assert config.allow_clear is True
        assert config.searchable is False
    
    def test_custom_values(self):
        """カスタム値のテスト"""
        config = FilterConfig(
            filter_type=FilterType.MULTISELECT,
            column="category",
            options=["A", "B", "C"],
            placeholder="Select category",
            allow_multiple=True,
            allow_clear=False,
            searchable=True
        )
        assert config.filter_type == FilterType.MULTISELECT
        assert config.column == "category"
        assert config.options == ["A", "B", "C"]
        assert config.placeholder == "Select category"
        assert config.allow_multiple is True
        assert config.allow_clear is False
        assert config.searchable is True
    
    def test_to_dict(self):
        """辞書形式への変換テスト"""
        config = FilterConfig(filter_type=FilterType.MULTISELECT)
        result = config.to_dict()
        assert "filter_type" in result
        assert result["filter_type"] == "multiselect"
        assert "column" in result
        assert "options" in result
        assert "placeholder" in result
        assert "allow_multiple" in result
        assert "allow_clear" in result
        assert "searchable" in result


class TestConfigManager:
    """ConfigManagerのテスト"""
    
    def setup_method(self):
        """テスト前の準備"""
        self.manager = ConfigManager()
    
    def test_register_default_config(self):
        """デフォルト設定の登録"""
        config = ComponentConfig(component_id="test")
        self.manager.register_default_config("test_component", config)
        assert "test_component" in self.manager._default_configs
        assert self.manager._default_configs["test_component"] == config
    
    def test_get_config_with_default(self):
        """デフォルト設定付きの設定取得"""
        default_config = ComponentConfig(component_id="default")
        self.manager.register_default_config("test_component", default_config)
        
        result = self.manager.get_config("test_component")
        assert result.component_id == "default"
    
    def test_get_config_with_custom_id(self):
        """カスタムID付きの設定取得"""
        default_config = ComponentConfig(component_id="default")
        custom_config = ComponentConfig(component_id="custom")
        
        self.manager.register_default_config("test_component", default_config)
        self.manager.set_config("test_component", custom_config, "custom_id")
        
        result = self.manager.get_config("test_component", "custom_id")
        assert result.component_id == "custom"
    
    def test_get_config_nonexistent(self):
        """存在しない設定の取得"""
        result = self.manager.get_config("nonexistent")
        assert result is None
    
    def test_set_config(self):
        """設定の設定"""
        config = ComponentConfig(component_id="test")
        self.manager.set_config("test_component", config, "test_id")
        
        result = self.manager.get_config("test_component", "test_id")
        assert result.component_id == "test"
    
    def test_save_and_load_configs(self):
        """設定の保存と読み込み"""
        # テスト用の設定を作成
        config1 = ComponentConfig(component_id="test1")
        config2 = ComponentConfig(component_id="test2")
        
        self.manager.set_config("component1", config1, "id1")
        self.manager.set_config("component2", config2, "id2")
        
        # 一時ファイルに保存
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            filename = f.name
        
        try:
            self.manager.save_configs(filename)
            
            # 新しいマネージャーで読み込み
            new_manager = ConfigManager()
            new_manager.load_configs(filename)
            
            # 設定が正しく読み込まれたことを確認
            result1 = new_manager.get_config("component1", "id1")
            result2 = new_manager.get_config("component2", "id2")
            
            assert result1.component_id == "test1"
            assert result2.component_id == "test2"
        
        finally:
            # 一時ファイルを削除
            if os.path.exists(filename):
                os.unlink(filename)
    
    def test_get_config_class(self):
        """設定クラスの取得"""
        # 既知のコンポーネントタイプ
        assert self.manager._get_config_class("table") == TableConfig
        assert self.manager._get_config_class("chart") == ChartConfig
        assert self.manager._get_config_class("filter") == FilterConfig
        
        # 未知のコンポーネントタイプ
        assert self.manager._get_config_class("unknown") is None