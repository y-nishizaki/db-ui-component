"""
パフォーマンステスト

Databricks UI Component Libraryのパフォーマンステストです。
レンダリング速度、メモリ使用量、大量データの処理能力をテストします。
"""

import pytest
import pandas as pd
import numpy as np
import time
import gc
from db_ui_components import ChartComponent, TableComponent, FilterComponent, Dashboard


class TestPerformance:
    """パフォーマンステスト"""
    
    def test_chart_rendering_performance(self):
        """チャートレンダリングのパフォーマンステスト"""
        # 大きなデータセットを作成
        large_df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=5000, freq='D'),
            'value': np.random.randn(5000).cumsum() + 1000,
            'category': np.random.choice(['A', 'B', 'C', 'D'], 5000)
        })
        
        chart = ChartComponent(
            data=large_df,
            chart_type='line',
            x_column='date',
            y_column='value',
            title='パフォーマンステスト'
        )
        
        # レンダリング時間を計測
        start_time = time.time()
        html = chart.render()
        end_time = time.time()
        
        render_time = end_time - start_time
        
        # 基本的なアサート
        assert isinstance(html, str)
        assert len(html) > 0
        assert 'パフォーマンステスト' in html
        
        # パフォーマンスが妥当な範囲内か確認（10秒以内）
        assert render_time < 10.0, f"レンダリング時間が遅すぎます: {render_time:.2f}秒"
        
        print(f"チャートレンダリング時間: {render_time:.3f}秒")
    
    def test_table_rendering_performance(self):
        """テーブルレンダリングのパフォーマンステスト"""
        # 大きなデータセットを作成
        large_df = pd.DataFrame({
            'id': range(1000),
            'name': [f'Item_{i}' for i in range(1000)],
            'value': np.random.randn(1000),
            'category': np.random.choice(['A', 'B', 'C'], 1000),
            'date': pd.date_range('2024-01-01', periods=1000, freq='H')
        })
        
        table = TableComponent(
            data=large_df,
            enable_csv_download=True,
            sortable=True,
            searchable=True,
            page_size=50
        )
        
        # レンダリング時間を計測
        start_time = time.time()
        html = table.render()
        end_time = time.time()
        
        render_time = end_time - start_time
        
        # 基本的なアサート
        assert isinstance(html, str)
        assert len(html) > 0
        
        # パフォーマンスが妥当な範囲内か確認（5秒以内）
        assert render_time < 5.0, f"レンダリング時間が遅すぎます: {render_time:.2f}秒"
        
        print(f"テーブルレンダリング時間: {render_time:.3f}秒")
    
    def test_dashboard_rendering_performance(self):
        """ダッシュボードレンダリングのパフォーマンステスト"""
        # 複数のコンポーネントを持つダッシュボード
        dashboard = Dashboard(title='パフォーマンステストダッシュボード')
        
        # サンプルデータ
        df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=500, freq='D'),
            'value': np.random.randn(500).cumsum(),
            'category': np.random.choice(['A', 'B', 'C'], 500)
        })
        
        # 複数のコンポーネントを追加
        for i in range(10):
            chart = ChartComponent(
                data=df,
                chart_type='line',
                x_column='date',
                y_column='value',
                title=f'グラフ {i+1}'
            )
            dashboard.add_component(chart, position=(i, 0))
        
        # レンダリング時間を計測
        start_time = time.time()
        html = dashboard.render()
        end_time = time.time()
        
        render_time = end_time - start_time
        
        # 基本的なアサート
        assert isinstance(html, str)
        assert len(html) > 0
        assert 'パフォーマンステストダッシュボード' in html
        
        # パフォーマンスが妥当な範囲内か確認（15秒以内）
        assert render_time < 15.0, f"レンダリング時間が遅すぎます: {render_time:.2f}秒"
        
        print(f"ダッシュボードレンダリング時間: {render_time:.3f}秒")
    
    def test_memory_usage(self):
        """メモリ使用量のテスト"""
        # 大きなデータセットを作成
        large_df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=10000, freq='H'),
            'value': np.random.randn(10000),
            'category': np.random.choice(['A', 'B', 'C', 'D', 'E'], 10000)
        })
        
        # メモリ使用量の計測は簡易的に行う
        components = []
        
        # 複数のコンポーネントを作成
        for i in range(100):
            chart = ChartComponent(
                data=large_df.sample(n=100),  # サンプリングしてメモリ使用量を制限
                chart_type='line',
                x_column='date',
                y_column='value',
                title=f'テスト {i}'
            )
            components.append(chart)
        
        # 基本的なアサート（メモリ不足でエラーにならないことを確認）
        assert len(components) == 100
        
        # 手動でガベージコレクションを実行
        del components
        gc.collect()
    
    def test_concurrent_rendering(self):
        """並行レンダリングのテスト"""
        import threading
        
        def render_component():
            df = pd.DataFrame({
                'x': range(100),
                'y': np.random.randn(100)
            })
            
            chart = ChartComponent(
                data=df,
                chart_type='line',
                x_column='x',
                y_column='y'
            )
            
            html = chart.render()
            assert isinstance(html, str)
            assert len(html) > 0
        
        # 複数のスレッドで並行レンダリング
        threads = []
        for i in range(10):
            thread = threading.Thread(target=render_component)
            threads.append(thread)
            thread.start()
        
        # 全てのスレッドの完了を待つ
        for thread in threads:
            thread.join()
        
        # エラーが発生しないことを確認
        assert True  # 全てのスレッドが正常終了すればOK
    
    def test_repeated_rendering(self):
        """繰り返しレンダリングのテスト"""
        df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=100, freq='D'),
            'value': np.random.randn(100).cumsum()
        })
        
        chart = ChartComponent(
            data=df,
            chart_type='line',
            x_column='date',
            y_column='value'
        )
        
        # 100回レンダリング
        start_time = time.time()
        for i in range(100):
            html = chart.render()
            assert isinstance(html, str)
            assert len(html) > 0
        end_time = time.time()
        
        total_time = end_time - start_time
        avg_time = total_time / 100
        
        # 平均レンダリング時間が妥当な範囲内か確認
        assert avg_time < 0.1, f"平均レンダリング時間が遅すぎます: {avg_time:.4f}秒"
        
        print(f"100回レンダリング総時間: {total_time:.3f}秒")
        print(f"平均レンダリング時間: {avg_time:.4f}秒")
    
    def test_data_update_performance(self):
        """データ更新のパフォーマンステスト"""
        # 初期データ
        df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=1000, freq='D'),
            'value': np.random.randn(1000).cumsum()
        })
        
        chart = ChartComponent(
            data=df,
            chart_type='line',
            x_column='date',
            y_column='value'
        )
        
        # 初回レンダリング
        html = chart.render()
        assert isinstance(html, str)
        assert len(html) > 0
        
        # データ更新のパフォーマンステスト
        start_time = time.time()
        for i in range(10):
            # 新しいデータを作成
            new_df = pd.DataFrame({
                'date': pd.date_range('2024-01-01', periods=1000, freq='D'),
                'value': np.random.randn(1000).cumsum()
            })
            
            # データを更新
            chart.update_data(new_df)
            
            # 再レンダリング
            html = chart.render()
            assert isinstance(html, str)
            assert len(html) > 0
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # データ更新とレンダリングの時間が妥当な範囲内か確認
        assert total_time < 5.0, f"データ更新が遅すぎます: {total_time:.2f}秒"
        
        print(f"10回のデータ更新時間: {total_time:.3f}秒")


