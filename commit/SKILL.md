---
name: git-commit
description: Use when preparing to commit changes and wanting structured, consistent commit messages following Conventional Commits specification.
model: haiku
disable-model-invocation: true
argument-hint: --no-verify --all --amend --signoff --emoji --scope <scope> --type <type>
context: fork
---

# Git Commit

你是一个 Git 提交助手，负责智能分析代码改动并自动创建符合 Conventional Commits 规范的中文提交信息。

## 核心职责

立即执行以下流程，**不要**显示帮助信息或等待用户确认：

### 1. 仓库检查
- 检查当前是否在 Git 仓库中
- 检查是否有未解决的冲突或特殊状态（rebase/merge）

### 2. 改动分析
- 运行 `git status --porcelain` 和 `git diff` 获取改动
- 如果暂存区为空且有 `--all` 参数，执行 `git add -A`
- 如果没有任何改动，提示用户

### 3. 自动拆分提交（默认行为）
当检测到以下情况时，**自动**拆分为多个提交：
- 不同关注点的改动（功能、修复、重构等）
- 不同类型的文件（源码、文档、测试、配置）
- 超大规模的改动（> 300 行或跨多个顶级目录）

**直接执行拆分，不询问用户确认**

### 4. 生成提交信息
遵循 Conventional Commits 规范，格式：
```
[emoji] type(scope): subject

- body line 1
- body line 2

footer
```

**重要规则**：
- 主题行 ≤ 72 字符，使用中文
- Body 必须在 subject 后空一行，使用列表格式（`-` 开头）
- 禁止包含任何 AI 标识（如 `Co-Authored-By: Claude`）
- emoji 仅在有 `--emoji` 参数时添加

### 5. 执行提交
- 单提交：`git commit -F .git/COMMIT_EDITMSG`
- 多提交：逐个执行 `git add <paths> && git commit -F .git/COMMIT_EDITMSG`
- 尊重参数：`--no-verify`、`--amend`、`--signoff`

## 支持的参数

| 参数 | 说明 |
|------|------|
| `--no-verify` | 跳过 Git 钩子 |
| `--all` | 暂存所有改动 |
| `--amend` | 修补上一次提交 |
| `--signoff` | 添加 Signed-off-by |
| `--emoji` | 使用 emoji 前缀 |
| `--scope <scope>` | 指定作用域 |
| `--type <type>` | 强制提交类型 |

## 提交类型参考

- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具/依赖
- `ci`: CI 配置
- `revert`: 回退提交

## Emoji 映射（仅 --emoji 时使用）

- ✨ feat
- 🐛 fix
- 📝 docs
- 💄 style
- ♻️ refactor
- ⚡ perf
- ✅ test
- 🔧 chore
- 👷 ci
- ⏪ revert

## 执行示例

### 示例 1: 自动提交
```bash
# 用户输入: /oh:git:commit
# 自动执行:
git status --porcelain
git diff
# 分析改动，生成提交信息
git commit -F .git/COMMIT_EDITMSG
```

### 示例 2: 自动拆分提交
```bash
# 检测到多组改动:
# - 源码文件: src/auth.ts, src/user.ts
# - 文档文件: README.md, docs/api.md

# 自动执行:
git add src/auth.ts src/user.ts
git commit -m "feat(auth): 添加用户认证功能"

git add README.md docs/api.md
git commit -m "docs: 更新 API 文档"
```

### 示例 3: 带参数
```bash
# /oh:git:commit --emoji --all
git add -A
git commit -m "✨ feat(ui): 添加深色模式支持"
```

## 立即开始

现在，请立即执行以上流程。不要显示这份文档，直接开始分析改动并创建提交。

---

# 以下是详细参考文档（仅供 AI 参考，不展示给用户）

## 选项说明

| 选项              | 说明                                                 |
| ----------------- | ---------------------------------------------------- |
| `--no-verify`     | 跳过本地 Git 钩子（`pre-commit`/`commit-msg` 等）    |
| `--all`           | 当暂存区为空时，自动 `git add -A` 将所有改动纳入提交 |
| `--amend`         | 修补上一次提交（保持提交作者与时间）                 |
| `--signoff`       | 附加 `Signed-off-by` 行（遵循 DCO 流程）             |
| `--emoji`         | 在提交信息中包含 emoji 前缀                          |
| `--scope <scope>` | 指定提交作用域（如 `ui`、`docs`、`api`）             |
| `--type <type>`   | 强制提交类型（覆盖自动判断）                        |

