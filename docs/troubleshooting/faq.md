# よくある問題 (FAQ)

このページでは、Databricks UI Component Libraryを使用する際によく発生する問題とその解決方法を説明します。

## 🚨 よくある問題

### Q1: グラフが表示されない

**症状:** `displayHTML()`を実行してもグラフが表示されない

**原因と解決方法:**

1. **データの問題**
```python
# データが空でないことを確認
print(f"データ行数: {len(df)}")
print(f"データ列: {df.columns.tolist()}")
```

2. **列名の問題**
```python
# 指定した列が存在することを確認
print(f"X軸列 '{x_column}' が存在: {x_column in df.columns}")
print(f"Y軸列 '{y_column}' が存在: {y_column in df.columns}")
```

3. **データ型の問題**
```python
# データ型を確認
print(f"X軸データ型: {df[x_column].dtype}")
print(f"Y軸データ型: {df[y_column].dtype}")
```

**解決例:**
```python
# 正しい使用例
import pandas as pd
import numpy as np
from db_ui_components import ChartComponent

# データを確認
df = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=30, freq='D'),
    'sales': np.random.normal(1000, 200, 30)
})

print(f"データ確認: {len(df)}行, 列: {df.columns.tolist()}")

# グラフを作成
chart = ChartComponent(
    data=df,
    chart_type='line',
    x_column='date',
    y_column='sales',
    title='売上推移'
)

# 表示
displayHTML(chart.render())
```

### Q2: テーブルが正しく表示されない

**症状:** テーブルのソートや検索が機能しない

**解決方法:**

1. **JavaScriptの有効化確認**
```python
# テーブルコンポーネントの基本設定
from db_ui_components import TableComponent

table = TableComponent(
    data=df,
    enable_csv_download=True,
    sortable=True,
    searchable=True,
    page_size=10  # ページサイズを明示的に設定
)
```

2. **データの前処理**
```python
# NULL値を処理
df = df.fillna('')  # または適切な値で置換

# データ型を確認
print(df.dtypes)
```

### Q3: パフォーマンスが悪い

**症状:** 大量データでグラフの表示が遅い

**解決方法:**

1. **データサイズの制限**
```python
# 表示するデータを制限
df_sample = df.head(1000)  # 最大1000行に制限

chart = ChartComponent(
    data=df_sample,
    chart_type='line',
    x_column='date',
    y_column='sales'
)
```

2. **データの集約**
```python
# 日次データを月次に集約
df_monthly = df.groupby(df['date'].dt.to_period('M')).agg({
    'sales': 'sum',
    'profit': 'sum'
}).reset_index()
```

3. **キャッシュの活用**
```python
# グラフを一度作成して再利用
chart = ChartComponent(data=df, chart_type='line', x_column='date', y_column='sales')
html_output = chart.render()

# 複数回表示
displayHTML(html_output)
```

### Q4: エラーメッセージが表示される

**よくあるエラーと解決方法:**

#### ImportError: No module named 'db_ui_components'

```bash
# インストール確認
pip install db-ui-components

# または開発版
pip install git+https://github.com/your-username/db-ui-components.git
```

#### ValueError: Invalid chart type

```python
# サポートされているグラフタイプを確認
valid_types = ['line', 'bar', 'pie', 'scatter', 'heatmap']
print(f"使用可能なグラフタイプ: {valid_types}")

# 正しいグラフタイプを使用
chart = ChartComponent(
    data=df,
    chart_type='line',  # 正しいタイプ
    x_column='date',
    y_column='sales'
)
```

#### KeyError: Column not found

```python
# 列名を確認
print(f"利用可能な列: {df.columns.tolist()}")

# 正しい列名を使用
chart = ChartComponent(
    data=df,
    chart_type='line',
    x_column='date',  # 存在する列名
    y_column='sales'  # 存在する列名
)
```

### Q5: スタイルが適用されない

**症状:** `set_style()`で設定したスタイルが反映されない

**解決方法:**

```python
# スタイルを設定してからレンダリング
chart = ChartComponent(data=df, chart_type='line', x_column='date', y_column='sales')

# スタイルを設定
chart.set_style({
    'backgroundColor': '#f5f5f5',
    'borderRadius': '8px',
    'padding': '16px'
})

# レンダリング
displayHTML(chart.render())
```

### Q6: ダッシュボードのレイアウトが崩れる

**症状:** ダッシュボードのコンポーネントが正しく配置されない

**解決方法:**

```python
from db_ui_components import Dashboard, ChartComponent, TableComponent

# ダッシュボードを作成
dashboard = Dashboard(title='売上ダッシュボード')

# コンポーネントを追加（位置を明示的に指定）
chart = ChartComponent(data=df, chart_type='line', x_column='date', y_column='sales')
table = TableComponent(data=df.head(10))

dashboard.add_component(chart, position=(0, 0))  # 1行目、1列目
dashboard.add_component(table, position=(1, 0))  # 2行目、1列目

# 表示
displayHTML(dashboard.render())
```

## 🔧 デバッグのヒント

### 1. データの確認

```python
# データの基本情報を確認
print(f"データ形状: {df.shape}")
print(f"データ型: {df.dtypes}")
print(f"NULL値: {df.isnull().sum()}")
print(f"サンプルデータ:\n{df.head()}")
```

### 2. コンポーネントの確認

```python
# コンポーネントの設定を確認
print(f"グラフタイプ: {chart.chart_type}")
print(f"X軸列: {chart.x_column}")
print(f"Y軸列: {chart.y_column}")
print(f"データ行数: {len(chart.data)}")
```

### 3. HTML出力の確認

```python
# 生成されたHTMLを確認
html_output = chart.render()
print("生成されたHTML（最初の500文字）:")
print(html_output[:500])
```

## 📞 サポート

問題が解決しない場合は、以下の情報を含めて報告してください：

1. **エラーメッセージ**（完全なエラーメッセージ）
2. **使用しているコード**
3. **データのサンプル**
4. **環境情報**（Pythonバージョン、ライブラリバージョン）

**関連リンク:**
- [エラーリファレンス](./errors.md) - 詳細なエラー説明
- [デバッグガイド](./debugging.md) - デバッグの方法
- [パフォーマンス最適化](../guides/performance.md) - パフォーマンスの改善