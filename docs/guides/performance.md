# パフォーマンス最適化ガイド

このガイドでは、Databricks UI Component Libraryのパフォーマンスを最適化する方法を説明します。

## 🎯 概要

大量のデータを扱う際や、複数のコンポーネントを同時に表示する際のパフォーマンスを最適化するためのベストプラクティスを紹介します。

## 📊 データ最適化

### 1. データサイズの制限

```python
# 大量データのサンプリング
def limit_data_size(df, max_rows=10000):
    """データサイズを制限"""
    if len(df) > max_rows:
        return df.sample(n=max_rows, random_state=42)
    return df

# 使用例
large_df = spark.sql("SELECT * FROM large_table").toPandas()
optimized_df = limit_data_size(large_df, 5000)

chart = ChartComponent(
    data=optimized_df,
    chart_type='line',
    x_column='date',
    y_column='sales',
    title='最適化された売上データ'
)
```

### 2. データの集約

```python
# 時系列データの集約
def aggregate_time_series(df, time_column='date', value_column='sales', freq='D'):
    """時系列データを集約"""
    df[time_column] = pd.to_datetime(df[time_column])
    aggregated = df.groupby(pd.Grouper(key=time_column, freq=freq))[value_column].sum().reset_index()
    return aggregated.dropna()

# 使用例
daily_sales = aggregate_time_series(df, 'date', 'sales', 'D')
chart = ChartComponent(
    data=daily_sales,
    chart_type='line',
    x_column='date',
    y_column='sales',
    title='日次売上集計'
)
```

### 3. データ型の最適化

```python
# データ型の最適化
def optimize_data_types(df):
    """データ型を最適化してメモリ使用量を削減"""
    for col in df.columns:
        if df[col].dtype == 'object':
            # 文字列列の最適化
            if df[col].nunique() / len(df) < 0.5:
                df[col] = df[col].astype('category')
        elif df[col].dtype == 'float64':
            # 浮動小数点数の最適化
            if df[col].isnull().sum() == 0:
                df[col] = df[col].astype('float32')
        elif df[col].dtype == 'int64':
            # 整数の最適化
            df[col] = pd.to_numeric(df[col], downcast='integer')
    return df

# 使用例
optimized_df = optimize_data_types(df)
print(f"メモリ使用量削減: {df.memory_usage().sum() / optimized_df.memory_usage().sum():.2f}倍")
```

## 🚀 レンダリング最適化

### 1. 遅延レンダリング

```python
# 遅延レンダリングの実装
class LazyChartComponent:
    def __init__(self, data, **kwargs):
        self.data = data
        self.kwargs = kwargs
        self._chart = None
    
    def render(self):
        if self._chart is None:
            self._chart = ChartComponent(data=self.data, **self.kwargs)
        return self._chart.render()

# 使用例
lazy_chart = LazyChartComponent(
    data=df,
    chart_type='line',
    x_column='date',
    y_column='sales'
)

# 実際に表示する時までレンダリングを遅延
displayHTML(lazy_chart.render())
```

### 2. コンポーネントのキャッシュ

```python
import functools

# コンポーネントのキャッシュ
@functools.lru_cache(maxsize=10)
def create_cached_chart(chart_type, x_column, y_column, title):
    """チャートコンポーネントをキャッシュ"""
    return ChartComponent(
        data=df,
        chart_type=chart_type,
        x_column=x_column,
        y_column=y_column,
        title=title
    )

# 使用例
chart1 = create_cached_chart('line', 'date', 'sales', '売上推移')
chart2 = create_cached_chart('line', 'date', 'sales', '売上推移')  # キャッシュから取得
```

### 3. バッチ処理

```python
# 複数コンポーネントのバッチ処理
def render_components_batch(components):
    """複数コンポーネントを一括でレンダリング"""
    html_parts = []
    for component in components:
        html_parts.append(component.render())
    return '\n'.join(html_parts)

# 使用例
components = [
    ChartComponent(data=df, chart_type='line', x_column='date', y_column='sales'),
    ChartComponent(data=df, chart_type='bar', x_column='category', y_column='sales'),
    TableComponent(data=df.head(100))
]

batch_html = render_components_batch(components)
displayHTML(batch_html)
```

## 💾 メモリ最適化

### 1. 不要なデータの削除

```python
# 不要な列の削除
def remove_unnecessary_columns(df, keep_columns):
    """不要な列を削除"""
    return df[keep_columns]

# 使用例
essential_columns = ['date', 'sales', 'category']
clean_df = remove_unnecessary_columns(df, essential_columns)
```

### 2. データの分割処理

```python
# 大量データの分割処理
def process_large_data_in_chunks(df, chunk_size=10000):
    """大量データを分割して処理"""
    results = []
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i+chunk_size]
        # チャンクごとの処理
        processed_chunk = process_chunk(chunk)
        results.append(processed_chunk)
    return pd.concat(results, ignore_index=True)

def process_chunk(chunk):
    """チャンクの処理"""
    # チャンクごとの集約処理
    return chunk.groupby('category')['sales'].sum().reset_index()
```

### 3. ガベージコレクションの最適化

```python
import gc

# メモリの明示的な解放
def optimize_memory():
    """メモリの最適化"""
    gc.collect()  # ガベージコレクションの実行
    
    # 大きなオブジェクトの削除
    large_objects = [obj for obj in gc.get_objects() if sys.getsizeof(obj) > 1000000]
    for obj in large_objects:
        del obj
    
    gc.collect()  # 再度ガベージコレクション

# 使用例
# 大量データ処理後
optimize_memory()
```

