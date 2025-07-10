# インストールガイド

このドキュメントでは、`db-ui-components`パッケージのインストール方法を説明します。

## 前提条件

- Python 3.8以上
- pip（Pythonパッケージマネージャー）

## インストール方法

### 1. PyPIからのインストール（推奨）

```bash
pip install db-ui-components
```

### 2. 開発版のインストール

#### GitHubから直接インストール

```bash
pip install git+https://github.com/y-nishizaki/db-ui-components.git
```

#### ローカルでビルドしてインストール

```bash
# リポジトリをクローン
git clone https://github.com/y-nishizaki/db-ui-components.git
cd db-ui-components

# 開発モードでインストール（推奨）
pip install -e .

# または、通常のインストール
pip install .
```

### 3. Databricksノートブックでの使用

#### ノートブック内で直接インストール

```python
# 安定版をインストール
!pip install db-ui-components

# または、開発版をインストール
!pip install git+https://github.com/y-nishizaki/db-ui-components.git
```

#### ファイルをアップロードして使用

1. リポジトリをクローン
2. `db_ui_components`フォルダをDatabricksにアップロード
3. パスを追加

```python
import sys
sys.path.append('/dbfs/your-path/db-ui-components')
```

## 依存関係

このパッケージは以下の依存関係が必要です：

- pandas>=1.5.0
- numpy>=1.21.0
- plotly>=5.0.0
- dash>=2.0.0
- dash-bootstrap-components>=1.0.0
- dash-table>=5.0.0
- flask>=2.0.0
- jinja2>=3.0.0

## インストールの確認

インストールが成功したかどうかを確認するには：

```python
# パッケージをインポート
import db_ui_components

# バージョンを確認
print(f"バージョン: {db_ui_components.__version__}")

# 利用可能なコンポーネントを確認
print(f"コンポーネント: {db_ui_components.__all__}")
```

## トラブルシューティング

### 権限エラーが発生する場合

```bash
# ユーザーディレクトリにインストール
pip install --user db-ui-components
```

### 仮想環境を使用する場合

```bash
# 仮想環境を作成
python -m venv venv

# 仮想環境をアクティベート
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# パッケージをインストール
pip install db-ui-components
```

### 依存関係の競合が発生する場合

```bash
# 既存のパッケージをアンインストール
pip uninstall db-ui-components

# 依存関係を確認してから再インストール
pip install db-ui-components
```

## 開発者向けインストール

開発に参加する場合は、以下の手順でセットアップしてください：

```bash
# リポジトリをクローン
git clone https://github.com/y-nishizaki/db-ui-components.git
cd db-ui-components

# 開発依存関係を含めてインストール
pip install -e ".[dev]"

# テストを実行
python -m pytest

# コードフォーマット
black db_ui_components tests
```

## アンインストール

```bash
pip uninstall db-ui-components
```

## サポート

インストールで問題が発生した場合は、以下をご確認ください：

1. Pythonのバージョン（3.8以上が必要）
2. pipのバージョン
3. 依存関係の競合
4. ネットワーク接続（GitHubからのインストール時）

問題が解決しない場合は、GitHubのIssuesページで報告してください。