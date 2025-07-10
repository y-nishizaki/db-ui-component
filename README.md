# Databricks UI Components

[![CI/CD Pipeline](https://github.com/y-nishizaki/db-ui-components/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/y-nishizaki/db-ui-components/actions)
[![PyPI version](https://badge.fury.io/py/db-ui-components.svg)](https://badge.fury.io/py/db-ui-components)
[![Python Versions](https://img.shields.io/pypi/pyversions/db-ui-components.svg)](https://pypi.org/project/db-ui-components/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

DatabricksノートブックやPython環境で美しいダッシュボードやインタラクティブな可視化を簡単に作成できるUIコンポーネントライブラリです。

## 特徴
- Databricksの`displayHTML`で即表示
- グラフ・テーブル・フィルター・ダッシュボード等の豊富なコンポーネント
- CSVダウンロード・検索・ソート・ページネーション等の便利機能
- Databricks SQLやPySpark連携
- 高度な可視化（サンキーチャート、ヒートマップ、ネットワークグラフ等）
- カスタマイズ・イベントハンドリング対応

## クイックスタート

```bash
pip install db-ui-components
```

```python
from db_ui_components import ChartComponent, TableComponent
import pandas as pd

df = pd.DataFrame({
    'x': range(10),
    'y': range(10)
})
chart = ChartComponent(data=df, chart_type='line', x_column='x', y_column='y')
displayHTML(chart.render())
```

## ドキュメント
- [インストールガイド](docs/guides/installation.md)
- [クイックスタート](docs/tutorials/quickstart.md)
- [APIリファレンス](docs/api/)
- [トラブルシューティング](docs/troubleshooting/faq.md)
- [コントリビューションガイド](docs/development/contributing.md)

---

より詳しい使い方・高度な機能・開発参加方法は上記リンクや`docs/`配下をご覧ください。

## ライセンス
MIT License

## 開発状況

### CI/CDパイプライン
- ✅ GitHub Actionsによる自動テスト（Python 3.10, 3.11, 3.12）
- ✅ コード品質チェック（flake8, black, mypy）
- ✅ 自動デプロイ（TestPyPI, PyPI）
- ✅ テストカバレッジレポート

### テスト
- 21個のテストファイル
- 主要コンポーネントの単体テスト・統合テスト
- パフォーマンステスト・エッジケーステスト

## サポート
ご質問・不具合は[GitHub Issues](https://github.com/y-nishizaki/db-ui-components/issues)まで。

## コントリビューション
プルリクエスト歓迎です！[コントリビューションガイド](docs/development/contributing.md)をご覧ください。 