## ⚡ ネットワーク最適化

### 1. HTMLサイズの最適化

```python
# HTMLサイズの最適化
def optimize_html_size(html_content, max_size=1000000):
    """HTMLサイズを最適化"""
    if len(html_content) > max_size:
        # 不要な空白や改行を削除
        import re
        optimized_html = re.sub(r'\s+', ' ', html_content)
        optimized_html = re.sub(r'>\s+<', '><', optimized_html)
        return optimized_html
    return html_content

# 使用例
chart = ChartComponent(data=df, chart_type='line', x_column='date', y_column='sales')
html_content = chart.render()
optimized_html = optimize_html_size(html_content)
displayHTML(optimized_html)
```

### 2. 外部リソースの最適化

```python
# 外部リソースの最適化
def optimize_external_resources(html_content):
    """外部リソースを最適化"""
    # CDNの使用
    html_content = html_content.replace(
        'https://cdn.plot.ly/plotly-latest.min.js',
        'https://cdn.jsdelivr.net/npm/plotly.js@2.0.0/dist/plotly.min.js'
    )
    return html_content
```

## 🔧 プロファイリングと監視

### 1. パフォーマンスの測定

```python
import time
import psutil
import os

# パフォーマンス測定
def measure_performance(func, *args, **kwargs):
    """関数のパフォーマンスを測定"""
    start_time = time.time()
    start_memory = psutil.Process(os.getpid()).memory_info().rss
    
    result = func(*args, **kwargs)
    
    end_time = time.time()
    end_memory = psutil.Process(os.getpid()).memory_info().rss
    
    execution_time = end_time - start_time
    memory_usage = end_memory - start_memory
    
    print(f"実行時間: {execution_time:.2f}秒")
    print(f"メモリ使用量: {memory_usage / 1024 / 1024:.2f}MB")
    
    return result

# 使用例
def create_chart():
    return ChartComponent(data=df, chart_type='line', x_column='date', y_column='sales')

chart = measure_performance(create_chart)
```

### 2. メモリ使用量の監視

```python
# メモリ使用量の監視
def monitor_memory_usage():
    """メモリ使用量を監視"""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    
    print(f"RSS: {memory_info.rss / 1024 / 1024:.2f}MB")
    print(f"VMS: {memory_info.vms / 1024 / 1024:.2f}MB")
    print(f"使用可能メモリ: {psutil.virtual_memory().available / 1024 / 1024:.2f}MB")

# 使用例
monitor_memory_usage()
```

## 📈 実践的な最適化例

### 1. 大規模ダッシュボードの最適化

```python
# 大規模ダッシュボードの最適化
def create_optimized_dashboard(large_dataset):
    """大規模データセット用の最適化されたダッシュボード"""
    
    # 1. データの前処理
    processed_data = optimize_data_types(large_dataset)
    sampled_data = limit_data_size(processed_data, 10000)
    
    # 2. 集約データの作成
    daily_data = aggregate_time_series(sampled_data, 'date', 'sales', 'D')
    category_data = sampled_data.groupby('category')['sales'].sum().reset_index()
    
    # 3. コンポーネントの作成（遅延レンダリング）
    components = [
        LazyChartComponent(data=daily_data, chart_type='line', x_column='date', y_column='sales'),
        LazyChartComponent(data=category_data, chart_type='pie', x_column='category', y_column='sales'),
        TableComponent(data=sampled_data.head(100))
    ]
    
    # 4. バッチレンダリング
    dashboard_html = render_components_batch(components)
    
    # 5. HTML最適化
    optimized_html = optimize_html_size(dashboard_html)
    
    return optimized_html

# 使用例
large_df = spark.sql("SELECT * FROM large_sales_table").toPandas()
dashboard_html = create_optimized_dashboard(large_df)
displayHTML(dashboard_html)
```

### 2. リアルタイム更新の最適化

```python
# リアルタイム更新の最適化
class OptimizedRealTimeDashboard:
    def __init__(self, initial_data):
        self.data = initial_data
        self.charts = {}
        self.last_update = time.time()
        self.update_interval = 30  # 30秒間隔
    
    def should_update(self):
        """更新が必要かどうかを判定"""
        return time.time() - self.last_update > self.update_interval
    
    def update_charts(self, new_data):
        """チャートを更新（最適化版）"""
        if not self.should_update():
            return
        
        # 差分データのみを処理
        new_records = new_data[new_data['timestamp'] > self.data['timestamp'].max()]
        
        if len(new_records) > 0:
            # 最新の1000件のみを保持
            self.data = pd.concat([self.data, new_records]).tail(1000)
            
            # チャートの更新
            for chart_name, chart in self.charts.items():
                chart.update_data(self.data)
            
            self.last_update = time.time()
    
    def render(self):
        """ダッシュボードをレンダリング"""
        return render_components_batch(self.charts.values())

# 使用例
dashboard = OptimizedRealTimeDashboard(initial_data)
# 定期的にupdate_chartsを呼び出して更新
```

## 🚀 次のステップ

- [セキュリティ](./security.md) - セキュリティのベストプラクティス
- [デプロイメント](./deployment.md) - 本番環境へのデプロイ
- [トラブルシューティング](../troubleshooting/faq.md) - パフォーマンス関連のFAQ

## ❓ サポート

パフォーマンス最適化で問題が発生した場合は、以下を確認してください：

- [よくある問題](../troubleshooting/faq.md)
- [エラーリファレンス](../troubleshooting/errors.md)
- [GitHub Issues](https://github.com/databricks/db-ui-components/issues)