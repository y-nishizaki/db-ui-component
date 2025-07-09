"""
可視化コンポーネントの基底クラスのテスト

このモジュールには、BaseVisualizationComponentのテストが含まれています。
"""

import pytest
import pandas as pd
from unittest.mock import Mock, patch
from db_ui_components.visualization.base_visualization import BaseVisualizationComponent
from db_ui_components.exceptions import ComponentError


class TestBaseVisualizationComponent:
    """BaseVisualizationComponentのテスト"""
    
    def setup_method(self):
        """テスト前のセットアップ"""
        self.component = BaseVisualizationComponent(
            title='テストチャート',
            height=600
        )
    
    def test_initialization(self):
        """初期化テスト"""
        assert self.component.title == 'テストチャート'
        assert self.component.height == 600
        assert hasattr(self.component, 'component_id')
    
    def test_prepare_chart_data_not_implemented(self):
        """_prepare_chart_dataの未実装テスト"""
        data = pd.DataFrame({'test': [1, 2, 3]})
        
        with pytest.raises(NotImplementedError):
            self.component._prepare_chart_data(data)
    
    def test_get_chart_type_not_implemented(self):
        """_get_chart_typeの未実装テスト"""
        with pytest.raises(NotImplementedError):
            self.component._get_chart_type()
    
    def test_add_axis_titles_both(self):
        """軸タイトル追加テスト（両方）"""
        layout = {}
        result = self.component._add_axis_titles(
            layout, 
            x_title='X軸', 
            y_title='Y軸'
        )
        
        assert 'xaxis' in result
        assert 'yaxis' in result
        assert result['xaxis']['title'] == 'X軸'
        assert result['yaxis']['title'] == 'Y軸'
    
    def test_add_axis_titles_x_only(self):
        """軸タイトル追加テスト（X軸のみ）"""
        layout = {}
        result = self.component._add_axis_titles(
            layout, 
            x_title='X軸'
        )
        
        assert 'xaxis' in result
        assert 'yaxis' not in result
        assert result['xaxis']['title'] == 'X軸'
    
    def test_add_axis_titles_y_only(self):
        """軸タイトル追加テスト（Y軸のみ）"""
        layout = {}
        result = self.component._add_axis_titles(
            layout, 
            y_title='Y軸'
        )
        
        assert 'xaxis' not in result
        assert 'yaxis' in result
        assert result['yaxis']['title'] == 'Y軸'
    
    def test_add_axis_titles_none(self):
        """軸タイトル追加テスト（なし）"""
        layout = {'test': 'value'}
        result = self.component._add_axis_titles(layout)
        
        assert result == layout
        assert 'xaxis' not in result
        assert 'yaxis' not in result
    
    def test_generate_html_template(self):
        """HTMLテンプレート生成テスト"""
        # モックで_get_chart_typeを実装
        self.component._get_chart_type = Mock(return_value='test-chart')
        
        chart_data = {'type': 'scatter', 'x': [1, 2, 3], 'y': [4, 5, 6]}
        html = self.component._generate_html_template(chart_data)
        
        assert isinstance(html, str)
        assert 'test-chart-' in html
        assert 'テストチャート' in html
        assert 'Plotly.newPlot' in html
        assert 'height: 600px' in html
        assert 'scatter' in html
    
    def test_render_with_error(self):
        """エラーハンドリングテスト"""
        # モックで_prepare_chart_dataでエラーを発生
        self.component._prepare_chart_data = Mock(side_effect=Exception("テストエラー"))
        
        data = pd.DataFrame({'test': [1, 2, 3]})
        
        with pytest.raises(ComponentError) as exc_info:
            self.component.render(data)
        
        assert "BaseVisualizationComponentのレンダリングに失敗しました" in str(exc_info.value)
        assert "テストエラー" in str(exc_info.value)


class ConcreteVisualizationComponent(BaseVisualizationComponent):
    """テスト用の具象クラス"""
    
    def _prepare_chart_data(self, data: pd.DataFrame):
        return {'type': 'scatter', 'x': data.iloc[:, 0].tolist(), 'y': data.iloc[:, 1].tolist()}
    
    def _get_chart_type(self) -> str:
        return 'concrete-chart'


class TestConcreteVisualizationComponent:
    """具象クラスのテスト"""
    
    def setup_method(self):
        """テスト前のセットアップ"""
        self.component = ConcreteVisualizationComponent(
            title='具象チャート',
            height=400
        )
    
    def test_concrete_initialization(self):
        """具象クラスの初期化テスト"""
        assert self.component.title == '具象チャート'
        assert self.component.height == 400
    
    def test_prepare_chart_data_implementation(self):
        """_prepare_chart_dataの実装テスト"""
        data = pd.DataFrame({
            'x': [1, 2, 3],
            'y': [4, 5, 6]
        })
        
        result = self.component._prepare_chart_data(data)
        
        assert 'type' in result
        assert result['type'] == 'scatter'
        assert 'x' in result
        assert 'y' in result
        assert result['x'] == [1, 2, 3]
        assert result['y'] == [4, 5, 6]
    
    def test_get_chart_type_implementation(self):
        """_get_chart_typeの実装テスト"""
        result = self.component._get_chart_type()
        assert result == 'concrete-chart'
    
    def test_render_success(self):
        """正常なレンダリングテスト"""
        data = pd.DataFrame({
            'x': [1, 2, 3],
            'y': [4, 5, 6]
        })
        
        html = self.component.render(data)
        
        assert isinstance(html, str)
        assert 'concrete-chart-' in html
        assert '具象チャート' in html
        assert 'Plotly.newPlot' in html
        assert 'height: 400px' in html
        assert 'scatter' in html
    
    def test_generate_html_template_with_axis_titles(self):
        """軸タイトル付きHTMLテンプレート生成テスト"""
        chart_data = {'type': 'scatter', 'x': [1, 2, 3], 'y': [4, 5, 6]}
        
        # 軸タイトルを追加
        layout = {'title': '具象チャート', 'height': 400}
        layout_with_axes = self.component._add_axis_titles(
            layout, 
            x_title='X軸タイトル', 
            y_title='Y軸タイトル'
        )
        
        # モックで_get_chart_typeを実装
        self.component._get_chart_type = Mock(return_value='concrete-chart')
        
        html = self.component._generate_html_template(chart_data)
        
        assert isinstance(html, str)
        assert 'concrete-chart-' in html
        assert '具象チャート' in html


