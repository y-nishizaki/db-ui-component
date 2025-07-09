"""
データ変換モジュールの最終テスト

このモジュールには、data_transformer.pyの未カバー部分のテストが含まれています。
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
from db_ui_components.visualization.data_transformer import (
    DataTransformer,
    SankeyDataTransformer,
    HeatmapDataTransformer,
    NetworkDataTransformer
)


class TestDataTransformerFinalUncovered:
    """DataTransformerの最終未カバー部分のテスト"""
    
    def setup_method(self):
        """テスト前のセットアップ"""
        self.transformer = SankeyDataTransformer(
            source_column="source",
            target_column="target",
            value_column="value"
        )
    
    def test_validate_data_with_empty_dataframe(self):
        """空のデータフレームでの検証テスト"""
        empty_data = pd.DataFrame()
        required_columns = ["col1", "col2"]
        
        result = self.transformer.validate_data(empty_data, required_columns)
        assert result is False
    
    def test_validate_data_with_missing_columns(self):
        """不足列での検証テスト"""
        data = pd.DataFrame({"col1": [1, 2, 3]})
        required_columns = ["col1", "col2"]
        
        result = self.transformer.validate_data(data, required_columns)
        assert result is False
    
    def test_validate_data_with_valid_data(self):
        """有効なデータでの検証テスト"""
        data = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
        required_columns = ["col1", "col2"]
        
        result = self.transformer.validate_data(data, required_columns)
        assert result is True
    
    def test_validate_data_with_partial_columns(self):
        """部分的な列での検証テスト"""
        data = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6], "col3": [7, 8, 9]})
        required_columns = ["col1", "col2"]
        
        result = self.transformer.validate_data(data, required_columns)
        assert result is True
    
    def test_validate_data_with_empty_required_columns(self):
        """空の必須列リストでの検証テスト"""
        data = pd.DataFrame({"col1": [1, 2, 3]})
        required_columns = []
        
        result = self.transformer.validate_data(data, required_columns)
        assert result is True
    
    def test_validate_data_with_none_values(self):
        """None値での検証テスト"""
        data = pd.DataFrame({
            "col1": [1, None, 3],
            "col2": [4, 5, None]
        })
        required_columns = ["col1", "col2"]
        
        result = self.transformer.validate_data(data, required_columns)
        assert result is True
    
    def test_validate_data_with_duplicate_columns(self):
        """重複列での検証テスト"""
        data = pd.DataFrame({
            "col1": [1, 2, 3],
            "col2": [4, 5, 6]
        })
        required_columns = ["col1", "col1"]  # 重複
        
        result = self.transformer.validate_data(data, required_columns)
        assert result is True
    
    def test_validate_data_with_special_characters_in_columns(self):
        """特殊文字を含む列名での検証テスト"""
        data = pd.DataFrame({
            "col-1": [1, 2, 3],
            "col_2": [4, 5, 6],
            "col 3": [7, 8, 9]
        })
        required_columns = ["col-1", "col_2", "col 3"]
        
        result = self.transformer.validate_data(data, required_columns)
        assert result is True
    
    def test_validate_data_with_numeric_column_names(self):
        """数値列名での検証テスト"""
        data = pd.DataFrame({
            1: [1, 2, 3],
            2: [4, 5, 6]
        })
        required_columns = [1, 2]
        
        result = self.transformer.validate_data(data, required_columns)
        assert result is True
    
    def test_validate_data_with_mixed_data_types(self):
        """混合データ型での検証テスト"""
        data = pd.DataFrame({
            "string_col": ["a", "b", "c"],
            "int_col": [1, 2, 3],
            "float_col": [1.1, 2.2, 3.3],
            "bool_col": [True, False, True]
        })
        required_columns = ["string_col", "int_col", "float_col", "bool_col"]
        
        result = self.transformer.validate_data(data, required_columns)
        assert result is True
    
    def test_validate_data_with_single_row(self):
        """単一行での検証テスト"""
        data = pd.DataFrame({
            "col1": [1],
            "col2": [2]
        })
        required_columns = ["col1", "col2"]
        
        result = self.transformer.validate_data(data, required_columns)
        assert result is True
    
    def test_validate_data_with_large_dataframe(self):
        """大規模データフレームでの検証テスト"""
        # 大規模データフレームを作成
        large_data = pd.DataFrame({
            "col1": range(10000),
            "col2": range(10000, 20000),
            "col3": range(20000, 30000)
        })
        required_columns = ["col1", "col2", "col3"]
        
        result = self.transformer.validate_data(large_data, required_columns)
        assert result is True
    
    def test_validate_data_with_multiindex_columns(self):
        """マルチインデックス列での検証テスト"""
        # マルチインデックス列を持つデータフレームを作成
        arrays = [['A', 'A', 'B', 'B'], ['col1', 'col2', 'col1', 'col2']]
        multi_index = pd.MultiIndex.from_arrays(arrays, names=['level1', 'level2'])
        
        data = pd.DataFrame({
            ('A', 'col1'): [1, 2, 3],
            ('A', 'col2'): [4, 5, 6],
            ('B', 'col1'): [7, 8, 9],
            ('B', 'col2'): [10, 11, 12]
        })
        
        required_columns = [('A', 'col1'), ('B', 'col2')]
        
        result = self.transformer.validate_data(data, required_columns)
        assert result is True
    
    def test_validate_data_with_datetime_columns(self):
        """日時列での検証テスト"""
        data = pd.DataFrame({
            "date": pd.date_range('2024-01-01', periods=5),
            "value": [1, 2, 3, 4, 5]
        })
        required_columns = ["date", "value"]
        
        result = self.transformer.validate_data(data, required_columns)
        assert result is True
    
    def test_validate_data_with_categorical_columns(self):
        """カテゴリカル列での検証テスト"""
        data = pd.DataFrame({
            "category": pd.Categorical(['A', 'B', 'A', 'C']),
            "value": [1, 2, 3, 4]
        })
        required_columns = ["category", "value"]
        
        result = self.transformer.validate_data(data, required_columns)
        assert result is True
    
    def test_validate_data_with_nan_values(self):
        """NaN値での検証テスト"""
        data = pd.DataFrame({
            "col1": [1, np.nan, 3],
            "col2": [4, 5, np.nan]
        })
        required_columns = ["col1", "col2"]
        
        result = self.transformer.validate_data(data, required_columns)
        assert result is True
    
    def test_validate_data_with_inf_values(self):
        """無限値での検証テスト"""
        data = pd.DataFrame({
            "col1": [1, np.inf, 3],
            "col2": [4, 5, -np.inf]
        })
        required_columns = ["col1", "col2"]
        
        result = self.transformer.validate_data(data, required_columns)
        assert result is True
    
    def test_validate_data_with_complex_objects(self):
        """複雑なオブジェクトでの検証テスト"""
        data = pd.DataFrame({
            "list_col": [[1, 2], [3, 4], [5, 6]],
            "dict_col": [{"a": 1}, {"b": 2}, {"c": 3}],
            "tuple_col": [(1, 2), (3, 4), (5, 6)]
        })
        required_columns = ["list_col", "dict_col", "tuple_col"]
        
        result = self.transformer.validate_data(data, required_columns)
        assert result is True
    
    def test_validate_data_performance(self):
        """検証パフォーマンスのテスト"""
        # 大きなデータフレームでパフォーマンスをテスト
        large_data = pd.DataFrame({
            "col1": range(100000),
            "col2": range(100000, 200000),
            "col3": range(200000, 300000)
        })
        required_columns = ["col1", "col2", "col3"]
        
        # 時間を計測
        import time
        start_time = time.time()
        result = self.transformer.validate_data(large_data, required_columns)
        end_time = time.time()
        
        assert result is True
        assert end_time - start_time < 1.0  # 1秒以内に完了することを確認
    
    def test_validate_data_edge_cases(self):
        """検証のエッジケーステスト"""
        # 空の列名リスト
        data = pd.DataFrame({"col1": [1, 2, 3]})
        result = self.transformer.validate_data(data, [])
        assert result is True
        
        # 存在しない列名
        data = pd.DataFrame({"col1": [1, 2, 3]})
        result = self.transformer.validate_data(data, ["nonexistent"])
        assert result is False
        
        # 部分的な列の存在
        data = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
        result = self.transformer.validate_data(data, ["col1", "col2", "col3"])
        assert result is False
    
    def test_validate_data_integration(self):
        """検証の統合テスト"""
        # 様々なデータ型を組み合わせたテスト
        data = pd.DataFrame({
            "string_col": ["a", "b", "c"],
            "int_col": [1, 2, 3],
            "float_col": [1.1, 2.2, 3.3],
            "bool_col": [True, False, True],
            "date_col": pd.date_range('2024-01-01', periods=3),
            "category_col": pd.Categorical(['A', 'B', 'A']),
            "list_col": [[1], [2], [3]],
            "dict_col": [{"a": 1}, {"b": 2}, {"c": 3}]
        })
        
        # すべての列が存在する場合
        all_columns = ["string_col", "int_col", "float_col", "bool_col", 
                      "date_col", "category_col", "list_col", "dict_col"]
        result = self.transformer.validate_data(data, all_columns)
        assert result is True
        
        # 一部の列のみ
        partial_columns = ["string_col", "int_col"]
        result = self.transformer.validate_data(data, partial_columns)
        assert result is True
        
        # 存在しない列を含む場合
        invalid_columns = ["string_col", "nonexistent_col"]
        result = self.transformer.validate_data(data, invalid_columns)
        assert result is False