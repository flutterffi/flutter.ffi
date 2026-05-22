---
title: Git 日常使用案例：从改代码到安全上线
date: 2026-05-22
category: 技术
tags:
  - Git
  - 工作流
excerpt: 用一条真实分支流程串起 clone、分支、提交、推送、合并与回滚，适合个人博客与小型项目。
---
<img src="/photos/thumb-13.jpg" alt="配图" class="article-banner" loading="lazy" />

<div class="figure wide">
  <img src="/photos/photo-06.jpg" alt="随拍配图" loading="lazy" />
  <p class="figure-caption">留白处，读者可以补上自己的判断。</p>
</div>


# Git 日常使用案例：从改代码到安全上线

下面用「给博客加一篇文章并部署」这条线，把 Git 最常用的命令串起来。你可以在自己的项目里照着做一遍。

## 场景一：第一次拿到仓库

```bash
git clone git@github.com:yourname/your-repo.git
cd your-repo
git status
```

`clone` 会复制远程仓库，并默认建立 `origin` 远程与当前分支跟踪关系。

## 场景二：开分支写新功能

不要在 `main` 上直接堆提交，习惯用功能分支：

```bash
git checkout -b feat/new-post
# 编辑文件……
git add docs/posts/生活/my-post.md
git commit -m "feat: add weekend walk post"
```

查看提交记录：

```bash
git log --oneline -5
```

## 场景三：推送到远程并提 PR

```bash
git push -u origin feat/new-post
```

在 GitHub 上发起 Pull Request，Review 通过后合并进 `main`。合并后本地同步：

```bash
git checkout main
git pull origin main
git branch -d feat/new-post
```

## 场景四：改错了，还没 push

### 只改最近一次提交说明

```bash
git commit --amend -m "fix: correct post title"
```

### 撤销工作区修改（未 add）

```bash
git restore path/to/file.md
```

### 已 add，想撤回暂存

```bash
git restore --staged path/to/file.md
```

> 若提交已经 push 到共享分支，避免 `--amend` 和 `rebase` 改写历史，应使用新提交修复。

## 场景五：临时切换任务（stash）

写到一半要切去修 bug：

```bash
git stash push -m "wip: half-written post"
git checkout main
# 修 bug、提交、推送……
git checkout feat/new-post
git stash pop
```

## 场景六：和远程冲突了

```bash
git pull origin main
# 若冲突，Git 会标记文件，手动编辑后：
git add .
git commit -m "merge: resolve conflict with main"
git push origin feat/new-post
```

建议养成 **先 pull 再 push** 的习惯，减少冲突面。

## 场景七：找回误删的提交

```bash
git reflog
# 找到丢失提交前的 hash，例如 abc1234
git checkout abc1234 -- path/to/file.md
git add path/to/file.md
git commit -m "fix: restore accidentally deleted post"
```

`reflog` 是本地安全网，很多「以为丢了」的提交都能找回来。

## 推荐的最小工作流（个人博客）

```text
main          ──●────────●────────●──  （可部署的稳定线）
                 \      /
feat/xxx        ──●──●──●              （写文、改样式）
```

1. 从最新的 `main` 拉分支  
2. 小步提交，写清楚的英文或中文 commit message  
3. push 后合并进 `main`  
4. CI（如 GitHub Actions）自动构建部署  

## 常用命令速查

| 目的 | 命令 |
|------|------|
| 看状态 | `git status` |
| 看差异 | `git diff` |
| 暂存 | `git add .` |
| 提交 | `git commit -m "message"` |
| 推送 | `git push` |
| 拉取 | `git pull` |
| 分支列表 | `git branch -a` |
| 切换分支 | `git checkout branch-name` |

## 小结

Git 不必背完全部参数，记住 **分支 + 小提交 + 先 pull 后 push** 就能覆盖日常九成场景。博客这类内容仓库尤其适合：文章一篇一个分支，合并后由 Actions 自动发布，省心也安全。
