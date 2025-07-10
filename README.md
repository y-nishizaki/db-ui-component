# Databricks UI Components

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

## サポート
ご質問・不具合は[GitHub Issues](https://github.com/y-nishizaki/db-ui-components/issues)まで。 