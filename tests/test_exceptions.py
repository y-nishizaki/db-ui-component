"""
例外クラスのテスト

カスタム例外クラスの全機能をテストします。
"""

import pytest
from db_ui_components.exceptions import (
    ComponentError,
    ValidationError,
    ConfigurationError,
    RenderingError,
    DataError,
    DependencyError,
)


class TestComponentError:
    """ComponentErrorのテスト"""

    def test_basic_exception(self):
        """基本的な例外のテスト"""
        error = ComponentError("Test error")
        assert str(error) == "Test error"
        assert isinstance(error, Exception)

    def test_exception_with_details(self):
        """詳細情報付きの例外のテスト"""
        error = ComponentError("Test error", details={"key": "value"})
        assert str(error) == "Test error"

    def test_exception_inheritance(self):
        """継承関係のテスト"""
        error = ComponentError("Test error")
        assert isinstance(error, Exception)
        assert isinstance(error, ComponentError)


class TestValidationError:
    """ValidationErrorのテスト"""

    def test_basic_validation_error(self):
        """基本的なバリデーションエラーのテスト"""
        error = ValidationError("Validation failed")
        assert str(error) == "Validation failed"
        assert isinstance(error, ComponentError)
        assert isinstance(error, ValidationError)

    def test_validation_error_with_field(self):
        """フィールド情報付きのバリデーションエラーのテスト"""
        error = ValidationError("Invalid field", field="test_field")
        assert str(error) == "Invalid field"

    def test_validation_error_inheritance(self):
        """継承関係のテスト"""
        error = ValidationError("Test error")
        assert isinstance(error, Exception)
        assert isinstance(error, ComponentError)
        assert isinstance(error, ValidationError)


class TestConfigurationError:
    """ConfigurationErrorのテスト"""

    def test_basic_configuration_error(self):
        """基本的な設定エラーのテスト"""
        error = ConfigurationError("Configuration error")
        assert str(error) == "Configuration error"
        assert isinstance(error, ComponentError)
        assert isinstance(error, ConfigurationError)

    def test_configuration_error_with_config(self):
        """設定情報付きの設定エラーのテスト"""
        error = ConfigurationError("Invalid config", config={"key": "value"})
        assert str(error) == "Invalid config"

    def test_configuration_error_inheritance(self):
        """継承関係のテスト"""
        error = ConfigurationError("Test error")
        assert isinstance(error, Exception)
        assert isinstance(error, ComponentError)
        assert isinstance(error, ConfigurationError)


class TestRenderingError:
    """RenderingErrorのテスト"""

    def test_basic_rendering_error(self):
        """基本的なレンダリングエラーのテスト"""
        error = RenderingError("Rendering failed")
        assert str(error) == "Rendering failed"
        assert isinstance(error, ComponentError)
        assert isinstance(error, RenderingError)

    def test_rendering_error_with_component(self):
        """コンポーネント情報付きのレンダリングエラーのテスト"""
        error = RenderingError("Render failed", component="test_component")
        assert str(error) == "Render failed"

    def test_rendering_error_inheritance(self):
        """継承関係のテスト"""
        error = RenderingError("Test error")
        assert isinstance(error, Exception)
        assert isinstance(error, ComponentError)
        assert isinstance(error, RenderingError)


class TestDataError:
    """DataErrorのテスト"""

    def test_basic_data_error(self):
        """基本的なデータエラーのテスト"""
        error = DataError("Data error")
        assert str(error) == "Data error"
        assert isinstance(error, ComponentError)
        assert isinstance(error, DataError)

    def test_data_error_with_data_info(self):
        """データ情報付きのデータエラーのテスト"""
        error = DataError("Invalid data", data_type="test_data")
        assert str(error) == "Invalid data"

    def test_data_error_inheritance(self):
        """継承関係のテスト"""
        error = DataError("Test error")
        assert isinstance(error, Exception)
        assert isinstance(error, ComponentError)
        assert isinstance(error, DataError)


class TestDependencyError:
    """DependencyErrorのテスト"""

    def test_basic_dependency_error(self):
        """基本的な依存関係エラーのテスト"""
        error = DependencyError("Dependency error")
        assert str(error) == "Dependency error"
        assert isinstance(error, ComponentError)
        assert isinstance(error, DependencyError)

    def test_dependency_error_with_dependency(self):
        """依存関係情報付きの依存関係エラーのテスト"""
        error = DependencyError("Missing dependency", dependency="test_dep")
        assert str(error) == "Missing dependency"

    def test_dependency_error_inheritance(self):
        """継承関係のテスト"""
        error = DependencyError("Test error")
        assert isinstance(error, Exception)
        assert isinstance(error, ComponentError)
        assert isinstance(error, DependencyError)


class TestExceptionHierarchy:
    """例外階層のテスト"""

    def test_exception_hierarchy(self):
        """例外階層の確認"""
        # すべての例外がComponentErrorを継承していることを確認
        validation_error = ValidationError("test")
        config_error = ConfigurationError("test")
        rendering_error = RenderingError("test")
        data_error = DataError("test")
        dependency_error = DependencyError("test")

        assert isinstance(validation_error, ComponentError)
        assert isinstance(config_error, ComponentError)
        assert isinstance(rendering_error, ComponentError)
        assert isinstance(data_error, ComponentError)
        assert isinstance(dependency_error, ComponentError)

    def test_exception_uniqueness(self):
        """例外の一意性の確認"""
        # 各例外が異なるクラスであることを確認
        validation_error = ValidationError("test")
        config_error = ConfigurationError("test")
        rendering_error = RenderingError("test")
        data_error = DataError("test")
        dependency_error = DependencyError("test")

        assert not isinstance(validation_error, type(config_error))
        assert not isinstance(validation_error, type(rendering_error))
        assert not isinstance(validation_error, type(data_error))
        assert not isinstance(validation_error, type(dependency_error))
        assert not isinstance(config_error, type(rendering_error))
        assert not isinstance(config_error, type(data_error))
        assert not isinstance(config_error, type(dependency_error))
        assert not isinstance(rendering_error, type(data_error))
        assert not isinstance(rendering_error, type(dependency_error))
        assert not isinstance(data_error, type(dependency_error))


class TestExceptionUsage:
    """例外使用例のテスト"""

    def test_validation_error_usage(self):
        """ValidationErrorの使用例"""
        try:
            raise ValidationError("Invalid input", field="username")
        except ValidationError as e:
            assert str(e) == "Invalid input"
        except Exception:
            assert False, "Should not catch other exceptions"

    def test_configuration_error_usage(self):
        """ConfigurationErrorの使用例"""
        try:
            raise ConfigurationError("Invalid configuration", config={"key": "value"})
        except ConfigurationError as e:
            assert str(e) == "Invalid configuration"
        except Exception:
            assert False, "Should not catch other exceptions"

    def test_rendering_error_usage(self):
        """RenderingErrorの使用例"""
        try:
            raise RenderingError("Failed to render component", component="chart")
        except RenderingError as e:
            assert str(e) == "Failed to render component"
        except Exception:
            assert False, "Should not catch other exceptions"

    def test_data_error_usage(self):
        """DataErrorの使用例"""
        try:
            raise DataError("Invalid data format", data_type="json")
        except DataError as e:
            assert str(e) == "Invalid data format"
        except Exception:
            assert False, "Should not catch other exceptions"

    def test_dependency_error_usage(self):
        """DependencyErrorの使用例"""
        try:
            raise DependencyError("Missing required dependency", dependency="plotly")
        except DependencyError as e:
            assert str(e) == "Missing required dependency"
        except Exception:
            assert False, "Should not catch other exceptions"
