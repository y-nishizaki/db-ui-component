# エラーリファレンス

このドキュメントでは、Databricks UI Component Libraryで発生する可能性のあるエラーとその解決方法を詳しく説明します。

## 🚨 エラーの種類

### 1. インポートエラー

#### ImportError: No module named 'db_ui_components'

**原因:** ライブラリがインストールされていない

**解決方法:**
```bash
# インストール
pip install db-ui-components

# または開発版
pip install git+https://github.com/your-username/db-ui-components.git
```

**Databricksでの解決方法:**
```python
# ノートブック内でインストール
!pip install db-ui-components

# インストール確認
import db_ui_components
print(f"バージョン: {db_ui_components.__version__}")
```

#### ImportError: No module named 'pandas'

**原因:** 依存関係が不足している

**解決方法:**
```bash
# 依存関係をインストール
pip install pandas>=1.5.0
pip install numpy>=1.21.0
pip install plotly>=5.0.0
pip install db-ui-components
```

### 2. データエラー

#### ValueError: Invalid chart type

**原因:** サポートされていないグラフタイプを指定

**解決方法:**
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

**原因:** 指定した列がデータフレームに存在しない

**解決方法:**
```python
# 利用可能な列を確認
print(f"利用可能な列: {df.columns.tolist()}")

# 正しい列名を使用
chart = ChartComponent(
    data=df,
    chart_type='line',
    x_column='date',  # 存在する列名
    y_column='sales'  # 存在する列名
)
```

#### ValueError: Data is empty

**原因:** データフレームが空

**解決方法:**
```python
# データの確認
print(f"データ行数: {len(df)}")
print(f"データ形状: {df.shape}")

# データが空でないことを確認
if not df.empty:
    chart = ChartComponent(
        data=df,
        chart_type='line',
        x_column='date',
        y_column='sales'
    )
else:
    print("データが空です。データを確認してください。")
```

### 3. データ型エラー

#### TypeError: Object of type 'datetime' is not JSON serializable

**原因:** 日付データがJSONシリアライズできない

**解決方法:**
```python
# 日付データを文字列に変換
df['date'] = df['date'].astype(str)

# または、日付フォーマットを指定
df['date'] = df['date'].dt.strftime('%Y-%m-%d')

chart = ChartComponent(
    data=df,
    chart_type='line',
    x_column='date',
    y_column='sales'
)
```

#### TypeError: Object of type 'numpy.int64' is not JSON serializable

**原因:** NumPyデータ型がJSONシリアライズできない

**解決方法:**
```python
# NumPyデータ型をPythonネイティブ型に変換
df = df.astype({
    'sales': 'float64',
    'profit': 'float64',
    'customer_count': 'int64'
})

chart = ChartComponent(
    data=df,
    chart_type='line',
    x_column='date',
    y_column='sales'
)
```

### 4. メモリエラー

#### MemoryError: Unable to allocate array

**原因:** 大量データでメモリ不足

**解決方法:**
```python
# データサイズを制限
def limit_data_size(df, max_rows=10000):
    """データサイズを制限"""
    if len(df) > max_rows:
        return df.sample(n=max_rows, random_state=42)
    return df

# 制限されたデータでグラフ作成
limited_data = limit_data_size(df, 5000)

chart = ChartComponent(
    data=limited_data,
    chart_type='line',
    x_column='date',
    y_column='sales'
)
```

### 5. レンダリングエラー

#### ValueError: Invalid HTML generated

**原因:** HTMLの生成に失敗

**解決方法:**
```python
# データの前処理
def clean_data(df):
    """データをクリーンアップ"""
    # NULL値を処理
    df = df.fillna('')
    
    # 特殊文字をエスケープ
    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].astype(str).str.replace('<', '&lt;').replace('>', '&gt;')
    
    return df

# データをクリーンアップしてからグラフ作成
clean_df = clean_data(df)

chart = ChartComponent(
    data=clean_df,
    chart_type='line',
    x_column='date',
    y_column='sales'
)
```

### 6. 設定エラー

#### ValueError: Invalid height value

**原因:** 無効な高さ値

**解決方法:**
```python
# 正しい高さ値を指定
chart = ChartComponent(
    data=df,
    chart_type='line',
    x_column='date',
    y_column='sales',
    height=400  # 正の整数値
)
```

#### ValueError: Invalid color value

**原因:** 無効な色値

**解決方法:**
```python
# 正しい色値を指定
chart = ChartComponent(
    data=df,
    chart_type='line',
    x_column='date',
    y_column='sales',
    color='#1f77b4'  # 有効なHEX色コード
)
```

