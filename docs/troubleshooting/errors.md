# エラーリファレンス

このドキュメントでは、db-ui-componentsライブラリで発生する可能性のあるエラーとその対処法を説明します。

## インストール関連エラー

### ImportError: No module named 'db_ui_components'

**原因**: ライブラリがインストールされていない

**解決方法**:
```bash
pip install db-ui-components
```

**開発版の場合**:
```bash
pip install git+https://github.com/y-nishizaki/db-ui-components.git
```

### ModuleNotFoundError: No module named 'plotly'

**原因**: 依存関係が不足している

**解決方法**:
```bash
pip install plotly dash pandas
```

## Databricks環境でのエラー

### Databricksノートブックでのインポートエラー

**原因**: Databricks環境での依存関係不足

**解決方法**:
```python
# ノートブック内で直接インストール
!pip install db-ui-components
```

**または**:
```python
!pip install git+https://github.com/y-nishizaki/db-ui-components.git
```

## コンポーネント関連エラー

### ValueError: Invalid chart type

**原因**: サポートされていないグラフタイプを指定

**解決方法**: サポートされているグラフタイプを使用
```python
# サポートされているグラフタイプ
supported_types = ['line', 'bar', 'pie', 'scatter', 'heatmap']
```

### KeyError: Column not found

**原因**: 指定した列がデータフレームに存在しない

**解決方法**: 正しい列名を確認
```python
# 利用可能な列を確認
print(df.columns)
```

### TypeError: Data must be a pandas DataFrame

**原因**: データフレーム以外のデータを渡している

**解決方法**: pandas DataFrameに変換
```python
import pandas as pd
df = pd.DataFrame(your_data)
```

## レンダリング関連エラー

### HTML rendering failed

**原因**: HTMLの生成に失敗

**解決方法**:
1. データの妥当性を確認
2. コンポーネントの設定を確認
3. エラーログを確認

### JavaScript error in browser

**原因**: ブラウザでのJavaScriptエラー

**解決方法**:
1. ブラウザの開発者ツールでエラーを確認
2. データに特殊文字が含まれていないか確認
3. コンポーネントの設定を確認

## パフォーマンス関連エラー

### MemoryError: Out of memory

**原因**: 大量データによるメモリ不足

**解決方法**:
1. データサイズを削減
2. データの前処理を実施
3. より効率的なデータ構造を使用

### TimeoutError: Rendering timeout

**原因**: レンダリングに時間がかかりすぎ

**解決方法**:
1. データサイズを削減
2. コンポーネントの設定を最適化
3. 非同期処理を検討

## データベース関連エラー

### ConnectionError: Database connection failed

**原因**: データベース接続の失敗

**解決方法**:
1. 接続情報を確認
2. ネットワーク接続を確認
3. 認証情報を確認

### SQLSyntaxError: Invalid SQL query

**原因**: SQLクエリの構文エラー

**解決方法**:
1. SQLクエリの構文を確認
2. データベースの方言を確認
3. エスケープ処理を確認

## セキュリティ関連エラー

### SecurityWarning: Potential XSS vulnerability

**原因**: XSS攻撃の可能性

**解決方法**:
1. 入力データのサニタイゼーション
2. HTMLエスケープ処理
3. セキュリティヘッダーの設定

## デバッグ方法

### ログの確認

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# コンポーネントの作成時にログを確認
chart = ChartComponent(data=df, chart_type='line')
```

### データの確認

```python
# データの基本情報を確認
print(df.info())
print(df.head())
print(df.describe())
```

### コンポーネントの確認

```python
# コンポーネントの設定を確認
print(chart.__dict__)
```

## よくあるエラーと対処法

| エラー | 原因 | 対処法 |
|--------|------|--------|
| `ImportError` | インポートエラー | ライブラリ未インストール | `pip install db-ui-components` |
| `ValueError` | 値エラー | 不正なパラメータ | パラメータの確認 |
| `KeyError` | キーエラー | 列名が存在しない | 列名の確認 |
| `TypeError` | 型エラー | 不正なデータ型 | データ型の変換 |
| `MemoryError` | メモリエラー | メモリ不足 | データサイズの削減 |
| `TimeoutError` | タイムアウト | 処理時間超過 | 最適化 |

## サポート

エラーが解決しない場合は、以下をご確認ください：

1. [よくある質問](../troubleshooting/faq.md)
2. [GitHub Issues](https://github.com/y-nishizaki/db-ui-components/issues)
3. エラーログの詳細情報
4. 環境情報（Pythonバージョン、OS等）