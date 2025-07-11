"""
可視化コンポーネントの基底クラス

SRPに準拠するため、可視化コンポーネントの共通責任を分離します。
"""

import json
import pandas as pd
from typing import Dict, Any, Optional
from ..base_component import BaseComponent
from ..exceptions import ComponentError


class BaseVisualizationComponent(BaseComponent):
    """
    可視化コンポーネントの基底クラス

    責任:
    - HTMLテンプレートの生成
    - JavaScriptコードの生成
    - エラーハンドリング
    """

    def __init__(self, title: str = "Chart", height: int = 500, **kwargs):
        """
        初期化

        Args:
            title: チャートのタイトル
            height: チャートの高さ
            **kwargs: その他のパラメータ
        """
        super().__init__(**kwargs)
        self.title = title
        self.height = height
        self._data: Optional[pd.DataFrame] = None

    def set_data(self, data: pd.DataFrame) -> None:
        """データを設定"""
        self._data = data

    def render(self) -> str:
        """
        可視化コンポーネントをレンダリング

        Returns:
            レンダリングされたHTML
        """
        if self._data is None:
            return "<div>データが設定されていません</div>"

        try:
            # データの前処理（サブクラスで実装）
            chart_data = self._prepare_chart_data(self._data)

            # HTMLテンプレートの生成
            html = self._generate_html_template(chart_data)

            return html

        except Exception as e:
            raise ComponentError(
                f"{self.__class__.__name__}のレンダリングに失敗しました: {str(e)}"
            )

    def _prepare_chart_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        チャート用のデータを準備（サブクラスで実装）

        Args:
            data: 元のデータフレーム

        Returns:
            チャート用のデータ辞書
        """
        raise NotImplementedError("サブクラスで実装してください")

    def _generate_html_template(self, chart_data: Dict[str, Any]) -> str:
        """
        HTMLテンプレートを生成

        Args:
            chart_data: チャートデータ

        Returns:
            HTMLテンプレート
        """
        chart_type = self._get_chart_type()
        div_id = f"{chart_type}-{self.component_id}"

        html = f"""
        <div id="{div_id}" style="width: 100%; height: {self.height}px;"></div>
        <script>
            const data = {json.dumps(chart_data)};

            const layout = {{
                title: '{self.title}',
                height: {self.height}
            }};

            Plotly.newPlot('{div_id}', data, layout);
        </script>
        """

        return html

    def _get_chart_type(self) -> str:
        """
        チャートタイプを取得（サブクラスで実装）

        Returns:
            チャートタイプ
        """
        raise NotImplementedError("サブクラスで実装してください")

    def _add_axis_titles(
        self,
        layout: Dict[str, Any],
        x_title: Optional[str] = None,
        y_title: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        軸タイトルを追加

        Args:
            layout: レイアウト辞書
            x_title: X軸タイトル
            y_title: Y軸タイトル

        Returns:
            更新されたレイアウト辞書
        """
        if x_title:
            layout["xaxis"] = {"title": x_title}
        if y_title:
            layout["yaxis"] = {"title": y_title}

        return layout
