---
name: git-clean-branches
description: Use when repository has dozens of stale or merged branches cluttering the namespace, or when onboarding onto a project with an overwhelming branch list.
model: haiku
disable-model-invocation: true
argument-hint: --base <branch> --stale <days> --remote --dry-run --yes --force
context: fork
---

# Git Clean Branches

安全识别并清理已合并或过期的 Git 分支。

> 💡 **建议**: 执行本命令前,建议先运行 `/clear`
> 命令清理上下文,以获得更好的分析效果。

## 目录

- [选项说明](#选项说明)
- [执行流程](#执行流程)
- [配置保护分支](#配置保护分支)
- [最佳实践](#最佳实践)

---

## 选项说明

| 选项              | 说明                                                 |
| ----------------- | ---------------------------------------------------- |
| `--base <branch>` | 指定清理的基准分支（默认为 `main`/`master`）         |
| `--stale <days>`  | 清理超过指定天数未提交的分支（默认不启用）           |
| `--remote`        | 同时清理远程已合并/过期的分支                        |
| `--dry-run`       | **默认行为**。仅列出将要删除的分支，不执行任何操作   |
| `--yes`           | 跳过逐一确认，直接删除所有已识别的分支（适合 CI/CD） |
| `--force`         | 使用 `-D` 强制删除本地分支（即使未合并）             |

---

## 执行流程

### 1. 配置与安全预检

- **更新信息**：自动执行 `git fetch --all --prune`，确保分支状态最新
- **读取保护分支**：从 Git 配置读取不应被清理的分支列表
- **确定基准**：使用 `--base` 参数或自动识别的 `main`/`master`

### 2. 分析识别（Find）

- **已合并分支**：找出已完全合并到 `--base` 的本地（及远程）分支
- **过期分支**：如指定 `--stale <days>`，找出最后一次提交在 N 天前的分支
- **排除保护分支**：从待清理列表中移除所有已配置的保护分支

### 3. 报告预览（Report）

- 清晰列出"将要删除的已合并分支"与"将要删除的过期分支"
- 若无 `--yes` 参数，命令到此结束，等待用户确认

### 4. 执行清理（Execute）

仅在不带 `--dry-run` 且用户确认后（或带 `--yes`）执行：

- 逐一删除已识别的分支
- 本地用 `git branch -d <branch>`
- 远程用 `git push origin --delete <branch>`
- 若指定 `--force`，本地删除改用 `git branch -D <branch>`

---

## 配置保护分支

为防止误删重要分支，在仓库的 Git 配置中添加保护规则：

```bash
# 保护 develop 分支
git config --add branch.cleanup.protected develop

# 保护所有 release/ 开头的分支 (通配符)
git config --add branch.cleanup.protected 'release/*'

# 查看所有已配置的保护分支
git config --get-all branch.cleanup.protected
```

---

## 使用示例

```bash
# [最安全] 预览将要清理的分支，不执行任何删除
git fetch --all --prune
git branch --merged main

# 清理已合并到 main 且超过 90 天未动的本地分支
# 先识别过期分支
git for-each-ref --sort=-committerdate --format='%(refname:short) %(committerdate:relative)' refs/heads/

# 清理已合并到 release/v2.1 的本地与远程分支
git branch --merged release/v2.1
git push origin --delete <branch>

# 强制删除一个未合并的本地分支
git branch -D outdated-feature
```

---

## 最佳实践

1. **优先 `--dry-run`**：养成先预览再执行的习惯
2. **活用 `--base`**：维护长期 `release` 分支时，用它来清理已合并到该 release
   的分支
3. **谨慎 `--force`**：除非百分百确定某个未合并分支是无用的
4. **团队协作**：在清理共享的远程分支前，先在团队频道通知
5. **定期运行**：每月或每季度运行一次，保持仓库清爽

---

## 优势

- ✅ **更安全**：默认只读预览，且有可配置的保护分支列表
- ✅ **更灵活**：支持自定义基准分支，完美适配 `release` / `develop` 工作流
- ✅ **更兼容**：避免了在不同系统上行为不一的命令
- ✅ **更直观**：清晰的参数设计与安全选项
