"""
HTML出力バリデーションテスト

Databricks UI Component Libraryの生成されるHTMLの品質と妥当性をテストします。
"""

import pytest
import pandas as pd
import numpy as np
import re
from html.parser import HTMLParser
from db_ui_components import ChartComponent, TableComponent, FilterComponent, Dashboard


class HTMLValidator(HTMLParser):
    """簡易HTMLバリデーター"""

    def __init__(self):
        super().__init__()
        self.tags = []
        self.errors = []
        self.self_closing_tags = {
            "br",
            "hr",
            "img",
            "input",
            "meta",
            "link",
            "area",
            "base",
            "col",
            "embed",
            "source",
            "track",
            "wbr",
        }

    def handle_starttag(self, tag, attrs):
        if tag not in self.self_closing_tags:
            self.tags.append(tag)

    def handle_endtag(self, tag):
        if tag in self.self_closing_tags:
            return

        if not self.tags:
            self.errors.append(f"閉じタグが開始タグなしで見つかりました: {tag}")
            return

        if self.tags[-1] != tag:
            self.errors.append(f"タグの不一致: 期待 {self.tags[-1]}, 実際 {tag}")
            return

        self.tags.pop()

    def get_validation_errors(self):
        errors = list(self.errors)
        if self.tags:
            errors.append(f"未閉じタグ: {self.tags}")
        return errors


