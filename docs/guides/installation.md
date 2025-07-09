# インストールガイド

このガイドでは、Databricks UI Component Libraryのインストール方法を詳しく説明します。

## 📋 前提条件

### 必要な環境

- **Python**: 3.8以上
- **pandas**: 1.5.0以上
- **numpy**: 1.21.0以上
- **plotly**: 5.0.0以上

### 推奨環境

- **Databricks Runtime**: 10.4以上
- **メモリ**: 4GB以上（大量データ処理時）
- **ストレージ**: 1GB以上の空き容量

## 🚀 インストール方法

### 1. PyPIからのインストール（推奨）

```bash
pip install db-ui-components
```

### 2. 開発版のインストール

```bash
# GitHubから直接インストール
pip install git+https://github.com/your-username/db-ui-components.git

# または、ローカルでビルドしてインストール
git clone https://github.com/your-username/db-ui-components.git
cd db-ui-components
pip install -e .
```

### 3. Databricksノートブックでのインストール

```python
# ノートブック内で直接インストール
!pip install db-ui-components

# または、開発版をインストール
!pip install git+https://github.com/your-username/db-ui-components.git
```

## 🔧 環境別インストール

### Databricks環境

#### Databricks Runtime 10.4以上

```python
# ノートブックの最初のセルで実行
!pip install db-ui-components

# インストール確認
import db_ui_components
print(f"バージョン: {db_ui_components.__version__}")
```

#### Databricks Runtime 10.4未満

```python
# 依存関係を個別にインストール
!pip install pandas>=1.5.0
!pip install numpy>=1.21.0
!pip install plotly>=5.0.0
!pip install dash>=2.0.0
!pip install db-ui-components
```

### ローカル環境

#### 仮想環境の作成（推奨）

```bash
# 仮想環境を作成
python -m venv db-ui-env

# 仮想環境をアクティベート
# Windows
db-ui-env\Scripts\activate

# macOS/Linux
source db-ui-env/bin/activate

# インストール
pip install db-ui-components
```

#### グローバルインストール

```bash
pip install db-ui-components
```

### Docker環境

```dockerfile
# Dockerfile
FROM python:3.9-slim

# 依存関係をインストール
RUN pip install db-ui-components

# アプリケーションコードをコピー
COPY . /app
WORKDIR /app

# アプリケーションを実行
CMD ["python", "app.py"]
```

## 📦 依存関係の詳細

### 必須依存関係

| パッケージ | バージョン | 用途 |
|-----------|-----------|------|
| pandas | >=1.5.0 | データ処理 |
| numpy | >=1.21.0 | 数値計算 |
| plotly | >=5.0.0 | グラフ描画 |
| dash | >=2.0.0 | Webアプリケーションフレームワーク |
| dash-bootstrap-components | >=1.0.0 | UIコンポーネント |
| dash-table | >=5.0.0 | テーブルコンポーネント |
| flask | >=2.0.0 | Webサーバー |
| jinja2 | >=3.0.0 | テンプレートエンジン |

### 開発用依存関係

```bash
# 開発用パッケージをインストール
pip install db-ui-components[dev]
```

開発用パッケージには以下が含まれます：
- pytest: テスト実行
- black: コードフォーマット
- flake8: リンター
- mypy: 型チェック

## 🔍 インストール確認

### 基本的な確認

```python
# インポートテスト
try:
    from db_ui_components import ChartComponent, TableComponent, FilterComponent, Dashboard
    print("✓ インポート成功")
except ImportError as e:
    print(f"✗ インポート失敗: {e}")

# バージョン確認
import db_ui_components
print(f"バージョン: {db_ui_components.__version__}")
```

### 機能テスト

```python
import pandas as pd
import numpy as np
from db_ui_components import ChartComponent

# サンプルデータ
df = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=10, freq='D'),
    'value': np.random.randn(10)
})

# グラフコンポーネントのテスト
chart = ChartComponent(
    data=df,
    chart_type='line',
    x_column='date',
    y_column='value',
    title='テストグラフ'
)

# HTML生成テスト
html_output = chart.render()
print(f"✓ HTML生成成功（長さ: {len(html_output)}文字）")
```

## ⚠️ トラブルシューティング

### よくある問題

#### 1. ImportError: No module named 'db_ui_components'

**解決方法:**
```bash
# インストール確認
pip list | grep db-ui-components

# 再インストール
pip uninstall db-ui-components
pip install db-ui-components
```

#### 2. 依存関係の競合

**解決方法:**
```bash
# 仮想環境を使用
python -m venv fresh-env
source fresh-env/bin/activate  # macOS/Linux
pip install db-ui-components
```

#### 3. Databricksでの権限エラー

**解決方法:**
```python
# ユーザー権限でインストール
!pip install --user db-ui-components
```

#### 4. メモリ不足

**解決方法:**
```python
# クラスターの設定を確認
# Databricksクラスター設定でメモリを増やす
# または、データサイズを制限する
```

## 🔄 アップデート

### 最新版へのアップデート

```bash
# PyPIから最新版をインストール
pip install --upgrade db-ui-components

# 開発版にアップデート
pip install --upgrade git+https://github.com/your-username/db-ui-components.git
```

### 特定バージョンのインストール

```bash
# 特定バージョンをインストール
pip install db-ui-components==1.0.0

# バージョン範囲を指定
pip install "db-ui-components>=1.0.0,<2.0.0"
```

## 📚 次のステップ

インストールが完了したら、以下のドキュメントを参照してください：

- [クイックスタートガイド](../tutorials/quickstart.md) - 5分で始める
- [基本使用法](../tutorials/basic_usage.md) - 基本的な使用方法
- [Databricksでの使用](./databricks_usage.md) - Databricks環境での使用方法

## 🤝 サポート

インストールで問題が発生した場合は、以下を確認してください：

1. **Pythonバージョン**: `python --version`
2. **pipバージョン**: `pip --version`
3. **エラーメッセージ**: 完全なエラーメッセージをコピー
4. **環境情報**: OS、Python環境、Databricksバージョン

**関連リンク:**
- [よくある問題](../troubleshooting/faq.md) - インストール関連のFAQ
- [エラーリファレンス](../troubleshooting/errors.md) - エラーメッセージの説明