#!/usr/bin/env python3
"""
リリース用スクリプト
バージョン管理とリリースプロセスを自動化します
"""

import re
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

def run_command(command, description, check=True):
    """コマンドを実行し、エラーがあれば終了する"""
    print(f"実行中: {description}")
    print(f"コマンド: {command}")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0 and check:
        print(f"エラー: {description}")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        sys.exit(1)
    else:
        print(f"成功: {description}")
        if result.stdout.strip():
            print(f"出力: {result.stdout.strip()}")
    
    return result

def get_current_version():
    """現在のバージョンを取得"""
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        print("エラー: pyproject.tomlが見つかりません")
        sys.exit(1)
    
    with open(pyproject_path, 'r') as f:
        content = f.read()
    
    match = re.search(r'version = "([^"]+)"', content)
    if not match:
        print("エラー: バージョンが見つかりません")
        sys.exit(1)
    
    return match.group(1)

def update_version(new_version):
    """バージョンを更新"""
    pyproject_path = Path("pyproject.toml")
    
    with open(pyproject_path, 'r') as f:
        content = f.read()
    
    # バージョンを更新
    content = re.sub(r'version = "[^"]+"', f'version = "{new_version}"', content)
    
    with open(pyproject_path, 'w') as f:
        f.write(content)
    
    print(f"バージョンを {new_version} に更新しました")

def create_release_notes(version, changes):
    """リリースノートを作成"""
    release_notes_path = Path("RELEASE_NOTES.md")
    
    with open(release_notes_path, 'a') as f:
        f.write(f"\n## Release {version}\n")
        f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write("### Changes\n")
        f.write(f"{changes}\n\n")
        f.write("### Installation\n")
        f.write(f"```bash\npip install db-ui-components=={version}\n```\n\n")

def main():
    """メイン関数"""
    print("=== db-ui-components リリーススクリプト ===")
    
    if len(sys.argv) < 3:
        print("使用方法: python scripts/release.py <version> <changes>")
        print("例: python scripts/release.py 1.0.1 'Bug fixes and improvements'")
        sys.exit(1)
    
    new_version = sys.argv[1]
    changes = sys.argv[2]
    
    # バージョン形式の検証
    if not re.match(r'^\d+\.\d+\.\d+$', new_version):
        print("エラー: バージョンは x.y.z 形式である必要があります")
        sys.exit(1)
    
    current_version = get_current_version()
    print(f"現在のバージョン: {current_version}")
    print(f"新しいバージョン: {new_version}")
    
    # 確認
    confirm = input(f"\nバージョンを {current_version} から {new_version} に更新しますか？ (y/N): ")
    if confirm.lower() != 'y':
        print("リリースをキャンセルしました")
        sys.exit(0)
    
    # 作業ディレクトリを確認
    if not Path("pyproject.toml").exists():
        print("エラー: プロジェクトルートで実行してください")
        sys.exit(1)
    
    # リポジトリの状態を確認
    run_command("git status --porcelain", "リポジトリの状態を確認")
    
    # 変更がある場合はコミットを促す
    result = run_command("git status --porcelain", "変更をチェック", check=False)
    if result.stdout.strip():
        print("警告: コミットされていない変更があります")
        commit = input("変更をコミットしますか？ (y/N): ")
        if commit.lower() == 'y':
            message = input("コミットメッセージを入力してください: ")
            run_command(f'git add . && git commit -m "{message}"', "変更をコミット")
    
    # バージョンを更新
    update_version(new_version)
    
    # リリースノートを作成
    create_release_notes(new_version, changes)
    
    # 変更をコミット
    run_command(
        f'git add . && git commit -m "Release version {new_version}"',
        "バージョン更新をコミット"
    )
    
    # タグを作成
    run_command(f'git tag -a v{new_version} -m "Release version {new_version}"', "タグを作成")
    
    # プッシュ
    push = input("変更をプッシュしますか？ (y/N): ")
    if push.lower() == 'y':
        run_command("git push origin main", "mainブランチをプッシュ")
        run_command(f"git push origin v{new_version}", "タグをプッシュ")
    
    print(f"\n=== リリース {new_version} の準備が完了しました ===")
    print("次のステップ:")
    print("1. GitHubでリリースを作成")
    print("2. CI/CDが自動的にPyPIにアップロードします")
    print("3. リリースノートを確認")

if __name__ == "__main__":
    main()