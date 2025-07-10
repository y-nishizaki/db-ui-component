# Databricks UI Component Library

Databricksでノートブックからダッシュボードを作成する際に使用できる、便利なUIコンポーネントライブラリです。

## インストール

### PyPIからのインストール（推奨）

```bash
pip install db-ui-components
```

### 開発版のインストール

```bash
# GitHubから直接インストール
pip install git+https://github.com/y-nishizaki/db-ui-components.git

# または、ローカルでビルドしてインストール
git clone https://github.com/y-nishizaki/db-ui-components.git
cd db-ui-components
pip install -e .
```

### Databricksノートブックでの使用

```python
# ノートブック内で直接インストール
!pip install db-ui-components

# または、開発版をインストール
!pip install git+https://github.com/y-nishizaki/db-ui-components.git
```

**特徴:**
- 🎯 Databricksの`displayHTML`関数で直接表示可能
- 📊 データを渡すとHTMLが自動生成される
- 🚀 ノートブック内で簡単に美しいダッシュボードを作成
- 💡 インタラクティブなグラフ・テーブル・フィルター機能

## 概要

このライブラリは、Databricksのダッシュボードでよく使用される以下のようなコンポーネントを提供します：

- 📊 インタラクティブなグラフ・チャート
- 📋 CSVダウンロード機能付きテーブル
- 🔍 フィルター・検索機能
- 📈 リアルタイムデータ更新
- 🎨 カスタマイズ可能なスタイリング
- 🎯 `displayHTML`で直接表示可能

## 機能

### グラフ・チャートコンポーネント
- 折れ線グラフ
- 棒グラフ
- 円グラフ
- 散布図
- ヒートマップ
- 時系列グラフ

### 高度な可視化コンポーネント
- サンキーチャート（データフロー可視化）
- ヒートマップ（相関分析）
- ネットワークグラフ（関係性可視化）
- ツリーマップ（階層データ可視化）
- バブルチャート（3次元データ可視化）

### テーブルコンポーネント
- CSVダウンロード機能
- ソート機能
- ページネーション
- 検索・フィルター機能
- カスタム列表示

### フィルターコンポーネント
- 日付範囲フィルター
- ドロップダウンフィルター
- マルチセレクトフィルター
- テキスト検索フィルター

### データベースアクセスコンポーネント
- Databricks SQL接続
- テーブル一覧表示
- SQLクエリ実行
- テーブルスキーマ取得
- データプレビュー機能
- PySpark統合
- クエリキャッシュ機能

## 使用方法

### 基本的な使用例

```python
# 1. ライブラリをインポート
from db_ui_components import ChartComponent, TableComponent

# 2. データを準備
import pandas as pd
df = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=30, freq='D'),
    'value': [100 + i * 2 + np.random.randn() for i in range(30)]
})

# 3. コンポーネントを作成
chart = ChartComponent(
    data=df,
    chart_type='line',
    x_column='date',
    y_column='value',
    title='売上推移'
)

# 4. displayHTMLで表示
displayHTML(chart.render())
```

### テーブルの例

```python
# CSVダウンロード機能付きテーブル
table = TableComponent(
    data=df,
    enable_csv_download=True,
    sortable=True,
    searchable=True
)

displayHTML(table.render())
```

### ダッシュボードでの使用

```python
# ダッシュボードにコンポーネントを追加
dashboard = Dashboard()
dashboard.add_component(chart, position=(0, 0))
dashboard.add_component(table, position=(1, 0))

# displayHTMLでダッシュボード全体を表示
displayHTML(dashboard.render())
```

## コンポーネント一覧

### ChartComponent
グラフ・チャートを表示するコンポーネント

**パラメータ:**
- `data`: データフレーム
- `chart_type`: グラフタイプ ('line', 'bar', 'pie', 'scatter', 'heatmap')
- `x_column`: X軸の列名
- `y_column`: Y軸の列名
- `title`: グラフのタイトル
- `height`: グラフの高さ（ピクセル）

