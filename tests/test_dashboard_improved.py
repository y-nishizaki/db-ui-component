"""
Dashboardの改善されたテスト

未カバー部分を含む全機能をテストします。
"""

import pytest
import json
import tempfile
import os
from unittest.mock import MagicMock, patch
from db_ui_components.dashboard import Dashboard


class TestDashboardUncovered:
    """Dashboardの未カバー部分のテスト"""

    def setup_method(self):
        """テスト前の準備"""
        self.dashboard = Dashboard(title="Test Dashboard")
        self.mock_component = MagicMock()
        self.mock_component.render.return_value = "<div>Test Component</div>"

    def test_remove_component(self):
        """コンポーネント削除のテスト"""
        # コンポーネントを追加
        self.dashboard.add_component(
            self.mock_component,
            position=(0, 0),
            size=(1, 1),
            component_id="test-component",
        )

        # 削除前の確認
        assert len(self.dashboard.components) == 1
        assert "test-component" in self.dashboard.positions

        # コンポーネントを削除
        self.dashboard.remove_component("test-component")

        # 削除後の確認
        assert len(self.dashboard.components) == 0
        assert "test-component" not in self.dashboard.positions
        assert "test-component" not in self.dashboard.styles

    def test_remove_nonexistent_component(self):
        """存在しないコンポーネントの削除テスト"""
        # エラーが発生しないことを確認
        self.dashboard.remove_component("nonexistent")

    def test_update_component(self):
        """コンポーネント更新のテスト"""
        # コンポーネントを追加
        self.dashboard.add_component(
            self.mock_component,
            position=(0, 0),
            size=(1, 1),
            component_id="test-component",
        )

        # 新しいコンポーネントを作成
        new_component = MagicMock()
        new_component.render.return_value = "<div>Updated Component</div>"

        # コンポーネントを更新
        self.dashboard.update_component("test-component", new_component)

        # 更新されたコンポーネントを取得
        updated_component = self.dashboard.get_component("test-component")
        assert updated_component == new_component

    def test_update_nonexistent_component(self):
        """存在しないコンポーネントの更新テスト"""
        new_component = MagicMock()
        # エラーが発生しないことを確認
        self.dashboard.update_component("nonexistent", new_component)

    def test_set_component_style(self):
        """コンポーネントスタイル設定のテスト"""
        style = {"backgroundColor": "#f5f5f5", "borderRadius": "8px", "padding": "16px"}

        self.dashboard.set_component_style("test-component", style)
        assert self.dashboard.styles["test-component"] == style

    def test_get_component(self):
        """コンポーネント取得のテスト"""
        # コンポーネントを追加
        self.dashboard.add_component(
            self.mock_component,
            position=(0, 0),
            size=(1, 1),
            component_id="test-component",
        )

        # コンポーネントを取得
        component = self.dashboard.get_component("test-component")
        assert component == self.mock_component

    def test_get_nonexistent_component(self):
        """存在しないコンポーネントの取得テスト"""
        component = self.dashboard.get_component("nonexistent")
        assert component is None

    def test_to_dict(self):
        """辞書形式への変換テスト"""
        # コンポーネントを追加
        self.dashboard.add_component(
            self.mock_component,
            position=(0, 0),
            size=(2, 1),
            component_id="test-component",
            style={"backgroundColor": "blue"},
        )

        result = self.dashboard.to_dict()
        expected = {
            "title": "Test Dashboard",
            "layout": "grid",
            "components": [
                {
                    "id": "test-component",
                    "position": (0, 0),
                    "size": (2, 1),
                    "kwargs": {"style": {"backgroundColor": "blue"}},
                }
            ],
            "styles": {"test-component": {"backgroundColor": "blue"}},
        }
        assert result == expected

    def test_save_and_load_layout(self):
        """レイアウトの保存と読み込みテスト"""
        # コンポーネントを追加
        self.dashboard.add_component(
            self.mock_component,
            position=(0, 0),
            size=(1, 1),
            component_id="test-component",
        )

        # 一時ファイルに保存
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            filename = f.name

        try:
            self.dashboard.save_layout(filename)

            # 新しいダッシュボードで読み込み
            new_dashboard = Dashboard()
            new_dashboard.load_layout(filename)

            # 設定が正しく読み込まれたことを確認
            assert new_dashboard.title == "Test Dashboard"
            assert new_dashboard.layout == "grid"
            assert "test-component" in new_dashboard.positions
            assert new_dashboard.positions["test-component"] == (0, 0)

        finally:
            # 一時ファイルを削除
            if os.path.exists(filename):
                os.unlink(filename)

    def test_render_without_title(self):
        """タイトルなしのレンダリングテスト"""
        dashboard = Dashboard()  # タイトルなし
        dashboard.add_component(self.mock_component, position=(0, 0), size=(1, 1))

        result = dashboard.render()
        assert isinstance(result, str)
        assert "dashboard-container" in result
        assert "dashboard-header" not in result

    def test_render_with_title(self):
        """タイトル付きのレンダリングテスト"""
        dashboard = Dashboard(title="Test Dashboard")
        dashboard.add_component(self.mock_component, position=(0, 0), size=(1, 1))

        result = dashboard.render()
        assert isinstance(result, str)
        assert "dashboard-header" in result
        assert "Test Dashboard" in result

    def test_render_flex_layout(self):
        """フレックスレイアウトのレンダリングテスト"""
        dashboard = Dashboard(title="Test Dashboard", layout="flex")
        dashboard.add_component(self.mock_component, position=(0, 0), size=(1, 1))

        result = dashboard.render()
        assert isinstance(result, str)
        assert "display: flex" in result
        assert "flex-wrap: wrap" in result

    def test_render_custom_layout(self):
        """カスタムレイアウトのレンダリングテスト"""
        dashboard = Dashboard(title="Test Dashboard", layout="custom")
        dashboard.add_component(self.mock_component, position=(0, 0), size=(1, 1))

        result = dashboard.render()
        assert isinstance(result, str)
        assert "dashboard-container" in result
        assert "display: grid" not in result
        assert "display: flex" not in result

    def test_render_component_with_style(self):
        """スタイル付きコンポーネントのレンダリングテスト"""
        dashboard = Dashboard(title="Test Dashboard")
        dashboard.add_component(
            self.mock_component,
            position=(0, 0),
            size=(1, 1),
            component_id="test-component",
        )

        # スタイルを設定
        style = {"backgroundColor": "red", "borderRadius": "10px"}
        dashboard.set_component_style("test-component", style)

        result = dashboard.render()
        assert isinstance(result, str)
        assert "background-color: red" in result
        assert "border-radius: 10px" in result

    def test_render_grid_component(self):
        """グリッドレイアウトのコンポーネントレンダリングテスト"""
        dashboard = Dashboard(title="Test Dashboard", layout="grid")
        dashboard.add_component(
            self.mock_component, position=(1, 2), size=(2, 1)  # 2行目、3列目  # 2列分、1行分
        )

        result = dashboard.render()
        assert isinstance(result, str)
        assert "grid-column: 3 / span 2" in result
        assert "grid-row: 2 / span 1" in result

    def test_render_flex_component(self):
        """フレックスレイアウトのコンポーネントレンダリングテスト"""
        dashboard = Dashboard(title="Test Dashboard", layout="flex")
        dashboard.add_component(
            self.mock_component,
            position=(0, 0),
            size=(2, 1),  # flex-grow: 2, flex-shrink: 1
        )

        result = dashboard.render()
        assert isinstance(result, str)
        assert "flex: 2 1 0" in result
        assert "min-width: 400px" in result

    def test_load_layout_with_missing_file(self):
        """存在しないファイルからのレイアウト読み込みテスト"""
        dashboard = Dashboard()

        with pytest.raises(FileNotFoundError):
            dashboard.load_layout("nonexistent_file.json")

    def test_load_layout_with_invalid_json(self):
        """無効なJSONファイルからのレイアウト読み込みテスト"""
        dashboard = Dashboard()

        # 無効なJSONファイルを作成
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("invalid json content")
            filename = f.name

        try:
            with pytest.raises(json.JSONDecodeError):
                dashboard.load_layout(filename)
        finally:
            if os.path.exists(filename):
                os.unlink(filename)

    def test_save_layout_with_directory_error(self):
        """ディレクトリエラー時のレイアウト保存テスト"""
        dashboard = Dashboard()
        dashboard.add_component(self.mock_component, position=(0, 0), size=(1, 1))

        # 存在しないディレクトリに保存しようとする
        with pytest.raises(FileNotFoundError):
            dashboard.save_layout("/nonexistent/directory/layout.json")

    def test_multiple_components(self):
        """複数コンポーネントのテスト"""
        dashboard = Dashboard(title="Test Dashboard")

        # 複数のコンポーネントを追加
        component1 = MagicMock()
        component1.render.return_value = "<div>Component 1</div>"

        component2 = MagicMock()
        component2.render.return_value = "<div>Component 2</div>"

        dashboard.add_component(
            component1, position=(0, 0), size=(1, 1), component_id="comp1"
        )
        dashboard.add_component(
            component2, position=(0, 1), size=(1, 1), component_id="comp2"
        )

        result = dashboard.render()
        assert isinstance(result, str)
        assert "Component 1" in result
        assert "Component 2" in result
        assert len(dashboard.components) == 2

    def test_component_without_id(self):
        """IDなしコンポーネントのテスト"""
        dashboard = Dashboard(title="Test Dashboard")

        # IDなしでコンポーネントを追加
        dashboard.add_component(self.mock_component, position=(0, 0), size=(1, 1))

        result = dashboard.render()
        assert isinstance(result, str)
        assert "dashboard-component" in result

    def test_component_with_custom_kwargs(self):
        """カスタムキーワード引数付きコンポーネントのテスト"""
        dashboard = Dashboard(title="Test Dashboard")

        # カスタムキーワード引数付きでコンポーネントを追加
        dashboard.add_component(
            self.mock_component,
            position=(0, 0),
            size=(1, 1),
            component_id="test-component",
            custom_param="custom_value",
            another_param=123,
        )

        # kwargsが正しく保存されていることを確認
        component_info = dashboard.components[0]
        assert component_info["kwargs"]["custom_param"] == "custom_value"
        assert component_info["kwargs"]["another_param"] == 123
