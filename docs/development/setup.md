# 開発環境セットアップガイド

このガイドでは、Databricks UI Component Libraryの開発環境を構築する方法を詳しく説明します。

## 🚀 前提条件

### 必要なソフトウェア

- **Python**: 3.8以上
- **Git**: 最新版
- **pip**: 最新版
- **仮想環境管理ツール**: venv, conda, pyenv等

### 推奨環境

- **OS**: macOS, Linux, Windows
- **メモリ**: 8GB以上
- **ストレージ**: 2GB以上の空き容量
- **エディタ**: VS Code, PyCharm, Vim等

## 📋 セットアップ手順

### 1. リポジトリのクローン

```bash
# リポジトリをクローン
git clone https://github.com/your-username/db-ui-components.git
cd db-ui-components

# リモートの確認
git remote -v
```

### 2. 仮想環境の作成

#### venvを使用する場合（推奨）

```bash
# 仮想環境を作成
python -m venv venv

# 仮想環境をアクティベート
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

#### condaを使用する場合

```bash
# conda環境を作成
conda create -n db-ui-dev python=3.9

# 環境をアクティベート
conda activate db-ui-dev
```

#### pyenvを使用する場合

```bash
# Pythonバージョンをインストール
pyenv install 3.9.7

# ローカルバージョンを設定
pyenv local 3.9.7

# 仮想環境を作成
python -m venv venv
source venv/bin/activate
```

### 3. 依存関係のインストール

```bash
# 開発用依存関係を含めてインストール
pip install -e ".[dev]"

# または、個別にインストール
pip install -e .
pip install -r requirements-dev.txt
```

### 4. 開発用ツールのセットアップ

```bash
# pre-commitフックのインストール
pre-commit install

# 開発用ツールの確認
python -c "import pytest, black, flake8, mypy; print('開発ツールが正しくインストールされました')"
```

## 🔧 開発環境の確認

### 1. 基本的な確認

```bash
# Pythonバージョンの確認
python --version

# pipバージョンの確認
pip --version

# 仮想環境の確認
which python  # macOS/Linux
where python  # Windows
```

### 2. パッケージの確認

```bash
# インストールされたパッケージの確認
pip list

# 開発用パッケージの確認
pip list | grep -E "(pytest|black|flake8|mypy|pre-commit)"
```

### 3. インポートテスト

```python
# 基本的なインポートテスト
try:
    from db_ui_components import ChartComponent, TableComponent, FilterComponent, Dashboard
    print("✓ 基本コンポーネントのインポート成功")
except ImportError as e:
    print(f"✗ インポートエラー: {e}")

# 開発用ツールのテスト
try:
    import pytest
    import black
    import flake8
    import mypy
    print("✓ 開発用ツールのインポート成功")
except ImportError as e:
    print(f"✗ 開発用ツールのインポートエラー: {e}")
```

## 🧪 テスト環境のセットアップ

### 1. テストの実行

```bash
# 全テストの実行
pytest

# 特定のテストファイル
pytest tests/test_chart_component.py

# カバレッジ付きで実行
pytest --cov=db_ui_components --cov-report=html

# パフォーマンステスト
pytest tests/test_performance.py
```

### 2. テストデータの準備

```python
# テスト用データの作成
import pandas as pd
import numpy as np

def create_test_data():
    """テスト用データを作成"""
    np.random.seed(42)
    dates = pd.date_range('2024-01-01', periods=100, freq='D')
    
    data = {
        'date': dates,
        'sales': np.random.normal(1000, 200, 100),
        'profit': np.random.normal(200, 50, 100),
        'category': np.random.choice(['A', 'B', 'C'], 100),
        'region': np.random.choice(['North', 'South', 'East', 'West'], 100)
    }
    
    return pd.DataFrame(data)

# テストデータの確認
test_df = create_test_data()
print(f"テストデータ形状: {test_df.shape}")
print(f"テストデータ列: {test_df.columns.tolist()}")
```

## 🔍 コード品質ツールの設定

### 1. Black（コードフォーマット）

```bash
# コードフォーマットの実行
black db_ui_components/

# 特定ファイルのフォーマット
black db_ui_components/chart_component.py

# 設定の確認
black --version
```

### 2. Flake8（リンター）

```bash
# リンターの実行
flake8 db_ui_components/

# 特定ファイルのリンター
flake8 db_ui_components/chart_component.py

# 設定の確認
flake8 --version
```

### 3. MyPy（型チェック）

```bash
# 型チェックの実行
mypy db_ui_components/

# 特定ファイルの型チェック
mypy db_ui_components/chart_component.py

# 設定の確認
mypy --version
```

### 4. Pre-commit（Gitフック）

```bash
# pre-commitフックの確認
pre-commit run --all-files

# 特定のフックの実行
pre-commit run black
pre-commit run flake8
pre-commit run mypy
```

## 📝 エディタ設定

### VS Code設定

`.vscode/settings.json`を作成：

```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": [
        "tests"
    ],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

### PyCharm設定

1. **プロジェクト設定**
   - File → Settings → Project → Python Interpreter
   - 仮想環境を選択

2. **コードスタイル**
   - File → Settings → Editor → Code Style → Python
   - Blackフォーマッターを設定

3. **リンター設定**
   - File → Settings → Tools → External Tools
   - Flake8とMyPyを追加

## 🚀 開発ワークフロー

### 1. ブランチの作成

```bash
# 最新のmainブランチを取得
git checkout main
git pull origin main

# 新しいブランチを作成
git checkout -b feature/your-feature-name
```

### 2. 開発・テスト

```bash
# コードの変更
# ...

# テストの実行
pytest

# コード品質チェック
black db_ui_components/
flake8 db_ui_components/
mypy db_ui_components/
```

### 3. コミット

```bash
# 変更をステージング
git add .

# コミット
git commit -m "feat: add new feature

- Add new functionality
- Include tests
- Update documentation"
```

### 4. プルリクエスト

```bash
# プッシュ
git push origin feature/your-feature-name

# GitHubでプルリクエストを作成
```

## 🔧 トラブルシューティング

### 1. 依存関係の問題

```bash
# 依存関係の競合を解決
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 仮想環境を再作成
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### 2. テストの問題

```bash
# テスト環境の確認
pytest --version
python -c "import pytest; print(pytest.__version__)"

# テストの詳細実行
pytest -v tests/

# 特定のテストのみ実行
pytest -k "test_chart_component" tests/
```

### 3. コード品質ツールの問題

```bash
# ツールのバージョン確認
black --version
flake8 --version
mypy --version

# 設定ファイルの確認
ls -la pyproject.toml .flake8 .mypy.ini
```

## 📚 開発リソース

### 1. ドキュメント

- [コントリビューションガイド](./contributing.md)
- [テスト](./testing.md)
- [リリースプロセス](./release.md)

### 2. コミュニティ

- **GitHub Issues**: バグ報告・機能要望
- **GitHub Discussions**: 質問・議論
- **Pull Requests**: コードレビュー

### 3. 学習リソース

- **Python公式ドキュメント**: https://docs.python.org/
- **pytest公式ドキュメント**: https://docs.pytest.org/
- **Black公式ドキュメント**: https://black.readthedocs.io/

## 🎯 次のステップ

開発環境のセットアップが完了したら：

1. **基本的なテストの実行**
2. **サンプルコードの作成**
3. **ドキュメントの確認**
4. **コミュニティへの参加**

**関連リンク:**
- [コントリビューションガイド](./contributing.md) - 開発のガイドライン
- [テスト](./testing.md) - テストの実行方法
- [リリースプロセス](./release.md) - リリースの手順