"""
統合テスト

Databricks UI Component Libraryの複雑なシナリオとコンポーネント間の相互作用をテストします。
"""

import pytest
import pandas as pd
import numpy as np
from db_ui_components import ChartComponent, TableComponent, FilterComponent, Dashboard


class TestComponentIntegration:
    """コンポーネント統合テスト"""

    def test_chart_table_integration(self):
        """チャートとテーブルの統合テスト"""
        # 共通データ
        df = pd.DataFrame(
            {
                "date": pd.date_range("2024-01-01", periods=30, freq="D"),
                "sales": np.random.randn(30).cumsum() + 1000,
                "category": np.random.choice(["A", "B", "C"], 30),
                "region": np.random.choice(["東京", "大阪", "名古屋"], 30),
            }
        )

        # チャートコンポーネント
        chart = ChartComponent(
            data=df, chart_type="line", x_column="date", y_column="sales", title="売上推移"
        )

        # テーブルコンポーネント
        table = TableComponent(
            data=df,
            columns=["date", "sales", "category", "region"],
            enable_csv_download=True,
            sortable=True,
            searchable=True,
        )

        # ダッシュボードに配置
        dashboard = Dashboard(title="売上ダッシュボード")
        dashboard.add_component(chart, position=(0, 0), size=(2, 1))
        dashboard.add_component(table, position=(1, 0), size=(2, 1))

        # レンダリング
        html = dashboard.render()

        # 基本的なアサート
        assert isinstance(html, str)
        assert len(html) > 0
        assert "売上ダッシュボード" in html
        assert "売上推移" in html
        assert "plotly" in html.lower()
        assert "table" in html.lower()

    def test_filter_chart_integration(self):
        """フィルターとチャートの統合テスト"""
        # サンプルデータ
        df = pd.DataFrame(
            {
                "month": pd.date_range("2024-01-01", periods=12, freq="M"),
                "revenue": np.random.randn(12).cumsum() + 10000,
                "product": np.random.choice(["商品A", "商品B", "商品C"], 12),
                "status": np.random.choice(["完了", "進行中", "計画中"], 12),
            }
        )

        # フィルターコンポーネント
        product_filter = FilterComponent(
            filter_type="dropdown",
            column="product",
            options=["商品A", "商品B", "商品C"],
            title="商品選択",
        )

        status_filter = FilterComponent(
            filter_type="multiselect",
            column="status",
            options=["完了", "進行中", "計画中"],
            title="ステータス",
        )

        # チャートコンポーネント
        chart = ChartComponent(
            data=df,
            chart_type="bar",
            x_column="month",
            y_column="revenue",
            title="月別売上",
        )

        # ダッシュボードに配置
        dashboard = Dashboard(title="売上分析ダッシュボード")
        dashboard.add_component(product_filter, position=(0, 0), size=(1, 1))
        dashboard.add_component(status_filter, position=(0, 1), size=(1, 1))
        dashboard.add_component(chart, position=(1, 0), size=(2, 1))

        # レンダリング
        html = dashboard.render()

        # 基本的なアサート
        assert isinstance(html, str)
        assert len(html) > 0
        assert "売上分析ダッシュボード" in html
        assert "商品選択" in html
        assert "ステータス" in html
        assert "月別売上" in html

    def test_multiple_charts_integration(self):
        """複数チャートの統合テスト"""
        # 共通データ
        df = pd.DataFrame(
            {
                "date": pd.date_range("2024-01-01", periods=50, freq="D"),
                "revenue": np.random.randn(50).cumsum() + 50000,
                "cost": np.random.randn(50).cumsum() + 30000,
                "profit": lambda x: x["revenue"] - x["cost"],
            }
        )
        df["profit"] = df["revenue"] - df["cost"]

        # 複数のチャート
        revenue_chart = ChartComponent(
            data=df,
            chart_type="line",
            x_column="date",
            y_column="revenue",
            title="売上推移",
        )

        cost_chart = ChartComponent(
            data=df, chart_type="line", x_column="date", y_column="cost", title="コスト推移"
        )

        profit_chart = ChartComponent(
            data=df, chart_type="line", x_column="date", y_column="profit", title="利益推移"
        )

        # ダッシュボードに配置
        dashboard = Dashboard(title="財務ダッシュボード")
        dashboard.add_component(revenue_chart, position=(0, 0), size=(2, 1))
        dashboard.add_component(cost_chart, position=(0, 2), size=(2, 1))
        dashboard.add_component(profit_chart, position=(1, 0), size=(4, 1))

        # レンダリング
        html = dashboard.render()

        # 基本的なアサート
        assert isinstance(html, str)
        assert len(html) > 0
        assert "財務ダッシュボード" in html
        assert "売上推移" in html
        assert "コスト推移" in html
        assert "利益推移" in html

    def test_complex_dashboard_layout(self):
        """複雑なダッシュボードレイアウトテスト"""
        # 複数の異なるデータセット
        sales_data = pd.DataFrame(
            {
                "month": pd.date_range("2024-01-01", periods=12, freq="M"),
                "sales": np.random.randn(12).cumsum() + 100000,
            }
        )

        product_data = pd.DataFrame(
            {
                "product": ["商品A", "商品B", "商品C", "商品D"],
                "quantity": [150, 200, 180, 120],
                "price": [1000, 1500, 800, 2000],
            }
        )

        region_data = pd.DataFrame(
            {
                "region": ["東京", "大阪", "名古屋", "福岡", "札幌"],
                "sales": [50000, 40000, 30000, 25000, 20000],
            }
        )

        # 複数のコンポーネント
        components = [
            # フィルター
            FilterComponent(filter_type="date", column="month", title="期間選択"),
            FilterComponent(
                filter_type="dropdown",
                column="product",
                options=["商品A", "商品B", "商品C", "商品D"],
                title="商品選択",
            ),
            # チャート
            ChartComponent(
                data=sales_data,
                chart_type="line",
                x_column="month",
                y_column="sales",
                title="月別売上",
            ),
            ChartComponent(
                data=product_data,
                chart_type="bar",
                x_column="product",
                y_column="quantity",
                title="商品別販売数",
            ),
            ChartComponent(
                data=region_data,
                chart_type="pie",
                x_column="region",
                y_column="sales",
                title="地域別売上",
            ),
            # テーブル
            TableComponent(
                data=product_data, enable_csv_download=True, sortable=True, title="商品詳細"
            ),
            TableComponent(
                data=region_data, enable_csv_download=True, sortable=True, title="地域別詳細"
            ),
        ]

        # ダッシュボードに配置
        dashboard = Dashboard(title="総合ダッシュボード")

        positions = [
            (0, 0),
            (0, 1),  # フィルター
            (1, 0),
            (1, 1),  # チャート
            (2, 0),  # 円グラフ
            (3, 0),
            (3, 1),  # テーブル
        ]

        for i, component in enumerate(components):
            dashboard.add_component(component, position=positions[i])

        # レンダリング
        html = dashboard.render()

        # 基本的なアサート
        assert isinstance(html, str)
        assert len(html) > 0
        assert "総合ダッシュボード" in html
        assert "期間選択" in html
        assert "商品選択" in html
        assert "月別売上" in html
        assert "商品別販売数" in html
        assert "地域別売上" in html
        assert "商品詳細" in html
        assert "地域別詳細" in html