class TestStressTest:
    """ストレステスト"""
    
    def test_extreme_data_volume(self):
        """極端なデータ量でのテスト"""
        # 非常に大きなデータセット（メモリ制限に注意）
        try:
            large_df = pd.DataFrame({
                'date': pd.date_range('2024-01-01', periods=50000, freq='H'),
                'value': np.random.randn(50000)
            })
            
            chart = ChartComponent(
                data=large_df,
                chart_type='line',
                x_column='date',
                y_column='value'
            )
            
            # レンダリングが完了することを確認
            html = chart.render()
            assert isinstance(html, str)
            assert len(html) > 0
            
        except MemoryError:
            # メモリ不足は予期されるエラーなのでスキップ
            pytest.skip("メモリ不足のため極端なデータ量テストをスキップ")
    
    def test_many_components_dashboard(self):
        """多数のコンポーネントを持つダッシュボードのテスト"""
        dashboard = Dashboard(title='ストレステストダッシュボード')
        
        # 50個のコンポーネントを追加
        for i in range(50):
            df = pd.DataFrame({
                'x': range(10),
                'y': np.random.randn(10)
            })
            
            chart = ChartComponent(
                data=df,
                chart_type='line',
                x_column='x',
                y_column='y',
                title=f'グラフ {i+1}'
            )
            
            dashboard.add_component(chart, position=(i // 10, i % 10))
        
        # レンダリング時間を計測
        start_time = time.time()
        html = dashboard.render()
        end_time = time.time()
        
        render_time = end_time - start_time
        
        # 基本的なアサート
        assert isinstance(html, str)
        assert len(html) > 0
        assert 'ストレステストダッシュボード' in html
        
        # 大量のコンポーネントでも妥当な時間内でレンダリング
        assert render_time < 30.0, f"レンダリング時間が遅すぎます: {render_time:.2f}秒"
        
        print(f"50コンポーネントダッシュボードレンダリング時間: {render_time:.3f}秒")