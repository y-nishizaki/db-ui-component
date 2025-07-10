# インストールガイド

このガイドでは、Databricks UI Component Libraryの詳細なインストール手順を説明します。

## 📋 前提条件

### システム要件

- Python 3.8以上
- pip 20.0以上
- Databricks Runtime 10.0以上（Databricks環境の場合）

### 必要な依存関係

- pandas >= 1.5.0
- numpy >= 1.21.0
- plotly >= 5.0.0
- dash >= 2.0.0
- dash-bootstrap-components >= 1.0.0
- dash-table >= 5.0.0
- flask >= 2.0.0
- jinja2 >= 3.0.0

## 🚀 インストール方法

### 1. PyPIからのインストール（推奨）

```bash
# 最新版のインストール
pip install db-ui-components

# 特定バージョンのインストール
pip install db-ui-components==1.0.0

# 開発版のインストール
pip install db-ui-components --pre
```

### 2. GitHubからのインストール

```bash
# 最新版のインストール
pip install git+https://github.com/databricks/db-ui-components.git

# 特定ブランチのインストール
pip install git+https://github.com/databricks/db-ui-components.git@develop

# 特定コミットのインストール
pip install git+https://github.com/databricks/db-ui-components.git@commit_hash
```

### 3. ローカルからのインストール

```bash
# リポジトリのクローン
git clone https://github.com/databricks/db-ui-components.git
cd db-ui-components

# 開発モードでのインストール
pip install -e .

# 通常のインストール
pip install .
```

## 🏢 Databricks環境でのインストール

### Databricksノートブックでのインストール

```python
# ノートブック内で直接インストール
!pip install db-ui-components

# または、GitHubからインストール
!pip install git+https://github.com/databricks/db-ui-components.git
```

### Databricksクラスターでのインストール

#### 方法1: クラスターライブラリの追加

1. Databricksワークスペースにログイン
2. クラスター設定画面に移動
3. 「Libraries」タブを選択
4. 「Install New」をクリック
5. 「PyPI」を選択
6. パッケージ名に `db-ui-components` を入力
7. 「Install」をクリック

#### 方法2: init scriptの使用

```bash
#!/bin/bash
pip install db-ui-components
```

### Databricksジョブでのインストール

```python
# requirements.txtファイルに追加
db-ui-components>=1.0.0

# または、ジョブの設定で直接指定
```

## 🔧 開発環境のセットアップ

### 1. 開発用依存関係のインストール

```bash
# 開発用依存関係を含めてインストール
pip install db-ui-components[dev]

# または、個別にインストール
pip install pytest pytest-cov black flake8 mypy pre-commit
```

### 2. 仮想環境の作成

```bash
# venvを使用
python -m venv db-ui-components-env
source db-ui-components-env/bin/activate  # Linux/Mac
# または
db-ui-components-env\Scripts\activate  # Windows

# condaを使用
conda create -n db-ui-components-env python=3.9
conda activate db-ui-components-env
```

### 3. 開発用インストール

```bash
# リポジトリのクローン
git clone https://github.com/databricks/db-ui-components.git
cd db-ui-components

# 開発用インストール
pip install -e .

# テストの実行
pytest

# コードフォーマット
black .

# リント
flake8
```

## 🔍 インストールの確認

### 基本的な確認

```python
# インポートの確認
from db_ui_components import ChartComponent, TableComponent, Dashboard

# バージョンの確認
import db_ui_components
print(db_ui_components.__version__)
```

### 動作確認

```python
import pandas as pd
import numpy as np
from db_ui_components import ChartComponent

# サンプルデータの作成
df = pd.DataFrame({
    'x': range(10),
    'y': np.random.randn(10)
})

# コンポーネントの作成
chart = ChartComponent(
    data=df,
    chart_type='line',
    x_column='x',
    y_column='y',
    title='テストグラフ'
)

# レンダリングの確認
html_output = chart.render()
print("インストール成功！")
```

## 🛠️ トラブルシューティング

### よくある問題

#### 1. 依存関係の競合

```bash
# 競合するパッケージの確認
pip list | grep -E "(pandas|plotly|dash)"

# 仮想環境の使用を推奨
python -m venv fresh-env
source fresh-env/bin/activate
pip install db-ui-components
```

#### 2. 権限エラー

```bash
# ユーザー権限でのインストール
pip install --user db-ui-components

# または、sudoを使用（推奨されません）
sudo pip install db-ui-components
```

#### 3. ネットワークエラー

```bash
# プロキシ設定
pip install --proxy http://proxy.company.com:8080 db-ui-components

# または、ミラーサーバーの使用
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple db-ui-components
```

### Databricks固有の問題

#### 1. クラスターの再起動が必要

インストール後、クラスターを再起動してください。

#### 2. ライブラリの競合

```python
# 既存のライブラリとの競合を確認
import sys
print(sys.path)

# 必要に応じてパスの調整
import db_ui_components
```

## 📦 アンインストール

```bash
# パッケージのアンインストール
pip uninstall db-ui-components

# 依存関係も含めてアンインストール
pip uninstall -y db-ui-components pandas plotly dash
```

## 🔄 アップデート

```bash
# 最新版へのアップデート
pip install --upgrade db-ui-components

# 特定バージョンへのアップデート
pip install --upgrade db-ui-components==1.1.0
```

## 📚 次のステップ

インストールが完了したら、以下のドキュメントを参照してください：

- [クイックスタートガイド](../tutorials/quickstart.md) - 5分で始める
- [基本使用法](../tutorials/basic_usage.md) - 基本的な使用方法
- [Databricksでの使用](./databricks_usage.md) - Databricks環境での使用方法

## ❓ サポート

インストールで問題が発生した場合は、以下を確認してください：

- [よくある問題](../troubleshooting/faq.md)
- [エラーリファレンス](../troubleshooting/errors.md)
- [GitHub Issues](https://github.com/databricks/db-ui-components/issues)