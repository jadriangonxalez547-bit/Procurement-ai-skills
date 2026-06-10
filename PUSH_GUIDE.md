# VSCode 推送教程（逐步带图）

本教程演示如何用 **VSCode 内置 Git** 把 `d:\AI\Procurement-ai-skills` 推送到 GitHub。

整个过程大约 5 分钟，**无需安装任何扩展**。

---

## 📋 准备：确认 4 件事

| # | 事项 | 检查方法 |
|---|------|---------|
| 1 | Git 已安装 | 终端运行 `git --version` |
| 2 | VSCode 已安装 | — |
| 3 | GitHub 账号已登录浏览器 | — |
| 4 | 项目文件就位 | `d:\AI\Procurement-ai-skills\` 有 19 个文件 |

打开 PowerShell 快速确认：

```powershell
git --version
# 应显示: git version 2.x.x
```

如果提示 "git 不是内部命令" → [安装 Git](https://git-scm.com/download/win)

---

## 第 1 步：打开项目文件夹

**操作：**

1. 打开 VSCode
2. 按 `Ctrl + K, Ctrl + O`（或菜单 文件 → 打开文件夹）
3. 输入路径：`d:\AI\Procurement-ai-skills`
4. 点击"选择文件夹"

**界面示意：**

```
┌─────────────────────────────────────────────────┐
│ File  Edit  Selection  View  Go  Run  Terminal  │  ← 顶部菜单栏
├─────────────────────────────────────────────────┤
│ Explorer                              [···]    │
│ ▼ PROCU~1                                       │  ← 大写显示（Windows 8.3 短名）
│   ▼ Procurement-ai-skills                       │  ← 实际目录
│     ▼ .vscode/                                  │
│     ▼ skills/                                   │
│       ▼ 1688-logistics-scraper/                 │
│         • SKILL.md                              │
│         • README.md                             │
│         • requirements.txt                      │
│         • install.ps1                           │
│         ...                                     │
│     • README.md                                 │
│     • LICENSE                                   │
│     • .gitignore                                │
│                                                 │
│                                                 │
│                  [空编辑器区域]                 │
└─────────────────────────────────────────────────┘
```

✅ **确认点**：左侧能看到 `.gitignore`、`LICENSE`、`README.md`、`skills/1688-logistics-scraper/` 等。

---

## 第 2 步：初始化 Git 仓库

**操作：**

1. 点击左侧活动栏的 **"源代码管理"图标**（看起来像 3 个圆点的分叉）
   ```
   活动栏位置：
   ┌──────┐
   │ 📁   │  ← Explorer
   │ 🔍   │  ← Search
   │ 🔀   │  ← Source Control ← 点这里！
   │ 🐛   │  ← Run and Debug
   │ 🧩   │  ← Extensions
   └──────┘
   ```

2. 源代码管理面板会显示 "源代码管理存储库中未发现任何内容" 或 "Initialize Repository" 按钮
3. 点击 **"Initialize Repository"** 按钮

**界面示意：**

```
源代码管理面板（点击 Initialize Repository 之前）：
┌──────────────────────────────────────────────┐
│ 源代码管理                          [···]    │
├──────────────────────────────────────────────┤
│                                              │
│   源代码管理存储库中未发现任何内容          │
│   Initialize Repository                      │  ← 点这个！
│                                              │
└──────────────────────────────────────────────┘
```

点击后，VSCode 会在文件夹下创建 `.git/` 目录，文件列表上会出现 **U**（Untracked）标记。

**界面示意（初始化后）：**

```
源代码管理面板：
┌──────────────────────────────────────────────┐
│ 源代码管理                       [···]       │
├──────────────────────────────────────────────┤
│ ▼ Changes (19)                               │  ← 19 个文件待暂存
│   U  .gitignore                               │
│   U  LICENSE                                  │
│   U  PUSH_GUIDE.md                            │
│   U  README.md                                │
│   U  skills/1688-logistics-scraper/...        │
│   ...                                        │
└──────────────────────────────────────────────┘
```

---

## 第 3 步：检查暂存内容（重要！）

**目的**：确保没有意外的文件被加入（比如本地数据、Excel 锁文件）

**操作：**

1. 在源代码管理面板，点 **"Changes"** 旁边的下拉箭头展开
2. 仔细查看 19 个待提交文件

**✅ 应该看到的：**

```
✓ .gitignore
✓ LICENSE
✓ PUSH_GUIDE.md（本文件）
✓ README.md
✓ skills/1688-logistics-scraper/SKILL.md
✓ skills/1688-logistics-scraper/README.md
✓ skills/1688-logistics-scraper/requirements.txt
✓ skills/1688-logistics-scraper/install.ps1
✓ skills/1688-logistics-scraper/install.sh
✓ skills/1688-logistics-scraper/references/operations.md
✓ skills/1688-logistics-scraper/references/excel-format.md
✓ skills/1688-logistics-scraper/scripts/click_next.js
✓ skills/1688-logistics-scraper/scripts/detect_pages.js
✓ skills/1688-logistics-scraper/scripts/extract_one_page.js
✓ skills/1688-logistics-scraper/scripts/gen_excel.py
✓ skills/1688-logistics-scraper/scripts/page_loop.py
✓ skills/supplier-reconciliation/SKILL.md
✓ skills/supplier-reconciliation/README.md
✓ skills/customs-declaration-checker/SKILL.md
✓ skills/customs-declaration-checker/README.md
```

**❌ 不应该看到的：**

```
✗ orders_data.json
✗ *.xlsx
✗ ~$*.xlsx（Excel 锁文件）
✗ __pycache__/
✗ .venv/
```

如果看到了意外文件：
- 在该文件上**右键** → "Discard Changes"（放弃）

---

## 第 4 步：暂存所有文件

**操作：**

1. 在源代码管理面板顶部，找到 **"+"** 按钮（"Stash" 旁边）
2. 或者在 "Changes" 文字上悬停，会出现 **"+"**
3. 点击 **"+"** 暂存所有更改

**快捷键**：`Ctrl + Shift + A`（macOS: `Cmd + Shift + A`）

**界面示意：**

```
源代码管理面板（暂存前）：
┌──────────────────────────────────────────────┐
│ 源代码管理                       [···]       │
├──────────────────────────────────────────────┤
│ ▼ Changes (19)                               │
│   U  .gitignore              [+][↶]          │  ← 单个文件 + 号
│   U  LICENSE                                  │
│   ...                            [+]         │  ← 这里：暂存所有
│   ────────────────────────                    │
│   Message (Ctrl+Enter to commit)             │
│   [输入框]                                    │
└──────────────────────────────────────────────┘
```

点击 **+** 后：

```
源代码管理面板（暂存后）：
┌──────────────────────────────────────────────┐
│ 源代码管理                       [···]       │
├──────────────────────────────────────────────┤
│ ▼ Staged Changes (19)                        │  ← 已暂存
│   A  .gitignore                               │  ← A = Added
│   A  LICENSE                                  │
│   ...                                        │
│ ▼ Changes (0)                                │  ← 没有未暂存了
└──────────────────────────────────────────────┘
```

---

## 第 5 步：首次提交

**操作：**

1. 在源代码管理面板顶部，找到 **"Message" 输入框**（写着 "Message (Ctrl+Enter to commit)"）
2. 输入提交信息：

```
Initial commit: 1688 Logistics Scraper + 2 placeholder skills

