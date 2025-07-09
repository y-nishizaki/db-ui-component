#!/usr/bin/env python3
"""
パッケージをビルドしてインストールするためのスクリプト
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """コマンドを実行し、エラーがあれば終了する"""
    print(f"実行中: {description}")
    print(f"コマンド: {command}")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"エラー: {description}")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        sys.exit(1)
    else:
        print(f"成功: {description}")
        if result.stdout.strip():
            print(f"出力: {result.stdout.strip()}")

def main():
    """メイン関数"""
    print("=== db-ui-components パッケージビルドスクリプト ===")
    
    # 必要なファイルが存在するかチェック
    required_files = [
        "pyproject.toml",
        "setup.py",
        "MANIFEST.in",
        "README.md",
        "LICENSE",
        "requirements.txt",
        "db_ui_components/__init__.py"
    ]
    
    for file_path in required_files:
        if not Path(file_path).exists():
            print(f"エラー: 必要なファイルが見つかりません: {file_path}")
            sys.exit(1)
    
    print("✓ 必要なファイルがすべて存在します")
    
    # 古いビルドファイルをクリーンアップ
    run_command("rm -rf build/ dist/ *.egg-info/", "古いビルドファイルをクリーンアップ")
    
    # パッケージをビルド
    run_command("python3 -m build", "パッケージをビルド")
    
    # ビルドされたファイルを確認
    dist_files = list(Path("dist").glob("*"))
    if dist_files:
        print("✓ ビルドされたファイル:")
        for file_path in dist_files:
            print(f"  - {file_path}")
    else:
        print("エラー: ビルドされたファイルが見つかりません")
        sys.exit(1)
    
    # 開発モードでインストール（オプション）
    install_dev = input("\n開発モードでインストールしますか？ (y/N): ").lower().strip()
    if install_dev == 'y':
        run_command("pip3 install -e .", "開発モードでインストール")
        
        # インストールテスト
        try:
            import db_ui_components
            print(f"✓ パッケージが正常にインポートされました: {db_ui_components.__version__}")
            print(f"✓ 利用可能なコンポーネント: {db_ui_components.__all__}")
        except ImportError as e:
            print(f"エラー: パッケージのインポートに失敗しました: {e}")
            sys.exit(1)
    
    print("\n=== ビルド完了 ===")
    print("パッケージをインストールするには:")
    print("  pip install .")
    print("または、開発モードでインストールするには:")
    print("  pip install -e .")

if __name__ == "__main__":
    main()