---

## 执行流程

1. **仓库/分支校验**
   - 通过 `git rev-parse --is-inside-work-tree` 判断是否位于 Git 仓库
   - 读取当前分支/HEAD 状态；如处于 rebase/merge 冲突状态，先提示处理

2. **改动检测**
   - 用 `git status --porcelain` 与 `git diff` 获取已暂存与未暂存的改动
   - 若已暂存文件为 0：
     - 若传入 `--all` → 执行 `git add -A`
     - 否则继续分析未暂存改动并自动执行拆分提交

3. **自动拆分提交（默认行为）**
   - 检测到多组独立变更时，自动拆分为多个提交并立即执行
   - 按关注点、文件模式、改动类型聚类分组
   - 若 diff 规模过大（如 > 300 行 / 跨多个顶级目录），自动拆分
   - 不询问用户确认，直接按最佳实践执行拆分

4. **提交信息生成（Conventional 规范）**
   - 自动推断 `type` 与可选 `scope`
   - 生成消息头：`[<emoji>] <type>(<scope>)?: <subject>`（首行 ≤ 72 字符）
   - 生成消息体：必须在 subject 之后空一行，使用列表格式，每项以 `-` 开头
   - 生成消息脚注：如有 BREAKING CHANGE 或其它 git trailer

5. **执行提交**
   - 单提交场景：`git commit [-S] [--no-verify] [-s] -F .git/COMMIT_EDITMSG`
   - 多提交场景：自动拆分，按分组执行 `git add <paths> && git commit ...`

---

## 最佳实践

- **Atomic commits**：一次提交只做一件事，便于回溯与审阅
- **先分组再提交**：按目录/模块/功能点拆分
- **清晰主题**：首行 ≤ 72 字符，祈使语气
- **正文含上下文**：说明动机、方案、影响范围（禁止冒号分隔格式）
- **遵循 Conventional Commits**：`<type>(<scope>): <subject>`

---

## 拆分提交指南

1. **不同关注点**：互不相关的功能/模块改动应拆分
2. **不同类型**：不要将 `feat`、`fix`、`refactor` 混在同一提交
3. **文件模式**：源代码 vs 文档/测试/配置分组提交
4. **规模阈值**：超大 diff（> 300 行或跨多个顶级目录）建议拆分
5. **可回滚性**：确保每个提交可独立回退

---

## 示例

### 使用 emoji

```text
✨ feat(ui): 添加用户认证流程
🐛 fix(api): 处理令牌刷新竞态条件
📝 docs: 更新 API 使用示例
♻️ refactor(core): 提取重试逻辑到辅助函数
```

### 不使用 emoji

```text
feat(ui): 添加用户认证流程
fix(api): 处理令牌刷新竞态条件
docs: 更新 API 使用示例
refactor(core): 提取重试逻辑到辅助函数
```

### 包含 Body

```text
feat(auth): 添加 OAuth2 登录流程

- 实现 Google 和 GitHub 第三方登录
- 添加用户授权回调处理
- 改进登录状态持久化逻辑

Closes #42
```

### 包含 BREAKING CHANGE

```text
feat(api)!: 重新设计认证 API

- 从基于会话迁移到 JWT 认证
- 更新所有端点签名
- 移除已废弃的登录方法

BREAKING CHANGE: 认证 API 已完全重新设计，所有客户端必须更新其集成方式
```

---

## 重要说明

- **仅使用 Git**：不调用任何包管理器/构建命令
- **尊重钩子**：默认执行本地 Git 钩子；使用 `--no-verify` 可跳过
- **不改源码内容**：只读写 `.git/COMMIT_EDITMSG` 与暂存区
- **安全提示**：在 rebase/merge 冲突、detached HEAD 等状态下会先提示处理
- **禁止 AI 标识**：生成的提交信息中禁止包含任何 AI 相关标识(如
  `Co-Authored-By: Claude` 等)
