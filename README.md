# my-notes

个人博客（功能安全 · 芯片架构 · 学习成长）。

- 网站：https://xiaoleill.github.io/my-notes/
- 基于 [Hugo](https://gohugo.io) + [LoveIt](https://github.com/dillonzq/LoveIt) 主题
- GitHub Actions 自动构建并部署到 GitHub Pages

---

## 日常使用流程

### ① 写一篇新文章

在 `content/posts/` 下新建一个 `.md` 文件，复制下面的头部模板，改标题 / 标签 / 分类：

```markdown
---
title: "文章标题"
date: 2026-08-25
draft: false          # true = 草稿，不发布
author: "xiaoleill"
tags: ["功能安全"]
categories: ["芯片架构"]
---

正文写这里……

<!--more-->          # 此行之前的内容会作为首页摘要
```

- 文件名建议用英文或拼音，例如 `e2e-timing.md`
- `draft: true` 的文章不会被发布，适合存草稿

### ② 本地预览（可选，想先看效果时）

新开一个终端，运行：

```bash
hugo -s /d/mywork/my-notes server
```

浏览器打开 http://localhost:1313/my-notes/ ，边改边实时刷新。

> 若提示找不到 `hugo` 命令，用完整路径：
> `C:\Users\yaozf\AppData\Local\Microsoft\WinGet\Packages\Hugo.Hugo.Extended_Microsoft.Winget.Source_8wekyb3d8bbwe\hugo.exe`

### ③ 发布

```bash
cd /d/mywork/my-notes
git add -A
git commit -m "add: 文章标题"
git push
```

push 后约 1 分钟，GitHub Actions 自动构建部署，网站更新。

---

## 注意事项

- **推送走 SSH**：本仓库 remote 已设为 `git@github.com:xiaoleill/my-notes.git`（因当前网络封锁 github.com 的 HTTPS/443 端口）。
- 换电脑 / 网络后若 push 报 `Could not connect`，重新生成 SSH 密钥加到 GitHub，或开 VPN 后把 remote 切回 HTTPS。
- 主题文件在 `themes/LoveIt/`，一般不用动。
