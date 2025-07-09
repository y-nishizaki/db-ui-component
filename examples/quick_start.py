"""
Databricks クイックスタート

Databricksノートブック内で最も簡単に始められる例です。
"""

import pandas as pd
import numpy as np
from db_ui_components import ChartComponent, TableComponent


# サンプルデータの作成
def create_quick_data():
    """クイックスタート用のサンプルデータ"""
    dates = pd.date_range('2024-01-01', periods=30, freq='D')
    values = np.random.randn(30).cumsum() + 100
    
    return pd.DataFrame({
        'date': dates,
        'value': values,
        'category': np.random.choice(['A', 'B', 'C'], 30)
    })


# 最もシンプルな例
def simple_chart():
    """最もシンプルなグラフ"""
    df = create_quick_data()
    
    chart = ChartComponent(
        data=df,
        chart_type='line',
        x_column='date',
        y_column='value'
    )
    
    displayHTML(chart.render())


def simple_table():
    """最もシンプルなテーブル"""
    df = create_quick_data()
    
    table = TableComponent(
        data=df,
        enable_csv_download=True
    )
    
    displayHTML(table.render())


def quick_dashboard():
    """クイックダッシュボード"""
    from db_ui_components import Dashboard
    
    df = create_quick_data()
    
    # グラフとテーブルを作成
    chart = ChartComponent(
        data=df,
        chart_type='line',
        x_column='date',
        y_column='value',
        title='売上推移'
    )
    
    table = TableComponent(
        data=df,
        enable_csv_download=True,
        sortable=True,
        title='データテーブル'
    )
    
    # ダッシュボードに配置
    dashboard = Dashboard(title='クイックダッシュボード')
    dashboard.add_component(chart, position=(0, 0), size=(6, 1))
    dashboard.add_component(table, position=(1, 0), size=(6, 1))
    
    displayHTML(dashboard.render())


# 実行例
if __name__ == "__main__":
    print("Databricks UI Component Library - クイックスタート")
    print("=" * 40)
    
    print("1. シンプルなグラフ")
    simple_chart()
    
    print("2. シンプルなテーブル")
    simple_table()
    
    print("3. クイックダッシュボード")
    quick_dashboard() 