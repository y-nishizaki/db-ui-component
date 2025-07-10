"""
設定モジュールの最終テスト

このモジュールには、config.pyの未カバー部分のテストが含まれています。
"""

import pytest
import json
import tempfile
import os
from unittest.mock import Mock, patch
from db_ui_components.config import (
    ConfigStorage,
    ConfigConverter,
    ConfigValidator,
    ConfigManager,
    DashboardConfig,
    TableConfig,
    ChartConfig,
    FilterConfig,
    ComponentConfig,
    LayoutType,
    ChartType,
    FilterType,
)


class TestConfigFinalUncovered:
    """Configの最終未カバー部分のテスト"""

    def setup_method(self):
        """テスト前のセットアップ"""
        self.storage = ConfigStorage()
        self.converter = ConfigConverter()

    def test_load_configs_with_missing_default_configs(self):
        """default_configsが存在しない場合の読み込みテスト"""
        # 一時ファイルを作成
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"configs": {}}, f)
            filename = f.name

        try:
            # エラーが発生しないことを確認
            self.storage.load_configs(filename, self.converter)
        finally:
            if os.path.exists(filename):
                os.unlink(filename)

    def test_load_configs_with_missing_configs(self):
        """configsが存在しない場合の読み込みテスト"""
        # 一時ファイルを作成
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"default_configs": {}}, f)
            filename = f.name

        try:
            # エラーが発生しないことを確認
            self.storage.load_configs(filename, self.converter)
        finally:
            if os.path.exists(filename):
                os.unlink(filename)

    def test_load_configs_with_invalid_component_type(self):
        """無効なコンポーネントタイプでの読み込みテスト"""
        # 一時ファイルを作成
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(
                {
                    "default_configs": {"invalid_type": {"title": "test"}},
                    "configs": {"invalid_type_custom": {"title": "test"}},
                },
                f,
            )
            filename = f.name

        try:
            # エラーが発生しないことを確認
            self.storage.load_configs(filename, self.converter)
        finally:
            if os.path.exists(filename):
                os.unlink(filename)

    def test_validate_config_with_unknown_type(self):
        """未知のタイプでの設定検証テスト"""
        manager = ConfigManager()
        config = ComponentConfig()

        # 未知のタイプではデフォルトの検証が使用されることを確認
        result = manager._validate_config("unknown_type", config)
        assert result is True

    def test_validate_config_with_invalid_table_config(self):
        """無効なテーブル設定での検証テスト"""
        manager = ConfigManager()
        config = TableConfig(page_size=0)  # 無効なページサイズ

        with pytest.raises(ValueError):
            manager.set_config("table", config)

    def test_validate_config_with_invalid_filter_config(self):
        """無効なフィルター設定での検証テスト"""
        manager = ConfigManager()
        config = FilterConfig(column="")  # 空の列

        with pytest.raises(ValueError):
            manager.set_config("filter", config)

    def test_validate_config_with_invalid_component_config(self):
        """無効なコンポーネント設定での検証テスト"""
        manager = ConfigManager()
        config = ComponentConfig(height=-10)  # 負の高さ

        with pytest.raises(ValueError):
            manager.set_config("dashboard", config)

    def test_save_configs_with_non_dict_objects(self):
        """辞書以外のオブジェクトでの保存テスト"""

        # to_dictメソッドを持たないオブジェクトを作成
        class NonDictObject:
            pass

        obj = NonDictObject()
        self.storage.set_config("test", obj)

        # 一時ファイルに保存
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            filename = f.name

        try:
            self.storage.save_configs(filename)

            # ファイルが作成されたことを確認
            assert os.path.exists(filename)

            # ファイル内容を確認
            with open(filename, "r", encoding="utf-8") as f:
                content = json.load(f)

            assert "default_configs" in content
            assert "configs" in content
            assert "test" in content["default_configs"]

        finally:
            if os.path.exists(filename):
                os.unlink(filename)

    def test_load_configs_with_complex_nested_data(self):
        """複雑なネストしたデータでの読み込みテスト"""
        # 複雑な設定データを作成
        complex_data = {
            "default_configs": {
                "dashboard": {
                    "title": "テストダッシュボード",
                    "layout": "grid",
                    "grid_columns": 12,
                    "gap": 20,
                    "padding": 20,
                    "show_header": True,
                    "header_background": "#f8f9fa",
                    "header_padding": 20,
                    "container_background": "transparent",
                    "container_border_radius": 8,
                },
                "table": {
                    "enable_csv_download": True,
                    "sortable": True,
                    "searchable": True,
                    "page_size": 20,
                    "show_pagination": True,
                    "header_background": "#f8f9fa",
                    "row_hover": True,
                    "striped_rows": False,
                    "columns": ["Name", "Age", "City"],
                    "column_widths": {"Name": 200, "Age": 100, "City": 150},
                },
            },
            "configs": {
                "dashboard_custom": {
                    "title": "カスタムダッシュボード",
                    "layout": "flex",
                    "grid_columns": 6,
                },
                "table_custom": {"page_size": 25, "enable_csv_download": False},
            },
        }

        # 一時ファイルに保存
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(complex_data, f)
            filename = f.name

        try:
            # 読み込みを実行
            self.storage.load_configs(filename, self.converter)

            # 設定が正しく読み込まれたことを確認
            dashboard_config = self.storage.get_config("dashboard")
            table_config = self.storage.get_config("table")
            custom_dashboard = self.storage.get_config("dashboard", "custom")
            custom_table = self.storage.get_config("table", "custom")

            assert dashboard_config is not None
            assert table_config is not None
            assert custom_dashboard is not None
            assert custom_table is not None

        finally:
            if os.path.exists(filename):
                os.unlink(filename)

    def test_config_converter_with_custom_class(self):
        """カスタムクラスでの設定変換テスト"""

        # カスタム設定クラスを作成
        class CustomConfig(ComponentConfig):
            custom_field: str = "default"

        # カスタムクラスを登録
        self.converter.register_config_class("custom", CustomConfig)

        # 登録されたクラスを取得
        result = self.converter.get_config_class("custom")
        assert result == CustomConfig

        # 無効なタイプでの取得
        result = self.converter.get_config_class("nonexistent")
        assert result is None

    def test_config_validator_edge_cases(self):
        """設定検証のエッジケーステスト"""
        validator = ConfigValidator()

        # 境界値でのテスト
        config = ComponentConfig(height=0)  # 境界値
        assert validator.validate_component_config(config) is True

        config = ComponentConfig(width=0)  # 境界値
        assert validator.validate_component_config(config) is True

        config = ComponentConfig(padding=0)  # 境界値
        assert validator.validate_component_config(config) is True

        config = ComponentConfig(margin=0)  # 境界値
        assert validator.validate_component_config(config) is True

        # 負の値でのテスト
        config = ComponentConfig(height=-1)
        assert validator.validate_component_config(config) is False

        config = ComponentConfig(width=-1)
        assert validator.validate_component_config(config) is False

        config = ComponentConfig(padding=-1)
        assert validator.validate_component_config(config) is False

        config = ComponentConfig(margin=-1)
        assert validator.validate_component_config(config) is False

    def test_table_config_validation_edge_cases(self):
        """テーブル設定検証のエッジケーステスト"""
        validator = ConfigValidator()

        # 境界値でのテスト
        config = TableConfig(page_size=1)  # 最小値
        assert validator.validate_table_config(config) is True

        # 無効な値でのテスト
        config = TableConfig(page_size=0)
        assert validator.validate_table_config(config) is False

        config = TableConfig(page_size=-1)
        assert validator.validate_table_config(config) is False

    def test_filter_config_validation_edge_cases(self):
        """フィルター設定検証のエッジケーステスト"""
        validator = ConfigValidator()

        # 空文字列でのテスト
        config = FilterConfig(column="")
        assert validator.validate_filter_config(config) is False

        # None値でのテスト
        config = FilterConfig(column=None)
        assert validator.validate_filter_config(config) is False

        # 有効な値でのテスト
        config = FilterConfig(column="test_column")
        assert validator.validate_filter_config(config) is True

    def test_chart_config_validation_edge_cases(self):
        """チャート設定検証のエッジケーステスト"""
        validator = ConfigValidator()

        # 正常な設定でのテスト
        config = ChartConfig()
        assert validator.validate_chart_config(config) is True

        # 無効な基底設定でのテスト
        config = ChartConfig(height=-10)
        assert validator.validate_chart_config(config) is False

    def test_config_manager_integration_edge_cases(self):
        """設定マネージャー統合のエッジケーステスト"""
        manager = ConfigManager()

        # None値での設定テスト
        manager.set_config("test", None)
        result = manager.get_config("test")
        assert result is None

        # 空文字列での設定テスト
        manager.set_config("test", "")
        result = manager.get_config("test")
        assert result == ""

        # 数値での設定テスト
        manager.set_config("test", 42)
        result = manager.get_config("test")
        assert result == 42

        # リストでの設定テスト
        manager.set_config("test", [1, 2, 3])
        result = manager.get_config("test")
        assert result == [1, 2, 3]

    def test_config_storage_edge_cases(self):
        """設定ストレージのエッジケーステスト"""
        # 空の設定でのテスト
        self.storage.set_config("empty", {})
        result = self.storage.get_config("empty")
        assert result == {}

        # ネストした辞書でのテスト
        nested_config = {"level1": {"level2": {"level3": "value"}}}
        self.storage.set_config("nested", nested_config)
        result = self.storage.get_config("nested")
        assert result == nested_config

        # リストでのテスト
        list_config = [1, 2, 3, {"nested": "value"}]
        self.storage.set_config("list", list_config)
        result = self.storage.get_config("list")
        assert result == list_config

    def test_config_converter_edge_cases(self):
        """設定変換器のエッジケーステスト"""
        # 空の辞書でのテスト
        empty_dict = {}
        self.converter.register_config_class("empty", empty_dict)
        result = self.converter.get_config_class("empty")
        assert result == empty_dict

        # None値でのテスト
        self.converter.register_config_class("none", None)
        result = self.converter.get_config_class("none")
        assert result is None

        # 文字列でのテスト
        self.converter.register_config_class("string", "test")
        result = self.converter.get_config_class("string")
        assert result == "test"

    def test_complete_workflow_with_edge_cases(self):
        """エッジケースを含む完全なワークフローテスト"""
        manager = ConfigManager()

        # 1. 様々な型の設定を登録
        manager.set_config("string", "test_string")
        manager.set_config("number", 42)
        manager.set_config("boolean", True)
        manager.set_config("list", [1, 2, 3])
        manager.set_config("dict", {"key": "value"})
        manager.set_config("none", None)

        # 2. 設定を取得して検証
        assert manager.get_config("string") == "test_string"
        assert manager.get_config("number") == 42
        assert manager.get_config("boolean") is True
        assert manager.get_config("list") == [1, 2, 3]
        assert manager.get_config("dict") == {"key": "value"}
        assert manager.get_config("none") is None

        # 3. 存在しない設定の取得
        assert manager.get_config("nonexistent") is None
        assert manager.get_config("nonexistent", "custom_id") is None

        # 4. 設定をファイルに保存
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            filename = f.name

        try:
            manager.save_configs(filename)

            # 5. 新しいマネージャーで設定を読み込み
            new_manager = ConfigManager()
            new_manager.load_configs(filename)

            # 6. 読み込まれた設定を検証
            assert new_manager.get_config("string") == "test_string"
            assert new_manager.get_config("number") == 42
            assert new_manager.get_config("boolean") is True
            assert new_manager.get_config("list") == [1, 2, 3]
            assert new_manager.get_config("dict") == {"key": "value"}
            assert new_manager.get_config("none") is None

        finally:
            if os.path.exists(filename):
                os.unlink(filename)
