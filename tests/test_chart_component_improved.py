"""
ChartComponentの改善されたテスト

未カバー部分を含む全機能をテストします。
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from db_ui_components.chart_component import ChartComponent


class TestChartComponentUncovered:
    """ChartComponentの未カバー部分のテスト"""
    
    def setup_method(self):
        """テスト前の準備"""
        self.df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [10, 20, 15, 25, 30],
            'category': ['A', 'B', 'A', 'B', 'A']
        })
    
    def test_unsupported_chart_type(self):
        """サポートされていないグラフタイプのテスト"""
        component = ChartComponent(
            data=self.df,
            chart_type="unsupported",
            x_column="x",
            y_column="y"
        )
        
        with pytest.raises(ValueError, match="Unsupported chart type: unsupported"):
            component.render()
    
    def test_set_style(self):
        """カスタムスタイルの設定テスト"""
        component = ChartComponent(
            data=self.df,
            chart_type="line",
            x_column="x",
            y_column="y"
        )
        
        custom_style = {
            "backgroundColor": "#f5f5f5",
            "borderRadius": "8px",
            "padding": "16px"
        }
        
        component.set_style(custom_style)
        assert hasattr(component, '_custom_style')
        assert component._custom_style == custom_style
    
    def test_render_with_custom_style(self):
        """カスタムスタイル付きのレンダリングテスト"""
        component = ChartComponent(
            data=self.df,
            chart_type="line",
            x_column="x",
            y_column="y"
        )
        
        custom_style = {
            "backgroundColor": "#f5f5f5",
            "borderRadius": "8px"
        }
        component.set_style(custom_style)
        
        result = component.render()
        assert isinstance(result, str)
        assert "plotly" in result.lower()
    
    def test_on_click_handler(self):
        """クリックイベントハンドラーのテスト"""
        component = ChartComponent(
            data=self.df,
            chart_type="line",
            x_column="x",
            y_column="y"
        )
        
        handler = MagicMock()
        component.on_click(handler)
        
        assert len(component._click_handlers) == 1
        assert component._click_handlers[0] == handler
    
    def test_multiple_click_handlers(self):
        """複数のクリックイベントハンドラーのテスト"""
        component = ChartComponent(
            data=self.df,
            chart_type="line",
            x_column="x",
            y_column="y"
        )
        
        handler1 = MagicMock()
        handler2 = MagicMock()
        
        component.on_click(handler1)
        component.on_click(handler2)
        
        assert len(component._click_handlers) == 2
        assert handler1 in component._click_handlers
        assert handler2 in component._click_handlers
    
    def test_update_data(self):
        """データ更新のテスト"""
        component = ChartComponent(
            data=self.df,
            chart_type="line",
            x_column="x",
            y_column="y"
        )
        
        new_df = pd.DataFrame({
            'x': [6, 7, 8],
            'y': [35, 40, 45],
            'category': ['C', 'C', 'C']
        })
        
        component.update_data(new_df)
        assert component.data.equals(new_df)
    
    def test_to_dict(self):
        """辞書形式への変換テスト"""
        component = ChartComponent(
            data=self.df,
            chart_type="bar",
            x_column="x",
            y_column="y",
            title="Test Chart",
            height=500,
            test_param="test_value"
        )
        
        result = component.to_dict()
        expected = {
            "type": "chart",
            "chart_type": "bar",
            "x_column": "x",
            "y_column": "y",
            "title": "Test Chart",
            "height": 500,
            "kwargs": {"test_param": "test_value"}
        }
        assert result == expected
    
    def test_heatmap_with_pivot_data(self):
        """ヒートマップのピボットデータテスト"""
        # ヒートマップ用のデータを作成
        heatmap_df = pd.DataFrame({
            'row': ['A', 'A', 'B', 'B', 'C', 'C'],
            'col': ['X', 'Y', 'X', 'Y', 'X', 'Y'],
            'value': [1, 2, 3, 4, 5, 6]
        })
        
        component = ChartComponent(
            data=heatmap_df,
            chart_type="heatmap",
            x_column="col",
            y_column="value"
        )
        
        result = component.render()
        assert isinstance(result, str)
        assert "plotly" in result.lower()
    
    def test_pie_chart_with_names_and_values(self):
        """円グラフの名前と値のテスト"""
        pie_df = pd.DataFrame({
            'category': ['A', 'B', 'C'],
            'value': [30, 40, 30]
        })
        
        component = ChartComponent(
            data=pie_df,
            chart_type="pie",
            x_column="category",
            y_column="value"
        )
        
        result = component.render()
        assert isinstance(result, str)
        assert "plotly" in result.lower()
    
    def test_scatter_chart(self):
        """散布図のテスト"""
        scatter_df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [2, 4, 1, 5, 3],
            'size': [10, 20, 15, 25, 30]
        })
        
        component = ChartComponent(
            data=scatter_df,
            chart_type="scatter",
            x_column="x",
            y_column="y"
        )
        
        result = component.render()
        assert isinstance(result, str)
        assert "plotly" in result.lower()
    
    def test_bar_chart_with_kwargs(self):
        """キーワード引数付きの棒グラフテスト"""
        component = ChartComponent(
            data=self.df,
            chart_type="bar",
            x_column="x",
            y_column="y",
            color="category",
            barmode="group"
        )
        
        result = component.render()
        assert isinstance(result, str)
        assert "plotly" in result.lower()
    
    def test_line_chart_with_kwargs(self):
        """キーワード引数付きの折れ線グラフテスト"""
        component = ChartComponent(
            data=self.df,
            chart_type="line",
            x_column="x",
            y_column="y",
            color="category",
            line_dash="dash"
        )
        
        result = component.render()
        assert isinstance(result, str)
        assert "plotly" in result.lower()
    
    def test_empty_dataframe(self):
        """空のデータフレームのテスト"""
        empty_df = pd.DataFrame()
        
        component = ChartComponent(
            data=empty_df,
            chart_type="line",
            x_column="x",
            y_column="y"
        )
        
        # 空のデータフレームでもエラーが発生しないことを確認
        result = component.render()
        assert isinstance(result, str)
    
    def test_none_columns(self):
        """Noneの列名のテスト"""
        component = ChartComponent(
            data=self.df,
            chart_type="line",
            x_column=None,
            y_column=None
        )
        
        result = component.render()
        assert isinstance(result, str)
        assert "plotly" in result.lower()
    
    def test_none_title(self):
        """Noneのタイトルのテスト"""
        component = ChartComponent(
            data=self.df,
            chart_type="line",
            x_column="x",
            y_column="y",
            title=None
        )
        
        result = component.render()
        assert isinstance(result, str)
        assert "plotly" in result.lower()
    
    def test_custom_height(self):
        """カスタム高さのテスト"""
        component = ChartComponent(
            data=self.df,
            chart_type="line",
            x_column="x",
            y_column="y",
            height=600
        )
        
        result = component.render()
        assert isinstance(result, str)
        assert "plotly" in result.lower()
    
    def test_complex_dataframe(self):
        """複雑なデータフレームのテスト"""
        complex_df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=10),
            'value': np.random.randn(10),
            'category': ['A'] * 5 + ['B'] * 5,
            'size': np.random.randint(10, 100, 10)
        })
        
        component = ChartComponent(
            data=complex_df,
            chart_type="scatter",
            x_column="date",
            y_column="value",
            size="size",
            color="category"
        )
        
        result = component.render()
        assert isinstance(result, str)
        assert "plotly" in result.lower()