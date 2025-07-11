"""
エッジケースとエラーシナリオのテスト

Databricks UI Component Libraryの境界値テストとエラーハンドリングテストです。
"""

import pytest
import pandas as pd
import numpy as np
from db_ui_components import ChartComponent, TableComponent, FilterComponent, Dashboard


class TestChartComponentEdgeCases:
    """ChartComponentのエッジケースとエラーハンドリングテスト"""

    def test_empty_dataframe(self):
        """空のDataFrameでのテスト"""
        empty_df = pd.DataFrame()

        with pytest.raises(Exception):
            chart = ChartComponent(
                data=empty_df, chart_type="line", x_column="date", y_column="value"
            )
            chart.render()

    def test_single_row_dataframe(self):
        """1行のDataFrameでのテスト"""
        single_row_df = pd.DataFrame({"date": ["2024-01-01"], "value": [100]})

        chart = ChartComponent(
            data=single_row_df, chart_type="line", x_column="date", y_column="value"
        )

        html = chart.render()
        assert isinstance(html, str)
        assert len(html) > 0

    def test_invalid_column_names(self):
        """存在しない列名でのテスト"""
        df = pd.DataFrame(
            {
                "date": pd.date_range("2024-01-01", periods=5, freq="D"),
                "value": [1, 2, 3, 4, 5],
            }
        )

        with pytest.raises(Exception):
            chart = ChartComponent(
                data=df,
                chart_type="line",
                x_column="nonexistent_column",
                y_column="value",
            )
            chart.render()

    def test_null_values_in_data(self):
        """データにNULL値が含まれる場合のテスト"""
        df = pd.DataFrame(
            {
                "date": pd.date_range("2024-01-01", periods=5, freq="D"),
                "value": [1, None, 3, None, 5],
            }
        )

        chart = ChartComponent(
            data=df, chart_type="line", x_column="date", y_column="value"
        )

        html = chart.render()
        assert isinstance(html, str)
        assert len(html) > 0

    def test_mixed_data_types(self):
        """混合データタイプでのテスト"""
        df = pd.DataFrame(
            {
                "category": ["A", "B", "C", "D"],
                "value": [1, 2.5, 3, 4.7],
                "mixed": [1, "text", 3.14, None],
            }
        )

        chart = ChartComponent(
            data=df, chart_type="bar", x_column="category", y_column="value"
        )

        html = chart.render()
        assert isinstance(html, str)
        assert len(html) > 0

    def test_large_dataset(self):
        """大きなデータセットでのテスト"""
        large_df = pd.DataFrame(
            {
                "date": pd.date_range("2024-01-01", periods=10000, freq="H"),
                "value": np.random.randn(10000).cumsum(),
            }
        )

        chart = ChartComponent(
            data=large_df, chart_type="line", x_column="date", y_column="value"
        )

        html = chart.render()
        assert isinstance(html, str)
        assert len(html) > 0

    def test_unicode_data(self):
        """Unicodeデータでのテスト"""
        unicode_df = pd.DataFrame(
            {
                "カテゴリ": ["製品A", "製品B", "製品C"],
                "売上": [100, 200, 300],
                "備考": ["良好", "普通", "優秀"],
            }
        )

        chart = ChartComponent(
            data=unicode_df,
            chart_type="bar",
            x_column="カテゴリ",
            y_column="売上",
            title="日本語テストグラフ",
        )

        html = chart.render()
        assert isinstance(html, str)
        assert len(html) > 0
        # PlotlyはUnicode文字をエスケープシーケンスに変換するため、エスケープされた形式で確認
        assert (
            "\\u65e5\\u672c\\u8a9e\\u30c6\\u30b9\\u30c8\\u30b0\\u30e9\\u30d5" in html
            or "日本語テストグラフ" in html
        )

    def test_negative_height(self):
        """負の高さでのテスト"""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})

        chart = ChartComponent(
            data=df, chart_type="line", x_column="x", y_column="y", height=-100
        )

        # 負の高さでもエラーにならずに適切にハンドリングされることを確認
        html = chart.render()
        assert isinstance(html, str)
        assert len(html) > 0


