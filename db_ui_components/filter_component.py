"""
フィルターコンポーネント

Databricksダッシュボードで使用するフィルター機能を提供するコンポーネントです。
"""

from typing import Optional, Dict, Any, List, Callable
from abc import ABC, abstractmethod


class FilterRenderer(ABC):
    """フィルターレンダリングの基底クラス"""

    def __init__(self, column: str, title: Optional[str] = None):
        self.column = column
        self.title = title

    @abstractmethod
    def render(self) -> str:
        """フィルターをレンダリング"""
        pass


class DateFilterRenderer(FilterRenderer):
    """日付フィルターレンダリングクラス"""

    def render(self) -> str:
        """日付範囲フィルターをレンダリング"""
        filter_id = f"date-filter-{self.column.replace(' ', '-')}"

        html = f"""
        <div class="date-filter" style="margin: 10px 0;">
            {('<label style="display: block; margin-bottom: 5px; '
              'font-weight: bold;">' + 
              (self.title or self.column) + '</label>') if self.title else ''}
            <div style="display: flex; gap: 10px; align-items: center;">
                <input type="date" id="{filter_id}-start"
                       placeholder="開始日"
                       style="padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                <span>〜</span>
                <input type="date" id="{filter_id}-end"
                       placeholder="終了日"
                       style="padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                <button onclick="applyDateFilter('{filter_id}', '{self.column}')"
                        style="padding: 8px 16px; background-color: #007bff; color: white;
                               border: none; border-radius: 4px; cursor: pointer;">
                    適用
                </button>
            </div>
        </div>
        <script>
        function applyDateFilter(filterId, column) {{
            const startDate = document.getElementById(filterId + '-start').value;
            const endDate = document.getElementById(filterId + '-end').value;

            // フィルター条件を保存
            window.currentFilters = window.currentFilters || {{}};
            window.currentFilters[column] = {{
                type: 'date',
                start: startDate,
                end: endDate
            }};

            // イベントハンドラーを呼び出し
            if (window.filterChangeHandlers &&
                window.filterChangeHandlers['{self.column}']) {{
                window.filterChangeHandlers['{self.column}'](window.currentFilters[column]);
            }}
        }}
        </script>
        """

        return html


class DropdownFilterRenderer(FilterRenderer):
    """ドロップダウンフィルターレンダリングクラス"""

    def __init__(self, column: str, options: List[Any], title: Optional[str] = None):
        super().__init__(column, title)
        self.options = options

    def render(self) -> str:
        """ドロップダウンフィルターをレンダリング"""
        filter_id = f"dropdown-filter-{self.column.replace(' ', '-')}"

        options_html = '<option value="">すべて</option>'
        for option in self.options:
            options_html += f'<option value="{option}">{option}</option>'

        html = f"""
        <div class="dropdown-filter" style="margin: 10px 0;">
            {f'<label style="display: block; margin-bottom: 5px; font-weight: bold;">{self.title or self.column}</label>' if self.title else ''}
            <select id="{filter_id}"
                    onchange="applyDropdownFilter('{filter_id}', '{self.column}')"
                    style="padding: 8px; border: 1px solid #ddd;
                          border-radius: 4px; width: 200px;">
                {options_html}
            </select>
        </div>
        <script>
        function applyDropdownFilter(filterId, column) {{
            const selectedValue = document.getElementById(filterId).value;

            // フィルター条件を保存
            window.currentFilters = window.currentFilters || {{}};
            window.currentFilters[column] = {{
                type: 'dropdown',
                value: selectedValue
            }};

            // イベントハンドラーを呼び出し
            if (window.filterChangeHandlers &&
                window.filterChangeHandlers['{self.column}']) {{
                window.filterChangeHandlers['{self.column}'](window.currentFilters[column]);
            }}
        }}
        </script>
        """

        return html


class MultiselectFilterRenderer(FilterRenderer):
    """マルチセレクトフィルターレンダリングクラス"""

    def __init__(self, column: str, options: List[Any], title: Optional[str] = None):
        super().__init__(column, title)
        self.options = options

    def render(self) -> str:
        """マルチセレクトフィルターをレンダリング"""
        filter_id = f"multiselect-filter-{self.column.replace(' ', '-')}"

        options_html = ""
        for option in self.options:
            options_html += f"""
            <label style="display: block; margin: 5px 0;">
                <input type="checkbox" value="{option}"
                       onchange="applyMultiselectFilter('{filter_id}', '{self.column}')">
                {option}
            </label>
            """

        html = f"""
        <div class="multiselect-filter" style="margin: 10px 0;">
            {f'<label style="display: block; margin-bottom: 5px; font-weight: bold;">{self.title or self.column}</label>' if self.title else ''}
            <div id="{filter_id}" style="max-height: 150px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; border-radius: 4px;">
                {options_html}
            </div>
        </div>
        <script>
        function applyMultiselectFilter(filterId, column) {{
            const checkboxes = document.querySelectorAll('#' + filterId + ' input[type="checkbox"]');
            const selectedValues = [];

            checkboxes.forEach(checkbox => {{
                if (checkbox.checked) {{
                    selectedValues.push(checkbox.value);
                }}
            }});

            // フィルター条件を保存
            window.currentFilters = window.currentFilters || {{}};
            window.currentFilters[column] = {{
                type: 'multiselect',
                values: selectedValues
            }};

            // イベントハンドラーを呼び出し
            if (window.filterChangeHandlers &&
                window.filterChangeHandlers['{self.column}']) {{
                window.filterChangeHandlers['{self.column}'](window.currentFilters[column]);
            }}
        }}
        </script>
        """

        return html


