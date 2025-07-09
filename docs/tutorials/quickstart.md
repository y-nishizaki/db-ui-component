# クイックスタートガイド

このガイドでは、Databricks UI Component Libraryを5分で始める方法を説明します。

## 🚀 5分で始める

### 1. インストール

```bash
pip install db-ui-components
```

### 2. 基本的なグラフを作成

```python
# 必要なライブラリをインポート
import pandas as pd
import numpy as np
from db_ui_components import ChartComponent

# サンプルデータを作成
df = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=30, freq='D'),
    'sales': np.random.normal(1000, 200, 30)
})

# グラフコンポーネントを作成
chart = ChartComponent(
    data=df,
    chart_type='line',
    x_column='date',
    y_column='sales',
    title='売上推移'
)

# Databricksで表示
displayHTML(chart.render())
```

### 3. テーブルを作成

```python
from db_ui_components import TableComponent

# テーブルコンポーネントを作成
table = TableComponent(
    data=df,
    enable_csv_download=True,
    sortable=True,
    searchable=True
)

# 表示
displayHTML(table.render())
```

### 4. ダッシュボードを作成

```python
from db_ui_components import Dashboard

# ダッシュボードを作成
dashboard = Dashboard()

# コンポーネントを追加
dashboard.add_component(chart, position=(0, 0))
dashboard.add_component(table, position=(1, 0))

# 表示
displayHTML(dashboard.render())
```

## 📊 サンプルコード

### 完全なサンプル

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from db_ui_components import ChartComponent, TableComponent, Dashboard

# サンプルデータの作成
np.random.seed(42)
dates = pd.date_range('2024-01-01', periods=100, freq='D')
data = {
    'date': dates,
    'sales': np.random.normal(1000, 200, 100),
    'profit': np.random.normal(200, 50, 100),
    'category': np.random.choice(['A', 'B', 'C'], 100)
}
df = pd.DataFrame(data)

# グラフコンポーネント
sales_chart = ChartComponent(
    data=df,
    chart_type='line',
    x_column='date',
    y_column='sales',
    title='売上推移'
)

# テーブルコンポーネント
data_table = TableComponent(
    data=df.head(20),
    enable_csv_download=True,
    sortable=True,
    searchable=True
)

# ダッシュボードの作成
dashboard = Dashboard(title='売上ダッシュボード')
dashboard.add_component(sales_chart, position=(0, 0))
dashboard.add_component(data_table, position=(1, 0))

# 表示
displayHTML(dashboard.render())
```

## 🎯 次のステップ

- [基本使用法](./basic_usage.md) - より詳細な使用方法
- [ダッシュボード作成](./dashboard_creation.md) - 複雑なダッシュボードの作成
- [高度な可視化](./advanced_visualization.md) - 高度な可視化コンポーネント
- [API リファレンス](../api/) - 全APIの詳細

## ❓ 問題が発生した場合

- [よくある問題](../troubleshooting/faq.md) - よくある問題と解決方法
- [エラーリファレンス](../troubleshooting/errors.md) - エラーメッセージの説明

## 📚 関連ドキュメント

- [インストールガイド](../guides/installation.md) - 詳細なインストール手順
- [Databricksでの使用](../guides/databricks_usage.md) - Databricks環境での使用方法
- [パフォーマンス最適化](../guides/performance.md) - パフォーマンスの最適化