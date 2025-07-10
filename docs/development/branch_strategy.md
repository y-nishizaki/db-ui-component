# ブランチ戦略ガイド

このドキュメントでは、Databricks UI Component Libraryプロジェクトの標準的なブランチ戦略と運用ルールについて説明します。

---

## 1. ブランチの種類と役割

| ブランチ名         | 役割・用途                         |
|-------------------|-------------------------------------|
| main              | 本番リリース用の安定ブランチ        |
| develop           | 開発・統合用の最新ブランチ          |
| feature/xxx       | 新機能開発用の一時ブランチ           |
| fix/xxx           | バグ修正用の一時ブランチ             |
| hotfix/xxx        | 本番緊急修正用の一時ブランチ         |
| release/xxx       | リリース準備用の一時ブランチ         |

---

## 2. 運用ルール

### ブランチ作成
- **feature/xxx**: developから分岐
- **fix/xxx**: developから分岐
- **hotfix/xxx**: mainから分岐
- **release/xxx**: developから分岐

### マージルール
- **feature/xxx → develop**: プルリクエスト（レビュー必須）
- **fix/xxx → develop**: プルリクエスト（レビュー必須）
- **release/xxx → main, develop**: プルリクエスト（テスト・レビュー必須）
- **hotfix/xxx → main, develop**: プルリクエスト（緊急時はmain優先、後でdevelopへもマージ）

### mainブランチの保護設定
mainブランチは本番リリース用の安定ブランチのため、以下の保護設定が適用されています：
- 直接push禁止（必ずPull Request経由でマージ）
- レビュー必須（最低1名以上の承認）
- CI（テスト・Lint）が全て成功しないとマージ不可
- 強制プッシュ（force push）禁止

### ブランチ削除
- マージ後は不要な一時ブランチ（feature, fix, hotfix, release）は削除

---

## 3. リリースフロー

1. **開発**: feature/xxx, fix/xxxで開発し、developへマージ
2. **リリース準備**: developからrelease/xxxを作成し、最終テスト
3. **本番反映**: release/xxxをmainへマージ（本番リリース）、同時にdevelopにもマージ
4. **緊急修正**: mainからhotfix/xxxを作成し、mainへマージ後、developにも反映

---

## 4. CI/CDとの連携

- **developブランチ**: push時にTestPyPIへ自動デプロイ
- **mainブランチ**: GitHub Release作成時にPyPIへ本番デプロイ
- **feature/fix/hotfix/releaseブランチ**: push/PR時にテスト・Lintのみ実行

---

## 5. 運用例

### 新機能開発の流れ
```bash
git checkout develop
git pull origin develop
git checkout -b feature/add-cool-chart
# ...開発...
git push origin feature/add-cool-chart
# PR作成→レビュー→developへマージ
```

### 本番リリースの流れ
```bash
git checkout develop
git pull origin develop
git checkout -b release/v1.2.0
# ...最終テスト...
git push origin release/v1.2.0
# PR作成→mainへマージ→GitHub Release作成
# release/v1.2.0をdevelopにもマージ
```

### 緊急修正の流れ
```bash
git checkout main
git pull origin main
git checkout -b hotfix/fix-critical-bug
# ...修正...
git push origin hotfix/fix-critical-bug
# PR作成→mainへマージ→developにもマージ
```

---

## 6. よくある質問

### Q. ブランチ名の命名規則は？
A. `feature/`, `fix/`, `hotfix/`, `release/`の後に内容を短く記述してください。

### Q. mainとdevelopの違いは？
A. mainは本番用、developは開発統合用です。

### Q. どのブランチでリリースされる？
A. mainブランチでGitHub Releaseを作成したときのみPyPIに本番リリースされます。



---

## 参考
- [contributing.md](./contributing.md)
- [setup.md](./setup.md) 