"""
FilterComponentの改善されたテスト

未カバー部分を含む全機能をテストします。
"""

import pytest
from unittest.mock import MagicMock
from db_ui_components.filter_component import FilterComponent
from unittest.mock import patch


class TestFilterComponentUncovered:
    """FilterComponentの未カバー部分のテスト"""
    
    def test_unsupported_filter_type(self):
        """サポートされていないフィルタータイプのテスト"""
        component = FilterComponent(
            filter_type="unsupported",
            column="test_column"
        )
        
        with pytest.raises(ValueError, match="Unsupported filter type: unsupported"):
            component.render()
    
    def test_on_change_handler(self):
        """フィルター変更イベントハンドラーのテスト"""
        component = FilterComponent(
            filter_type="dropdown",
            column="test_column",
            options=["A", "B", "C"]
        )
        
        handler = MagicMock()
        component.on_change(handler)
        
        assert len(component._change_handlers) == 1
        assert component._change_handlers[0] == handler
    
    def test_multiple_change_handlers(self):
        """複数のフィルター変更イベントハンドラーのテスト"""
        component = FilterComponent(
            filter_type="dropdown",
            column="test_column",
            options=["A", "B", "C"]
        )
        
        handler1 = MagicMock()
        handler2 = MagicMock()
        
        component.on_change(handler1)
        component.on_change(handler2)
        
        assert len(component._change_handlers) == 2
        assert handler1 in component._change_handlers
        assert handler2 in component._change_handlers
    
    def test_get_current_value(self):
        """現在の値の取得テスト"""
        component = FilterComponent(
            filter_type="dropdown",
            column="test_column",
            options=["A", "B", "C"]
        )
        
        # モックのwindow.currentFiltersを設定
        with patch('builtins.globals') as mock_globals:
            mock_globals.return_value = {
                'currentFilters': {
                    'test_column': {
                        'type': 'dropdown',
                        'value': 'A'
                    }
                }
            }
            
            result = component.get_current_value()
            expected = {
                'type': 'dropdown',
                'value': 'A'
            }
            assert result == expected
    
    def test_get_current_value_nonexistent(self):
        """存在しない現在の値の取得テスト"""
        component = FilterComponent(
            filter_type="dropdown",
            column="test_column",
            options=["A", "B", "C"]
        )
        
        # モックのwindow.currentFiltersを設定（存在しない場合）
        with patch('builtins.globals') as mock_globals:
            mock_globals.return_value = {'currentFilters': {}}
            
            result = component.get_current_value()
            assert result is None
    
    def test_to_dict(self):
        """辞書形式への変換テスト"""
        component = FilterComponent(
            filter_type="multiselect",
            column="test_column",
            options=["A", "B", "C"],
            placeholder="Select options",
            title="Test Filter",
            custom_param="custom_value"
        )
        
        result = component.to_dict()
        expected = {
            "type": "filter",
            "filter_type": "multiselect",
            "column": "test_column",
            "options": ["A", "B", "C"],
            "placeholder": "Select options",
            "title": "Test Filter",
            "kwargs": {"custom_param": "custom_value"}
        }
        assert result == expected
    
    def test_date_filter_with_title(self):
        """タイトル付きの日付フィルターテスト"""
        component = FilterComponent(
            filter_type="date",
            column="date_column",
            title="Date Range"
        )
        
        result = component.render()
        assert isinstance(result, str)
        assert "Date Range" in result
        assert "date-filter-date_column" in result
        assert "applyDateFilter" in result
    
    def test_date_filter_without_title(self):
        """タイトルなしの日付フィルターテスト"""
        component = FilterComponent(
            filter_type="date",
            column="date_column"
        )
        
        result = component.render()
        assert isinstance(result, str)
        assert "date_column" in result
        assert "applyDateFilter" in result
    
    def test_dropdown_filter_with_options(self):
        """オプション付きのドロップダウンフィルターテスト"""
        component = FilterComponent(
            filter_type="dropdown",
            column="category",
            options=["Category A", "Category B", "Category C"]
        )
        
        result = component.render()
        assert isinstance(result, str)
        assert "dropdown-filter-category" in result
        assert "Category A" in result
        assert "Category B" in result
        assert "Category C" in result
        assert "applyDropdownFilter" in result
    
    def test_dropdown_filter_without_options(self):
        """オプションなしのドロップダウンフィルターテスト"""
        component = FilterComponent(
            filter_type="dropdown",
            column="category"
        )
        
        result = component.render()
        assert isinstance(result, str)
        assert "dropdown-filter-category" in result
        assert "すべて" in result
        assert "applyDropdownFilter" in result
    
    def test_multiselect_filter(self):
        """マルチセレクトフィルターテスト"""
        component = FilterComponent(
            filter_type="multiselect",
            column="tags",
            options=["Tag1", "Tag2", "Tag3"]
        )
        
        result = component.render()
        assert isinstance(result, str)
        assert "multiselect-filter-tags" in result
        assert "Tag1" in result
        assert "Tag2" in result
        assert "Tag3" in result
        assert "applyMultiselectFilter" in result
        assert "checkbox" in result
    
    def test_text_filter_with_placeholder(self):
        """プレースホルダー付きのテキストフィルターテスト"""
        component = FilterComponent(
            filter_type="text",
            column="search",
            placeholder="Enter search term..."
        )
        
        result = component.render()
        assert isinstance(result, str)
        assert "text-filter-search" in result
        assert "Enter search term..." in result
        assert "applyTextFilter" in result
    
    def test_text_filter_without_placeholder(self):
        """プレースホルダーなしのテキストフィルターテスト"""
        component = FilterComponent(
            filter_type="text",
            column="search"
        )
        
        result = component.render()
        assert isinstance(result, str)
        assert "text-filter-search" in result
        assert "searchで検索..." in result
        assert "applyTextFilter" in result
    
    def test_filter_with_column_spaces(self):
        """スペースを含む列名のフィルターテスト"""
        component = FilterComponent(
            filter_type="dropdown",
            column="user name",
            options=["User A", "User B"]
        )
        
        result = component.render()
        assert isinstance(result, str)
        assert "dropdown-filter-user-name" in result  # スペースがハイフンに変換される
    
    def test_filter_with_special_characters(self):
        """特殊文字を含む列名のフィルターテスト"""
        component = FilterComponent(
            filter_type="text",
            column="user@email.com",
            placeholder="Enter email..."
        )
        
        result = component.render()
        assert isinstance(result, str)
        assert "text-filter-user@email.com" in result
        assert "Enter email..." in result
    
    def test_empty_options_list(self):
        """空のオプションリストのテスト"""
        component = FilterComponent(
            filter_type="dropdown",
            column="test_column",
            options=[]
        )
        
        result = component.render()
        assert isinstance(result, str)
        assert "dropdown-filter-test_column" in result
        assert "すべて" in result  # デフォルトオプション
    
    def test_none_options(self):
        """Noneのオプションのテスト"""
        component = FilterComponent(
            filter_type="dropdown",
            column="test_column",
            options=None
        )
        
        result = component.render()
        assert isinstance(result, str)
        assert "dropdown-filter-test_column" in result
        assert "すべて" in result  # デフォルトオプション
    
    def test_none_title(self):
        """Noneのタイトルのテスト"""
        component = FilterComponent(
            filter_type="dropdown",
            column="test_column",
            title=None
        )
        
        result = component.render()
        assert isinstance(result, str)
        assert "dropdown-filter-test_column" in result
        # タイトルがNoneの場合はラベルが表示されない
    
    def test_none_placeholder(self):
        """Noneのプレースホルダーのテスト"""
        component = FilterComponent(
            filter_type="text",
            column="test_column",
            placeholder=None
        )
        
        result = component.render()
        assert isinstance(result, str)
        assert "text-filter-test_column" in result
        assert "test_columnで検索..." in result  # デフォルトプレースホルダー
    
    def test_custom_kwargs(self):
        """カスタムキーワード引数のテスト"""
        component = FilterComponent(
            filter_type="dropdown",
            column="test_column",
            custom_param="custom_value",
            another_param=123
        )
        
        result = component.to_dict()
        assert result["kwargs"]["custom_param"] == "custom_value"
        assert result["kwargs"]["another_param"] == 123
    
    def test_all_filter_types(self):
        """すべてのフィルタータイプのテスト"""
        filter_types = ["date", "dropdown", "multiselect", "text"]
        
        for filter_type in filter_types:
            component = FilterComponent(
                filter_type=filter_type,
                column="test_column",
                options=["A", "B", "C"] if filter_type in ["dropdown", "multiselect"] else None
            )
            
            result = component.render()
            assert isinstance(result, str)
            assert f"{filter_type}-filter-test_column" in result
    
    def test_filter_with_complex_options(self):
        """複雑なオプションのフィルターテスト"""
        complex_options = [
            {"label": "Option 1", "value": "opt1"},
            {"label": "Option 2", "value": "opt2"},
            {"label": "Option 3", "value": "opt3"}
        ]
        
        component = FilterComponent(
            filter_type="dropdown",
            column="test_column",
            options=complex_options
        )
        
        result = component.render()
        assert isinstance(result, str)
        assert "dropdown-filter-test_column" in result
        # 辞書オブジェクトも文字列として表示される
        for option in complex_options:
            assert str(option) in result