class TextFilterRenderer(FilterRenderer):
    """テキストフィルターレンダリングクラス"""

    def __init__(
        self,
        column: str,
        placeholder: Optional[str] = None,
        title: Optional[str] = None,
    ):
        super().__init__(column, title)
        self.placeholder = placeholder

    def render(self) -> str:
        """テキスト検索フィルターをレンダリング"""
        filter_id = f"text-filter-{self.column.replace(' ', '-')}"
        placeholder = self.placeholder or f"{self.column}で検索..."

        html = f"""
        <div class="text-filter" style="margin: 10px 0;">
            {f'<label style="display: block; margin-bottom: 5px; font-weight: bold;">{self.title or self.column}</label>' if self.title else ''}
            <input type="text" id="{filter_id}"
                   placeholder="{placeholder}"
                   oninput="applyTextFilter('{filter_id}', '{self.column}')"
                   style="padding: 8px; border: 1px solid #ddd;
                          border-radius: 4px; width: 200px;">
        </div>
        <script>
        function applyTextFilter(filterId, column) {{
            const searchText = document.getElementById(filterId).value;

            // フィルター条件を保存
            window.currentFilters = window.currentFilters || {{}};
            window.currentFilters[column] = {{
                type: 'text',
                value: searchText
            }};

            // イベントハンドラーを呼び出し
            if (window.filterChangeHandlers &&
                window.filterChangeHandlers['{self.column}']) {{
                window.filterChangeHandlers['{self.column}'](window.currentFilters[column]);
            }}
        }}
        </script>
        """

        return html


class FilterEventManager:
    """フィルターイベント管理クラス"""

    def __init__(self):
        self._change_handlers: Dict[str, List[Callable]] = {}

    def add_handler(self, column: str, handler: Callable) -> None:
        """イベントハンドラーを追加"""
        if column not in self._change_handlers:
            self._change_handlers[column] = []
        self._change_handlers[column].append(handler)

    def remove_handler(self, column: str, handler: Callable) -> None:
        """イベントハンドラーを削除"""
        if column in self._change_handlers:
            self._change_handlers[column] = [
                h for h in self._change_handlers[column] if h != handler
            ]

    def get_handlers(self, column: str) -> List[Callable]:
        """イベントハンドラーを取得"""
        return self._change_handlers.get(column, [])

    def create_js_handler_code(self, column: str) -> str:
        """JavaScriptハンドラーコードを生成"""
        return f"""
        <script>
        window.filterChangeHandlers = window.filterChangeHandlers || {{}};
        window.filterChangeHandlers['{column}'] = function(filterValue) {{
            // Python側のハンドラーを呼び出すためのブリッジ
            console.log('Filter changed:', '{column}', filterValue);
        }};
        </script>
        """


class FilterComponent:
    """
    Databricksダッシュボード用のフィルターコンポーネント

    サポートするフィルタータイプ:
    - date: 日付範囲フィルター
    - dropdown: ドロップダウンフィルター
    - multiselect: マルチセレクトフィルター
    - text: テキスト検索フィルター
    """

    def __init__(
        self,
        filter_type: str,
        column: str,
        options: Optional[List[Any]] = None,
        placeholder: Optional[str] = None,
        title: Optional[str] = None,
        **kwargs,
    ):
        """
        初期化

        Args:
            filter_type: フィルタータイプ ('date', 'dropdown', 'multiselect', 'text')
            column: フィルター対象の列名
            options: フィルターオプション（ドロップダウン、マルチセレクト用）
            placeholder: プレースホルダーテキスト
            title: フィルターのタイトル
            **kwargs: その他のパラメータ
        """
        self.filter_type = filter_type
        self.column = column
        self.options = options or []
        self.placeholder = placeholder
        self.title = title
        self.kwargs = kwargs

        # レンダラーとイベントマネージャーの初期化
        self.renderer = self._create_renderer()
        self.event_manager = FilterEventManager()

    def _create_renderer(self) -> FilterRenderer:
        """フィルタータイプに応じたレンダラーを作成"""
        if self.filter_type == "date":
            return DateFilterRenderer(self.column, self.title)
        elif self.filter_type == "dropdown":
            return DropdownFilterRenderer(self.column, self.options, self.title)
        elif self.filter_type == "multiselect":
            return MultiselectFilterRenderer(self.column, self.options, self.title)
        elif self.filter_type == "text":
            return TextFilterRenderer(self.column, self.placeholder, self.title)
        else:
            raise ValueError(f"Unsupported filter type: {self.filter_type}")

    def render(self) -> str:
        """
        フィルターをHTMLとしてレンダリング

        Returns:
            HTML文字列
        """
        return self.renderer.render()

    def on_change(self, handler: Callable) -> None:
        """
        フィルター変更イベントハンドラーを追加

        Args:
            handler: フィルター変更時の処理関数
        """
        self.event_manager.add_handler(self.column, handler)

    def get_current_value(self) -> Dict[str, Any]:
        """
        現在のフィルター値を取得

        Returns:
            フィルター値の辞書
        """
        return {
            "type": self.filter_type,
            "column": self.column,
            "value": None,  # JavaScript側から取得する必要がある
        }

    def to_dict(self) -> Dict[str, Any]:
        """
        コンポーネントの設定を辞書として取得

        Returns:
            設定辞書
        """
        return {
            "type": "filter",
            "filter_type": self.filter_type,
            "column": self.column,
            "options": self.options,
            "placeholder": self.placeholder,
            "title": self.title,
            "kwargs": self.kwargs,
        }
