#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Obsidian 笔记 → Hugo 博客 半自动发布脚本

用法:
    python publish.py <笔记路径>

路径可以是:
  - 相对 vault 根目录:  "01-功能安全/E2E时序分析.md"
  - 绝对路径:          "D:/mywork/pkm/01-功能安全/E2E时序分析.md"

脚本会自动:
  1. 读取笔记
  2. 把 Obsidian 双链 [[note]] / [[note|别名]] 转成普通文本（Hugo 不认识双链）
  3. 把正文里的 #标签 移到 frontmatter 的 tags 里
  4. 补全 Hugo 需要的 frontmatter（title/date/draft/tags/categories）
  5. 写入 my-notes/content/posts/ 下，并打印接下来要执行的 git 命令
"""

import re
import sys
from datetime import date
from pathlib import Path

# Windows 控制台默认 GBK 编码，强制 UTF-8 避免打印 emoji/中文时报错
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ============ 路径配置（目录不同就改这里）============
VAULT_DIR = Path("D:/mywork/pkm")                      # Obsidian 笔记库根目录
HUGO_POSTS = Path("D:/mywork/my-notes/content/posts")  # Hugo 文章目录
# =====================================================


def split_frontmatter(text: str):
    """拆出 frontmatter 和正文。返回 (frontmatter_dict, body)。"""
    if text.startswith("---"):
        lines = text.splitlines()
        fm = {}
        for i, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                body = "\n".join(lines[i + 1:]).strip()
                return fm, body
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip()
    return {}, text.strip()


def convert_wikilinks(text: str) -> str:
    """[[note]] -> note ; [[note|别名]] -> 别名"""
    def repl(m):
        inner = m.group(1).strip()
        return inner.split("|", 1)[1].strip() if "|" in inner else inner
    return re.sub(r"\[\[([^\]]+)\]\]", repl, text)


def extract_tags(body: str):
    """把正文里的 #标签 提取出来，返回 (去掉标签后的正文, [标签...])。"""
    tags = re.findall(r"(?<!\S)#([\u4e00-\u9fff\w-]+)", body)
    body = re.sub(r"(?<!\S)#([\u4e00-\u9fff\w-]+)", "", body)
    return body.strip(), tags


def parse_list(value):
    """把 'a' / '[a, b]' / '["a", "b"]' 解析成 list[str]。"""
    if not value:
        return []
    value = value.strip()
    if value in ("[]", ""):
        return []
    value = value.strip("[]")
    items = [x.strip().strip('"').strip("'") for x in value.split(",")]
    return [x for x in items if x]


def render_frontmatter(fm: dict) -> str:
    lines = ["---"]
    lines.append(f'title: "{fm["title"]}"')
    lines.append(f"date: {fm["date"]}")
    lines.append(f"draft: {fm["draft"]}")
    if fm["categories"]:
        cats = ", ".join(f'"{c}"' for c in fm["categories"])
        lines.append(f"categories: [{cats}]")
    if fm["tags"]:
        tags = ", ".join(f'"{t}"' for t in fm["tags"])
        lines.append(f"tags: [{tags}]")
    lines.append("---")
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    src = Path(sys.argv[1])
    if not src.is_absolute():
        src = VAULT_DIR / src
    if not src.exists():
        print(f"❌ 找不到笔记: {src}")
        sys.exit(1)

    text = src.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    body = convert_wikilinks(body)
    body, inline_tags = extract_tags(body)

    tags = parse_list(fm.get("tags")) + inline_tags
    seen = set()
    tags = [t for t in tags if not (t in seen or seen.add(t))]

    merged_fm = {
        "title": fm.get("title") or src.stem,
        "date": fm.get("date") or date.today().isoformat(),
        "draft": fm.get("draft", "false"),
        "categories": parse_list(fm.get("categories")),
        "tags": tags,
    }

    dest = HUGO_POSTS / f"{src.stem}.md"
    dest.write_text(render_frontmatter(merged_fm) + "\n\n" + body + "\n", encoding="utf-8")

    print(f"✅ 已生成 Hugo 文章: {dest}")
    print(f"   标题: {merged_fm['title']}")
    print(f"   标签: {merged_fm['tags']}")
    print(f"   分类: {merged_fm['categories']}")
    print()
    print("下一步（发布）：")
    print("  cd D:/mywork/my-notes")
    print("  git add -A")
    print(f'  git commit -m "add: {merged_fm["title"]}"')
    print("  git push")


if __name__ == "__main__":
    main()
