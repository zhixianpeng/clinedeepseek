# Git + GitHub 完整命令速查手册

> 教程日期：2026-06-12
> 项目：d:/app/qoder_xiangmu/clinedeepseek
> GitHub 仓库：https://github.com/zhixianpeng/clinedeepseek

---

## 目录

- [一、核心概念：Git 工作区模型](#一核心概念git-工作区模型)
- [二、基础流程：从零到推送 GitHub（10 步）](#二基础流程从零到推送-github10-步)
- [三、本地分支操作（9 步）](#三本地分支操作9-步)
- [四、远程分支操作（7 步）](#四远程分支操作7-步)
- [五、日常开发流程](#五日常开发流程)
- [六、命令速查表](#六命令速查表)
- [七、.gitignore 配置参考](#七gitignore-配置参考)

---

## 一、核心概念：Git 工作区模型

```
  工作区          →     暂存区          →      本地仓库          →      远程仓库(GitHub)
  (你写的文件)         (git add 后)          (git commit 后)        (git push 后)
```

| 区域 | 是什么 | 类比 |
|------|--------|------|
| **工作区** | 你电脑上的文件夹，你在里面改代码 | 菜市场买回来的菜 |
| **暂存区** | 一个"草稿箱"，你告诉 Git "这些文件下次提交" | 洗好切好摆在砧板上的菜 |
| **本地仓库** | `.git` 隐藏文件夹，存着所有历史版本 | 做好的菜，归档记录 |
| **远程仓库** | GitHub 服务器上的仓库，别人也能看到 | 把菜发到朋友圈分享 |

---

## 二、基础流程：从零到推送 GitHub（10 步）

### 第 1 步：配置身份信息（一辈子只做一次）

```bash
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的GitHub绑定邮箱"

# 查看配置
git config --global --list
```

**为什么？** GitHub 根据邮箱来判定"这个提交是谁做的"。不配的话提交记录不会显示你的头像和名字。

> 当前项目配置：
> - `user.name` = `zhixianpeng`
> - `user.email` = `1798017672@qq.com`

---

### 第 2 步：`git init` — 初始化仓库

```bash
cd 你的项目目录
git init
```

**效果：** 创建 `.git` 隐藏文件夹，里面存着项目的所有版本历史。一个项目只需执行一次。

---

### 第 3 步：`git status` — 查看状态（最常用命令）

```bash
git status
```

| 输出 | 含义 |
|------|------|
| `Untracked files` | 新文件，Git 还没关注它们 |
| `Changes not staged for commit` | 文件被修改了，但还没暂存 |
| `Changes to be committed` | 文件已暂存，等待提交 |
| `nothing to commit, working tree clean` | 一切干净，没有变化 |

**建议：** 每次操作前后都执行一遍 `git status`，确保知道自己在干嘛。

---

### 第 4 步：`git add` — 加入暂存区

```bash
git add 文件名.py            # 添加单个文件
git add .                    # 添加当前目录下所有文件（最常用）
git add *.py                 # 添加所有 .py 文件
```

**效果：** 把文件的当前状态"拍照"放入暂存区（购物车），还没真正保存。

---

### 第 5 步：`git commit` — 创建提交

```bash
git commit -m "这里写提交说明"
```

**效果：** 把暂存区的内容打包成一个"版本快照"，永久存入 Git 历史。

**好的提交说明示例：**
```bash
git commit -m "添加数据导出功能"
git commit -m "修复了导出时日期格式错误"
```

---

### 第 6 步：`git log` — 查看提交历史

```bash
git log                  # 完整版（作者、时间、完整hash）
git log --oneline        # 简洁版（一行一条，最常用）
git log --oneline -5     # 只看最近 5 条
```

---

### 第 7 步：在 GitHub 上创建远程仓库

1. 打开 https://github.com 并登录
2. 点击右上角 **+** → **New repository**
3. 填写：
   - **Repository name**：项目名（如 `clinedeepseek`）
   - **Public / Private**：选 Public
   - ⚠️ **不要勾选** "Initialize with README" 等任何选项
4. 点击 **Create repository**
5. GitHub 会显示 3 条命令，记下来后面用

---

### 第 8 步：`git remote add` — 连接远程仓库

```bash
git remote add origin https://github.com/你的用户名/仓库名.git

# 验证连接
git remote -v
```

**效果：** 给本地仓库添加一个叫 `origin` 的远程地址。`origin` 是约定俗成的名字。

> 示例：`git remote add origin https://github.com/zhixianpeng/clinedeepseek.git`

---

### 第 9 步：`git push` — 推送到 GitHub

**第一次推送（需要 `-u` 设置上游分支）：**
```bash
git push -u origin main
```

**之后每次推送（简洁版）：**
```bash
git push
```

**效果：** 把本地仓库的所有提交"同步"到 GitHub。第一次会弹出浏览器要求登录认证。

---

### 第 10 步：验证

```bash
# 终端验证
git status
# 应该显示：Your branch is up to date with 'origin/main'.

# 浏览器验证：打开 https://github.com/你的用户名/仓库名
```

---

## 三、本地分支操作（9 步）

### 第 1 步：查看所有分支

```bash
git branch          # 查看本地所有分支（* 为当前分支）
git branch -a       # 查看本地 + 远程所有分支
git branch -r       # 只查看远程分支
```

### 第 2 步：创建新分支

```bash
git branch dev              # 创建 dev 分支
git branch feature-login    # 创建 feature-login 分支
```

**注意：** 创建后你还停在当前分支，没有自动切换过去。

### 第 3 步：切换分支

```bash
git switch 分支名              # 切换到已存在的分支
git switch -c 新分支名          # 创建并切换（一步到位，最常用）

# 旧版写法（也能用）
git checkout 分支名
git checkout -b 新分支名
```

### 第 4 步：在新分支上正常开发

```bash
git status           # 查看状态
git add .            # 暂存
git commit -m "提交说明"  # 提交
git log --oneline    # 查看历史
```

此时提交**只存在新分支上**，main 分支不受任何影响。

### 第 5 步：确认当前所在分支

```bash
git branch
# * 号表示你当前所在的分支
```

### 第 6 步：切回 main 分支

```bash
git switch main
```

切回 main 后，之前在 feature 分支上的代码**暂时不可见**（不是丢了，是 main 上本来就没有）。

### 第 7 步：合并分支到 main

```bash
git switch main              # 先切到目标分支（main）
git merge feature-export     # 把 feature-export 合并过来
```

**可能有冲突需要解决：**

打开冲突文件，找 `<<<<<<<` `=======` `>>>>>>>` 标记，手动决定保留哪边的代码后保存：

```bash
git add 冲突文件名
git commit -m "解决合并冲突"
```

### 第 8 步：推送合并后的 main 到 GitHub

```bash
git push
```

### 第 9 步：删除已合并的分支（清理）

```bash
git branch -d feature-export          # 删除本地分支（已合并）
git branch -D feature-export          # 强制删除（即使没合并）
```

---

## 四、远程分支操作（7 步）

### 第 1 步：首次推送本地分支到 GitHub

```bash
git push -u origin 分支名
```

示例：`git push -u origin feature-report`

**输出说明：**
```
branch 'feature-report' set up to track 'origin/feature-report'.
```
跟踪关系已建立，后续无需 `-u`。

### 第 2 步：后续推送（简洁版）

```bash
git push
```

### 第 3 步：查看远程分支

```bash
git branch -a        # 本地 + 远程
git branch -r        # 只看远程
```

### 第 4 步：下载远程分支信息（不合并）

```bash
git fetch origin
```

**效果：** 去 GitHub 看看有没有新分支或新提交，只下载不修改代码，安全操作。

### 第 5 步：把远程分支拉到本地（3 种方式）

**方式 A：`git pull` — 拉取 + 自动合并（最常用）**
```bash
git pull
```
等于 `git fetch` + `git merge` 一步完成。

**方式 B：克隆远程分支到本地**
```bash
git switch -c 本地分支名 origin/远程分支名
git switch -c feature-report origin/feature-report
```

**方式 C：如果本地该分支不存在，Git 可能自动处理**
```bash
git switch dev
# Git 会自动创建本地 dev → 跟踪 origin/dev → 切换过去
```

### 第 6 步：删除远程分支

```bash
git push origin --delete 分支名
```

### 第 7 步：在 GitHub 网页创建分支后拉到本地

```bash
git fetch origin               # 下载远程新分支信息
git branch -r                  # 确认看到远程新分支
git switch -c 本地名 origin/远程名  # 拉到本地
```

---

## 五、日常开发流程

### 日常只需 3 条命令

```bash
git add .
git commit -m "描述你做了什么修改"
git push
```

### 完整开发流程示例

```bash
# ===== 第 1 阶段：创建分支并开发 =====
git switch -c feature-新功能名     # 创建并切换
# 改代码...
git add .
git commit -m "完成新功能"
git push -u origin feature-新功能名  # 首次推送到 GitHub

# ===== 第 2 阶段：合并到 main =====
git switch main                    # 切回 main
git pull                           # 拉取最新代码
git merge feature-新功能名          # 合并
git push                           # 推送给 GitHub

# ===== 第 3 阶段：清理 =====
git branch -d feature-新功能名       # 删除本地分支
git push origin --delete feature-新功能名  # 删除远程分支
```

---

## 六、命令速查表

### 基础命令

| 命令 | 作用 | 频率 |
|------|------|:--:|
| `git status` | 查看当前状态 | 🔄 随时 |
| `git add .` | 暂存所有修改 | 📝 每次 |
| `git commit -m "..."` | 保存版本快照 | 📝 每次 |
| `git push` | 上传到 GitHub | 📤 每天 |
| `git log --oneline` | 查看提交历史 | 📖 偶尔 |
| `git pull` | 拉取远程最新代码 | 📥 合作时 |

### 分支命令

| 命令 | 作用 |
|------|------|
| `git branch` | 查看本地所有分支 |
| `git branch 分支名` | 创建分支 |
| `git switch 分支名` | 切换分支 |
| `git switch -c 分支名` | **创建 + 切换（最常用）** |
| `git merge 分支名` | 把指定分支合并到当前分支 |
| `git branch -d 分支名` | 删除已合并的本地分支 |
| `git branch -D 分支名` | 强制删除本地分支 |
| `git push -u origin 分支名` | 首次推送本地分支到 GitHub |
| `git push origin --delete 分支名` | 删除远程分支 |

### 远程分支命令

| 命令 | 作用 |
|------|------|
| `git branch -r` | 查看远程分支 |
| `git branch -a` | 查看本地 + 远程所有分支 |
| `git fetch origin` | 下载远程信息（不合并） |
| `git switch -c 本地名 origin/远程名` | 克隆远程分支到本地 |

---

## 七、.gitignore 配置参考

```gitignore
# 忽略真实的配置文件（含 Cookie）
config.json

# 忽略下载输出目录
output/

# VS Code 编辑器设置
.vscode/

# Python cache
__pycache__/
*.pyc
*.pyo

# 临时数据文件（不提交到仓库）
*.xlsx
*.txt
```

---

> **最后更新：** 2026-06-12
> **作者：** zhixianpeng
> **GitHub：** https://github.com/zhixianpeng/clinedeepseek