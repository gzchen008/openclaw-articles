#!/usr/bin/env python3
"""
OpenClaw 更新日志 - 公众号文章生成器
"""

import json
import sys
import re
from datetime import datetime
from pathlib import Path


def parse_changelog(body: str) -> dict:
    """解析 GitHub release 内容"""
    sections = {
        "changes": [],
        "breaking": [],
        "fixes": []
    }
    
    current_section = None
    
    for line in body.split('\n'):
        line = line.strip()
        
        # 检测章节标题
        if line.startswith('###'):
            if 'Changes' in line:
                current_section = 'changes'
            elif 'Breaking' in line:
                current_section = 'breaking'
            elif 'Fixes' in line:
                current_section = 'fixes'
            continue
        
        # 解析变更条目
        if line.startswith('-') and current_section:
            # 移除 "- " 前缀
            item = line[1:].strip()
            sections[current_section].append(item)
    
    return sections


def format_article(data: dict) -> str:
    """生成公众号文章内容"""
    version = data.get('latest_version', 'Unknown')
    release_date = data.get('release_date', datetime.now().strftime('%Y-%m-%d'))
    changelog_text = data.get('changelog', '')
    
    # 解析变更日志
    sections = parse_changelog(changelog_text)
    
    article = f"""# OpenClaw {version} 版本更新

> 发布时间：{release_date}

## 📦 更新总览

OpenClaw 发布了最新版本 **{version}**，带来了多项重要功能和改进。以下是本次更新的详细内容。

---

## 🚀 新功能

"""
    
    # 新功能
    for i, change in enumerate(sections['changes'][:5], 1):  # 最多显示 5 个
        # 移除 PR 链接
        clean_change = re.sub(r'\[#\d+\]', '', change)
        article += f"{i}. {clean_change}\n\n"
    
    if len(sections['changes']) > 5:
        article += f"\n*注：本次更新共 {len(sections['changes'])} 项新功能，以上为部分精选。*\n\n"
    
    # Breaking Changes
    if sections['breaking']:
        article += "---\n## ⚠️ 破坏性变更\n\n"
        for change in sections['breaking']:
            clean_change = re.sub(r'\[#\d+\]', '', change)
            article += f"- {clean_change}\n\n"
    
    # Bug 修复
    if sections['fixes']:
        article += "---\n## 🐛 Bug 修复\n\n"
        for i, fix in enumerate(sections['fixes'][:5], 1):
            clean_fix = re.sub(r'\[#\d+\]', '', fix)
            article += f"{i}. {clean_fix}\n\n"
    
    # 升级指南
    article += f"""---

## 📝 升级指南

### 升级命令

\`\`\`bash
# 使用 npm 升级
npm update -g openclaw

# 或使用 homebrew
brew upgrade openclaw
\`\`\`

### 检查版本

\`\`\`bash
openclaw --version
\`\`\`

### 查看完整更新日志

完整更新日志和详细说明请访问：

🔗 [OpenClaw Releases](https://github.com/openclaw/openclaw/releases/tag/{version})

---

## 💡 相关资源

- 📚 [OpenClaw 文档](https://docs.openclaw.ai)
- 💬 [Discord 社区](https://discord.gg/clawd)
- 🌟 [GitHub 仓库](https://github.com/openclaw/openclaw)

---

*本文由 OpenClaw 自动生成*

---

**关注我们，第一时间获取 OpenClaw 最新动态！**

"""
    return article


def save_article(article: str, version: str) -> Path:
    """保存文章文件"""
    output_dir = Path('/Users/cgz/.openclaw/workspace/articles/openclaw-updates')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    date_str = datetime.now().strftime('%Y%m%d')
    filename = f"openclaw-update-{version}-{date_str}.md"
    filepath = output_dir / filename
    
    filepath.write_text(article, encoding='utf-8')
    
    return filepath


def main():
    if len(sys.argv) < 2:
        print("Usage: generate-article.py <state.json>")
        sys.exit(1)
    
    state_file = sys.argv[1]
    
    with open(state_file, 'r') as f:
        data = json.load(f)
    
    # 只在有新版本时生成文章
    if not data.get('has_update'):
        print("No new version to generate article for.")
        sys.exit(0)
    
    article = format_article(data)
    filepath = save_article(article, data.get('latest_version', 'unknown'))
    
    print(f"Article generated: {filepath}")
    print(f"Version: {data.get('latest_version')}")


if __name__ == '__main__':
    main()
