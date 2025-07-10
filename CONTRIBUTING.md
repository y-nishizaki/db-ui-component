# コントリビューションガイド

Databricks UI Componentsへのコントリビューションをありがとうございます！このガイドでは、プロジェクトへの貢献方法を説明します。

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
git clone https://github.com/y-nishizaki/db-ui-components.git
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
```

## 🔍 テスト

### テストの実行

```bash
# 全テストの実行
pytest

# 特定のテストファイル
pytest tests/test_chart_component.py

# カバレッジ付き
pytest --cov=db_ui_components

# 詳細出力
pytest -v
```

### テストの追加

新しい機能を追加する際は、必ずテストも追加してください：

```python
def test_chart_component_creation():
    """ChartComponentの作成テスト"""
    df = pd.DataFrame({'x': [1, 2, 3], 'y': [1, 4, 9]})
    chart = ChartComponent(data=df, chart_type='line', x_column='x', y_column='y')
    
    assert chart.data is not None
    assert chart.chart_type == 'line'
    assert chart.x_column == 'x'
    assert chart.y_column == 'y'
```

## 📚 ドキュメント

### ドキュメントの更新

コードの変更に伴い、関連するドキュメントも更新してください：

- README.md
- APIドキュメント
- チュートリアル
- インストールガイド

### ドキュメントの確認

```bash
# ドキュメントの構文チェック
python -m pydocstyle docs/

# リンクの確認
python -m linkchecker docs/
```

## 🚀 リリースプロセス

### 1. バージョンの更新

```bash
# pyproject.tomlのバージョンを更新
# __init__.pyの__version__を更新
```

### 2. 変更履歴の更新

```bash
# CHANGELOG.mdに変更内容を追加
```

### 3. リリースの作成

```bash
# タグの作成
git tag v1.1.0

# プッシュ
git push origin v1.1.0
```

## 🤝 コミュニティ

### 質問・議論

- [GitHub Issues](https://github.com/y-nishizaki/db-ui-components/issues)
- [GitHub Discussions](https://github.com/y-nishizaki/db-ui-components/discussions)

### 行動規範

このプロジェクトは、すべての貢献者に対して友好的で歓迎的な環境を提供することを約束します。

## 📖 詳細情報

より詳しい開発情報については、[開発ガイド](docs/development/)をご覧ください。 