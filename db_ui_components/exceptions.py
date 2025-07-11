"""
カスタム例外クラス

コンポーネントライブラリで使用するカスタム例外を定義します。
"""


class ComponentError(Exception):
    """コンポーネント関連の基本例外クラス"""

    def __init__(self, message, **kwargs):
        super().__init__(message)
        self.message = message
        for key, value in kwargs.items():
            setattr(self, key, value)


class ValidationError(ComponentError):
    """バリデーションエラー"""

    pass


class ConfigurationError(ComponentError):
    """設定エラー"""

    pass


class RenderingError(ComponentError):
    """レンダリングエラー"""

    pass


class DataError(ComponentError):
    """データ関連エラー"""

    pass


class DependencyError(ComponentError):
    """依存関係エラー"""

    pass
