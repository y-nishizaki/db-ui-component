"""
BaseComponentのテスト

BaseComponentクラスの全機能をテストします。
"""

import pytest
import uuid
from unittest.mock import patch, MagicMock
from db_ui_components.base_component import BaseComponent


class TestBaseComponent(BaseComponent):
    """テスト用のBaseComponent実装"""

    def render(self) -> str:
        """テスト用のレンダリング実装"""
        return f"<div id='{self.component_id}'>Test Component</div>"


class TestBaseComponentInitialization:
    """BaseComponentの初期化テスト"""

    def test_init_with_component_id(self):
        """コンポーネントIDを指定して初期化"""
        component = TestBaseComponent(component_id="test-id")
        assert component.component_id == "test-id"
        assert component.kwargs == {}
        assert component._event_handlers == {}
        assert component._state == {}
        assert component._config == {}

    def test_init_without_component_id(self):
        """コンポーネントIDを指定せずに初期化"""
        with patch("uuid.uuid4") as mock_uuid:
            mock_uuid.return_value = "12345678"
            component = TestBaseComponent()
            assert component.component_id == "testbasecomponent-12345678"

    def test_init_with_kwargs(self):
        """キーワード引数で初期化"""
        component = TestBaseComponent(test_param="test_value", another_param=123)
        assert component.kwargs == {"test_param": "test_value", "another_param": 123}


class TestBaseComponentEventHandling:
    """イベントハンドリングのテスト"""

    def setup_method(self):
        """テスト前の準備"""
        self.component = TestBaseComponent()

    def test_add_event_handler(self):
        """イベントハンドラーの追加"""
        handler = MagicMock()
        self.component.add_event_handler("click", handler)
        assert "click" in self.component._event_handlers
        assert handler in self.component._event_handlers["click"]

    def test_add_multiple_event_handlers(self):
        """複数のイベントハンドラーの追加"""
        handler1 = MagicMock()
        handler2 = MagicMock()
        self.component.add_event_handler("click", handler1)
        self.component.add_event_handler("click", handler2)
        assert len(self.component._event_handlers["click"]) == 2
        assert handler1 in self.component._event_handlers["click"]
        assert handler2 in self.component._event_handlers["click"]

    def test_remove_event_handler(self):
        """イベントハンドラーの削除"""
        handler = MagicMock()
        self.component.add_event_handler("click", handler)
        self.component.remove_event_handler("click", handler)
        assert "click" not in self.component._event_handlers

    def test_remove_nonexistent_event_handler(self):
        """存在しないイベントハンドラーの削除"""
        handler = MagicMock()
        # エラーが発生しないことを確認
        self.component.remove_event_handler("click", handler)

    def test_trigger_event(self):
        """イベントのトリガー"""
        handler = MagicMock()
        self.component.add_event_handler("click", handler)
        self.component.trigger_event("click", x=1, y=2)
        handler.assert_called_once_with(x=1, y=2)

    def test_trigger_event_with_exception(self):
        """例外が発生するイベントハンドラーのトリガー"""

        def error_handler(**kwargs):
            raise ValueError("Test error")

        self.component.add_event_handler("click", error_handler)
        # 例外が発生しても処理が続行されることを確認
        self.component.trigger_event("click")

    def test_trigger_nonexistent_event(self):
        """存在しないイベントのトリガー"""
        # エラーが発生しないことを確認
        self.component.trigger_event("nonexistent")


class TestBaseComponentStateManagement:
    """状態管理のテスト"""

    def setup_method(self):
        """テスト前の準備"""
        self.component = TestBaseComponent()

    def test_set_and_get_state(self):
        """状態の設定と取得"""
        self.component.set_state("test_key", "test_value")
        assert self.component.get_state("test_key") == "test_value"

    def test_get_state_with_default(self):
        """デフォルト値付きの状態取得"""
        assert self.component.get_state("nonexistent", "default") == "default"

    def test_get_state_without_default(self):
        """デフォルト値なしの状態取得"""
        assert self.component.get_state("nonexistent") is None


class TestBaseComponentConfigManagement:
    """設定管理のテスト"""

    def setup_method(self):
        """テスト前の準備"""
        self.component = TestBaseComponent()

    def test_set_and_get_config(self):
        """設定の設定と取得"""
        self.component.set_config("test_key", "test_value")
        assert self.component.get_config("test_key") == "test_value"

    def test_get_config_with_default(self):
        """デフォルト値付きの設定取得"""
        assert self.component.get_config("nonexistent", "default") == "default"

    def test_get_config_without_default(self):
        """デフォルト値なしの設定取得"""
        assert self.component.get_config("nonexistent") is None


class TestBaseComponentSerialization:
    """シリアライゼーションのテスト"""

    def setup_method(self):
        """テスト前の準備"""
        self.component = TestBaseComponent(component_id="test-id")
        self.component.set_state("state_key", "state_value")
        self.component.set_config("config_key", "config_value")
        self.component.kwargs = {"kwarg_key": "kwarg_value"}

    def test_to_dict(self):
        """辞書形式への変換"""
        result = self.component.to_dict()
        expected = {
            "component_id": "test-id",
            "class_name": "TestBaseComponent",
            "config": {"config_key": "config_value"},
            "state": {"state_key": "state_value"},
            "kwargs": {"kwarg_key": "kwarg_value"},
        }
        assert result == expected

    def test_from_dict(self):
        """辞書形式からの復元"""
        data = {
            "config": {"new_config": "new_value"},
            "state": {"new_state": "new_value"},
            "kwargs": {"new_kwarg": "new_value"},
        }
        self.component.from_dict(data)
        assert self.component.get_config("new_config") == "new_value"
        assert self.component.get_state("new_state") == "new_value"
        assert self.component.kwargs["new_kwarg"] == "new_value"


class TestBaseComponentValidation:
    """バリデーションのテスト"""

    def setup_method(self):
        """テスト前の準備"""
        self.component = TestBaseComponent()

    def test_validate(self):
        """バリデーションのテスト"""
        assert self.component.validate() is True

    def test_get_required_dependencies(self):
        """必要な依存関係の取得"""
        dependencies = self.component.get_required_dependencies()
        assert isinstance(dependencies, list)
        assert len(dependencies) == 0


class TestBaseComponentRender:
    """レンダリングのテスト"""

    def setup_method(self):
        """テスト前の準備"""
        self.component = TestBaseComponent(component_id="test-id")

    def test_render(self):
        """レンダリングのテスト"""
        result = self.component.render()
        assert result == "<div id='test-id'>Test Component</div>"


class TestBaseComponentIDGeneration:
    """ID生成のテスト"""

    def test_generate_id(self):
        """ID生成のテスト"""
        component = TestBaseComponent()
        # IDが生成されることを確認
        assert component.component_id is not None
        assert isinstance(component.component_id, str)
        assert len(component.component_id) > 0

    def test_generate_id_format(self):
        """ID生成の形式テスト"""
        with patch("uuid.uuid4") as mock_uuid:
            mock_uuid.return_value = "12345678"
            component = TestBaseComponent()
            assert component.component_id == "testbasecomponent-12345678"