class TestBaseVisualizationComponentEdgeCases:
    """BaseVisualizationComponentのエッジケーステスト"""
    
    def test_empty_data(self):
        """空データのテスト"""
        component = ConcreteVisualizationComponent()
        empty_data = pd.DataFrame()
        
        html = component.render(empty_data)
        assert isinstance(html, str)
        assert 'concrete-chart-' in html
    
    def test_single_row_data(self):
        """単一行データのテスト"""
        component = ConcreteVisualizationComponent()
        single_data = pd.DataFrame({'x': [1], 'y': [2]})
        
        html = component.render(single_data)
        assert isinstance(html, str)
        assert 'concrete-chart-' in html
    
    def test_large_data(self):
        """大規模データのテスト"""
        component = ConcreteVisualizationComponent()
        large_data = pd.DataFrame({
            'x': list(range(1000)),
            'y': list(range(1000))
        })
        
        html = component.render(large_data)
        assert isinstance(html, str)
        assert 'concrete-chart-' in html
        assert len(html) > 0
    
    def test_special_characters_in_title(self):
        """タイトルに特殊文字を含むテスト"""
        component = ConcreteVisualizationComponent(
            title='特殊文字テスト: "クォート" & <タグ>'
        )
        
        data = pd.DataFrame({'x': [1, 2], 'y': [3, 4]})
        html = component.render(data)
        
        assert isinstance(html, str)
        assert '特殊文字テスト' in html
    
    def test_zero_height(self):
        """高さ0のテスト"""
        component = ConcreteVisualizationComponent(height=0)
        
        data = pd.DataFrame({'x': [1, 2], 'y': [3, 4]})
        html = component.render(data)
        
        assert isinstance(html, str)
        assert 'height: 0px' in html
    
    def test_very_large_height(self):
        """非常に大きな高さのテスト"""
        component = ConcreteVisualizationComponent(height=9999)
        
        data = pd.DataFrame({'x': [1, 2], 'y': [3, 4]})
        html = component.render(data)
        
        assert isinstance(html, str)
        assert 'height: 9999px' in html


class TestBaseVisualizationComponentIntegration:
    """BaseVisualizationComponentの統合テスト"""
    
    def test_multiple_components(self):
        """複数コンポーネントのテスト"""
        component1 = ConcreteVisualizationComponent(title='チャート1')
        component2 = ConcreteVisualizationComponent(title='チャート2')
        
        data = pd.DataFrame({'x': [1, 2], 'y': [3, 4]})
        
        html1 = component1.render(data)
        html2 = component2.render(data)
        
        assert isinstance(html1, str)
        assert isinstance(html2, str)
        assert component1.component_id != component2.component_id
        assert 'チャート1' in html1
        assert 'チャート2' in html2
    
    def test_json_serialization(self):
        """JSONシリアライゼーションテスト"""
        component = ConcreteVisualizationComponent()
        data = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        
        chart_data = component._prepare_chart_data(data)
        
        # JSONシリアライゼーションが正常に動作することを確認
        import json
        json_str = json.dumps(chart_data)
        assert isinstance(json_str, str)
        assert len(json_str) > 0
        assert 'scatter' in json_str
    
    def test_component_id_uniqueness(self):
        """コンポーネントIDの一意性テスト"""
        components = []
        for i in range(10):
            component = ConcreteVisualizationComponent()
            components.append(component)
        
        # すべてのコンポーネントIDが一意であることを確認
        component_ids = [comp.component_id for comp in components]
        assert len(component_ids) == len(set(component_ids))
    
    def test_inheritance_chain(self):
        """継承チェーンのテスト"""
        component = ConcreteVisualizationComponent()
        
        # BaseComponentの機能が利用できることを確認
        assert hasattr(component, 'component_id')
        assert hasattr(component, 'add_event_handler')
        assert hasattr(component, 'remove_event_handler')
        
        # BaseVisualizationComponentの機能が利用できることを確認
        assert hasattr(component, 'title')
        assert hasattr(component, 'height')
        assert hasattr(component, '_add_axis_titles')
        
        # ConcreteVisualizationComponentの機能が利用できることを確認
        assert hasattr(component, '_prepare_chart_data')
        assert hasattr(component, '_get_chart_type')