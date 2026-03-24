#!/usr/bin/env python3
"""
GitHub AI User Guide -> Feishu 自动同步脚本
使用方法：python3 sync-github-to-feishu.py
"""

import os
import time
import json
import subprocess
from typing import List, Dict

# 配置
REPO = "gzchen008/ai-user-guide"
FEISHU_FOLDER_TOKEN = "OwM2fGLEJlBrOjdEUdQcmXmOnic"
DELAY_SECONDS = 3  # 每次创建后等待时间（避免API限制）

# 已同步的文件（手动更新）
SYNCED_FILES = [
    "README.md",
    "01-新手入门/01-AI基础概念.md",
    "01-新手入门/02-主流AI工具.md",
    "01-新手入门/03-快速上手.md",
    "01-新手入门/04-提问技巧.md",
    "01-新手入门/05-常见问题.md",
    "02-AI工具大全/01-对话AI/ChatGPT.md",
    "02-AI工具大全/01-对话AI/Claude.md",
    "02-AI工具大全/01-对话AI/DeepSeek.md",
    "02-AI工具大全/01-对话AI/Kimi.md",
    "02-AI工具大全/01-对话AI/Gemini.md",
    "02-AI工具大全/01-对话AI/Grok.md",
    "02-AI工具大全/01-对话AI/GLM.md",
    "02-AI工具大全/01-对话AI/MiniMax.md",
    "02-AI工具大全/02-图像生成/MidJourney.md",
    "02-AI工具大全/02-图像生成/DALL-E-3.md",
    "02-AI工具大全/02-图像生成/Stable-Diffusion.md",
    "02-AI工具大全/02-图像生成/Ideogram.md",
    "02-AI工具大全/03-视频生成/Runway.md",
    "02-AI工具大全/03-视频生成/Pika.md",
    "02-AI工具大全/03-视频生成/可灵.md",
    "02-AI工具大全/04-音频语音/ElevenLabs.md",
    "02-AI工具大全/04-音频语音/Suno.md",
    "02-AI工具大全/04-音频语音/Udio.md",
    "02-AI工具大全/04-音频语音/Whisper.md",
    "02-AI工具大全/05-编程工具/Cursor.md",
    "02-AI工具大全/05-编程工具/GitHub-Copilot.md",
    "02-AI工具大全/06-办公效率/Gamma.md",
    "03-AI编程/01-VibeCoding入门.md",
    "03-AI编程/README.md",
]

def get_all_md_files() -> List[str]:
    """获取所有MD文件列表"""
    cmd = f'gh api "repos/{REPO}/git/trees/main?recursive=1" --jq -r \'.tree[] | select(.type=="blob") | select(.path | endswith(".md")) | .path\''
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip().split('\n')

def get_unsynced_files(all_files: List[str]) -> List[str]:
    """获取未同步的文件"""
    return [f for f in all_files if f not in SYNCED_FILES and f != "CHANGELOG.md"]

def fetch_github_content(file_path: str) -> str:
    """从GitHub获取文件内容"""
    cmd = f'gh api repos/{REPO}/contents/{file_path} --jq \'.content\' | base64 -d'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def simplify_markdown(content: str, title: str) -> str:
    """简化Markdown内容（飞书精简版）"""
    # 提取前100行作为摘要
    lines = content.split('\n')[:100]
    
    # 构建精简版
    simplified = f"""# {title}

<callout emoji="📌" background-color="light-blue" border-color="blue">
来自GitHub AI User Guide
</callout>

---

## 📖 内容预览

{chr(10).join(lines)}

---

<callout emoji="💡" background-color="light-yellow" border-color="yellow">
**完整内容**：请访问 [GitHub仓库](https://github.com/gzchen008/ai-user-guide/blob/main/{title})
</callout>
"""
    return simplified

def create_feishu_doc(markdown: str, title: str) -> Dict:
    """创建飞书文档"""
    # 这里需要调用OpenClaw的feishu_create_doc工具
    # 实际使用时需要通过OpenClaw API
    print(f"创建文档：{title}")
    return {"status": "success", "title": title}

def main():
    print("🚀 开始同步 GitHub AI User Guide 到飞书...")
    print(f"仓库：{REPO}")
    print(f"目标文件夹：{FEISHU_FOLDER_TOKEN}")
    print("")
    
    # 获取所有文件
    all_files = get_all_md_files()
    print(f"📁 总文件数：{len(all_files)}")
    
    # 获取未同步文件
    unsynced = get_unsynced_files(all_files)
    print(f"⏳ 未同步文件：{len(unsynced)}")
    print("")
    
    if not unsynced:
        print("✅ 所有文件已同步！")
        return
    
    print("📝 待同步文件列表：")
    for i, file in enumerate(unsynced, 1):
        print(f"{i}. {file}")
    print("")
    
    print("💡 使用方法：")
    print("1. 手动调用 OpenClaw 的 feishu_create_doc 工具")
    print("2. 或让 OpenClaw 继续批量同步")
    print("")
    
    # 保存待同步列表
    with open('/tmp/unsynced-files.txt', 'w') as f:
        f.write('\n'.join(unsynced))
    print("✅ 待同步文件列表已保存到：/tmp/unsynced-files.txt")

if __name__ == "__main__":
    main()