**使用例:**
```python
chart = ChartComponent(data=df, chart_type='line', x_column='date', y_column='value')
displayHTML(chart.render())
```

### TableComponent
データテーブルを表示するコンポーネント

**パラメータ:**
- `data`: データフレーム
- `enable_csv_download`: CSVダウンロード機能の有効化
- `sortable`: ソート機能の有効化
- `searchable`: 検索機能の有効化
- `page_size`: 1ページあたりの表示件数
- `columns`: 表示する列の指定

**使用例:**
```python
table = TableComponent(data=df, enable_csv_download=True, sortable=True)
displayHTML(table.render())
```

### FilterComponent
フィルター機能を提供するコンポーネント

**パラメータ:**
- `filter_type`: フィルタータイプ ('date', 'dropdown', 'multiselect', 'text')
- `options`: フィルターオプション
- `placeholder`: プレースホルダーテキスト

**使用例:**
```python
filter_comp = FilterComponent(filter_type='dropdown', column='category', options=['A', 'B', 'C'])
displayHTML(filter_comp.render())
```

### DatabaseComponent
Databricksデータベースアクセスを提供するコンポーネント

**パラメータ:**
- `component_id`: コンポーネントID
- `workspace_url`: DatabricksワークスペースURL
- `token`: Databricksアクセストークン
- `catalog`: カタログ名
- `schema`: スキーマ名

**使用例:**
```python
# 環境変数から認証情報を取得
import os
db = DatabaseComponent(
    component_id="my-db",
    workspace_url=os.getenv('DATABRICKS_WORKSPACE_URL'),
    token=os.getenv('DATABRICKS_TOKEN'),
    catalog="hive_metastore",
    schema="default"
)

# テーブル一覧を取得
tables = db.get_tables()

# SQLクエリを実行
result = db.execute_query("SELECT * FROM my_table LIMIT 100")

# テーブル統計を取得
stats = db.get_table_stats("my_table")

# displayHTMLで表示
displayHTML(db.render())
```

### SparkComponent
PySparkを使用したDatabricks接続コンポーネント

**パラメータ:**
- `component_id`: コンポーネントID
- `spark_config`: Spark設定辞書

**使用例:**
```python
spark = SparkComponent(
    component_id="my-spark",
    spark_config={
        "spark.sql.adaptive.enabled": "true",
        "spark.sql.adaptive.coalescePartitions.enabled": "true"
    }
)

# テーブルを読み込み
df = spark.read_table("my_table")

# SQLクエリを実行
result = spark.execute_sql("SELECT * FROM my_table")

# displayHTMLで表示
displayHTML(spark.render())
```

## カスタマイズ

### スタイリングのカスタマイズ

```python
# カスタムスタイルの適用
chart.set_style({
    'backgroundColor': '#f5f5f5',
    'borderRadius': '8px',
    'padding': '16px'
})

# displayHTMLで表示
displayHTML(chart.render())
```

### イベントハンドリング

```python
# クリックイベントの処理
def on_chart_click(data):
    print(f"Clicked on: {data}")

chart.on_click(on_chart_click)

# displayHTMLで表示（イベントハンドラー付き）
displayHTML(chart.render())
```

## 開発

### 環境構築

```bash
# 開発環境のセットアップ
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
```

### テスト

```bash
# テストの実行
pytest tests/
```

### ビルド

```bash
# パッケージのビルド
python setup.py build
```

## 貢献

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。

## サポート

