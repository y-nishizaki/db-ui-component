"""
Databricksでの使用例

Databricksノートブック内でdisplayHTMLを使用してコンポーネントを表示する例です。
"""

import pandas as pd
import numpy as np
from db_ui_components import ChartComponent, TableComponent, FilterComponent, Dashboard


def create_sample_sales_data():
    """サンプルの売上データを作成"""
    np.random.seed(42)
    
    # 日付範囲
    dates = pd.date_range('2024-01-01', periods=365, freq='D')
    
    # 地域データ
    regions = ['東京', '大阪', '名古屋', '福岡', '札幌']
    categories = ['電子機器', '衣類', '食品', '書籍', 'スポーツ']
    
    # 売上データの生成
    data = []
    for date in dates:
        for region in regions:
            for category in categories:
                # 季節性とトレンドを加味した売上
                base_sales = 1000 + np.random.normal(0, 200)
                seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * date.dayofyear / 365)
                trend_factor = 1 + 0.001 * (date - pd.Timestamp('2024-01-01')).days
                
                sales = base_sales * seasonal_factor * trend_factor
                
                data.append({
                    'date': date,
                    'region': region,
                    'category': category,
                    'sales': max(0, sales),
                    'quantity': max(1, int(sales / 100)),
                    'profit': sales * 0.2 * (0.8 + np.random.random() * 0.4)
                })
    
    return pd.DataFrame(data)


def example_1_basic_chart():
    """例1: 基本的なグラフ表示"""
    print("=== 例1: 基本的なグラフ表示 ===")
    
    # サンプルデータ
    df = create_sample_sales_data()
    daily_sales = df.groupby('date')['sales'].sum().reset_index()
    
    # 折れ線グラフを作成
    chart = ChartComponent(
        data=daily_sales,
        chart_type='line',
        x_column='date',
        y_column='sales',
        title='日次売上推移',
        height=400
    )
    
    # Databricksで表示
    displayHTML(chart.render())


def example_2_interactive_table():
    """例2: インタラクティブなテーブル"""
    print("=== 例2: インタラクティブなテーブル ===")
    
    df = create_sample_sales_data()
    
    # 地域・カテゴリ別の集計
    summary = df.groupby(['region', 'category']).agg({
        'sales': 'sum',
        'quantity': 'sum',
        'profit': 'sum'
    }).reset_index()
    
    # テーブルコンポーネントを作成
    table = TableComponent(
        data=summary,
        enable_csv_download=True,
        sortable=True,
        searchable=True,
        page_size=10,
        title='地域・カテゴリ別売上サマリー',
        height=300
    )
    
    # Databricksで表示
    displayHTML(table.render())


def example_3_multiple_charts():
    """例3: 複数のグラフ"""
    print("=== 例3: 複数のグラフ ===")
    
    df = create_sample_sales_data()
    
    # 地域別売上
    region_sales = df.groupby('region')['sales'].sum().reset_index()
    
    # 棒グラフ
    bar_chart = ChartComponent(
        data=region_sales,
        chart_type='bar',
        x_column='region',
        y_column='sales',
        title='地域別売上',
        height=300
    )
    
    # カテゴリ別売上
    category_sales = df.groupby('category')['sales'].sum().reset_index()
    
    # 円グラフ
    pie_chart = ChartComponent(
        data=category_sales,
        chart_type='pie',
        x_column='category',
        y_column='sales',
        title='カテゴリ別売上',
        height=300
    )
    
    # 個別に表示
    displayHTML(bar_chart.render())
    displayHTML(pie_chart.render())


