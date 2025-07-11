"""
テーブルコンポーネント

Databricksダッシュボードで使用するテーブルを表示するコンポーネントです。
CSVダウンロード機能、ソート機能、検索機能をサポートします。
"""

import pandas as pd
from typing import Optional, Dict, Any, List
import base64
import io
import html


class TableDataManager:
    """テーブルデータ管理クラス"""

    def __init__(self, data: pd.DataFrame, columns: Optional[List[str]] = None):
        self.data = data
        self.columns = columns or list(data.columns)
        self._display_data = self.data[self.columns].copy()

    def get_display_data(self) -> pd.DataFrame:
        """表示用データを取得"""
        return self._display_data

    def update_data(self, new_data: pd.DataFrame) -> None:
        """データを更新"""
        self.data = new_data
        self._display_data = self.data[self.columns].copy()

    def set_columns(self, columns: List[str]) -> None:
        """表示列を設定"""
        self.columns = columns
        self._display_data = self.data[self.columns].copy()

    def get_csv_data(self) -> str:
        """CSVデータを取得"""
        output = io.StringIO()
        self._display_data.to_csv(output, index=False, encoding="utf-8")
        return output.getvalue()


class TableRenderer:
    """テーブルレンダリングクラス"""

    def __init__(self, data_manager: TableDataManager):
        self.data_manager = data_manager

    def render_search_box(self) -> str:
        """検索ボックスをレンダリング"""
        return """
        <div class="search-box" style="margin-bottom: 10px;">
            <input type="text" id="table-search" placeholder="検索..."
                   style="padding: 8px; border: 1px solid #ddd;
                          border-radius: 4px; width: 200px;">
        </div>
        <script>
        document.getElementById('table-search').addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const table = document.getElementById('data-table');
            const rows = table.getElementsByTagName('tr');

            for (let i = 1; i < rows.length; i++) {
                const row = rows[i];
                const cells = row.getElementsByTagName('td');
                let found = false;

                for (let j = 0; j < cells.length; j++) {
                    const cellText = cells[j].textContent.toLowerCase();
                    if (cellText.includes(searchTerm)) {
                        found = true;
                        break;
                    }
                }

                row.style.display = found ? '' : 'none';
            }
        });
        </script>
        """

    def render_download_button(self) -> str:
        """CSVダウンロードボタンをレンダリング"""
        csv_data = self.data_manager.get_csv_data()
        b64_csv = base64.b64encode(csv_data.encode()).decode()

        return f"""
        <div class="download-section" style="margin-bottom: 10px;">
            <a href="data:text/csv;base64,{b64_csv}"
               download="table_data.csv"
               class="download-btn"
               style="padding: 8px 16px; background-color: #007bff; color: white;
                      text-decoration: none; border-radius: 4px;
                      display: inline-block;">
                📥 CSVダウンロード
            </a>
        </div>
        """

    def render_table(
        self, columns: List[str], page_size: int, sortable: bool, height: int
    ) -> str:
        """テーブルをレンダリング"""
        display_data = self.data_manager.get_display_data()

        table_html = f"""
        <div class="table-container"
             style="max-height: {height}px; overflow-y: auto;">
            <table id="data-table"
                   style="width: 100%; border-collapse: collapse;
                          border: 1px solid #ddd;">
                <thead>
                    <tr style="background-color: #f8f9fa;">
        """

        # ヘッダーの追加
        for col in columns:
            sort_attr = (
                f' onclick="sortTable(this, {columns.index(col)})"' if sortable else ""
            )
            escaped_col = html.escape(str(col))
            table_html += (
                f'<th style="padding: 12px; border: 1px solid #ddd; '
                f'text-align: left; cursor: pointer;"{sort_attr}>{escaped_col}</th>'
            )

        table_html += """
                    </tr>
                </thead>
                <tbody>
        """

        # データ行の追加
        # page_sizeが0以下の場合は、すべてのデータを表示
        rows_to_display = (
            display_data if page_size <= 0 else display_data.head(page_size)
        )

        for _, row in rows_to_display.iterrows():
            table_html += "<tr>"
            for col in columns:
                value = row[col] if pd.notna(row[col]) else ""
                # HTMLエスケープを適用
                escaped_value = html.escape(str(value))
                table_html += f'<td style="padding: 8px; border: 1px solid #ddd;">{escaped_value}</td>'
            table_html += "</tr>"

        table_html += """
                </tbody>
            </table>
        </div>
        """

        # ソート機能のJavaScript
        if sortable:
            table_html += """
            <script>
            function sortTable(header, columnIndex) {
                const table = document.getElementById('data-table');
                const tbody = table.getElementsByTagName('tbody')[0];
                const rows = Array.from(tbody.getElementsByTagName('tr'));

                // ソート方向の決定
                const currentOrder = header.getAttribute('data-order') || 'asc';
                const newOrder = currentOrder === 'asc' ? 'desc' : 'asc';
                header.setAttribute('data-order', newOrder);

                // 行のソート
                rows.sort((a, b) => {
                    const aValue = a.cells[columnIndex].textContent.trim();
                    const bValue = b.cells[columnIndex].textContent.trim();

                    // 数値として比較を試行
                    const aNum = parseFloat(aValue);
                    const bNum = parseFloat(bValue);

                    if (!isNaN(aNum) && !isNaN(bNum)) {
                        return newOrder === 'asc' ? aNum - bNum : bNum - aNum;
                    } else {
                        return newOrder === 'asc' ?
                            aValue.localeCompare(bValue) :
                            bValue.localeCompare(aValue);
                    }
                });

                // ソートされた行を再配置
                rows.forEach(row => tbody.appendChild(row));
            }
            </script>
            """

        return table_html

    def render_pagination(self, page_size: int) -> str:
        """ページネーションをレンダリング"""
        display_data = self.data_manager.get_display_data()

        # page_sizeが0以下の場合は、ページネーションを表示しない
        if page_size <= 0:
            return ""

        total_pages = (len(display_data) + page_size - 1) // page_size

        if total_pages <= 1:
            return ""

        pagination_html = """
        <div class="pagination" style="margin-top: 10px; text-align: center;">
            <span>ページ: </span>
        """

        for i in range(total_pages):
            page_num = i + 1
            pagination_html += f"""
            <a href="#" onclick="showPage({i})"
               style="padding: 5px 10px; margin: 0 2px; border: 1px solid #ddd;
                      text-decoration: none; color: #007bff;">
                {page_num}
            </a>
            """

        pagination_html += (
            """
        </div>
        <script>
        function showPage(pageIndex) {
            const table = document.getElementById('data-table');
            const tbody = table.getElementsByTagName('tbody')[0];
            const rows = tbody.getElementsByTagName('tr');
            const pageSize = """
            + str(page_size)
            + """;

            for (let i = 0; i < rows.length; i++) {
                const startIndex = pageIndex * pageSize;
                const endIndex = startIndex + pageSize;

                if (i >= startIndex && i < endIndex) {
                    rows[i].style.display = '';
                } else {
                    rows[i].style.display = 'none';
                }
            }
        }

        // 初期表示（1ページ目）
        showPage(0);
        </script>
        """
        )

        return pagination_html