- 1688 Logistics Scraper: 完整可用的物流抓取 skill
- Supplier Reconciliation: 占位 skill
- Customs Declaration Checker: 占位 skill
- 顶层 README、LICENSE、.gitignore
- 跨平台安装脚本（PowerShell + Bash）
```

3. 按 **`Ctrl + Enter`** 提交

**界面示意：**

```
源代码管理面板（提交后）：
┌──────────────────────────────────────────────┐
│ 源代码管理                       [···]       │
├──────────────────────────────────────────────┤
│                                              │
│   暂存更改后源代码管理提供程序中没有        │
│   任何待提交的内容                          │
│                                              │
└──────────────────────────────────────────────┘

状态栏（底部）：
[main]  ↓0 ↑0     ← 表示主分支，无未推送内容
```

---

## 第 6 步：添加远程仓库

**操作：**

1. 按 **`Ctrl + Shift + P`** 打开命令面板
2. 输入：`Git: Add Remote`
3. 选择它

**界面示意：**

```
命令面板（顶部）：
┌──────────────────────────────────────────────┐
│ 🔍 > Git: Add Remote                         │  ← 输入这个
├──────────────────────────────────────────────┤
│   Git: Add Remote                            │  ← 选中这条
│   Git: Remove Remote                         │
│   Git: Fetch                                 │
│   ...                                        │
└──────────────────────────────────────────────┘
```

4. 输入 **远程名称**：`origin`
5. 输入 **远程 URL**：`https://github.com/jadriangonxalez547-bit/Procurement-ai-skills.git`

