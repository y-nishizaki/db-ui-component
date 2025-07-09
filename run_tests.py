#!/usr/bin/env python3
"""
テスト実行スクリプト

Databricks UI Component Libraryのテストを実行するためのスクリプトです。
pytestが利用できない環境でも基本的なテストを実行できます。
"""

import sys
import os
import importlib.util
import traceback

def run_test_file(test_file_path):
    """テストファイルを実行"""
    print(f"\n{'='*60}")
    print(f"テストファイル実行: {test_file_path}")
    print(f"{'='*60}")
    
    if not os.path.exists(test_file_path):
        print(f"❌ テストファイルが見つかりません: {test_file_path}")
        return False
    
    # テストファイルを動的にインポート
    spec = importlib.util.spec_from_file_location("test_module", test_file_path)
    if spec is None:
        print(f"❌ テストファイルのspecが作成できませんでした: {test_file_path}")
        return False
    
    test_module = importlib.util.module_from_spec(spec)
    
    try:
        if spec.loader is not None:
            spec.loader.exec_module(test_module)
            print(f"✅ テストファイルを正常に読み込みました: {test_file_path}")
            return True
        else:
            print(f"❌ テストファイルのローダーが見つかりません: {test_file_path}")
            return False
    except Exception as e:
        print(f"❌ テストファイルの読み込みに失敗しました: {test_file_path}")
        print(f"エラー: {e}")
        traceback.print_exc()
        return False

def check_dependencies():
    """依存関係の確認"""
    print("📋 依存関係の確認")
    print("-" * 40)
    
    required_packages = [
        'pandas',
        'numpy',
        'pytest'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} - インストール済み")
        except ImportError:
            print(f"❌ {package} - 未インストール")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  以下のパッケージがインストールされていません:")
        for package in missing_packages:
            print(f"   - {package}")
        print(f"\n以下のコマンドでインストールしてください:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_project_structure():
    """プロジェクト構造の確認"""
    print("\n📁 プロジェクト構造の確認")
    print("-" * 40)
    
    required_files = [
        'db_ui_components/__init__.py',
        'db_ui_components/chart_component.py',
        'db_ui_components/table_component.py',
        'db_ui_components/filter_component.py',
        'db_ui_components/dashboard.py',
        'tests/test_components.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  以下のファイルが見つかりません:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    return True

def list_available_tests():
    """利用可能なテストの一覧"""
    print("\n🧪 利用可能なテストファイル")
    print("-" * 40)
    
    test_files = [
        'tests/test_components.py',
        'tests/test_edge_cases.py',
        'tests/test_performance.py',
        'tests/test_html_validation.py',
        'tests/test_integration.py',
        'tests/conftest.py'
    ]
    
    available_tests = []
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"✅ {test_file}")
            available_tests.append(test_file)
        else:
            print(f"❌ {test_file}")
    
    return available_tests

def run_basic_syntax_check():
    """基本的な構文チェック"""
    print("\n🔍 基本的な構文チェック")
    print("-" * 40)
    
    test_files = [
        'tests/test_components.py',
        'tests/test_edge_cases.py',
        'tests/test_performance.py',
        'tests/test_html_validation.py',
        'tests/test_integration.py',
        'tests/conftest.py'
    ]
    
    success_count = 0
    total_count = 0
    
    for test_file in test_files:
        if os.path.exists(test_file):
            total_count += 1
            if run_test_file(test_file):
                success_count += 1
    
    print(f"\n📊 結果: {success_count}/{total_count} ファイルが正常に読み込まれました")
    return success_count == total_count

def main():
    """メイン実行関数"""
    print("🚀 Databricks UI Component Library テストランナー")
    print("=" * 60)
    
    # 1. 依存関係の確認
    if not check_dependencies():
        print("\n❌ 依存関係の確認に失敗しました")
        sys.exit(1)
    
    # 2. プロジェクト構造の確認
    if not check_project_structure():
        print("\n❌ プロジェクト構造の確認に失敗しました")
        sys.exit(1)
    
    # 3. 利用可能なテストの確認
    available_tests = list_available_tests()
    
    if not available_tests:
        print("\n❌ 利用可能なテストファイルが見つかりません")
        sys.exit(1)
    
    # 4. 基本的な構文チェック
    if run_basic_syntax_check():
        print("\n✅ 全てのテストファイルが正常に読み込まれました")
    else:
        print("\n❌ 一部のテストファイルに問題があります")
        sys.exit(1)
    
    # 5. 実行方法の案内
    print("\n📝 テスト実行方法")
    print("-" * 40)
    print("pytestがインストールされている場合:")
    print("  pytest tests/")
    print("  pytest tests/test_components.py")
    print("  pytest tests/test_performance.py -v")
    print("  pytest --cov=db_ui_components tests/")
    print()
    print("個別のテストファイルを確認する場合:")
    print("  python3 -c \"import sys; sys.path.append('.'); import tests.test_components\"")
    print()
    print("✅ テストの準備が完了しました！")

if __name__ == "__main__":
    main()