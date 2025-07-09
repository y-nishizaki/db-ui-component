# コントリビューションガイド

Databricks UI Component Libraryへのコントリビューションをありがとうございます！このガイドでは、プロジェクトへの貢献方法を説明します。

## 🤝 コントリビューションの種類

### 🐛 バグ報告
- バグの詳細な説明
- 再現手順
- 期待される動作
- 環境情報

### 💡 機能要望
- 新機能の提案
- ユースケースの説明
- 実装のアイデア

### 📝 ドキュメント改善
- ドキュメントの追加・修正
- 翻訳の提供
- サンプルコードの改善

### 🔧 コードコントリビューション
- バグ修正
- 新機能の実装
- パフォーマンス改善
- テストの追加

## 🚀 開発環境のセットアップ

### 1. リポジトリのクローン

```bash
git clone https://github.com/your-username/db-ui-components.git
cd db-ui-components
```

### 2. 仮想環境の作成

```bash
python -m venv venv

# アクティベート
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

## 📋 開発ワークフロー

### 1. ブランチの作成

```bash
# 最新のmainブランチを取得
git checkout main
git pull origin main

# 新しいブランチを作成
git checkout -b feature/your-feature-name
# または
git checkout -b fix/your-bug-fix
```

### 2. 開発・テスト

```bash
# コードの変更
# ...

# テストの実行
pytest

# リンターの実行
flake8 db_ui_components/

# 型チェック
mypy db_ui_components/

# コードフォーマット
black db_ui_components/
```

### 3. コミット

```bash
# 変更をステージング
git add .

# コミットメッセージの作成
git commit -m "feat: add new chart component

- Add support for bubble charts
- Include interactive tooltips
- Add comprehensive tests"
```

### 4. プルリクエストの作成

```bash
# プッシュ
git push origin feature/your-feature-name

# GitHubでプルリクエストを作成
```

## 📝 コーディング規約

### Pythonコード規約

#### 1. スタイルガイド
- **PEP 8**に準拠
- **Black**フォーマッターを使用
- 行長: 88文字以内

#### 2. 命名規則
```python
# クラス名: PascalCase
class ChartComponent:
    pass

# 関数・変数名: snake_case
def create_chart():
    chart_data = get_data()
    return chart_data

# 定数: UPPER_SNAKE_CASE
DEFAULT_HEIGHT = 400
SUPPORTED_CHART_TYPES = ['line', 'bar', 'pie']
```

#### 3. ドキュメント文字列
```python
def create_chart(data, chart_type, x_column, y_column):
    """
    グラフコンポーネントを作成します。
    
    Args:
        data (pd.DataFrame): グラフに表示するデータ
        chart_type (str): グラフのタイプ ('line', 'bar', 'pie')
        x_column (str): X軸に使用する列名
        y_column (str): Y軸に使用する列名
    
    Returns:
        ChartComponent: 作成されたグラフコンポーネント
    
    Raises:
        ValueError: 無効なグラフタイプが指定された場合
        KeyError: 指定された列が存在しない場合
    """
    pass
```

### コミットメッセージ規約

**Conventional Commits**形式を使用：

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### タイプ
- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメントのみの変更
- `style`: コードの意味に影響しない変更
- `refactor`: バグ修正や機能追加ではないコードの変更
- `test`: テストの追加や修正
- `chore`: ビルドプロセスや補助ツールの変更

#### 例
```
feat: add support for bubble charts

- Add BubbleChartComponent class
- Include size and color mapping options
- Add comprehensive tests for bubble chart functionality

Closes #123
```

## 🧪 テスト

### テストの実行

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

### テストの作成

```python
# tests/test_new_component.py
import pytest
import pandas as pd
import numpy as np
from db_ui_components import NewComponent

class TestNewComponent:
    """NewComponentのテストクラス"""
    
    def test_initialization(self):
        """初期化テスト"""
        df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        component = NewComponent(data=df)
        assert component.data is not None
        assert len(component.data) == 3
    
    def test_render(self):
        """レンダリングテスト"""
        df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        component = NewComponent(data=df)
        html = component.render()
        assert '<div' in html
        assert 'NewComponent' in html
    
    def test_edge_cases(self):
        """エッジケーステスト"""
        # 空のデータフレーム
        empty_df = pd.DataFrame()
        component = NewComponent(data=empty_df)
        assert component.data.empty
```

## 📚 ドキュメント

### ドキュメントの更新

1. **APIドキュメント**: `docs/api/`ディレクトリ
2. **チュートリアル**: `docs/tutorials/`ディレクトリ
3. **ガイド**: `docs/guides/`ディレクトリ

### ドキュメントの作成例

```markdown
# 新機能のドキュメント

## 概要
新機能の説明

## 使用方法
```python
from db_ui_components import NewComponent

component = NewComponent(data=df)
displayHTML(component.render())
```

## パラメータ
| パラメータ | 型 | 説明 |
|-----------|----|------|
| data | pd.DataFrame | データ |

## 使用例
具体的な使用例
```

## 🔍 コードレビュー

### レビューのポイント

1. **機能性**: 要件を満たしているか
2. **パフォーマンス**: 効率的な実装か
3. **セキュリティ**: セキュリティリスクがないか
4. **テスト**: 十分なテストが含まれているか
5. **ドキュメント**: ドキュメントが更新されているか

### レビューコメントの例

```python
# 良い例
# この関数は複雑すぎるので、小さな関数に分割することを検討してください

# 改善提案
def process_data(data):
    """データを処理する関数"""
    # データの検証
    validated_data = validate_data(data)
    
    # データの変換
    transformed_data = transform_data(validated_data)
    
    return transformed_data
```

## 🚀 リリースプロセス

### 1. バージョン管理

```bash
# バージョンの更新
# pyproject.toml の version を更新
# CHANGELOG.md を更新
```

### 2. テストの実行

```bash
# 全テストの実行
pytest

# パフォーマンステスト
pytest tests/test_performance.py

# セキュリティテスト
pytest tests/test_security.py
```

### 3. ドキュメントの更新

```bash
# ドキュメントの確認
# README.md の更新
# API ドキュメントの更新
```

### 4. リリース

```bash
# タグの作成
git tag v1.1.0

# プッシュ
git push origin v1.1.0
```

## 🤝 コミュニティ

### 質問・議論

- **GitHub Issues**: バグ報告・機能要望
- **GitHub Discussions**: 一般的な質問・議論
- **Pull Requests**: コードレビュー・改善提案

### 行動規範

1. **尊重**: 他のコントリビューターを尊重する
2. **建設的**: 建設的なフィードバックを提供する
3. **協力的**: チームワークを重視する
4. **学習**: お互いから学び合う

## 📞 サポート

コントリビューションに関する質問がある場合は：

1. **GitHub Issues**で質問
2. **GitHub Discussions**で議論
3. **ドキュメント**を確認

**関連リンク:**
- [開発環境セットアップ](./setup.md) - 詳細なセットアップ手順
- [テスト](./testing.md) - テストの実行方法
- [リリースプロセス](./release.md) - リリースの手順