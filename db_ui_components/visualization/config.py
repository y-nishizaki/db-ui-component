"""
可視化コンポーネント設定管理

責任:
- 可視化コンポーネントの設定管理
- 設定の検証
- デフォルト値の提供
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class VisualizationConfig:
    """
    可視化コンポーネントの設定クラス

    責任: 設定の管理と検証
    """

    title: str = "Chart"
    height: int = 500
    width: Optional[int] = None
    background_color: str = "#ffffff"
    border_color: str = "#e0e0e0"
    border_width: int = 1
    margin: Dict[str, int] = field(
        default_factory=lambda: {"top": 50, "bottom": 50, "left": 50, "right": 50}
    )

    def to_dict(self) -> Dict[str, Any]:
        """
        設定を辞書形式で取得

        Returns:
            設定辞書
        """
        return {
            "title": self.title,
            "height": self.height,
            "width": self.width,
            "background_color": self.background_color,
            "border_color": self.border_color,
            "border_width": self.border_width,
            "margin": self.margin.copy(),
        }

    def validate(self) -> bool:
        """
        設定の妥当性を検証

        Returns:
            妥当性の結果
        """
        if self.height <= 0:
            return False
        if self.width is not None and self.width <= 0:
            return False
        if not all(
            key in ["top", "bottom", "left", "right"] for key in self.margin.keys()
        ):
            return False
        return True


@dataclass
class SankeyConfig(VisualizationConfig):
    """
    サンキーチャート専用設定
    """

    node_color: str = "#1f77b4"
    link_color: str = "#888888"
    font_size: int = 10

    def to_dict(self) -> Dict[str, Any]:
        base_dict = super().to_dict()
        base_dict.update(
            {
                "node_color": self.node_color,
                "link_color": self.link_color,
                "font_size": self.font_size,
            }
        )
        return base_dict


@dataclass
class HeatmapConfig(VisualizationConfig):
    """
    ヒートマップ専用設定
    """

    color_scale: str = "Viridis"
    show_colorbar: bool = True
    colorbar_title: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        base_dict = super().to_dict()
        base_dict.update(
            {
                "color_scale": self.color_scale,
                "show_colorbar": self.show_colorbar,
                "colorbar_title": self.colorbar_title,
            }
        )
        return base_dict


@dataclass
class NetworkConfig(VisualizationConfig):
    """
    ネットワークグラフ専用設定
    """

    node_size: int = 20
    node_color: str = "#1f77b4"
    edge_color: str = "#888888"
    edge_width: int = 1
    show_legend: bool = False

    def to_dict(self) -> Dict[str, Any]:
        base_dict = super().to_dict()
        base_dict.update(
            {
                "node_size": self.node_size,
                "node_color": self.node_color,
                "edge_color": self.edge_color,
                "edge_width": self.edge_width,
                "show_legend": self.show_legend,
            }
        )
        return base_dict


@dataclass
class BubbleConfig(VisualizationConfig):
    """
    バブルチャート専用設定
    """

    min_bubble_size: int = 4
    max_bubble_size: int = 50
    color_scale: str = "Viridis"
    show_colorbar: bool = True

    def to_dict(self) -> Dict[str, Any]:
        base_dict = super().to_dict()
        base_dict.update(
            {
                "min_bubble_size": self.min_bubble_size,
                "max_bubble_size": self.max_bubble_size,
                "color_scale": self.color_scale,
                "show_colorbar": self.show_colorbar,
            }
        )
        return base_dict
