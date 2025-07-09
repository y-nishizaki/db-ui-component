# FilterComponent API リファレンス

`FilterComponent`は、データのフィルタリング機能を提供するコンポーネントです。ドロップダウン、マルチセレクト、日付範囲、テキスト検索などの様々なフィルタータイプをサポートしています。

## 📋 概要

```python
from db_ui_components import FilterComponent

filter_comp = FilterComponent(
    filter_type='dropdown',
    column='category',
    options=['A', 'B', 'C'],
    placeholder='カテゴリを選択',
    title='カテゴリフィルター'
)
```

## 🔧 パラメータ

### 必須パラメータ

| パラメータ | 型 | 説明 | 例 |
|-----------|----|------|-----|
| `filter_type` | str | フィルターのタイプ | `'dropdown'`, `'multiselect'`, `'date'`, `'text'` |
| `column` | str | フィルター対象の列名 | `'category'`, `'date'`, `'region'` |

### オプションパラメータ

| パラメータ | 型 | デフォルト | 説明 |
|-----------|----|-----------|------|
| `title` | str | `None` | フィルターのタイトル |
| `options` | list | `[]` | フィルターオプション（dropdown, multiselect用） |
| `placeholder` | str | `'選択してください'` | プレースホルダーテキスト |
| `start_date` | str/datetime | `None` | 開始日（date用） |
| `end_date` | str/datetime | `None` | 終了日（date用） |
| `default_value` | str/list | `None` | デフォルト値 |
| `width` | int | `200` | フィルターの幅（ピクセル） |
| `height` | int | `40` | フィルターの高さ（ピクセル） |

## 📊 フィルタータイプ

### 1. ドロップダウンフィルター (`'dropdown'`)

```python
# 基本的なドロップダウンフィルター
dropdown_filter = FilterComponent(
    filter_type='dropdown',
    column='category',
    options=['A', 'B', 'C'],
    placeholder='カテゴリを選択',
    title='カテゴリフィルター'
)

displayHTML(dropdown_filter.render())
```

**特徴:**
- 単一選択
- プレースホルダーテキスト
- カスタムオプション

### 2. マルチセレクトフィルター (`'multiselect'`)

```python
# マルチセレクトフィルター
multiselect_filter = FilterComponent(
    filter_type='multiselect',
    column='region',
    options=['North', 'South', 'East', 'West'],
    placeholder='地域を選択',
    title='地域フィルター'
)

displayHTML(multiselect_filter.render())
```

**特徴:**
- 複数選択
- チェックボックス表示
- 全選択/全解除機能

### 3. 日付範囲フィルター (`'date'`)

```python
# 日付範囲フィルター
date_filter = FilterComponent(
    filter_type='date',
    column='date',
    start_date='2024-01-01',
    end_date='2024-12-31',
    title='日付範囲フィルター'
)

displayHTML(date_filter.render())
```

**特徴:**
- 日付範囲選択
- カレンダーUI
- 開始日・終了日設定

### 4. テキスト検索フィルター (`'text'`)

```python
# テキスト検索フィルター
text_filter = FilterComponent(
    filter_type='text',
    column='category',
    placeholder='カテゴリを検索',
    title='検索フィルター'
)

displayHTML(text_filter.render())
```

**特徴:**
- リアルタイム検索
- 部分一致検索
- 大文字小文字区別なし

## 🎨 スタイリング

### カスタムスタイルの適用

```python
filter_comp = FilterComponent(
    filter_type='dropdown',
    column='category',
    options=['A', 'B', 'C']
)

# スタイルを設定
filter_comp.set_style({
    'backgroundColor': '#f8f9fa',
    'borderRadius': '8px',
    'padding': '8px',
    'fontFamily': 'Arial, sans-serif',
    'fontSize': '14px',
    'border': '1px solid #dee2e6'
})

displayHTML(filter_comp.render())
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

## 🔄 イベントハンドリング

### フィルター値の取得

```python
# フィルターコンポーネントを作成
filter_comp = FilterComponent(
    filter_type='dropdown',
    column='category',
    options=['A', 'B', 'C']
)