class TestTableComponentEdgeCases:
    """TableComponentのエッジケースとエラーハンドリングテスト"""

    def test_empty_dataframe(self):
        """空のDataFrameでのテスト"""
        empty_df = pd.DataFrame()

        table = TableComponent(data=empty_df)
        html = table.render()

        assert isinstance(html, str)
        assert len(html) > 0

    def test_single_column_dataframe(self):
        """1列のDataFrameでのテスト"""
        single_col_df = pd.DataFrame({"value": [1, 2, 3, 4, 5]})

        table = TableComponent(data=single_col_df)
        html = table.render()

        assert isinstance(html, str)
        assert len(html) > 0
        assert "value" in html

    def test_invalid_columns(self):
        """存在しない列を指定した場合のテスト"""
        df = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})

        with pytest.raises(Exception):
            table = TableComponent(data=df, columns=["col1", "nonexistent_col"])
            table.render()

    def test_zero_page_size(self):
        """ページサイズが0の場合のテスト"""
        df = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})

        table = TableComponent(data=df, page_size=0)

        html = table.render()
        assert isinstance(html, str)
        assert len(html) > 0

    def test_very_large_page_size(self):
        """非常に大きなページサイズでのテスト"""
        df = pd.DataFrame({"col1": range(100), "col2": range(100, 200)})

        table = TableComponent(data=df, page_size=10000)

        html = table.render()
        assert isinstance(html, str)
        assert len(html) > 0

    def test_special_characters_in_data(self):
        """特殊文字を含むデータでのテスト"""
        df = pd.DataFrame(
            {
                "text": ['<script>alert("test")</script>', "&lt;test&gt;", '"quotes"'],
                "symbols": ["@#$%", "&amp;", "<>"],
            }
        )

        table = TableComponent(data=df)
        html = table.render()

        assert isinstance(html, str)
        assert len(html) > 0
        # HTMLエスケープされているか確認
        assert "<script>" not in html or "&lt;script&gt;" in html


class TestFilterComponentEdgeCases:
    """FilterComponentのエッジケースとエラーハンドリングテスト"""

    def test_empty_options(self):
        """空のオプションでのテスト"""
        filter_comp = FilterComponent(filter_type="dropdown", column="test", options=[])

        html = filter_comp.render()
        assert isinstance(html, str)
        assert len(html) > 0

    def test_none_options(self):
        """オプションがNoneの場合のテスト"""
        filter_comp = FilterComponent(
            filter_type="dropdown", column="test", options=None
        )

        html = filter_comp.render()
        assert isinstance(html, str)
        assert len(html) > 0

    def test_special_characters_in_options(self):
        """特殊文字を含むオプションでのテスト"""
        filter_comp = FilterComponent(
            filter_type="dropdown",
            column="test",
            options=["<script>", "&amp;", '"quotes"'],
        )

        html = filter_comp.render()
        assert isinstance(html, str)
        assert len(html) > 0

    def test_very_long_options(self):
        """非常に長いオプションでのテスト"""
        long_options = ["A" * 1000, "B" * 1000, "C" * 1000]

        filter_comp = FilterComponent(
            filter_type="dropdown", column="test", options=long_options
        )

        html = filter_comp.render()
        assert isinstance(html, str)
        assert len(html) > 0

    def test_invalid_column_name(self):
        """無効な列名でのテスト"""
        filter_comp = FilterComponent(
            filter_type="dropdown", column="", options=["A", "B", "C"]  # 空の列名
        )

        html = filter_comp.render()
        assert isinstance(html, str)
        assert len(html) > 0


class TestDashboardEdgeCases:
    """Dashboardのエッジケースとエラーハンドリングテスト"""

    def test_empty_dashboard(self):
        """空のダッシュボードでのテスト"""
        dashboard = Dashboard()

        html = dashboard.render()
        assert isinstance(html, str)
        assert len(html) > 0

    def test_invalid_position(self):
        """無効な位置でのテスト"""
        dashboard = Dashboard()
        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})
        chart = ChartComponent(data=df, chart_type="line", x_column="x", y_column="y")

        # 負の位置
        dashboard.add_component(chart, position=(-1, -1))

        html = dashboard.render()
        assert isinstance(html, str)
        assert len(html) > 0

    def test_overlapping_components(self):
        """重複するコンポーネントでのテスト"""
        dashboard = Dashboard()
        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})

        chart1 = ChartComponent(data=df, chart_type="line", x_column="x", y_column="y")
        chart2 = ChartComponent(data=df, chart_type="bar", x_column="x", y_column="y")

        # 同じ位置に配置
        dashboard.add_component(chart1, position=(0, 0))
        dashboard.add_component(chart2, position=(0, 0))

        html = dashboard.render()
        assert isinstance(html, str)
        assert len(html) > 0

    def test_remove_nonexistent_component(self):
        """存在しないコンポーネントの削除テスト"""
        dashboard = Dashboard()

        # 存在しないコンポーネントを削除してもエラーにならない
        dashboard.remove_component("nonexistent-id")

        html = dashboard.render()
        assert isinstance(html, str)
        assert len(html) > 0

    def test_very_long_title(self):
        """非常に長いタイトルでのテスト"""
        long_title = "A" * 10000
        dashboard = Dashboard(title=long_title)

        html = dashboard.render()
        assert isinstance(html, str)
        assert len(html) > 0
        assert long_title in html
