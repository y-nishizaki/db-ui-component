#!/usr/bin/env python3
"""
簡単な可視化コンポーネントテスト

SRPに準拠した可視化コンポーネントの基本的な動作をテストします。
"""

import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """インポートテスト"""
    print("=== インポートテスト ===")
    
    try:
        from db_ui_components.visualization import (
            SankeyChartComponent,
            HeatmapComponent,
            NetworkGraphComponent,
            TreemapComponent,
            BubbleChartComponent
        )
        print("✓ 可視化コンポーネントのインポートが成功しました")
        return True
    except ImportError as e:
        print(f"✗ インポートに失敗しました: {e}")
        return False

def test_config_classes():
    """設定クラスのテスト"""
    print("\n=== 設定クラステスト ===")
    
    try:
        from db_ui_components.visualization.config import (
            VisualizationConfig,
            SankeyConfig,
            HeatmapConfig
        )
        
        # 基本設定のテスト
        config = VisualizationConfig(title="Test Chart", height=400)
        assert config.title == "Test Chart"
        assert config.height == 400
        print("✓ VisualizationConfigのテストが成功しました")
        
        # サンキー設定のテスト
        sankey_config = SankeyConfig(node_color="#ff0000")
        assert sankey_config.node_color == "#ff0000"
        print("✓ SankeyConfigのテストが成功しました")
        
        # ヒートマップ設定のテスト
        heatmap_config = HeatmapConfig(color_scale="Plasma")
        assert heatmap_config.color_scale == "Plasma"
        print("✓ HeatmapConfigのテストが成功しました")
        
        return True
    except Exception as e:
        print(f"✗ 設定クラスのテストに失敗しました: {e}")
        return False

def test_data_transformers():
    """データ変換クラスのテスト"""
    print("\n=== データ変換クラステスト ===")
    
    try:
        from db_ui_components.visualization.data_transformer import (
            SankeyDataTransformer,
            HeatmapDataTransformer
        )
        
        # サンキーデータ変換のテスト
        sankey_transformer = SankeyDataTransformer(
            source_column="source",
            target_column="target",
            value_column="value"
        )
        print("✓ SankeyDataTransformerの作成が成功しました")
        
        # ヒートマップデータ変換のテスト
        heatmap_transformer = HeatmapDataTransformer(
            x_column="x",
            y_column="y",
            value_column="value"
        )
        print("✓ HeatmapDataTransformerの作成が成功しました")
        
        return True
    except Exception as e:
        print(f"✗ データ変換クラスのテストに失敗しました: {e}")
        return False

def test_component_creation():
    """コンポーネント作成テスト"""
    print("\n=== コンポーネント作成テスト ===")
    
    try:
        from db_ui_components.visualization import SankeyChartComponent
        
        # サンキーチャートコンポーネントの作成
        component = SankeyChartComponent(
            source_column="source",
            target_column="target",
            value_column="value",
            title="Test Sankey"
        )
        
        assert component.source_column == "source"
        assert component.target_column == "target"
        assert component.value_column == "value"
        assert component.title == "Test Sankey"
        print("✓ SankeyChartComponentの作成が成功しました")
        
        return True
    except Exception as e:
        print(f"✗ コンポーネント作成のテストに失敗しました: {e}")
        return False

def test_html_generation():
    """HTML生成テスト"""
    print("\n=== HTML生成テスト ===")
    
    try:
        from db_ui_components.visualization import SankeyChartComponent
        
        # テストデータの作成（pandasなしで）
        test_data = {
            "source": ["A", "A", "B"],
            "target": ["X", "Y", "X"],
            "value": [10, 5, 8]
        }
        
        # コンポーネントの作成
        component = SankeyChartComponent(
            source_column="source",
            target_column="target",
            value_column="value",
            title="Test Sankey"
        )
        
        # HTML生成のテスト（データ変換部分をスキップ）
        chart_type = component._get_chart_type()
        assert chart_type == "sankey-chart"
        print("✓ チャートタイプの取得が成功しました")
        
        # コンポーネントIDの確認
        assert hasattr(component, 'component_id')
        assert component.component_id is not None
        print("✓ コンポーネントIDの生成が成功しました")
        
        return True
    except Exception as e:
        print(f"✗ HTML生成のテストに失敗しました: {e}")
        return False

def main():
    """メイン関数"""
    print("=== SRP準拠可視化コンポーネントテスト ===")
    
    tests = [
        test_imports,
        test_config_classes,
        test_data_transformers,
        test_component_creation,
        test_html_generation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ テストの実行中にエラーが発生しました: {e}")
    
    print(f"\n=== テスト結果 ===")
    print(f"✓ 成功: {passed}/{total}")
    print(f"✗ 失敗: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 すべてのテストが成功しました！")
        return True
    else:
        print("❌ 一部のテストが失敗しました")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)