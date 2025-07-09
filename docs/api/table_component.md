# TableComponent API リファレンス

`TableComponent`は、データをテーブル形式で表示し、CSVダウンロード、ソート、検索、ページネーションなどの機能を提供するコンポーネントです。

## 📋 概要

```python
from db_ui_components import TableComponent

table = TableComponent(
    data=df,
    enable_csv_download=True,
    sortable=True,
    searchable=True,
    title='データテーブル'
)
```

## 🔧 パラメータ

### 必須パラメータ

| パラメータ | 型 | 説明 | 例 |
|-----------|----|------|-----|
| `data` | pandas.DataFrame | テーブルに表示するデータ | `df` |

### オプションパラメータ

| パラメータ | 型 | デフォルト | 説明 |
|-----------|----|-----------|------|
| `title` | str | `None` | テーブルのタイトル |
| `enable_csv_download` | bool | `False` | CSVダウンロード機能の有効化 |
| `sortable` | bool | `False` | ソート機能の有効化 |
| `searchable` | bool | `False` | 検索機能の有効化 |
| `page_size` | int | `10` | 1ページあたりの表示件数 |
| `columns` | list | `None` | 表示する列の指定 |
| `height` | int | `400` | テーブルの高さ（ピクセル） |
| `width` | int | `None` | テーブルの幅（ピクセル） |
| `show_index` | bool | `True` | インデックスの表示 |
| `sticky_header` | bool | `True` | ヘッダーの固定 |

## 📊 機能

### 1. 基本的なテーブル表示

```python
# 基本的なテーブル
basic_table = TableComponent(
    data=df,
    title='売上データ'
)

displayHTML(basic_table.render())
```

### 2. CSVダウンロード機能

```python
# CSVダウンロード機能付きテーブル
download_table = TableComponent(
    data=df,
    enable_csv_download=True,
    title='ダウンロード可能な売上データ'
)

displayHTML(download_table.render())
```

### 3. ソート機能

```python
# ソート機能付きテーブル
sortable_table = TableComponent(
    data=df,
    sortable=True,
    title='ソート可能な売上データ'
)

displayHTML(sortable_table.render())
```

### 4. 検索機能

```python
# 検索機能付きテーブル
searchable_table = TableComponent(
    data=df,
    searchable=True,
    title='検索可能な売上データ'
)

displayHTML(searchable_table.render())
```

### 5. ページネーション

```python
# ページネーション機能付きテーブル
paged_table = TableComponent(
    data=df,
    page_size=5,
    title='ページネーション付き売上データ'
)

displayHTML(paged_table.render())
```

### 6. カスタム列設定

```python
# 特定の列のみを表示
custom_table = TableComponent(
    data=df,
    columns=['date', 'sales', 'profit', 'category'],
    enable_csv_download=True,
    sortable=True,
    title='カスタム列設定'
)

displayHTML(custom_table.render())
```

## 🎨 スタイリング

### カスタムスタイルの適用

```python
table = TableComponent(
    data=df,
    enable_csv_download=True,
    sortable=True,
    searchable=True
)

# スタイルを設定
table.set_style({
    'backgroundColor': '#f8f9fa',
    'borderRadius': '8px',
    'padding': '16px',
    'fontFamily': 'Arial, sans-serif',
    'fontSize': '14px'
})

displayHTML(table.render())
```

### 利用可能なスタイルプロパティ

| プロパティ | 型 | 説明 |
|-----------|----|------|
| `backgroundColor` | str | 背景色 |
| `borderRadius` | str | 角丸の半径 |
| `padding` | str | 内側の余白 |
| `margin` | str | 外側の余白 |
| `fontFamily` | str | フォントファミリー |
| `fontSize` | str | フォントサイズ |
| `color` | str | テキスト色 |
| `border` | str | ボーダー |
| `boxShadow` | str | ボックスシャドウ |

## 🔄 データ更新

### 動的データ更新

```python
# 初期データでテーブルを作成
table = TableComponent(
    data=df.head(10),
    enable_csv_download=True,
    sortable=True,
    searchable=True
)

displayHTML(table.render())

# データを更新
new_data = df.tail(10)
table.update_data(new_data)
displayHTML(table.render())
```

## 📱 レスポンシブ対応

```python
table = TableComponent(
    data=df,
    enable_csv_download=True,
    sortable=True,
    searchable=True,
    responsive=True  # レスポンシブ対応を有効化
)

displayHTML(table.render())
```

## 🎯 使用例

### 基本的な使用例

```python
import pandas as pd
import numpy as np
from db_ui_components import TableComponent

# サンプルデータ
df = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=20, freq='D'),
    'sales': np.random.normal(1000, 200, 20),
    'profit': np.random.normal(200, 50, 20),
    'category': np.random.choice(['A', 'B', 'C'], 20),
    'region': np.random.choice(['North', 'South', 'East', 'West'], 20)
})

# 基本的なテーブル
basic_table = TableComponent(
    data=df,
    title='売上データ'
)

displayHTML(basic_table.render())
```

### 高度な機能付きテーブル

```python
# 全機能付きテーブル
advanced_table = TableComponent(
    data=df,
    enable_csv_download=True,
    sortable=True,
    searchable=True,
    page_size=5,
    columns=['date', 'sales', 'profit', 'category'],
    title='高度な機能付き売上データ'
)

displayHTML(advanced_table.render())
```

### 大量データの処理

```python
# 大量データの処理
large_df = pd.DataFrame({
    'id': range(10000),
    'value': np.random.randn(10000),
    'category': np.random.choice(['A', 'B', 'C', 'D'], 10000)
})

# ページネーション付きテーブル
large_table = TableComponent(
    data=large_df,
    enable_csv_download=True,
    sortable=True,
    searchable=True,
    page_size=100,
    title='大量データテーブル'
)

displayHTML(large_table.render())
```

### カスタムスタイル付きテーブル

```python
# カスタムスタイル付きテーブル
styled_table = TableComponent(
    data=df,
    enable_csv_download=True,
    sortable=True,
    searchable=True,
    title='カスタムスタイル付きテーブル'
)

# スタイルを設定
styled_table.set_style({
    'backgroundColor': '#2c3e50',
    'color': '#ecf0f1',
    'borderRadius': '10px',
    'padding': '20px',
    'fontFamily': 'Roboto, sans-serif',
    'fontSize': '16px',
    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
})

displayHTML(styled_table.render())
```

## ⚠️ 制限事項

- **データサイズ**: 推奨最大100,000行
- **列数**: 推奨最大50列
- **メモリ使用量**: 大量データの場合は注意が必要
- **ブラウザ互換性**: モダンブラウザが必要

## 🔗 関連リンク

- [ChartComponent](./chart_component.md) - グラフ・チャートコンポーネント
- [FilterComponent](./filter_component.md) - フィルターコンポーネント
- [Dashboard](./dashboard.md) - ダッシュボードクラス
- [トラブルシューティング](../troubleshooting/faq.md) - よくある問題