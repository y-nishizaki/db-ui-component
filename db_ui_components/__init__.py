"""
Databricks UI Component Library

Databricksでノートブックからダッシュボードを作成する際に使用できる、
便利なUIコンポーネントライブラリです。

このライブラリは、PlotlyとDashを使用して、データビジュアライゼーションと
インタラクティブなダッシュボードを作成するためのコンポーネントを提供します。
"""

from .chart_component import ChartComponent
from .table_component import TableComponent
from .filter_component import FilterComponent
from .dashboard import Dashboard
from .visualization import (
    SankeyChartComponent,
    HeatmapComponent,
    NetworkGraphComponent,
    TreemapComponent,
    BubbleChartComponent
)

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"
__description__ = "Databricksダッシュボード用UIコンポーネントライブラリ"
__url__ = "https://github.com/your-username/db-ui-components"

__all__ = [
    "ChartComponent",
    "TableComponent", 
    "FilterComponent",
    "Dashboard",
    "SankeyChartComponent",
    "HeatmapComponent",
    "NetworkGraphComponent",
    "TreemapComponent",
    "BubbleChartComponent",
] 