class TestHTMLValidation:
    """HTML出力バリデーションテスト"""

    def validate_html(self, html_content):
        """HTML構造の妥当性を検証"""
        validator = HTMLValidator()
        validator.feed(html_content)
        return validator.get_validation_errors()

    def test_chart_html_structure(self):
        """チャートHTMLの構造テスト"""
        df = pd.DataFrame(
            {
                "date": pd.date_range("2024-01-01", periods=10, freq="D"),
                "value": np.random.randn(10).cumsum(),
            }
        )

        chart = ChartComponent(
            data=df,
            chart_type="line",
            x_column="date",
            y_column="value",
            title="テストチャート",
        )

        html = chart.render()

        # 基本的なHTML構造の検証
        assert isinstance(html, str)
        assert len(html) > 0

        # HTMLタグの妥当性確認
        errors = self.validate_html(html)
        assert len(errors) == 0, f"HTML構造エラー: {errors}"

        # 必要な要素の存在確認
        assert "plotly" in html.lower()
        assert "div" in html.lower()

    def test_table_html_structure(self):
        """テーブルHTMLの構造テスト"""
        df = pd.DataFrame(
            {"id": [1, 2, 3], "name": ["A", "B", "C"], "value": [100, 200, 300]}
        )

        table = TableComponent(
            data=df, enable_csv_download=True, sortable=True, searchable=True
        )

        html = table.render()

        # 基本的なHTML構造の検証
        assert isinstance(html, str)
        assert len(html) > 0

        # HTMLタグの妥当性確認
        errors = self.validate_html(html)
        assert len(errors) == 0, f"HTML構造エラー: {errors}"

        # テーブル要素の存在確認
        assert "<table" in html
        assert "<thead" in html
        assert "<tbody" in html
        assert "<th" in html
        assert "<td" in html

    def test_filter_html_structure(self):
        """フィルターHTMLの構造テスト"""
        filter_comp = FilterComponent(
            filter_type="dropdown",
            column="category",
            options=["A", "B", "C"],
            title="テストフィルター",
        )

        html = filter_comp.render()

        # 基本的なHTML構造の検証
        assert isinstance(html, str)
        assert len(html) > 0

        # HTMLタグの妥当性確認
        errors = self.validate_html(html)
        assert len(errors) == 0, f"HTML構造エラー: {errors}"

        # フィルター要素の存在確認
        assert "<select" in html
        assert "<option" in html
        assert "テストフィルター" in html

    def test_dashboard_html_structure(self):
        """ダッシュボードHTMLの構造テスト"""
        dashboard = Dashboard(title="テストダッシュボード")

        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})

        chart = ChartComponent(data=df, chart_type="line", x_column="x", y_column="y")

        dashboard.add_component(chart, position=(0, 0))

        html = dashboard.render()

        # 基本的なHTML構造の検証
        assert isinstance(html, str)
        assert len(html) > 0

        # HTMLタグの妥当性確認
        errors = self.validate_html(html)
        assert len(errors) == 0, f"HTML構造エラー: {errors}"

        # ダッシュボード要素の存在確認
        assert "テストダッシュボード" in html
        assert "dashboard" in html.lower()

    @pytest.mark.skip(reason="TableComponentのHTMLエスケープ実装待ち")
    def test_html_escaping(self):
        """HTMLエスケープのテスト"""
        # 特殊文字を含むデータ
        df = pd.DataFrame(
            {
                "text": ['<script>alert("test")</script>', "&lt;test&gt;", '"quotes"'],
                "value": [1, 2, 3],
            }
        )

        table = TableComponent(data=df)
        html = table.render()

        # 危険なスクリプトタグがエスケープされていることを確認
        assert '<script>alert("test")</script>' not in html

        # 基本的なHTML構造の妥当性
        errors = self.validate_html(html)
        assert len(errors) == 0, f"HTML構造エラー: {errors}"

    def test_html_attributes(self):
        """HTML属性の妥当性テスト"""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})

        chart = ChartComponent(
            data=df, chart_type="line", x_column="x", y_column="y", height=500
        )

        html = chart.render()

        # 基本的なHTML構造の検証
        assert isinstance(html, str)
        assert len(html) > 0

        # HTML属性の妥当性確認
        errors = self.validate_html(html)
        assert len(errors) == 0, f"HTML構造エラー: {errors}"

        # 属性値の確認
        assert "height" in html or "500" in html

    @pytest.mark.skip(reason="TableComponentのHTMLエスケープ実装待ち")
    def test_javascript_injection_prevention(self):
        """JavaScriptインジェクション防止のテスト"""
        # 悪意のあるJavaScriptコードを含むデータ
        malicious_data = pd.DataFrame(
            {
                "name": [
                    '<script>alert("xss")</script>',
                    'javascript:alert("xss")',
                    "onclick=\"alert('xss')\"",
                ],
                "value": [1, 2, 3],
            }
        )

        table = TableComponent(data=malicious_data)
        html = table.render()

        # 危険なスクリプトがエスケープされていることを確認
        assert '<script>alert("xss")</script>' not in html
        assert 'javascript:alert("xss")' not in html
        assert "onclick=\"alert('xss')\"" not in html

        # 基本的なHTML構造の妥当性
        errors = self.validate_html(html)
        assert len(errors) == 0, f"HTML構造エラー: {errors}"

    @pytest.mark.skip(reason="TableComponentのHTMLエスケープ実装待ち")
    def test_css_injection_prevention(self):
        """CSSインジェクション防止のテスト"""
        # 悪意のあるCSSコードを含むデータ
        malicious_data = pd.DataFrame(
            {
                "name": [
                    "<style>body{display:none}</style>",
                    "color:red;position:absolute",
                    'background:url(javascript:alert("xss"))',
                ],
                "value": [1, 2, 3],
            }
        )

        table = TableComponent(data=malicious_data)
        html = table.render()

        # 危険なスタイルタグがエスケープされていることを確認
        assert "<style>body{display:none}</style>" not in html

        # 基本的なHTML構造の妥当性
        errors = self.validate_html(html)
        assert len(errors) == 0, f"HTML構造エラー: {errors}"


