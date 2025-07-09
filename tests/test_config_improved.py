"""
設定モジュールの改善されたテスト

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
    FilterType
)


class TestConfigStorageUncovered:
    """ConfigStorageの未カバー部分のテスト"""
    
    def setup_method(self):
        """テスト前のセットアップ"""
        self.storage = ConfigStorage()
        self.converter = ConfigConverter()
    
    def test_save_configs_with_complex_objects(self):
        """複雑なオブジェクトを含む設定保存テスト"""
        # 複雑な設定オブジェクトを作成
        dashboard_config = DashboardConfig(
            title="テストダッシュボード",
            layout=LayoutType.FLEX,
            grid_columns=6
        )
        
        table_config = TableConfig(
            enable_csv_download=True,
            sortable=True,
            page_size=20
        )
        
        self.storage.set_config("dashboard", dashboard_config)
        self.storage.set_config("table", table_config, "custom_id")
        
        # 一時ファイルに保存
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            filename = f.name
        
        try:
            self.storage.save_configs(filename)
            
            # ファイルが作成されたことを確認
            assert os.path.exists(filename)
            
            # ファイル内容を確認
            with open(filename, 'r', encoding='utf-8') as f:
                content = json.load(f)
            
            assert "default_configs" in content
            assert "configs" in content
            assert "dashboard" in content["default_configs"]
            assert "table_custom_id" in content["configs"]
            
        finally:
            # 一時ファイルを削除
            if os.path.exists(filename):
                os.unlink(filename)
    
    def test_load_configs_with_invalid_file(self):
        """無効なファイルからの設定読み込みテスト"""
        # 存在しないファイル
        with pytest.raises(FileNotFoundError):
            self.storage.load_configs("nonexistent_file.json", self.converter)
    
    def test_load_configs_with_invalid_json(self):
        """無効なJSONファイルからの設定読み込みテスト"""
        # 無効なJSONファイルを作成
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"invalid": json}')
            filename = f.name
        
        try:
            with pytest.raises(json.JSONDecodeError):
                self.storage.load_configs(filename, self.converter)
        finally:
            if os.path.exists(filename):
                os.unlink(filename)
    
    def test_get_config_with_nonexistent_id(self):
        """存在しないIDでの設定取得テスト"""
        # デフォルト設定を設定
        default_config = DashboardConfig(title="デフォルト")
        self.storage.set_config("dashboard", default_config)
        
        # 存在しないIDで取得
        result = self.storage.get_config("dashboard", "nonexistent_id")
        
        # デフォルト設定が返されることを確認
        assert result == default_config
    
    def test_set_config_with_none_value(self):
        """None値での設定テスト"""
        self.storage.set_config("test", None)
        result = self.storage.get_config("test")
        assert result is None


class TestConfigConverterUncovered:
    """ConfigConverterの未カバー部分のテスト"""
    
    def setup_method(self):
        """テスト前のセットアップ"""
        self.converter = ConfigConverter()
    
    def test_get_config_class_with_nonexistent_type(self):
        """存在しないタイプでの設定クラス取得テスト"""
        result = self.converter.get_config_class("nonexistent_type")
        assert result is None
    
    def test_register_config_class(self):
        """設定クラスの登録テスト"""
        # カスタム設定クラスを作成
        class CustomConfig(ComponentConfig):
            pass
        
        # 新しいタイプを登録
        self.converter.register_config_class("custom", CustomConfig)
        
        # 登録されたクラスを取得
        result = self.converter.get_config_class("custom")
        assert result == CustomConfig
    
    def test_register_config_class_overwrite(self):
        """設定クラスの上書き登録テスト"""
        # カスタム設定クラスを作成
        class CustomConfig(ComponentConfig):
            pass
        
        class AnotherCustomConfig(ComponentConfig):
            pass
        
        # 最初のクラスを登録
        self.converter.register_config_class("custom", CustomConfig)
        
        # 別のクラスで上書き
        self.converter.register_config_class("custom", AnotherCustomConfig)
        
        # 上書きされたクラスを取得
        result = self.converter.get_config_class("custom")
        assert result == AnotherCustomConfig


class TestConfigValidatorUncovered:
    """ConfigValidatorの未カバー部分のテスト"""
    
    def setup_method(self):
        """テスト前のセットアップ"""
        self.validator = ConfigValidator()
    
    def test_validate_component_config_with_negative_height(self):
        """負の高さでのコンポーネント設定検証テスト"""
        config = ComponentConfig(height=-10)
        result = self.validator.validate_component_config(config)
        assert result is False
    
    def test_validate_component_config_with_negative_width(self):
        """負の幅でのコンポーネント設定検証テスト"""
        config = ComponentConfig(width=-10)
        result = self.validator.validate_component_config(config)
        assert result is False
    
    def test_validate_component_config_with_negative_padding(self):
        """負のパディングでのコンポーネント設定検証テスト"""
        config = ComponentConfig(padding=-10)
        result = self.validator.validate_component_config(config)
        assert result is False
    
    def test_validate_component_config_with_negative_margin(self):
        """負のマージンでのコンポーネント設定検証テスト"""
        config = ComponentConfig(margin=-10)
        result = self.validator.validate_component_config(config)
        assert result is False
    
    def test_validate_table_config_with_invalid_page_size(self):
        """無効なページサイズでのテーブル設定検証テスト"""
        config = TableConfig(page_size=0)
        result = self.validator.validate_table_config(config)
        assert result is False
    
    def test_validate_filter_config_with_empty_column(self):
        """空の列でのフィルター設定検証テスト"""
        config = FilterConfig(column="")
        result = self.validator.validate_filter_config(config)
        assert result is False
    
    def test_validate_filter_config_with_none_column(self):
        """None列でのフィルター設定検証テスト"""
        config = FilterConfig(column=None)
        result = self.validator.validate_filter_config(config)
        assert result is False


class TestConfigManagerUncovered:
    """ConfigManagerの未カバー部分のテスト"""
    
    def setup_method(self):
        """テスト前のセットアップ"""
        self.manager = ConfigManager()
    
    def test_register_default_config(self):
        """デフォルト設定の登録テスト"""
        config = DashboardConfig(title="テスト")
        self.manager.register_default_config("dashboard", config)
        
        result = self.manager.get_config("dashboard")
        assert result == config
    
    def test_save_and_load_configs(self):
        """設定の保存と読み込みテスト"""
        # 設定を作成
        dashboard_config = DashboardConfig(title="テストダッシュボード")
        table_config = TableConfig(page_size=25)
        
        self.manager.register_default_config("dashboard", dashboard_config)
        self.manager.set_config("table", table_config, "custom_id")
        
        # 一時ファイルに保存
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            filename = f.name
        
        try:
            self.manager.save_configs(filename)
            
            # 新しいマネージャーを作成して読み込み
            new_manager = ConfigManager()
            new_manager.load_configs(filename)
            
            # 設定が正しく読み込まれたことを確認
            loaded_dashboard = new_manager.get_config("dashboard")
            loaded_table = new_manager.get_config("table", "custom_id")
            
            assert loaded_dashboard.title == "テストダッシュボード"
            assert loaded_table.page_size == 25
            
        finally:
            if os.path.exists(filename):
                os.unlink(filename)
    
    def test_get_config_class(self):
        """設定クラス取得テスト"""
        # 内部のconverterにアクセス
        result = self.manager.converter.get_config_class("dashboard")
        assert result == DashboardConfig
    
    def test_set_config_with_invalid_config(self):
        """無効な設定での設定テスト"""
        # 無効な設定を作成
        invalid_config = ComponentConfig(height=-10)
        
        with pytest.raises(ValueError):
            self.manager.set_config("dashboard", invalid_config)
    
    def test_validate_config_with_unknown_type(self):
        """未知のタイプでの設定検証テスト"""
        config = ComponentConfig()
        result = self.manager._validate_config("unknown_type", config)
        assert result is True  # デフォルトでTrueを返す


class TestConfigEdgeCases:
    """設定のエッジケーステスト"""
    
    def test_dashboard_config_with_enum_values(self):
        """列挙値でのダッシュボード設定テスト"""
        config = DashboardConfig(
            layout=LayoutType.CUSTOM,
            title="カスタムレイアウト"
        )
        
        # to_dictで列挙値が文字列に変換されることを確認
        config_dict = config.to_dict()
        assert config_dict["layout"] == "custom"
        
        # from_dictで文字列が列挙値に変換されることを確認
        restored_config = DashboardConfig.from_dict(config_dict)
        assert restored_config.layout == LayoutType.CUSTOM
    
    def test_chart_config_with_enum_values(self):
        """列挙値でのチャート設定テスト"""
        config = ChartConfig(
            chart_type=ChartType.PIE,
            x_column="category",
            y_column="value"
        )
        
        # to_dictで列挙値が文字列に変換されることを確認
        config_dict = config.to_dict()
        assert config_dict["chart_type"] == "pie"
        
        # from_dictで文字列が列挙値に変換されることを確認
        restored_config = ChartConfig.from_dict(config_dict)
        assert restored_config.chart_type == ChartType.PIE
    
    def test_filter_config_with_enum_values(self):
        """列挙値でのフィルター設定テスト"""
        config = FilterConfig(
            filter_type=FilterType.MULTISELECT,
            column="category",
            allow_multiple=True
        )
        
        # to_dictで列挙値が文字列に変換されることを確認
        config_dict = config.to_dict()
        assert config_dict["filter_type"] == "multiselect"
        
        # from_dictで文字列が列挙値に変換されることを確認
        restored_config = FilterConfig.from_dict(config_dict)
        assert restored_config.filter_type == FilterType.MULTISELECT
    
    def test_config_with_none_values(self):
        """None値での設定テスト"""
        config = ComponentConfig(
            component_id=None,
            title=None,
            width=None,
            min_width=None,
            max_width=None
        )
        
        config_dict = config.to_dict()
        restored_config = ComponentConfig.from_dict(config_dict)
        
        assert restored_config.component_id is None
        assert restored_config.title is None
        assert restored_config.width is None
        assert restored_config.min_width is None
        assert restored_config.max_width is None
    
    def test_table_config_with_complex_columns(self):
        """複雑な列設定でのテーブル設定テスト"""
        config = TableConfig(
            columns=["Name", "Age", "City"],
            column_widths={"Name": 200, "Age": 100, "City": 150}
        )
        
        config_dict = config.to_dict()
        restored_config = TableConfig.from_dict(config_dict)
        
        assert restored_config.columns == ["Name", "Age", "City"]
        assert restored_config.column_widths == {"Name": 200, "Age": 100, "City": 150}
    
    def test_filter_config_with_complex_options(self):
        """複雑なオプションでのフィルター設定テスト"""
        options = [
            {"label": "オプション1", "value": "opt1"},
            {"label": "オプション2", "value": "opt2"},
            {"label": "オプション3", "value": "opt3"}
        ]
        
        config = FilterConfig(
            filter_type=FilterType.DROPDOWN,
            column="category",
            options=options,
            placeholder="選択してください"
        )
        
        config_dict = config.to_dict()
        restored_config = FilterConfig.from_dict(config_dict)
        
        assert restored_config.options == options
        assert restored_config.placeholder == "選択してください"


class TestConfigIntegration:
    """設定の統合テスト"""
    
    def test_complete_config_workflow(self):
        """完全な設定ワークフローテスト"""
        manager = ConfigManager()
        
        # 1. デフォルト設定を登録
        dashboard_config = DashboardConfig(
            title="統合テストダッシュボード",
            layout=LayoutType.GRID,
            grid_columns=12
        )
        manager.register_default_config("dashboard", dashboard_config)
        
        # 2. 個別設定を設定
        table_config = TableConfig(
            page_size=15,
            enable_csv_download=True,
            sortable=True
        )
        manager.set_config("table", table_config, "custom_table")
        
        # 3. 設定を取得して検証
        retrieved_dashboard = manager.get_config("dashboard")
        retrieved_table = manager.get_config("table", "custom_table")
        
        assert retrieved_dashboard.title == "統合テストダッシュボード"
        assert retrieved_table.page_size == 15
        
        # 4. 設定をファイルに保存
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            filename = f.name
        
        try:
            manager.save_configs(filename)
            
            # 5. 新しいマネージャーで設定を読み込み
            new_manager = ConfigManager()
            new_manager.load_configs(filename)
            
            # 6. 読み込まれた設定を検証
            loaded_dashboard = new_manager.get_config("dashboard")
            loaded_table = new_manager.get_config("table", "custom_table")
            
            assert loaded_dashboard.title == "統合テストダッシュボード"
            assert loaded_table.page_size == 15
            
        finally:
            if os.path.exists(filename):
                os.unlink(filename)
    
    def test_multiple_config_types(self):
        """複数の設定タイプのテスト"""
        manager = ConfigManager()
        
        # 各タイプの設定を作成
        dashboard_config = DashboardConfig(title="ダッシュボード")
        table_config = TableConfig(page_size=20)
        chart_config = ChartConfig(chart_type=ChartType.BAR)
        filter_config = FilterConfig(column="category")
        
        # 設定を登録
        manager.register_default_config("dashboard", dashboard_config)
        manager.set_config("table", table_config, "table1")
        manager.set_config("chart", chart_config, "chart1")
        manager.set_config("filter", filter_config, "filter1")
        
        # すべての設定を取得して検証
        assert manager.get_config("dashboard").title == "ダッシュボード"
        assert manager.get_config("table", "table1").page_size == 20
        assert manager.get_config("chart", "chart1").chart_type == ChartType.BAR
        assert manager.get_config("filter", "filter1").column == "category"
    
    def test_config_validation_integration(self):
        """設定検証の統合テスト"""
        manager = ConfigManager()
        
        # 有効な設定
        valid_config = DashboardConfig(title="有効な設定")
        manager.set_config("dashboard", valid_config)
        
        # 無効な設定（負の高さ）
        invalid_config = DashboardConfig(height=-100)
        
        with pytest.raises(ValueError):
            manager.set_config("dashboard", invalid_config)
        
        # 元の有効な設定が保持されていることを確認
        retrieved_config = manager.get_config("dashboard")
        assert retrieved_config.title == "有効な設定"
        assert retrieved_config.height == 400  # デフォルト値