## 🔧 デバッグ方法

### 1. データの確認

```python
def debug_data(df):
    """データのデバッグ情報を表示"""
    print(f"データ形状: {df.shape}")
    print(f"データ型: {df.dtypes}")
    print(f"NULL値: {df.isnull().sum()}")
    print(f"サンプルデータ:\n{df.head()}")
    print(f"列名: {df.columns.tolist()}")

# デバッグ実行
debug_data(df)
```

### 2. コンポーネントの確認

```python
def debug_component(component):
    """コンポーネントのデバッグ情報を表示"""
    print(f"コンポーネントタイプ: {type(component)}")
    print(f"データ行数: {len(component.data)}")
    print(f"設定: {component.__dict__}")

# デバッグ実行
chart = ChartComponent(data=df, chart_type='line', x_column='date', y_column='sales')
debug_component(chart)
```

### 3. HTML出力の確認

```python
def debug_html(component):
    """HTML出力をデバッグ"""
    try:
        html_output = component.render()
        print(f"HTML長さ: {len(html_output)}")
        print(f"HTMLサンプル: {html_output[:500]}...")
        return html_output
    except Exception as e:
        print(f"HTML生成エラー: {e}")
        return None

# デバッグ実行
html = debug_html(chart)
```

## 📋 エラーコード一覧

| エラーコード | エラータイプ | 原因 | 解決方法 |
|-------------|-------------|------|----------|
| `ImportError` | インポートエラー | ライブラリ未インストール | `pip install db-ui-components` |
| `KeyError` | キーエラー | 列名が存在しない | 正しい列名を確認 |
| `ValueError` | 値エラー | 無効なパラメータ | パラメータを確認 |
| `TypeError` | 型エラー | データ型の問題 | データ型を変換 |
| `MemoryError` | メモリエラー | メモリ不足 | データサイズを制限 |
| `AttributeError` | 属性エラー | メソッドが存在しない | APIバージョンを確認 |

## 🛠️ 予防策

### 1. データの前処理

```python
def preprocess_data(df):
    """データの前処理"""
    # NULL値を処理
    df = df.fillna('')
    
    # データ型を確認
    for col in df.select_dtypes(include=['datetime64']):
        df[col] = df[col].astype(str)
    
    # NumPy型をPythonネイティブ型に変換
    for col in df.select_dtypes(include=['number']):
        df[col] = df[col].astype(float)
    
    return df

# 前処理を実行
df = preprocess_data(df)
```

### 2. エラーハンドリング

```python
def safe_create_chart(data, chart_type, x_column, y_column):
    """安全なグラフ作成"""
    try:
        # データの検証
        if data.empty:
            raise ValueError("データが空です")
        
        if x_column not in data.columns:
            raise ValueError(f"列 '{x_column}' が存在しません")
        
        if y_column not in data.columns:
            raise ValueError(f"列 '{y_column}' が存在しません")
        
        # グラフを作成
        chart = ChartComponent(
            data=data,
            chart_type=chart_type,
            x_column=x_column,
            y_column=y_column
        )
        
        return chart
        
    except Exception as e:
        print(f"グラフ作成エラー: {e}")
        return None

# 安全なグラフ作成
chart = safe_create_chart(df, 'line', 'date', 'sales')
if chart:
    displayHTML(chart.render())
```

### 3. ログ機能

```python
import logging

# ログの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_chart_with_logging(data, chart_type, x_column, y_column):
    """ログ付きグラフ作成"""
    logger.info(f"グラフ作成開始: {chart_type}")
    logger.info(f"データ形状: {data.shape}")
    
    try:
        chart = ChartComponent(
            data=data,
            chart_type=chart_type,
            x_column=x_column,
            y_column=y_column
        )
        
        logger.info("グラフ作成成功")
        return chart
        
    except Exception as e:
        logger.error(f"グラフ作成失敗: {e}")
        raise

# ログ付きグラフ作成
chart = create_chart_with_logging(df, 'line', 'date', 'sales')
```

## 📞 サポート

エラーが解決しない場合は、以下の情報を含めて報告してください：

1. **完全なエラーメッセージ**
2. **使用しているコード**
3. **データのサンプル**
4. **環境情報**（Pythonバージョン、ライブラリバージョン）
5. **実行環境**（Databricks、ローカル等）

**関連リンク:**
- [よくある問題](./faq.md) - よくある問題と解決方法
- [デバッグガイド](./debugging.md) - デバッグの方法
- [トラブルシューティング](../troubleshooting/) - トラブルシューティング全般