**界面示意（输入过程）：**

```
┌──────────────────────────────────────────────┐
│ 🔍 > origin                                  │  ← 第 1 步：输入名称
├──────────────────────────────────────────────┤
│ > origin                                     │
│   (Press 'Enter' to confirm or 'Escape' to   │
│    cancel)                                   │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│ 🔍 > https://github.com/jadriangonxalez547-  │  ← 第 2 步：输入 URL
│     bit/Procurement-ai-skills.git            │
├──────────────────────────────────────────────┤
│ > https://github.com/jadriangonxalez547-bit/ │
│   Procurement-ai-skills.git                  │
└──────────────────────────────────────────────┘
```

✅ 添加成功后，VSCode 会弹出提示"Successfully added remote"

---

## 第 7 步：推送到 GitHub

**操作（方案 A - 自动弹窗）：**

提交后右下角应该弹出：

```
┌──────────────────────────────────────────────┐
│ The current branch 'main' has no upstream   │
│ branch. Would you like to publish it?       │
│                                              │
│        [OK]              [Cancel]            │
└──────────────────────────────────────────────┘
```

点 **"OK"** 开始推送。

**操作（方案 B - 手动触发）：**

如果弹窗没出现：
1. 源代码管理面板 → 点 **"···"** 菜单
2. 选择 **"Push"**（推送）
3. 或 `Ctrl + Shift + P` → 输入 `Git: Push`

**界面示意：**

```
源代码管理面板（点 ··· 菜单）：
┌──────────────────────────────────────────────┐
│ 源代码管理                       [···]       │
├──────────────────────────────────────────────┤
│                                  Push        │  ← 点这个
│                                  Pull        │
│                                  Fetch       │
│                                  ...         │
└──────────────────────────────────────────────┘
```

---

## 第 8 步：处理推送冲突

**如果远程仓库已有内容**（比如之前的 1 行 README），会报错：

```
! [rejected] main -> main (fetch first)
error: failed to push some refs to ...
```

**解决方法：先拉取再推送**

**操作：**

1. 源代码管理面板 → 点 **"···"** 菜单
2. 选择 **"Pull"**（拉取）
3. 如果提示合并冲突 → 选择 **"Accept Incoming"**（接受远程版本，因为远程只有 1 行 README）
4. 然后再次 **"Push"**

**界面示意（合并冲突）：**

```
┌──────────────────────────────────────────────┐
│ Git: Merge conflict detected                │
│                                              │
│   [Accept Incoming]    [Accept Current]      │
│   [Accept Both]        [Compare]             │
└──────────────────────────────────────────────┘
```

