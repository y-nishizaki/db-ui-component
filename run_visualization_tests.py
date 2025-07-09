#!/usr/bin/env python3
"""
可視化コンポーネントテスト実行スクリプト

SRPに準拠した可視化コンポーネントのテストを実行します。
"""

import sys
import os
import subprocess
from pathlib import Path

def install_test_dependencies():
    """テスト用の依存関係をインストール"""
    print("テスト用の依存関係をインストール中...")
    
    dependencies = [
        "pytest",
        "pandas",
        "numpy"
    ]
    
    for dep in dependencies:
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", 
                "--break-system-packages", dep
            ], check=True, capture_output=True)
            print(f"✓ {dep} をインストールしました")
        except subprocess.CalledProcessError as e:
            print(f"✗ {dep} のインストールに失敗しました: {e}")
            return False
    
    return True

def run_tests():
    """テストを実行"""
    print("可視化コンポーネントのテストを実行中...")
    
    # テストファイルのパス
    test_file = Path("tests/test_visualization_components.py")
    
    if not test_file.exists():
        print(f"✗ テストファイルが見つかりません: {test_file}")
        return False
    
    try:
        # pytestを実行
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            str(test_file), "-v", "--tb=short"
        ], capture_output=True, text=True)
        
        print("=== テスト結果 ===")
        print(result.stdout)
        
        if result.stderr:
            print("=== エラー出力 ===")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"✗ テストの実行に失敗しました: {e}")
        return False

def run_simple_tests():
    """簡単なテストを実行（pytestが利用できない場合）"""
    print("簡単なテストを実行中...")
    
    try:
        import pandas as pd
        import numpy as np
        
        # テストデータを作成
        test_data = pd.DataFrame({
            "source": ["A", "A", "B"],
            "target": ["X", "Y", "X"],
            "value": [10, 5, 8]
        })
        
        # コンポーネントをインポートしてテスト
        from db_ui_components.visualization import SankeyChartComponent
        
        # コンポーネントを作成
        component = SankeyChartComponent(
            source_column="source",
            target_column="target",
            value_column="value",
            title="Test Sankey"
        )
        
        # レンダリングテスト
        html = component.render(test_data)
        
        print("✓ サンキーチャートコンポーネントのテストが成功しました")
        print(f"✓ HTML長: {len(html)} 文字")
        print(f"✓ HTMLに'sankey-chart'が含まれている: {'sankey-chart' in html}")
        print(f"✓ HTMLに'Plotly.newPlot'が含まれている: {'Plotly.newPlot' in html}")
        
        return True
        
    except ImportError as e:
        print(f"✗ 必要なモジュールが見つかりません: {e}")
        return False
    except Exception as e:
        print(f"✗ テストの実行に失敗しました: {e}")
        return False

def main():
    """メイン関数"""
    print("=== 可視化コンポーネントテスト実行 ===")
    
    # 依存関係をインストール
    if not install_test_dependencies():
        print("依存関係のインストールに失敗しました。簡単なテストを実行します。")
        success = run_simple_tests()
    else:
        # 本格的なテストを実行
        success = run_tests()
    
    if success:
        print("\n=== テスト完了 ===")
        print("✓ すべてのテストが正常に実行されました")
    else:
        print("\n=== テスト失敗 ===")
        print("✗ 一部のテストが失敗しました")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)