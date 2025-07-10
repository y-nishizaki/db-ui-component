# 開発環境セットアップ

このドキュメントでは、db-ui-componentsライブラリの開発環境をセットアップする方法を説明します。

## 前提条件

- Python 3.8以上
- Git
- pip（Pythonパッケージマネージャー）

## セットアップ手順

### 1. リポジトリのクローン

```bash
git clone https://github.com/y-nishizaki/db-ui-components.git
cd db-ui-components
```

### 2. 仮想環境の作成

```bash
# 仮想環境を作成
python -m venv venv

# 仮想環境をアクティベート
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. 依存関係のインストール

```bash
# 開発用依存関係を含めてインストール
pip install -e ".[dev]"
```

### 4. 開発用ツールのセットアップ

```bash
# pre-commitフックのインストール
pre-commit install

# テストの実行
pytest
```

## 開発ツール

### コードフォーマット

```bash
# Blackフォーマッター
black db_ui_components/ tests/

# isort（インポートの整理）
isort db_ui_components/ tests/
```

### リンター

```bash
# flake8（コード品質チェック）
flake8 db_ui_components/

# mypy（型チェック）
mypy db_ui_components/
```

### テスト

```bash
# 全テストの実行
pytest

# カバレッジ付き
pytest --cov=db_ui_components

# 特定のテストファイル
pytest tests/test_chart_component.py
```

## 開発ワークフロー

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

# コードフォーマット
black db_ui_components/
```

### 3. コミット

```bash
# 変更をステージング
git add .

# コミット
git commit -m "feat: add new feature"
```

### 4. プルリクエスト

```bash
# プッシュ
git push origin feature/your-feature-name

# GitHubでプルリクエストを作成
```

## 設定ファイル

### pyproject.toml

プロジェクトの設定は`pyproject.toml`で管理されています：

```toml
[tool.black]
line-length = 88
target-version = ['py38']

[tool.isort]
profile = "black"
line_length = 88

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

### .pre-commit-config.yaml

pre-commitフックの設定：

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

## トラブルシューティング

### 依存関係の競合

```bash
# 仮想環境を再作成
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### テストの失敗

```bash
# テストデータの確認
pytest -v

# 特定のテストを実行
pytest tests/test_chart_component.py::test_chart_creation -v
```

### コードフォーマットの問題

```bash
# 強制的にフォーマット
black --line-length=88 db_ui_components/ tests/

# インポートの整理
isort db_ui_components/ tests/
```

## IDE設定

### VS Code

`.vscode/settings.json`を作成：

```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

### PyCharm

1. 仮想環境を設定
2. Blackフォーマッターを設定
3. flake8リンターを設定

## デバッグ

### ログの設定

```python
import logging

# ログレベルを設定
logging.basicConfig(level=logging.DEBUG)

# コンポーネントのデバッグ
chart = ChartComponent(data=df, chart_type='line')
print(f"Chart config: {chart.__dict__}")
```

### テストのデバッグ

```bash
# 詳細なテスト出力
pytest -v -s

# 特定のテストをデバッグ
pytest tests/test_chart_component.py::test_chart_creation -v -s --pdb
```

## パフォーマンステスト

```bash
# パフォーマンステストの実行
pytest tests/test_performance.py

# メモリ使用量の確認
python -m memory_profiler tests/test_performance.py
```

## セキュリティテスト

```bash
# セキュリティテストの実行
pytest tests/test_security.py

# 依存関係の脆弱性チェック
safety check
```

## ドキュメント生成

```bash
# APIドキュメントの生成
pydoc -w db_ui_components

# Sphinxドキュメントの生成
cd docs
make html
```

## リリース準備

```bash
# テストの実行
pytest

# コードフォーマット
black db_ui_components/

# リンター
flake8 db_ui_components/

# 型チェック
mypy db_ui_components/

# ビルド
python setup.py build
```

## サポート

開発環境のセットアップで問題が発生した場合は、以下をご確認ください：

1. Pythonバージョン（3.8以上）
2. 仮想環境の設定
3. 依存関係の競合
4. 権限の問題

問題が解決しない場合は、[GitHub Issues](https://github.com/y-nishizaki/db-ui-components/issues)で報告してください。