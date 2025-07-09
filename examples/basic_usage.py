"""
基本的な使用例

Databricks UI Component Libraryの基本的な使用方法を示すサンプルコードです。
"""

import pandas as pd
import numpy as np
from db_ui_components import ChartComponent, TableComponent, FilterComponent, Dashboard


def create_sample_data():
    """サンプルデータを作成"""
    # 時系列データ
    dates = pd.date_range('2024-01-01', periods=100, freq='D')
    values = np.random.randn(100).cumsum() + 100
    
    time_series_data = pd.DataFrame({
        'date': dates,
        'value': values,
        'category': np.random.choice(['A', 'B', 'C'], 100)
    })
    
    # カテゴリ別データ
    category_data = pd.DataFrame({
        'category': ['A', 'B', 'C', 'D', 'E'],
        'count': [25, 30, 15, 20, 10],
        'percentage': [25, 30, 15, 20, 10]
    })
    
    return time_series_data, category_data


def create_chart_examples():
    """グラフコンポーネントの例"""
    time_data, category_data = create_sample_data()
    
    # 折れ線グラフ
    line_chart = ChartComponent(
        data=time_data,
        chart_type='line',
        x_column='date',
        y_column='value',
        title='時系列データ（折れ線グラフ）',
        height=400
    )
    
    # 棒グラフ
    bar_chart = ChartComponent(
        data=category_data,
        chart_type='bar',
        x_column='category',
        y_column='count',
        title='カテゴリ別データ（棒グラフ）',
        height=400
    )
    
    # 円グラフ
    pie_chart = ChartComponent(
        data=category_data,
        chart_type='pie',
        x_column='category',
        y_column='percentage',
        title='カテゴリ別データ（円グラフ）',
        height=400
    )
    
    return line_chart, bar_chart, pie_chart


def create_table_examples():
    """テーブルコンポーネントの例"""
    time_data, category_data = create_sample_data()
    
    # CSVダウンロード機能付きテーブル
    table = TableComponent(
        data=time_data,
        enable_csv_download=True,
        sortable=True,
        searchable=True,
        page_size=10,
        title='データテーブル',
        height=300
    )
    
    return table


def create_filter_examples():
    """フィルターコンポーネントの例"""
    time_data, category_data = create_sample_data()
    
    # 日付範囲フィルター
    date_filter = FilterComponent(
        filter_type='date',
        column='date',
        title='日付範囲'
    )
    
    # ドロップダウンフィルター
    dropdown_filter = FilterComponent(
        filter_type='dropdown',
        column='category',
        options=['A', 'B', 'C'],
        title='カテゴリ選択'
    )
    
    # テキスト検索フィルター
    text_filter = FilterComponent(
        filter_type='text',
        column='category',
        placeholder='カテゴリで検索...',
        title='テキスト検索'
    )
    
    return date_filter, dropdown_filter, text_filter


def create_dashboard_example():
    """ダッシュボードの例"""
    # コンポーネントを作成
    line_chart, bar_chart, pie_chart = create_chart_examples()
    table = create_table_examples()
    date_filter, dropdown_filter, text_filter = create_filter_examples()
    
    # ダッシュボードを作成
    dashboard = Dashboard(title='サンプルダッシュボード')
    
    # コンポーネントを追加
    dashboard.add_component(date_filter, position=(0, 0), size=(3, 1))
    dashboard.add_component(dropdown_filter, position=(0, 3), size=(3, 1))
    dashboard.add_component(text_filter, position=(0, 6), size=(3, 1))
    
    dashboard.add_component(line_chart, position=(1, 0), size=(6, 1))
    dashboard.add_component(bar_chart, position=(1, 6), size=(6, 1))
    
    dashboard.add_component(pie_chart, position=(2, 0), size=(4, 1))
    dashboard.add_component(table, position=(2, 4), size=(8, 1))
    
    return dashboard


def main():
    """メイン関数"""
    print("Databricks UI Component Library - 基本使用例")
    print("=" * 50)
    
    # ダッシュボードを作成
    dashboard = create_dashboard_example()
    
    # HTMLとしてレンダリング
    html_output = dashboard.render()
    
    # ファイルに保存
    with open('dashboard_example.html', 'w', encoding='utf-8') as f:
        f.write(f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Databricks UI Component Library - サンプル</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }}
    </style>
</head>
<body>
    {html_output}
</body>
</html>
        ''')
    
    print("ダッシュボードが 'dashboard_example.html' に保存されました。")


if __name__ == "__main__":
    main() 