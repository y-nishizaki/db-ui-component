"""
ベースコンポーネント

すべてのUIコンポーネントの基底クラスを定義します。
共通の機能とインターフェースを提供します。
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Callable


class BaseComponent(ABC):
    """
    すべてのUIコンポーネントの基底クラス

    共通機能:
    - レンダリングインターフェース
    - イベントハンドラー管理
    - 設定管理
    - 状態管理
    """

    def __init__(self, component_id: Optional[str] = None, **kwargs):
        """
        初期化

        Args:
            component_id: コンポーネントの一意識別子
            **kwargs: その他のパラメータ
        """
        self.component_id = component_id or self._generate_id()
        self.kwargs = kwargs
        self._event_handlers: Dict[str, List[Callable]] = {}
        self._state: Dict[str, Any] = {}
        self._config: Dict[str, Any] = {}

    def _generate_id(self) -> str:
        """コンポーネントIDを生成"""
        import uuid

        return f"{self.__class__.__name__.lower()}-{str(uuid.uuid4())[:8]}"

    @abstractmethod
    def render(self) -> str:
        """
        コンポーネントをHTMLとしてレンダリング

        Returns:
            HTML文字列
        """
        pass

    def add_event_handler(self, event_type: str, handler: Callable) -> None:
        """
        イベントハンドラーを追加

        Args:
            event_type: イベントタイプ
            handler: イベントハンドラー関数
        """
        if event_type not in self._event_handlers:
            self._event_handlers[event_type] = []
        self._event_handlers[event_type].append(handler)

    def remove_event_handler(self, event_type: str, handler: Callable) -> None:
        """
        イベントハンドラーを削除

        Args:
            event_type: イベントタイプ
            handler: 削除するイベントハンドラー関数
        """
        if event_type in self._event_handlers:
            self._event_handlers[event_type] = [
                h for h in self._event_handlers[event_type] if h != handler
            ]

    def trigger_event(self, event_type: str, **kwargs) -> None:
        """
        イベントをトリガー

        Args:
            event_type: イベントタイプ
            **kwargs: イベントパラメータ
        """
        if event_type in self._event_handlers:
            for handler in self._event_handlers[event_type]:
                try:
                    handler(**kwargs)
                except Exception as e:
                    print(f"Error in event handler: {e}")

    def set_state(self, key: str, value: Any) -> None:
        """
        状態を設定

        Args:
            key: 状態キー
            value: 状態値
        """
        self._state[key] = value

    def get_state(self, key: str, default: Any = None) -> Any:
        """
        状態を取得

        Args:
            key: 状態キー
            default: デフォルト値

        Returns:
            状態値
        """
        return self._state.get(key, default)

    def set_config(self, key: str, value: Any) -> None:
        """
        設定を設定

        Args:
            key: 設定キー
            value: 設定値
        """
        self._config[key] = value

    def get_config(self, key: str, default: Any = None) -> Any:
        """
        設定を取得

        Args:
            key: 設定キー
            default: デフォルト値

        Returns:
            設定値
        """
        return self._config.get(key, default)

    def to_dict(self) -> Dict[str, Any]:
        """
        コンポーネントの設定を辞書として取得

        Returns:
            設定辞書
        """
        return {
            "component_id": self.component_id,
            "class_name": self.__class__.__name__,
            "config": self._config.copy(),
            "state": self._state.copy(),
            "kwargs": self.kwargs.copy(),
        }

    def from_dict(self, data: Dict[str, Any]) -> None:
        """
        辞書からコンポーネントを復元

        Args:
            data: 設定辞書
        """
        if "config" in data:
            self._config.update(data["config"])
        if "state" in data:
            self._state.update(data["state"])
        if "kwargs" in data:
            self.kwargs.update(data["kwargs"])

    def validate(self) -> bool:
        """
        コンポーネントの妥当性を検証

        Returns:
            妥当性の結果
        """
        return True

    def get_required_dependencies(self) -> List[str]:
        """
        必要な依存関係を取得

        Returns:
            依存関係のリスト
        """
        return []
