"""
コンポーネントのテスト

Databricks UI Component Libraryの各コンポーネントのテストコードです。
"""

import pytest
import pandas as pd
import numpy as np
from db_ui_components import ChartComponent, TableComponent, FilterComponent, Dashboard


class TestChartComponent:
    """ChartComponentのテスト"""
    
    def setup_method(self):
        """テスト前の準備"""
        self.sample_data = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=10, freq='D'),
            'value': np.random.randn(10).cumsum() + 100,
            'category': ['A', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C']
        })
    
    def test_chart_component_initialization(self):
        """ChartComponentの初期化テスト"""
        chart = ChartComponent(
            data=self.sample_data,
            chart_type='line',
            x_column='date',
            y_column='value',
            title='テストグラフ'
        )
        
        assert chart.data.equals(self.sample_data)
        assert chart.chart_type == 'line'
        assert chart.x_column == 'date'
        assert chart.y_column == 'value'
        assert chart.title == 'テストグラフ'
    
    def test_chart_component_render(self):
        """ChartComponentのレンダリングテスト"""
        chart = ChartComponent(
            data=self.sample_data,
            chart_type='line',
            x_column='date',
            y_column='value'
        )
        
        html = chart.render()
        assert isinstance(html, str)
        assert len(html) > 0
        assert 'plotly' in html.lower()
    
    def test_unsupported_chart_type(self):
        """サポートされていないグラフタイプのテスト"""
        with pytest.raises(ValueError):
            ChartComponent(
                data=self.sample_data,
                chart_type='unsupported',
                x_column='date',
                y_column='value'
            )
    
    def test_chart_component_style(self):
        """ChartComponentのスタイル設定テスト"""
        chart = ChartComponent(
            data=self.sample_data,
            chart_type='bar',
            x_column='category',
            y_column='value'
        )
        
        style = {'backgroundColor': '#f0f0f0', 'borderRadius': '8px'}
        chart.set_style(style)
        
        assert hasattr(chart, '_custom_style')
        assert chart._custom_style == style


class TestTableComponent:
    """TableComponentのテスト"""
    
    def setup_method(self):
        """テスト前の準備"""
        self.sample_data = pd.DataFrame({
            'id': range(1, 11),
            'name': [f'Item {i}' for i in range(1, 11)],
            'value': np.random.randn(10),
            'category': ['A', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C']
        })
    
    def test_table_component_initialization(self):
        """TableComponentの初期化テスト"""
        table = TableComponent(
            data=self.sample_data,
            enable_csv_download=True,
            sortable=True,
            searchable=True,
            page_size=5
        )
        
        assert table.data.equals(self.sample_data)
        assert table.enable_csv_download is True
        assert table.sortable is True
        assert table.searchable is True
        assert table.page_size == 5
    
    def test_table_component_render(self):
        """TableComponentのレンダリングテスト"""
        table = TableComponent(
            data=self.sample_data,
            enable_csv_download=True,
            sortable=True,
            searchable=True
        )
        
        html = table.render()
        assert isinstance(html, str)
        assert len(html) > 0
        assert 'table' in html.lower()
    
    def test_table_component_columns(self):
        """TableComponentの列設定テスト"""
        table = TableComponent(
            data=self.sample_data,
            columns=['id', 'name']
        )
        
        assert table.columns == ['id', 'name']
        assert len(table._display_data.columns) == 2


class TestFilterComponent:
    """FilterComponentのテスト"""
    
    def test_filter_component_initialization(self):
        """FilterComponentの初期化テスト"""
        filter_comp = FilterComponent(
            filter_type='dropdown',
            column='category',
            options=['A', 'B', 'C'],
            title='カテゴリ選択'
        )
        
        assert filter_comp.filter_type == 'dropdown'
        assert filter_comp.column == 'category'
        assert filter_comp.options == ['A', 'B', 'C']
        assert filter_comp.title == 'カテゴリ選択'
    
    def test_filter_component_render(self):
        """FilterComponentのレンダリングテスト"""
        filter_comp = FilterComponent(
            filter_type='text',
            column='name',
            placeholder='名前で検索...'
        )
        
        html = filter_comp.render()
        assert isinstance(html, str)
        assert len(html) > 0
        assert 'input' in html.lower()
    
    def test_unsupported_filter_type(self):
        """サポートされていないフィルタータイプのテスト"""
        with pytest.raises(ValueError):
            FilterComponent(
                filter_type='unsupported',
                column='category'
            )


class TestDashboard:
    """Dashboardのテスト"""
    
    def setup_method(self):
        """テスト前の準備"""
        self.sample_data = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=5, freq='D'),
            'value': [1, 2, 3, 4, 5]
        })
    
    def test_dashboard_initialization(self):
        """Dashboardの初期化テスト"""
        dashboard = Dashboard(title='テストダッシュボード')
        
        assert dashboard.title == 'テストダッシュボード'
        assert dashboard.layout == 'grid'
        assert len(dashboard.components) == 0
    
    def test_dashboard_add_component(self):
        """Dashboardへのコンポーネント追加テスト"""
        dashboard = Dashboard()
        chart = ChartComponent(
            data=self.sample_data,
            chart_type='line',
            x_column='date',
            y_column='value'
        )
        
        dashboard.add_component(chart, position=(0, 0), size=(1, 1))
        
        assert len(dashboard.components) == 1
        assert dashboard.components[0]['position'] == (0, 0)
        assert dashboard.components[0]['size'] == (1, 1)
    
    def test_dashboard_render(self):
        """Dashboardのレンダリングテスト"""
        dashboard = Dashboard(title='テストダッシュボード')
        chart = ChartComponent(
            data=self.sample_data,
            chart_type='line',
            x_column='date',
            y_column='value'
        )
        
        dashboard.add_component(chart, position=(0, 0))
        
        html = dashboard.render()
        assert isinstance(html, str)
        assert len(html) > 0
        assert 'テストダッシュボード' in html


def test_integration():
    """統合テスト"""
    # サンプルデータ
    data = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=10, freq='D'),
        'value': np.random.randn(10).cumsum() + 100,
        'category': ['A', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C']
    })
    
    # コンポーネントを作成
    chart = ChartComponent(
        data=data,
        chart_type='line',
        x_column='date',
        y_column='value',
        title='統合テストグラフ'
    )
    
    table = TableComponent(
        data=data,
        enable_csv_download=True,
        sortable=True,
        searchable=True
    )
    
    filter_comp = FilterComponent(
        filter_type='dropdown',
        column='category',
        options=['A', 'B', 'C'],
        title='カテゴリ選択'
    )
    
    # ダッシュボードを作成
    dashboard = Dashboard(title='統合テストダッシュボード')
    dashboard.add_component(filter_comp, position=(0, 0), size=(3, 1))
    dashboard.add_component(chart, position=(1, 0), size=(6, 1))
    dashboard.add_component(table, position=(2, 0), size=(6, 1))
    
    # レンダリング
    html = dashboard.render()
    
    # 基本的な検証
    assert isinstance(html, str)
    assert len(html) > 0
    assert '統合テストダッシュボード' in html
    assert 'plotly' in html.lower()
    assert 'table' in html.lower()
    assert 'select' in html.lower()


if __name__ == "__main__":
    pytest.main([__file__]) 