# フィルター値の取得
def get_filter_value():
    """フィルター値を取得"""
    return filter_comp.get_value()

# フィルター値の設定
def set_filter_value(value):
    """フィルター値を設定"""
    filter_comp.set_value(value)

# フィルター値の変更イベント
def on_filter_change(value):
    """フィルター値が変更された時の処理"""
    print(f"フィルター値が変更されました: {value}")
    # データの再フィルタリング処理
    filtered_data = df[df['category'] == value]
    return filtered_data
```

## 📱 レスポンシブ対応

```python
filter_comp = FilterComponent(
    filter_type='dropdown',
    column='category',
    options=['A', 'B', 'C'],
    responsive=True  # レスポンシブ対応を有効化
)

displayHTML(filter_comp.render())
```

## 🎯 使用例

### 基本的な使用例

```python
import pandas as pd
import numpy as np
from db_ui_components import FilterComponent

# サンプルデータ
df = pd.DataFrame({
    'category': np.random.choice(['A', 'B', 'C'], 100),
    'region': np.random.choice(['North', 'South', 'East', 'West'], 100),
    'date': pd.date_range('2024-01-01', periods=100, freq='D')
})

# カテゴリフィルター
category_filter = FilterComponent(
    filter_type='dropdown',
    column='category',
    options=df['category'].unique().tolist(),
    placeholder='カテゴリを選択',
    title='カテゴリフィルター'
)

displayHTML(category_filter.render())
```

### 複数フィルターの組み合わせ

```python
# 地域フィルター
region_filter = FilterComponent(
    filter_type='multiselect',
    column='region',
    options=df['region'].unique().tolist(),
    placeholder='地域を選択',
    title='地域フィルター'
)

# 日付フィルター
date_filter = FilterComponent(
    filter_type='date',
    column='date',
    start_date=df['date'].min(),
    end_date=df['date'].max(),
    title='日付範囲フィルター'
)

# 検索フィルター
search_filter = FilterComponent(
    filter_type='text',
    column='category',
    placeholder='カテゴリを検索',
    title='検索フィルター'
)

# 複数フィルターを表示
displayHTML(category_filter.render())
displayHTML(region_filter.render())
displayHTML(date_filter.render())
displayHTML(search_filter.render())
```

### 動的オプション生成

```python
# データから動的にオプションを生成
def create_dynamic_filter(df, column_name):
    """データから動的にフィルターを作成"""
    unique_values = df[column_name].unique().tolist()
    
    filter_comp = FilterComponent(
        filter_type='dropdown',
        column=column_name,
        options=unique_values,
        placeholder=f'{column_name}を選択',
        title=f'{column_name}フィルター'
    )
    
    return filter_comp

# 動的フィルターの作成
dynamic_filter = create_dynamic_filter(df, 'category')
displayHTML(dynamic_filter.render())
```

### カスタムスタイル付きフィルター

```python
# カスタムスタイル付きフィルター
styled_filter = FilterComponent(
    filter_type='dropdown',
    column='category',
    options=['A', 'B', 'C'],
    title='カスタムスタイル付きフィルター'
)

# スタイルを設定
styled_filter.set_style({
    'backgroundColor': '#2c3e50',
    'color': '#ecf0f1',
    'borderRadius': '10px',
    'padding': '12px',
    'fontFamily': 'Roboto, sans-serif',
    'fontSize': '16px',
    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
    'border': '2px solid #3498db'
})

displayHTML(styled_filter.render())
```

## ⚠️ 制限事項

- **オプション数**: 推奨最大1,000オプション
- **日付範囲**: 推奨最大1年
- **テキスト検索**: 推奨最大10,000文字
- **ブラウザ互換性**: モダンブラウザが必要

## 🔗 関連リンク

- [ChartComponent](./chart_component.md) - グラフ・チャートコンポーネント
- [TableComponent](./table_component.md) - テーブルコンポーネント
- [Dashboard](./dashboard.md) - ダッシュボードクラス
- [トラブルシューティング](../troubleshooting/faq.md) - よくある問題