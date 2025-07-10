"""
設定管理

コンポーネントの設定を管理するクラスを定義します。
"""

from typing import Dict, Any, Optional, List
import json
from dataclasses import dataclass, field
from enum import Enum


class LayoutType(Enum):
    """レイアウトタイプの列挙"""

    GRID = "grid"
    FLEX = "flex"
    CUSTOM = "custom"


class ChartType(Enum):
    """チャートタイプの列挙"""

    LINE = "line"
    BAR = "bar"
    PIE = "pie"
    SCATTER = "scatter"
    HEATMAP = "heatmap"


class FilterType(Enum):
    """フィルタータイプの列挙"""

    DATE = "date"
    DROPDOWN = "dropdown"
    MULTISELECT = "multiselect"
    TEXT = "text"


@dataclass
class ComponentConfig:
    """コンポーネント設定のデータクラス"""

    # 共通設定
    component_id: Optional[str] = None
    title: Optional[str] = None
    height: int = 400
    width: Optional[int] = None

    # スタイル設定
    background_color: str = "white"
    border_color: str = "#ddd"
    border_radius: int = 8
    padding: int = 16
    margin: int = 10

    # レスポンシブ設定
    responsive: bool = True
    min_width: Optional[int] = None
    max_width: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """辞書形式で取得"""
        return {
            "component_id": self.component_id,
            "title": self.title,
            "height": self.height,
            "width": self.width,
            "background_color": self.background_color,
            "border_color": self.border_color,
            "border_radius": self.border_radius,
            "padding": self.padding,
            "margin": self.margin,
            "responsive": self.responsive,
            "min_width": self.min_width,
            "max_width": self.max_width,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ComponentConfig":
        """辞書から作成"""
        return cls(**data)


@dataclass
class DashboardConfig(ComponentConfig):
    """ダッシュボード設定のデータクラス"""

    title: Optional[str] = None
    layout: LayoutType = LayoutType.GRID
    grid_columns: int = 12
    gap: int = 20
    padding: int = 20

    # ヘッダー設定
    show_header: bool = True
    header_background: str = "#f8f9fa"
    header_padding: int = 20

    # コンテナ設定
    container_background: str = "transparent"
    container_border_radius: int = 8

    def to_dict(self) -> Dict[str, Any]:
        """辞書形式で取得"""
        base_dict = super().to_dict()
        base_dict.update(
            {
                "title": self.title,
                "layout": self.layout.value,
                "grid_columns": self.grid_columns,
                "gap": self.gap,
                "padding": self.padding,
                "show_header": self.show_header,
                "header_background": self.header_background,
                "header_padding": self.header_padding,
                "container_background": self.container_background,
                "container_border_radius": self.container_border_radius,
            }
        )
        return base_dict

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DashboardConfig":
        """辞書から作成"""
        if "layout" in data and isinstance(data["layout"], str):
            data["layout"] = LayoutType(data["layout"])
        return cls(**data)


@dataclass
class TableConfig(ComponentConfig):
    """テーブル設定のデータクラス"""

    enable_csv_download: bool = True
    sortable: bool = True
    searchable: bool = True
    page_size: int = 10
    show_pagination: bool = True

    # テーブルスタイル
    header_background: str = "#f8f9fa"
    row_hover: bool = True
    striped_rows: bool = False

    # 列設定
    columns: Optional[List[str]] = None
    column_widths: Optional[Dict[str, int]] = None

    def to_dict(self) -> Dict[str, Any]:
        """辞書形式で取得"""
        base_dict = super().to_dict()
        base_dict.update(
            {
                "enable_csv_download": self.enable_csv_download,
                "sortable": self.sortable,
                "searchable": self.searchable,
                "page_size": self.page_size,
                "show_pagination": self.show_pagination,
                "header_background": self.header_background,
                "row_hover": self.row_hover,
                "striped_rows": self.striped_rows,
                "columns": self.columns,
                "column_widths": self.column_widths,
            }
        )
        return base_dict


@dataclass
class ChartConfig(ComponentConfig):
    """チャート設定のデータクラス"""

    chart_type: ChartType = ChartType.LINE
    x_column: Optional[str] = None
    y_column: Optional[str] = None

    # チャートスタイル
    show_legend: bool = True
    show_grid: bool = True
    color_scheme: str = "plotly"

    # インタラクション設定
    enable_zoom: bool = True
    enable_pan: bool = True
    enable_hover: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """辞書形式で取得"""
        base_dict = super().to_dict()
        base_dict.update(
            {
                "chart_type": self.chart_type.value,
                "x_column": self.x_column,
                "y_column": self.y_column,
                "show_legend": self.show_legend,
                "show_grid": self.show_grid,
                "color_scheme": self.color_scheme,
                "enable_zoom": self.enable_zoom,
                "enable_pan": self.enable_pan,
                "enable_hover": self.enable_hover,
            }
        )
        return base_dict


@dataclass
class FilterConfig(ComponentConfig):
    """フィルター設定のデータクラス"""

    filter_type: FilterType = FilterType.DROPDOWN
    column: str = ""
    options: List[Any] = field(default_factory=list)
    placeholder: Optional[str] = None

    # フィルター固有設定
    allow_multiple: bool = False
    allow_clear: bool = True
    searchable: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """辞書形式で取得"""
        base_dict = super().to_dict()
        base_dict.update(
            {
                "filter_type": self.filter_type.value,
                "column": self.column,
                "options": self.options,
                "placeholder": self.placeholder,
                "allow_multiple": self.allow_multiple,
                "allow_clear": self.allow_clear,
                "searchable": self.searchable,
            }
        )
        return base_dict


class ConfigStorage:
    """設定ストレージクラス"""

    def __init__(self):
        self._configs: Dict[str, Any] = {}
        self._default_configs: Dict[str, Any] = {}

    def save_configs(self, filename: str) -> None:
        """設定をファイルに保存"""
        configs_dict = {
            "default_configs": {
                k: v.to_dict() if hasattr(v, "to_dict") else v
                for k, v in self._default_configs.items()
            },
            "configs": {
                k: v.to_dict() if hasattr(v, "to_dict") else v
                for k, v in self._configs.items()
            },
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(configs_dict, f, indent=2, ensure_ascii=False)

    def load_configs(self, filename: str, config_converter: "ConfigConverter") -> None:
        """設定をファイルから読み込み"""
        with open(filename, "r", encoding="utf-8") as f:
            configs_dict = json.load(f)

        # デフォルト設定の復元
        for component_type, config_data in configs_dict.get(
            "default_configs", {}
        ).items():
            config_class = config_converter.get_config_class(component_type)
            if config_class and hasattr(config_class, 'from_dict'):
                self._default_configs[component_type] = config_class.from_dict(
                    config_data
                )

        # 個別設定の復元
        for config_key, config_data in configs_dict.get("configs", {}).items():
            component_type = config_key.split("_")[0]
            config_class = config_converter.get_config_class(component_type)
            if config_class and hasattr(config_class, 'from_dict'):
                self._configs[config_key] = config_class.from_dict(config_data)

    def get_config(self, component_type: str, config_id: Optional[str] = None) -> Any:
        """設定を取得"""
        if config_id is None:
            return self._default_configs.get(component_type)

        key = f"{component_type}_{config_id}"
        return self._configs.get(key, self._default_configs.get(component_type))

    def set_config(
        self, component_type: str, config: Any, config_id: Optional[str] = None
    ) -> None:
        """設定を設定"""
        if config_id is None:
            self._default_configs[component_type] = config
        else:
            key = f"{component_type}_{config_id}"
            self._configs[key] = config


class ConfigConverter:
    """設定変換クラス"""

    def __init__(self):
        self._config_classes = {
            "dashboard": DashboardConfig,
            "table": TableConfig,
            "chart": ChartConfig,
            "filter": FilterConfig,
        }

    def get_config_class(self, component_type: str) -> Optional[type]:
        """設定クラスを取得"""
        return self._config_classes.get(component_type)

    def register_config_class(self, component_type: str, config_class: type) -> None:
        """設定クラスを登録"""
        self._config_classes[component_type] = config_class


class ConfigValidator:
    """設定検証クラス"""

    @staticmethod
    def validate_component_config(config: ComponentConfig) -> bool:
        """コンポーネント設定を検証"""
        if config.height < 0:
            return False
        if config.width is not None and config.width < 0:
            return False
        if config.padding < 0:
            return False
        if config.margin < 0:
            return False
        return True

    @staticmethod
    def validate_table_config(config: TableConfig) -> bool:
        """テーブル設定を検証"""
        if not ConfigValidator.validate_component_config(config):
            return False
        if config.page_size < 1:
            return False
        return True

    @staticmethod
    def validate_chart_config(config: ChartConfig) -> bool:
        """チャート設定を検証"""
        if not ConfigValidator.validate_component_config(config):
            return False
        return True

    @staticmethod
    def validate_filter_config(config: FilterConfig) -> bool:
        """フィルター設定を検証"""
        if not ConfigValidator.validate_component_config(config):
            return False
        if not config.column:
            return False
        return True


class ConfigManager:
    """設定管理クラス"""

    def __init__(self):
        """初期化"""
        self.storage = ConfigStorage()
        self.converter = ConfigConverter()
        self.validator = ConfigValidator()

    def register_default_config(self, component_type: str, config: Any) -> None:
        """
        デフォルト設定を登録

        Args:
            component_type: コンポーネントタイプ
            config: 設定オブジェクト
        """
        self.storage.set_config(component_type, config)

    def get_config(self, component_type: str, config_id: Optional[str] = None) -> Any:
        """
        設定を取得

        Args:
            component_type: コンポーネントタイプ
            config_id: 設定ID（Noneの場合はデフォルト設定）

        Returns:
            設定オブジェクト
        """
        return self.storage.get_config(component_type, config_id)

    def set_config(
        self, component_type: str, config: Any, config_id: Optional[str] = None
    ) -> None:
        """
        設定を設定

        Args:
            component_type: コンポーネントタイプ
            config: 設定オブジェクト
            config_id: 設定ID
        """
        # 設定を検証
        if not self._validate_config(component_type, config):
            raise ValueError(f"Invalid config for component type: {component_type}")

        self.storage.set_config(component_type, config, config_id)

    def save_configs(self, filename: str) -> None:
        """
        設定をファイルに保存

        Args:
            filename: ファイル名
        """
        self.storage.save_configs(filename)

    def load_configs(self, filename: str) -> None:
        """
        設定をファイルから読み込み

        Args:
            filename: ファイル名
        """
        self.storage.load_configs(filename, self.converter)

    def _validate_config(self, component_type: str, config: Any) -> bool:
        """設定を検証"""
        if component_type == "table":
            return bool(self.validator.validate_table_config(config))
        elif component_type == "chart":
            return bool(self.validator.validate_chart_config(config))
        elif component_type == "filter":
            return bool(self.validator.validate_filter_config(config))
        else:
            return bool(self.validator.validate_component_config(config))


# グローバル設定マネージャー
config_manager = ConfigManager()

# デフォルト設定の登録
config_manager.register_default_config("dashboard", DashboardConfig())
config_manager.register_default_config("table", TableConfig())
config_manager.register_default_config("chart", ChartConfig())
config_manager.register_default_config("filter", FilterConfig())