> 💡 **更简单的方法**：直接先 `git pull --rebase`，让提交历史是干净的。

---

## 第 9 步：首次推送认证

**如果弹出认证窗口：**

```
┌──────────────────────────────────────────────┐
│ Sign in to GitHub                            │
│                                              │
│   [Sign in with your browser]                │  ← 点这个
│                                              │
└──────────────────────────────────────────────┘
```

**步骤：**
1. 点击 "Sign in with your browser"
2. 浏览器自动打开 GitHub 授权页
3. 点 "Authorize GitCredentialManager"
4. 回到 VSCode，推送继续

**界面示意（GitHub 浏览器授权页）：**

```
┌──────────────────────────────────────────────┐
│ Git Credential Manager wants to access      │
│ your jadriangonxalez547-bit account          │
│                                              │
│   [Authorize]   [Cancel]                     │
└──────────────────────────────────────────────┘
```

---

## 第 10 步：验证推送成功

**操作：**

1. VSCode 底部状态栏应该显示：
   ```
   [main ↑0]    ← 表示无待推送
   ```

2. 打开浏览器访问：https://github.com/jadriangonxalez547-bit/Procurement-ai-skills

**应该看到：**

```
✅ 仓库不再只有 1 行 README
✅ 看到完整目录树：
   ├── .gitignore
   ├── LICENSE
   ├── README.md
   ├── PUSH_GUIDE.md
   └── skills/
       ├── 1688-logistics-scraper/
       ├── supplier-reconciliation/
       └── customs-declaration-checker/

✅ README 渲染正常（不显示 README.md 源码，而是排版后的内容）
✅ commit history 显示你的提交
```

---

## 🎯 推送后：设置 Topics

1. 访问 https://github.com/jadriangonxalez547-bit/Procurement-ai-skills
2. 点右上角 **⚙️** （About 旁的齿轮）
3. 在 **Topics** 输入：
   ```
   claude-code ai-skills procurement 1688 logistics supply-chain
   ```
4. 点 "Save changes"

**界面示意：**

```
┌──────────────────────────────────────────────┐
│ About                                        │
├──────────────────────────────────────────────┤
│ ⭐ 0 stars  🍴 0 forks                        │
│                                              │
│ Description:                                │
│ 采购、供应商管理、对账及流程自动化的生产级   │
│ AI Skills。                                  │
│                                              │
│ Topics:                                      │
│ [claude-code] [ai-skills] [procurement]      │
│ [1688] [logistics] [supply-chain]            │  ← 添加这些
│                                              │
│                [Save changes]                │
└──────────────────────────────────────────────┘
```

---

## 🐛 常见错误速查

| 错误信息 | 原因 | 解决 |
|---------|------|------|
| `git: command not found` | Git 未安装 | [安装 Git](https://git-scm.com/download/win) |
| `fatal: not a git repository` | 没初始化 | 第 2 步重来 |
| `Permission denied` | 没仓库写权限 | 确认是仓库 owner |
| `Authentication failed` | 凭证问题 | 第 9 步重新认证 |
| `Updates were rejected` | 远程有新内容 | 第 8 步先 Pull |
| `fatal: refusing to merge unrelated histories` | 历史不相关 | `git pull origin main --allow-unrelated-histories` |
| 推送按钮是灰的 | 没有提交 | 回到第 5 步 |

---

## 🎉 完成！

推送成功后：

1. ✅ 在 README 里加 1-2 张截图（可选）
2. ✅ 设置仓库 Topics
3. ✅ 创建 v0.1.0 Release
4. ✅ 分享给别人测试安装

**让别人测试你的 skill**：

让朋友在 PowerShell 跑：
```powershell
irm https://raw.githubusercontent.com/jadriangonxalez547-bit/Procurement-ai-skills/main/skills/1688-logistics-scraper/install.ps1 | iex
```

如果他装上后能成功抓取 1688 物流 → 你的发布就成功了！🎉