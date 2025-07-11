"""
pytest設定ファイル

Databricks UI Component Libraryのテスト用の共通設定とフィクスチャを定義します。
"""

import pytest
import pandas as pd
import numpy as np
from db_ui_components import ChartComponent, TableComponent, FilterComponent, Dashboard


@pytest.fixture
def sample_data():
    """サンプルデータのフィクスチャ"""
    return pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=10, freq="D"),
            "value": np.random.randn(10).cumsum() + 100,
            "category": np.random.choice(["A", "B", "C"], 10),
            "region": np.random.choice(["東京", "大阪", "名古屋"], 10),
        }
    )


@pytest.fixture
def large_sample_data():
    """大きなサンプルデータのフィクスチャ"""
    return pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=1000, freq="H"),
            "value": np.random.randn(1000).cumsum() + 1000,
            "category": np.random.choice(["A", "B", "C", "D", "E"], 1000),
            "region": np.random.choice(["東京", "大阪", "名古屋", "福岡"], 1000),
            "product": np.random.choice(["商品1", "商品2", "商品3"], 1000),
        }
    )


@pytest.fixture
def empty_data():
    """空のデータフレームのフィクスチャ"""
    return pd.DataFrame()


@pytest.fixture
def single_row_data():
    """1行のデータフレームのフィクスチャ"""
    return pd.DataFrame({"date": ["2024-01-01"], "value": [100], "category": ["A"]})


@pytest.fixture
def unicode_data():
    """Unicode文字を含むデータのフィクスチャ"""
    return pd.DataFrame(
        {
            "カテゴリ": ["製品A", "製品B", "製品C"],
            "売上": [100, 200, 300],
            "備考": ["良好", "普通", "優秀"],
        }
    )


@pytest.fixture
def malicious_data():
    """悪意のあるデータを含むフィクスチャ"""
    return pd.DataFrame(
        {
            "name": [
                '<script>alert("xss")</script>',
                'javascript:alert("xss")',
                "onclick=\"alert('xss')\"",
            ],
            "value": [1, 2, 3],
            "text": ["<style>body{display:none}</style>", "&lt;test&gt;", '"quotes"'],
        }
    )


@pytest.fixture
def basic_chart(sample_data):
    """基本的なチャートコンポーネントのフィクスチャ"""
    return ChartComponent(
        data=sample_data,
        chart_type="line",
        x_column="date",
        y_column="value",
        title="テストチャート",
    )


@pytest.fixture
def basic_table(sample_data):
    """基本的なテーブルコンポーネントのフィクスチャ"""
    return TableComponent(
        data=sample_data, enable_csv_download=True, sortable=True, searchable=True
    )


@pytest.fixture
def basic_filter():
    """基本的なフィルターコンポーネントのフィクスチャ"""
    return FilterComponent(
        filter_type="dropdown",
        column="category",
        options=["A", "B", "C"],
        title="テストフィルター",
    )


@pytest.fixture
def basic_dashboard():
    """基本的なダッシュボードのフィクスチャ"""
    return Dashboard(title="テストダッシュボード")


@pytest.fixture
def configured_dashboard(basic_dashboard, basic_chart, basic_table, basic_filter):
    """設定済みダッシュボードのフィクスチャ"""
    basic_dashboard.add_component(basic_filter, position=(0, 0))
    basic_dashboard.add_component(basic_chart, position=(1, 0))
    basic_dashboard.add_component(basic_table, position=(2, 0))
    return basic_dashboard


# テスト設定
def pytest_configure(config):
    """pytest設定の追加"""
    # 警告を無視
    config.option.filterwarnings = [
        "ignore::DeprecationWarning",
        "ignore::FutureWarning",
    ]


# テストマーカーの定義
pytest_plugins = []


def pytest_collection_modifyitems(config, items):
    """テストアイテムの修正"""
    # 長時間実行されるテストにマーカーを追加
    for item in items:
        if "performance" in item.name or "stress" in item.name:
            item.add_marker(pytest.mark.slow)
        if "integration" in item.name:
            item.add_marker(pytest.mark.integration)


# パラメータ化されたテスト用のデータ
chart_types = ["line", "bar", "pie", "scatter", "heatmap"]
filter_types = ["dropdown", "multiselect", "text", "date"]
layout_types = ["grid", "flex", "custom"]


@pytest.fixture(params=chart_types)
def chart_type(request):
    """チャートタイプのパラメータ化フィクスチャ"""
    return request.param


@pytest.fixture(params=filter_types)
def filter_type(request):
    """フィルタータイプのパラメータ化フィクスチャ"""
    return request.param


@pytest.fixture(params=layout_types)
def layout_type(request):
    """レイアウトタイプのパラメータ化フィクスチャ"""
    return request.param


# テストスキップ条件
def pytest_addoption(parser):
    """pytestオプションの追加"""
    parser.addoption(
        "--skip-slow", action="store_true", default=False, help="Skip slow tests"
    )


skip_slow_tests = pytest.mark.skipif(
    True, reason="Slow tests skipped"  # この条件は実際のテストで動的に設定
)


# テストデータ生成ヘルパー
def generate_test_data(rows=100, columns=None):
    """テストデータ生成ヘルパー関数"""
    if columns is None:
        columns = ["date", "value", "category"]

    data = {}
    for col in columns:
        if col == "date":
            data[col] = pd.date_range("2024-01-01", periods=rows, freq="D")
        elif col == "value":
            data[col] = np.random.randn(rows).cumsum() + 100
        elif col == "category":
            data[col] = np.random.choice(["A", "B", "C"], rows)
        else:
            data[col] = np.random.randn(rows)

    return pd.DataFrame(data)


# テストユーティリティ
class TestUtils:
    """テストユーティリティクラス"""

    @staticmethod
    def assert_html_valid(html):
        """HTMLの妥当性を検証"""
        assert isinstance(html, str)
        assert len(html) > 0
        assert "<" in html and ">" in html

    @staticmethod
    def assert_contains_all(html, *args):
        """HTMLに指定された全ての文字列が含まれているかチェック"""
        for arg in args:
            assert arg in html, f"'{arg}' not found in HTML"

    @staticmethod
    def assert_not_contains_any(html, *args):
        """HTMLに指定された文字列が含まれていないかチェック"""
        for arg in args:
            assert arg not in html, f"'{arg}' found in HTML (should not be present)"


@pytest.fixture
def test_utils():
    """テストユーティリティのフィクスチャ"""
    return TestUtils()
