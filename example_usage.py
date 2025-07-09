#!/usr/bin/env python3
"""
db-ui-components パッケージの使用例

このスクリプトは、パッケージが正しくインストールされているかを確認し、
基本的な使用方法を示します。
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def test_import():
    """パッケージのインポートをテスト"""
    try:
        from db_ui_components import ChartComponent, TableComponent, FilterComponent, Dashboard
        print("✓ パッケージのインポートに成功しました")
        return True
    except ImportError as e:
        print(f"✗ パッケージのインポートに失敗しました: {e}")
        return False

def create_sample_data():
    """サンプルデータを作成"""
    # 日付範囲を作成
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    dates = pd.date_range(start_date, end_date, freq='D')
    
    # サンプルデータを作成
    np.random.seed(42)
    data = {
        'date': dates,
        'sales': np.random.normal(1000, 200, len(dates)),
        'profit': np.random.normal(200, 50, len(dates)),
        'category': np.random.choice(['A', 'B', 'C'], len(dates)),
        'region': np.random.choice(['North', 'South', 'East', 'West'], len(dates))
    }
    
    df = pd.DataFrame(data)
    return df

def test_chart_component(df):
    """ChartComponentのテスト"""
    try:
        from db_ui_components import ChartComponent
        
        # 折れ線グラフを作成
        chart = ChartComponent(
            data=df,
            chart_type='line',
            x_column='date',
            y_column='sales',
            title='売上推移'
        )
        
        print("✓ ChartComponentの作成に成功しました")
        return True
    except Exception as e:
        print(f"✗ ChartComponentの作成に失敗しました: {e}")
        return False

def test_table_component(df):
    """TableComponentのテスト"""
    try:
        from db_ui_components import TableComponent
        
        # テーブルを作成
        table = TableComponent(
            data=df.head(10),
            enable_csv_download=True,
            sortable=True,
            searchable=True
        )
        
        print("✓ TableComponentの作成に成功しました")
        return True
    except Exception as e:
        print(f"✗ TableComponentの作成に失敗しました: {e}")
        return False

def test_filter_component(df):
    """FilterComponentのテスト"""
    try:
        from db_ui_components import FilterComponent
        
        # フィルターを作成
        filter_comp = FilterComponent(
            filter_type='dropdown',
            column='category',
            options=df['category'].unique().tolist()
        )
        
        print("✓ FilterComponentの作成に成功しました")
        return True
    except Exception as e:
        print(f"✗ FilterComponentの作成に失敗しました: {e}")
        return False

def test_dashboard(df):
    """Dashboardのテスト"""
    try:
        from db_ui_components import Dashboard, ChartComponent, TableComponent
        
        # ダッシュボードを作成
        dashboard = Dashboard()
        
        # チャートを追加
        chart = ChartComponent(
            data=df,
            chart_type='line',
            x_column='date',
            y_column='sales',
            title='売上推移'
        )
        dashboard.add_component(chart, position=(0, 0))
        
        # テーブルを追加
        table = TableComponent(
            data=df.head(10),
            enable_csv_download=True
        )
        dashboard.add_component(table, position=(1, 0))
        
        print("✓ Dashboardの作成に成功しました")
        return True
    except Exception as e:
        print(f"✗ Dashboardの作成に失敗しました: {e}")
        return False

def main():
    """メイン関数"""
    print("=== db-ui-components パッケージテスト ===")
    
    # パッケージのインポートをテスト
    if not test_import():
        print("パッケージが正しくインストールされていません。")
        print("インストール方法: pip install db-ui-components")
        return
    
    # サンプルデータを作成
    print("\nサンプルデータを作成中...")
    df = create_sample_data()
    print(f"✓ サンプルデータを作成しました（{len(df)}行）")
    
    # 各コンポーネントをテスト
    print("\nコンポーネントのテスト:")
    
    test_chart_component(df)
    test_table_component(df)
    test_filter_component(df)
    test_dashboard(df)
    
    print("\n=== テスト完了 ===")
    print("すべてのテストが成功した場合、パッケージは正常に動作しています。")
    print("\n使用方法:")
    print("from db_ui_components import ChartComponent, TableComponent, FilterComponent, Dashboard")

if __name__ == "__main__":
    main()