class TestDataFlowIntegration:
    """データフロー統合テスト"""

    def test_data_update_propagation(self):
        """データ更新の伝播テスト"""
        # 初期データ
        df = pd.DataFrame(
            {
                "date": pd.date_range("2024-01-01", periods=10, freq="D"),
                "value": np.random.randn(10).cumsum(),
            }
        )

        # コンポーネントの作成
        chart = ChartComponent(
            data=df,
            chart_type="line",
            x_column="date",
            y_column="value",
            title="データ更新テスト",
        )

        table = TableComponent(data=df, enable_csv_download=True)

        dashboard = Dashboard(title="データ更新ダッシュボード")
        dashboard.add_component(chart, position=(0, 0))
        dashboard.add_component(table, position=(1, 0))

        # 初期レンダリング
        html1 = dashboard.render()
        assert isinstance(html1, str)
        assert len(html1) > 0

        # データ更新
        new_df = pd.DataFrame(
            {
                "date": pd.date_range("2024-01-01", periods=15, freq="D"),
                "value": np.random.randn(15).cumsum(),
            }
        )

        chart.update_data(new_df)
        table.update_data(new_df)

        # 更新後のレンダリング
        html2 = dashboard.render()
        assert isinstance(html2, str)
        assert len(html2) > 0

        # 更新前後でHTMLが異なることを確認
        assert html1 != html2

    def test_component_configuration_consistency(self):
        """コンポーネント設定の整合性テスト"""
        # 共通データ
        df = pd.DataFrame({"category": ["A", "B", "C", "D"], "value": [10, 20, 30, 40]})

        # 同じデータで異なるコンポーネントを作成
        chart = ChartComponent(
            data=df,
            chart_type="bar",
            x_column="category",
            y_column="value",
            title="設定テスト",
        )

        table = TableComponent(data=df, columns=["category", "value"], title="設定テスト")

        filter_comp = FilterComponent(
            filter_type="dropdown",
            column="category",
            options=["A", "B", "C", "D"],
            title="設定テスト",
        )

        # 設定の一貫性を確認
        chart_config = chart.to_dict()
        table_config = table.to_dict()
        filter_config = filter_comp.to_dict()

        assert chart_config["type"] == "chart"
        assert table_config["type"] == "table"
        assert filter_config["type"] == "filter"

        # 共通のタイトルが設定されているか確認
        assert chart_config.get("title") == "設定テスト"
        assert table_config.get("title") == "設定テスト"
        assert filter_config.get("title") == "設定テスト"

    def test_large_scale_integration(self):
        """大規模統合テスト"""
        # 大きなデータセット
        large_df = pd.DataFrame(
            {
                "date": pd.date_range("2024-01-01", periods=1000, freq="D"),
                "sales": np.random.randn(1000).cumsum() + 100000,
                "category": np.random.choice(["A", "B", "C", "D", "E"], 1000),
                "region": np.random.choice(["東京", "大阪", "名古屋", "福岡"], 1000),
                "product": np.random.choice(["商品1", "商品2", "商品3", "商品4", "商品5"], 1000),
            }
        )

        # 複数のコンポーネント
        dashboard = Dashboard(title="大規模ダッシュボード")

        # 10個のチャートを追加
        for i in range(10):
            sample_data = large_df.sample(n=100)
            chart = ChartComponent(
                data=sample_data,
                chart_type="line",
                x_column="date",
                y_column="sales",
                title=f"チャート{i+1}",
            )
            dashboard.add_component(chart, position=(i // 5, i % 5))

        # 5個のテーブルを追加
        for i in range(5):
            sample_data = large_df.sample(n=50)
            table = TableComponent(
                data=sample_data,
                columns=["date", "sales", "category", "region"],
                page_size=10,
                title=f"テーブル{i+1}",
            )
            dashboard.add_component(table, position=(i + 10, 0))

        # 5個のフィルターを追加
        for i, column in enumerate(["category", "region", "product"]):
            unique_values = large_df[column].unique().tolist()
            filter_comp = FilterComponent(
                filter_type="dropdown",
                column=column,
                options=unique_values,
                title=f"{column}フィルター",
            )
            dashboard.add_component(filter_comp, position=(i + 15, 0))

        # レンダリング
        html = dashboard.render()

        # 基本的なアサート
        assert isinstance(html, str)
        assert len(html) > 0
        assert "大規模ダッシュボード" in html

        # 全てのコンポーネントが含まれているか確認
        for i in range(10):
            assert f"チャート{i+1}" in html

        for i in range(5):
            assert f"テーブル{i+1}" in html


class TestErrorHandlingIntegration:
    """エラーハンドリング統合テスト"""

    def test_component_error_isolation(self):
        """コンポーネントエラーの分離テスト"""
        # 正常なデータ
        good_df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})

        # 問題のあるデータ
        bad_df = pd.DataFrame()

        dashboard = Dashboard(title="エラー分離テスト")

        # 正常なコンポーネント
        good_chart = ChartComponent(
            data=good_df, chart_type="line", x_column="x", y_column="y", title="正常なチャート"
        )

        # 問題のあるコンポーネント
        try:
            bad_chart = ChartComponent(
                data=bad_df,
                chart_type="line",
                x_column="x",
                y_column="y",
                title="問題のあるチャート",
            )
            dashboard.add_component(bad_chart, position=(1, 0))
        except BaseException:
            # エラーが発生した場合はスキップ
            pass

        dashboard.add_component(good_chart, position=(0, 0))

        # 正常なコンポーネントは動作することを確認
        html = dashboard.render()
        assert isinstance(html, str)
        assert len(html) > 0
        assert "正常なチャート" in html

    def test_dashboard_resilience(self):
        """ダッシュボードの回復性テスト"""
        dashboard = Dashboard(title="回復性テスト")

        # 複数のコンポーネントを追加（一部は問題がある可能性）
        for i in range(10):
            try:
                if i % 3 == 0:
                    # 空のデータフレーム
                    df = pd.DataFrame()
                else:
                    # 正常なデータ
                    df = pd.DataFrame({"x": range(10), "y": np.random.randn(10)})

                chart = ChartComponent(
                    data=df,
                    chart_type="line",
                    x_column="x",
                    y_column="y",
                    title=f"チャート{i}",
                )
                dashboard.add_component(chart, position=(i, 0))
            except BaseException:
                # エラーが発生した場合はスキップ
                continue

        # ダッシュボードがレンダリングできることを確認
        html = dashboard.render()
        assert isinstance(html, str)
        assert len(html) > 0
        assert "回復性テスト" in html