def example_4_dashboard():
    """例4: ダッシュボード"""
    print("=== 例4: ダッシュボード ===")
    
    df = create_sample_sales_data()
    
    # 各種集計データ
    daily_sales = df.groupby('date')['sales'].sum().reset_index()
    region_sales = df.groupby('region')['sales'].sum().reset_index()
    category_sales = df.groupby('category')['sales'].sum().reset_index()
    
    # コンポーネントを作成
    line_chart = ChartComponent(
        data=daily_sales,
        chart_type='line',
        x_column='date',
        y_column='sales',
        title='日次売上推移',
        height=300
    )
    
    bar_chart = ChartComponent(
        data=region_sales,
        chart_type='bar',
        x_column='region',
        y_column='sales',
        title='地域別売上',
        height=300
    )
    
    pie_chart = ChartComponent(
        data=category_sales,
        chart_type='pie',
        x_column='category',
        y_column='sales',
        title='カテゴリ別売上',
        height=300
    )
    
    summary_table = TableComponent(
        data=df.groupby(['region', 'category']).agg({
            'sales': 'sum',
            'profit': 'sum'
        }).reset_index(),
        enable_csv_download=True,
        sortable=True,
        searchable=True,
        page_size=8,
        title='売上サマリー',
        height=200
    )
    
    # ダッシュボードを作成
    dashboard = Dashboard(title='売上分析ダッシュボード')
    
    # コンポーネントを配置
    dashboard.add_component(line_chart, position=(0, 0), size=(6, 1))
    dashboard.add_component(bar_chart, position=(0, 6), size=(6, 1))
    dashboard.add_component(pie_chart, position=(1, 0), size=(4, 1))
    dashboard.add_component(summary_table, position=(1, 4), size=(8, 1))
    
    # Databricksで表示
    displayHTML(dashboard.render())


def example_5_filters():
    """例5: フィルター機能"""
    print("=== 例5: フィルター機能 ===")
    
    df = create_sample_sales_data()
    
    # フィルターコンポーネントを作成
    region_filter = FilterComponent(
        filter_type='dropdown',
        column='region',
        options=df['region'].unique().tolist(),
        title='地域選択'
    )
    
    category_filter = FilterComponent(
        filter_type='multiselect',
        column='category',
        options=df['category'].unique().tolist(),
        title='カテゴリ選択'
    )
    
    date_filter = FilterComponent(
        filter_type='date',
        column='date',
        title='日付範囲'
    )
    
    # フィルターを表示
    displayHTML(region_filter.render())
    displayHTML(category_filter.render())
    displayHTML(date_filter.render())
    
    # フィルター適用後のデータ表示例
    filtered_df = df[df['region'] == '東京']
    filtered_chart = ChartComponent(
        data=filtered_df.groupby('date')['sales'].sum().reset_index(),
        chart_type='line',
        x_column='date',
        y_column='sales',
        title='東京の日次売上',
        height=300
    )
    
    displayHTML(filtered_chart.render())


def example_6_custom_styling():
    """例6: カスタムスタイリング"""
    print("=== 例6: カスタムスタイリング ===")
    
    df = create_sample_sales_data()
    daily_sales = df.groupby('date')['sales'].sum().reset_index()
    
    # カスタムスタイルを適用したグラフ
    chart = ChartComponent(
        data=daily_sales,
        chart_type='line',
        x_column='date',
        y_column='sales',
        title='カスタムスタイル付き売上グラフ',
        height=400
    )
    
    # スタイルを設定
    chart.set_style({
        'backgroundColor': '#f8f9fa',
        'borderRadius': '12px',
        'padding': '20px',
        'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
    })
    
    displayHTML(chart.render())


def main():
    """メイン関数 - すべての例を実行"""
    print("Databricks UI Component Library - 使用例")
    print("=" * 50)
    
    # 各例を実行
    example_1_basic_chart()
    example_2_interactive_table()
    example_3_multiple_charts()
    example_4_dashboard()
    example_5_filters()
    example_6_custom_styling()
    
    print("\nすべての例が完了しました！")


# Databricksで実行する場合のコメント例
"""
# ノートブック内で以下のように実行してください：

# 1. ライブラリをインポート
from examples.databricks_usage import *

# 2. 個別の例を実行
example_1_basic_chart()

# または、すべての例を実行
main()
""" 