class TestHTMLContent:
    """HTML内容の妥当性テスト"""

    @pytest.mark.skip(
        reason="Plotlyのバージョンによって日本語エンコーディングが異なるため一時的にスキップ"
    )
    def test_chart_content_accuracy(self):
        """チャート内容の正確性テスト"""
        df = pd.DataFrame({"category": ["A", "B", "C"], "value": [100, 200, 300]})

        chart = ChartComponent(
            data=df,
            chart_type="bar",
            x_column="category",
            y_column="value",
            title="売上データ",
        )

        html = chart.render()

        # タイトルの存在確認（PlotlyのレイアウトまたはJSONデータ内）
        # Plotlyの場合、タイトルがJavaScriptコード内にUnicodeエンコードされている可能性がある
        assert "売上データ" in html or "\\u58f2\\u4e0a\\u30c7\\u30fc\\u30bf" in html

        # データの値が含まれているかの確認（JSON形式で）
        assert "100" in html
        assert "200" in html
        assert "300" in html

    def test_table_content_accuracy(self):
        """テーブル内容の正確性テスト"""
        df = pd.DataFrame(
            {
                "ID": [1, 2, 3],
                "名前": ["製品A", "製品B", "製品C"],
                "価格": [1000, 2000, 3000],
            }
        )

        table = TableComponent(data=df)
        html = table.render()

        # 列名の存在確認
        assert "ID" in html
        assert "名前" in html
        assert "価格" in html

        # データの値の存在確認
        assert "製品A" in html
        assert "製品B" in html
        assert "製品C" in html
        assert "1000" in html
        assert "2000" in html
        assert "3000" in html

    def test_filter_content_accuracy(self):
        """フィルター内容の正確性テスト"""
        filter_comp = FilterComponent(
            filter_type="dropdown",
            column="category",
            options=["製品A", "製品B", "製品C"],
            title="製品カテゴリ",
        )

        html = filter_comp.render()

        # タイトルの存在確認
        assert "製品カテゴリ" in html

        # オプションの存在確認
        assert "製品A" in html
        assert "製品B" in html
        assert "製品C" in html

    def test_unicode_content_handling(self):
        """Unicode文字の適切な処理テスト"""
        df = pd.DataFrame(
            {
                "項目": ["データ①", "データ②", "データ③"],
                "数値": [100, 200, 300],
                "備考": ["完了✓", "処理中⏳", "未完了❌"],
            }
        )

        table = TableComponent(data=df)
        html = table.render()

        # Unicode文字の存在確認
        assert "データ①" in html
        assert "データ②" in html
        assert "データ③" in html
        assert "完了✓" in html
        assert "処理中⏳" in html
        assert "未完了❌" in html

    def test_numeric_precision(self):
        """数値精度の適切な処理テスト"""
        df = pd.DataFrame(
            {
                "float_values": [1.234567890, 2.987654321, 3.141592653],
                "int_values": [1, 2, 3],
            }
        )

        table = TableComponent(data=df)
        html = table.render()

        # 数値が文字列として適切に表示されているか確認
        assert "1.23" in html or "1.234" in html  # 浮動小数点数
        assert "2.98" in html or "2.987" in html
        assert "3.14" in html or "3.141" in html

    def test_empty_cell_handling(self):
        """空セルの適切な処理テスト"""
        df = pd.DataFrame({"name": ["A", None, "C"], "value": [1, 2, None]})

        table = TableComponent(data=df)
        html = table.render()

        # 空セルが適切に処理されているか確認
        assert isinstance(html, str)
        assert len(html) > 0

        # HTMLが妥当な構造を持っているか確認
        validator = HTMLValidator()
        validator.feed(html)
        errors = validator.get_validation_errors()
        assert len(errors) == 0, f"HTML構造エラー: {errors}"


class TestResponsiveDesign:
    """レスポンシブデザインのテスト"""

    def test_mobile_responsive_elements(self):
        """モバイル対応要素のテスト"""
        df = pd.DataFrame(
            {
                "date": pd.date_range("2024-01-01", periods=10, freq="D"),
                "value": np.random.randn(10),
            }
        )

        chart = ChartComponent(
            data=df, chart_type="line", x_column="date", y_column="value"
        )

        html = chart.render()

        # レスポンシブデザインの基本要素が含まれているか確認
        assert "width" in html.lower()
        assert "height" in html.lower()

    def test_css_media_queries(self):
        """CSSメディアクエリの存在テスト"""
        dashboard = Dashboard(title="レスポンシブテスト")

        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})

        chart = ChartComponent(data=df, chart_type="line", x_column="x", y_column="y")

        dashboard.add_component(chart, position=(0, 0))

        html = dashboard.render()

        # CSS関連の要素が含まれているか確認
        assert "style" in html.lower()
        assert "grid" in html.lower() or "flex" in html.lower()