問題や質問がある場合は、[Issues](https://github.com/y-nishizaki/db-ui-components/issues)で報告してください。

## よくある質問

### Q: Databricksでどのように使用しますか？
A: ノートブック内で`displayHTML(component.render())`を呼び出すことで、コンポーネントを表示できます。

### Q: 複数のコンポーネントを同時に表示できますか？
A: はい、`Dashboard`コンポーネントを使用して複数のコンポーネントをレイアウトできます。

### Q: インタラクティブな機能は動作しますか？
A: はい、Plotly.jsを使用しているため、ズーム、パン、ホバーなどのインタラクティブ機能が利用できます。

### Q: データの更新はどうやって行いますか？
A: `component.update_data(new_df)`でデータを更新し、再度`displayHTML(component.render())`を呼び出してください。

### Q: カスタムCSSは適用できますか？
A: はい、`component.set_style()`でスタイルを設定できます。また、`displayHTML()`に直接CSSを含めることも可能です。

### Q: 高度な可視化コンポーネントはどのようなものがありますか？
A: サンキーチャート、ヒートマップ、ネットワークグラフ、ツリーマップ、バブルチャートなどの高度な可視化コンポーネントが利用できます。

## 高度な可視化コンポーネント

### SankeyChartComponent
データフローやプロセスフローを可視化するサンキーチャート

**パラメータ:**
- `source_column`: ソースノードの列名
- `target_column`: ターゲットノードの列名
- `value_column`: フロー値の列名
- `title`: チャートのタイトル
- `height`: チャートの高さ

**使用例:**
```python
from db_ui_components import SankeyChartComponent

sankey = SankeyChartComponent(
    source_column='source',
    target_column='target',
    value_column='value',
    title='データフロー図'
)
displayHTML(sankey.render(data))
```

### HeatmapComponent
2次元データの相関や分布を可視化するヒートマップ

**パラメータ:**
- `x_column`: X軸の列名
- `y_column`: Y軸の列名
- `value_column`: 値の列名
- `title`: チャートのタイトル
- `color_scale`: カラースケール

**使用例:**
```python
from db_ui_components import HeatmapComponent

heatmap = HeatmapComponent(
    x_column='x',
    y_column='y',
    value_column='value',
    title='相関ヒートマップ'
)
displayHTML(heatmap.render(data))
```

### NetworkGraphComponent
ノードとエッジの関係を可視化するネットワークグラフ

**パラメータ:**
- `source_column`: ソースノードの列名
- `target_column`: ターゲットノードの列名
- `weight_column`: エッジの重みの列名（オプション）
- `title`: チャートのタイトル

**使用例:**
```python
from db_ui_components import NetworkGraphComponent

network = NetworkGraphComponent(
    source_column='source',
    target_column='target',
    title='ネットワーク関係図'
)
displayHTML(network.render(data))
```

### TreemapComponent
階層構造を持つデータを可視化するツリーマップ

**パラメータ:**
- `labels_column`: ラベルの列名
- `parents_column`: 親要素の列名
- `values_column`: 値の列名
- `title`: チャートのタイトル

**使用例:**
```python
from db_ui_components import TreemapComponent

treemap = TreemapComponent(
    labels_column='labels',
    parents_column='parents',
    values_column='values',
    title='階層データ可視化'
)
displayHTML(treemap.render(data))
```

### BubbleChartComponent
3次元データを可視化するバブルチャート

**パラメータ:**
- `x_column`: X軸の列名
- `y_column`: Y軸の列名
- `size_column`: バブルサイズの列名
- `color_column`: カラー分けの列名（オプション）
- `title`: チャートのタイトル

**使用例:**
```python
from db_ui_components import BubbleChartComponent

bubble = BubbleChartComponent(
    x_column='x',
    y_column='y',
    size_column='size',
    color_column='color',
    title='3次元データ可視化'
)
displayHTML(bubble.render(data))
```

## 更新履歴

### v1.0.0
- 初期リリース
- 基本的なグラフ・テーブルコンポーネント
- CSVダウンロード機能
- フィルター機能
- Databricks `displayHTML`対応
- 高度な可視化コンポーネント
  - サンキーチャート
  - ヒートマップ
  - ネットワークグラフ
  - ツリーマップ
  - バブルチャート

## ライセンス

MIT License - 詳細は[LICENSE](LICENSE)ファイルを参照してください。 