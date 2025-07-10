# CI/CD セットアップガイド

このドキュメントでは、db-ui-componentsパッケージのCI/CDパイプラインの設定と使用方法について説明します。

## 概要

このプロジェクトでは、GitHub Actionsを使用して以下の自動化を実現しています：

- **テスト**: 複数のPythonバージョンでの自動テスト
- **コード品質チェック**: リンティング、フォーマットチェック、型チェック
- **セキュリティチェック**: 依存関係の脆弱性チェック
- **自動配布**: PyPIへの自動アップロード
- **リリース管理**: バージョン管理とリリースノートの自動生成

## ワークフロー

### 1. CI/CD Pipeline (`.github/workflows/ci.yml`)

**トリガー**:
- `main`、`develop`ブランチへのプッシュ
- プルリクエスト
- リリースの公開

**実行内容**:
- 複数Pythonバージョンでのテスト
- コード品質チェック
- パッケージのビルドとテスト
- PyPIへの自動配布（リリース時のみ）

### 2. Development Workflow (`.github/workflows/dev.yml`)

**トリガー**:
- `develop`、`feature/*`、`hotfix/*`ブランチへのプッシュ
- プルリクエスト

**実行内容**:
- テストとコード品質チェック
- セキュリティチェック
- パッケージのビルドテスト

### 3. Manual Release (`.github/workflows/manual-release.yml`)

**トリガー**: 手動実行

**実行内容**:
- バージョン更新
- パッケージのビルド
- PyPI/TestPyPIへの配布
- GitHubリリースの作成

## セットアップ手順

### 1. PyPI API トークンの取得

#### PyPI トークン
1. [PyPI](https://pypi.org)にログイン
2. Account Settings → API tokens
3. Add API token
4. トークンをコピー

#### TestPyPI トークン
1. [TestPyPI](https://test.pypi.org)にログイン
2. Account Settings → API tokens
3. Add API token
4. トークンをコピー

### 2. GitHub Secrets の設定

GitHubリポジトリの Settings → Secrets and variables → Actions で以下を設定：

```
PYPI_API_TOKEN: PyPIのAPIトークン
TEST_PYPI_API_TOKEN: TestPyPIのAPIトークン
```

### 3. ローカル設定

#### `.pypirc` ファイルの設定
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = your-pypi-api-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = your-testpypi-api-token-here
```

## 使用方法

### 自動リリース

1. リリース用のタグを作成
2. GitHubでリリースを作成
3. CI/CDが自動的にPyPIにアップロード

```bash
# リリーススクリプトを使用
python scripts/release.py 1.0.1 "Bug fixes and improvements"
```

### 手動リリース

1. GitHub Actions → Manual Release
2. バージョンとリリースノートを入力
3. 実行

### 開発ワークフロー

1. 機能ブランチを作成
2. 変更をコミット・プッシュ
3. プルリクエストを作成
4. CI/CDが自動でテストを実行

## ファイル構成

```
.github/
├── workflows/
│   ├── ci.yml              # メインCI/CDパイプライン
│   ├── dev.yml             # 開発用ワークフロー
│   └── manual-release.yml  # 手動リリース用
scripts/
└── release.py              # リリーススクリプト
.pypirc                     # PyPI設定ファイル
```

## トラブルシューティング

### よくある問題

1. **PyPIアップロードエラー**
   - APIトークンが正しく設定されているか確認
   - パッケージ名が重複していないか確認

2. **テストエラー**
   - 依存関係が正しくインストールされているか確認
   - コードの構文エラーがないか確認

3. **ビルドエラー**
   - `pyproject.toml`の設定が正しいか確認
   - 必要なファイルが`MANIFEST.in`に含まれているか確認

### ログの確認

GitHub Actionsのログで以下を確認：
- テスト結果
- ビルドログ
- アップロードログ

## ベストプラクティス

1. **バージョン管理**
   - セマンティックバージョニングを使用
   - リリース前に十分なテストを実行

2. **セキュリティ**
   - APIトークンを定期的に更新
   - 依存関係の脆弱性を定期的にチェック

3. **品質管理**
   - コードレビューを必須にする
   - テストカバレッジを維持する

## 参考リンク

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyPI Documentation](https://packaging.python.org/tutorials/packaging-projects/)
- [TestPyPI Documentation](https://test.pypi.org/help/)