class TableComponent:
    """
    Databricksダッシュボード用のテーブルコンポーネント

    機能:
    - CSVダウンロード機能
    - ソート機能
    - ページネーション
    - 検索・フィルター機能
    - カスタム列表示
    """

    def __init__(
        self,
        data: pd.DataFrame,
        enable_csv_download: bool = True,
        sortable: bool = True,
        searchable: bool = True,
        page_size: int = 10,
        columns: Optional[List[str]] = None,
        title: Optional[str] = None,
        height: int = 400,
        **kwargs,
    ):
        """
        初期化

        Args:
            data: データフレーム
            enable_csv_download: CSVダウンロード機能の有効化
            sortable: ソート機能の有効化
            searchable: 検索機能の有効化
            page_size: 1ページあたりの表示件数
            columns: 表示する列の指定
            title: テーブルのタイトル
            height: テーブルの高さ（ピクセル）
            **kwargs: その他のパラメータ
        """
        self.data_manager = TableDataManager(data, columns)
        self.renderer = TableRenderer(self.data_manager)
        self.enable_csv_download = enable_csv_download
        self.sortable = sortable
        self.searchable = searchable
        self.page_size = page_size
        self.title = title
        self.height = height
        self.kwargs = kwargs

    def render(self) -> str:
        """
        テーブルをHTMLとしてレンダリング

        Returns:
            HTML文字列
        """
        html_parts = []

        # タイトルの追加
        if self.title:
            html_parts.append(f"<h3>{self.title}</h3>")

        # 検索機能の追加
        if self.searchable:
            html_parts.append(self.renderer.render_search_box())

        # CSVダウンロードボタンの追加
        if self.enable_csv_download:
            html_parts.append(self.renderer.render_download_button())

        # テーブルの追加
        html_parts.append(
            self.renderer.render_table(
                self.data_manager.columns, self.page_size, self.sortable, self.height
            )
        )

        # ページネーションの追加
        html_parts.append(self.renderer.render_pagination(self.page_size))

        return "\n".join(html_parts)

    def update_data(self, new_data: pd.DataFrame) -> None:
        """
        データを更新

        Args:
            new_data: 新しいデータフレーム
        """
        self.data_manager.update_data(new_data)

    def set_columns(self, columns: List[str]) -> None:
        """
        表示列を設定

        Args:
            columns: 表示する列のリスト
        """
        self.data_manager.set_columns(columns)

    def to_dict(self) -> Dict[str, Any]:
        """
        コンポーネントの設定を辞書として取得

        Returns:
            設定辞書
        """
        return {
            "type": "table",
            "enable_csv_download": self.enable_csv_download,
            "sortable": self.sortable,
            "searchable": self.searchable,
            "page_size": self.page_size,
            "columns": self.data_manager.columns,
            "title": self.title,
            "height": self.height,
            "kwargs": self.kwargs,
        }
