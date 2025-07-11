"""
TableComponentの改善されたテスト

未カバー部分を含む全機能をテストします。
"""

import pytest
import pandas as pd
import base64
from unittest.mock import MagicMock, patch
from db_ui_components.table_component import TableComponent


class TestTableComponentUncovered:
    """TableComponentの未カバー部分のテスト"""

    def setup_method(self):
        """テスト前の準備"""
        self.df = pd.DataFrame(
            {
                "Name": ["Alice", "Bob", "Charlie", "David", "Eve"],
                "Age": [25, 30, 35, 28, 32],
                "City": ["Tokyo", "Osaka", "Kyoto", "Nagoya", "Fukuoka"],
                "Salary": [50000, 60000, 70000, 55000, 65000],
            }
        )

    def test_update_data(self):
        """データ更新のテスト"""
        component = TableComponent(data=self.df, columns=["Name", "Age", "City"])

        new_df = pd.DataFrame(
            {"Name": ["Frank", "Grace"], "Age": [40, 45], "City": ["Sapporo", "Sendai"]}
        )

        component.update_data(new_df)
        assert component.data_manager.data.equals(new_df)
        assert component.data_manager.get_display_data().equals(new_df)

    def test_set_columns(self):
        """列設定のテスト"""
        component = TableComponent(data=self.df, columns=["Name", "Age"])

        new_columns = ["Name", "City", "Salary"]
        component.set_columns(new_columns)
        assert component.data_manager.columns == new_columns

    def test_to_dict(self):
        """辞書形式への変換テスト"""
        component = TableComponent(
            data=self.df,
            enable_csv_download=False,
            sortable=False,
            searchable=False,
            page_size=20,
            columns=["Name", "Age"],
            title="Test Table",
            height=500,
            custom_param="custom_value",
        )

        result = component.to_dict()
        expected = {
            "type": "table",
            "enable_csv_download": False,
            "sortable": False,
            "searchable": False,
            "page_size": 20,
            "columns": ["Name", "Age"],
            "title": "Test Table",
            "height": 500,
            "kwargs": {"custom_param": "custom_value"},
        }
        assert result == expected

    def test_render_without_title(self):
        """タイトルなしのレンダリングテスト"""
        component = TableComponent(data=self.df, columns=["Name", "Age"])

        result = component.render()
        assert isinstance(result, str)
        assert "data-table" in result
        assert "<h3>" not in result  # タイトルが表示されない

    def test_render_with_title(self):
        """タイトル付きのレンダリングテスト"""
        component = TableComponent(
            data=self.df, columns=["Name", "Age"], title="Employee Table"
        )

        result = component.render()
        assert isinstance(result, str)
        assert "Employee Table" in result
        assert "<h3>" in result

    def test_render_without_search(self):
        """検索機能なしのレンダリングテスト"""
        component = TableComponent(
            data=self.df, columns=["Name", "Age"], searchable=False
        )

        result = component.render()
        assert isinstance(result, str)
        assert "table-search" not in result

    def test_render_with_search(self):
        """検索機能付きのレンダリングテスト"""
        component = TableComponent(
            data=self.df, columns=["Name", "Age"], searchable=True
        )

        result = component.render()
        assert isinstance(result, str)
        assert "table-search" in result
        assert "検索..." in result

    def test_render_without_csv_download(self):
        """CSVダウンロードなしのレンダリングテスト"""
        component = TableComponent(
            data=self.df, columns=["Name", "Age"], enable_csv_download=False
        )

        result = component.render()
        assert isinstance(result, str)
        assert "CSVダウンロード" not in result

    def test_render_with_csv_download(self):
        """CSVダウンロード付きのレンダリングテスト"""
        component = TableComponent(
            data=self.df, columns=["Name", "Age"], enable_csv_download=True
        )

        result = component.render()
        assert isinstance(result, str)
        assert "CSVダウンロード" in result
        assert "📥" in result

    def test_render_without_sortable(self):
        """ソート機能なしのレンダリングテスト"""
        component = TableComponent(
            data=self.df, columns=["Name", "Age"], sortable=False
        )

        result = component.render()
        assert isinstance(result, str)
        assert "sortTable" not in result

    def test_render_with_sortable(self):
        """ソート機能付きのレンダリングテスト"""
        component = TableComponent(data=self.df, columns=["Name", "Age"], sortable=True)

        result = component.render()
        assert isinstance(result, str)
        assert "sortTable" in result
        assert "cursor: pointer" in result

    def test_render_without_pagination(self):
        """ページネーションなしのレンダリングテスト（1ページのみ）"""
        component = TableComponent(
            data=self.df.head(5), columns=["Name", "Age"], page_size=10  # 5行のみ
        )

        result = component.render()
        assert isinstance(result, str)
        assert "ページ:" not in result  # ページネーションが表示されない

    def test_render_with_pagination(self):
        """ページネーション付きのレンダリングテスト"""
        component = TableComponent(
            data=self.df, columns=["Name", "Age"], page_size=2  # 2行ずつ表示
        )

        result = component.render()
        assert isinstance(result, str)
        assert "ページ:" in result
        assert "showPage" in result

    def test_get_csv_data(self):
        """CSVデータ取得のテスト"""
        component = TableComponent(data=self.df, columns=["Name", "Age"])

        csv_data = component.data_manager.get_csv_data()
        assert isinstance(csv_data, str)
        assert "Name,Age" in csv_data
        assert "Alice,25" in csv_data
        assert "Bob,30" in csv_data

    def test_render_with_none_values(self):
        """None値を含むデータのレンダリングテスト"""
        df_with_none = pd.DataFrame(
            {
                "Name": ["Alice", "Bob", None, "David"],
                "Age": [25, None, 35, 28],
                "City": ["Tokyo", "Osaka", "Kyoto", None],
            }
        )

        component = TableComponent(data=df_with_none, columns=["Name", "Age", "City"])

        result = component.render()
        assert isinstance(result, str)
        assert "data-table" in result
        # None値は空文字列として表示される

    def test_render_with_empty_dataframe(self):
        """空のデータフレームのレンダリングテスト"""
        empty_df = pd.DataFrame()

        component = TableComponent(data=empty_df, columns=[])

        result = component.render()
        assert isinstance(result, str)
        assert "data-table" in result

    def test_render_with_custom_height(self):
        """カスタム高さのレンダリングテスト"""
        component = TableComponent(data=self.df, columns=["Name", "Age"], height=600)

        result = component.render()
        assert isinstance(result, str)
        assert "max-height: 600px" in result

    def test_render_with_custom_page_size(self):
        """カスタムページサイズのレンダリングテスト"""
        component = TableComponent(data=self.df, columns=["Name", "Age"], page_size=3)

        result = component.render()
        assert isinstance(result, str)
        assert "showPage(0)" in result

    def test_csv_download_with_special_characters(self):
        """特殊文字を含むCSVダウンロードテスト"""
        df_special = pd.DataFrame(
            {
                "Name": ["Alice, Smith", 'Bob "Johnson"', "Charlie & Co."],
                "Age": [25, 30, 35],
                "City": ["New York, NY", "Los Angeles, CA", "Chicago, IL"],
            }
        )

        component = TableComponent(
            data=df_special, columns=["Name", "Age", "City"], enable_csv_download=True
        )

        result = component.render()
        assert isinstance(result, str)
        assert "CSVダウンロード" in result

        # CSVデータの確認
        csv_data = component.data_manager.get_csv_data()
        assert "Alice, Smith" in csv_data
        # CSVでは二重引用符はエスケープされる
        assert 'Bob ""Johnson""' in csv_data or 'Bob "Johnson"' in csv_data

    def test_sortable_with_numeric_data(self):
        """数値データのソート機能テスト"""
        component = TableComponent(
            data=self.df, columns=["Name", "Age", "Salary"], sortable=True
        )

        result = component.render()
        assert isinstance(result, str)
        assert "sortTable" in result
        assert "parseFloat" in result  # 数値ソート機能

    def test_search_with_multiple_columns(self):
        """複数列の検索機能テスト"""
        component = TableComponent(
            data=self.df, columns=["Name", "Age", "City"], searchable=True
        )

        result = component.render()
        assert isinstance(result, str)
        assert "table-search" in result
        assert "cells.length" in result  # 複数列検索

    def test_pagination_with_large_dataset(self):
        """大きなデータセットのページネーションテスト"""
        # 大きなデータセットを作成
        large_df = pd.DataFrame(
            {
                "ID": range(1, 101),
                "Name": [f"User{i}" for i in range(1, 101)],
                "Value": range(1, 101),
            }
        )

        component = TableComponent(
            data=large_df, columns=["ID", "Name", "Value"], page_size=10
        )

        result = component.render()
        assert isinstance(result, str)
        assert "ページ:" in result
        assert "showPage" in result

    def test_custom_kwargs(self):
        """カスタムキーワード引数のテスト"""
        component = TableComponent(
            data=self.df,
            columns=["Name", "Age"],
            custom_param="custom_value",
            another_param=123,
        )

        result = component.to_dict()
        assert result["kwargs"]["custom_param"] == "custom_value"
        assert result["kwargs"]["another_param"] == 123

    def test_render_all_features_disabled(self):
        """すべての機能を無効にしたレンダリングテスト"""
        component = TableComponent(
            data=self.df,
            columns=["Name", "Age"],
            enable_csv_download=False,
            sortable=False,
            searchable=False,
            title=None,
        )

        result = component.render()
        assert isinstance(result, str)
        assert "data-table" in result
        assert "table-search" not in result
        assert "CSVダウンロード" not in result
        assert "sortTable" not in result
        assert "<h3>" not in result

    def test_render_all_features_enabled(self):
        """すべての機能を有効にしたレンダリングテスト"""
        component = TableComponent(
            data=self.df,
            columns=["Name", "Age", "City"],
            enable_csv_download=True,
            sortable=True,
            searchable=True,
            title="Full Featured Table",
            page_size=2,
        )

        result = component.render()
        assert isinstance(result, str)
        assert "data-table" in result
        assert "table-search" in result
        assert "CSVダウンロード" in result
        assert "sortTable" in result
        assert "Full Featured Table" in result
        assert "ページ:" in result
