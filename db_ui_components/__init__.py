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
from .database_component import DatabaseComponent, SparkComponent
from .databricks_database import (
    DatabricksDatabaseComponent,
    create_databricks_database_component,
    execute_sql,
    get_tables,
    preview_table,
    get_table_stats
)
from .visualization import (
    SankeyChartComponent,
    HeatmapComponent,
    NetworkGraphComponent,
    TreemapComponent,
    BubbleChartComponent
)

__version__ = "1.0.0"
__author__ = "Databricks Team"
__email__ = "team@databricks.com"
__description__ = "Databricksダッシュボード用UIコンポーネントライブラリ"
__url__ = "https://github.com/y-nishizaki/db-ui-components"

__all__ = [
    "ChartComponent",
    "TableComponent", 
    "FilterComponent",
    "Dashboard",
    "DatabaseComponent",
    "SparkComponent",
    "DatabricksDatabaseComponent",
    "create_databricks_database_component",
    "execute_sql",
    "get_tables",
    "preview_table",
    "get_table_stats",
    "SankeyChartComponent",
    "HeatmapComponent",
    "NetworkGraphComponent",
    "TreemapComponent",
    "BubbleChartComponent",
] 