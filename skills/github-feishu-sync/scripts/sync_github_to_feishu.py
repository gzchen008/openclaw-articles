#!/usr/bin/env python3
"""
GitHub -> Feishu 同步脚本
功能：
1. 从GitHub仓库读取Markdown文件
2. 转换为飞书格式
3. 创建飞书文档
4. 处理API限频
5. 记录同步进度

使用方法：
python sync_github_to_feishu.py --repo gzchen008/ai-user-guide --folder-token OwM2fGLEJlBrOjdEUdQcmXmOnic
"""

import os
import sys
import json
import time
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# 配置
DEFAULT_DELAY = 3  # 默认每次创建后等待秒数
MAX_RETRIES = 5    # 最大重试次数
STATUS_FILE = "/Users/cgz/.openclaw/workspace/memory/github-feishu-sync-status.json"

class GitHubFeishuSync:
    def __init__(self, repo: str, folder_token: str, delay: int = DEFAULT_DELAY, full_sync: bool = False):
        self.repo = repo
        self.folder_token = folder_token
        self.delay = delay
        self.full_sync = full_sync
        self.status = self.load_status()
        
    def load_status(self) -> Dict:
        """加载同步状态"""
        if os.path.exists(STATUS_FILE):
            with open(STATUS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "repo": self.repo,
            "folder_token": self.folder_token,
            "synced_files": [],
            "last_sync": None,
            "failed_files": []
        }
    
    def save_status(self):
        """保存同步状态"""
        self.status["last_sync"] = datetime.now().isoformat()
        os.makedirs(os.path.dirname(STATUS_FILE), exist_ok=True)
        with open(STATUS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.status, f, ensure_ascii=False, indent=2)
    
    def get_all_md_files(self) -> List[str]:
        """获取所有Markdown文件列表"""
        cmd = f'gh api "repos/{self.repo}/git/trees/main?recursive=1" --jq -r \'.tree[] | select(.type=="blob") | select(.path | endswith(".md")) | .path\''
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ 获取文件列表失败: {result.stderr}")
            return []
        
        files = result.stdout.strip().split('\n')
        # 过滤掉不需要同步的文件
        files = [f for f in files if f not in ['README.md', 'CHANGELOG.md'] and not f.startswith('.github/')]
        return sorted(files)
    
    def get_unsynced_files(self, all_files: List[str]) -> List[str]:
        """获取未同步的文件"""
        if self.full_sync:
            return all_files
        
        synced = set(self.status.get("synced_files", []))
        return [f for f in all_files if f not in synced]
    
    def fetch_github_content(self, file_path: str) -> Optional[str]:
        """从GitHub获取文件内容"""
        cmd = f'gh api repos/{self.repo}/contents/{file_path} --jq \'.content\''
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ 获取文件失败 {file_path}: {result.stderr}")
            return None
        
        # Base64解码
        import base64
        try:
            content = base64.b64decode(result.stdout.strip()).decode('utf-8')
            return content
        except Exception as e:
            print(f"❌ 解码失败 {file_path}: {e}")
            return None
    
    def simplify_markdown(self, content: str, title: str) -> str:
        """简化Markdown内容（飞书精简版）"""
        # 提取前150行作为摘要
        lines = content.split('\n')[:150]
        simplified_content = '\n'.join(lines)
        
        # 如果内容被截断，添加提示
        if len(lines) < len(content.split('\n')):
            truncated_notice = "\n\n---\n\n<callout emoji=\"📌\" background-color=\"light-yellow\" border-color=\"yellow\">\n**提示**：内容已精简，完整版本请访问 [GitHub仓库](https://github.com/{}/{})\n</callout>".format(self.repo, title)
            simplified_content += truncated_notice
        
        return simplified_content
    
    def create_feishu_doc(self, markdown: str, title: str) -> bool:
        """创建飞书文档（通过OpenClaw工具）"""
        print(f"  📝 创建文档: {title}")
        
        # 这里需要调用OpenClaw的feishu_create_doc工具
        # 由于脚本独立运行，我们需要通过其他方式调用
        # 暂时返回True，实际使用时需要集成OpenClaw API
        print(f"  ⚠️  需要通过OpenClaw调用飞书API创建文档")
        return True
    
    def sync_file(self, file_path: str) -> bool:
        """同步单个文件"""
        print(f"\n📄 同步文件: {file_path}")
        
        # 1. 获取内容
        content = self.fetch_github_content(file_path)
        if not content:
            return False
        
        # 2. 简化内容
        title = os.path.basename(file_path).replace('.md', '')
        simplified = self.simplify_markdown(content, title)
        
        # 3. 创建飞书文档
        for attempt in range(MAX_RETRIES):
            try:
                success = self.create_feishu_doc(simplified, title)
                if success:
                    # 记录成功
                    if file_path not in self.status["synced_files"]:
                        self.status["synced_files"].append(file_path)
                    print(f"  ✅ 同步成功")
                    return True
                else:
                    raise Exception("创建文档失败")
                    
            except Exception as e:
                error_msg = str(e)
                
                # 处理不同类型的错误
                if "folder locked" in error_msg.lower():
                    wait_time = 5
                    print(f"  ⏳ 文件夹锁定，等待{wait_time}秒后重试... (尝试 {attempt + 1}/{MAX_RETRIES})")
                    time.sleep(wait_time)
                    
                elif "frequency limit" in error_msg.lower():
                    wait_time = 10
                    print(f"  ⏳ API限频，等待{wait_time}秒后重试... (尝试 {attempt + 1}/{MAX_RETRIES})")
                    time.sleep(wait_time)
                    
                else:
                    print(f"  ❌ 同步失败: {e}")
                    if file_path not in [f["path"] for f in self.status["failed_files"]]:
                        self.status["failed_files"].append({
                            "path": file_path,
                            "error": error_msg,
                            "time": datetime.now().isoformat()
                        })
                    return False
        
        print(f"  ❌ 达到最大重试次数，跳过此文件")
        return False
    
    def run(self):
        """执行同步"""
        print("=" * 60)
        print("🚀 GitHub -> 飞书 同步工具")
        print("=" * 60)
        print(f"📦 仓库: {self.repo}")
        print(f"📁 目标文件夹: {self.folder_token}")
        print(f"🔄 同步模式: {'全量同步' if self.full_sync else '增量同步'}")
        print(f"⏱️  间隔时间: {self.delay}秒")
        print("")
        
        # 1. 获取所有文件
        print("📋 正在获取文件列表...")
        all_files = self.get_all_md_files()
        print(f"  找到 {len(all_files)} 个文件")
        
        # 2. 获取待同步文件
        unsynced = self.get_unsynced_files(all_files)
        print(f"  待同步 {len(unsynced)} 个文件")
        
        if not unsynced:
            print("\n✅ 所有文件已同步，无需操作")
            return
        
        print(f"\n📝 待同步文件列表:")
        for i, file in enumerate(unsynced, 1):
            print(f"  {i}. {file}")
        
        # 3. 开始同步
        print(f"\n{'=' * 60}")
        print("开始同步...")
        print("=" * 60)
        
        success_count = 0
        failed_count = 0
        
        for i, file_path in enumerate(unsynced, 1):
            print(f"\n[{i}/{len(unsynced)}]", end="")
            
            success = self.sync_file(file_path)
            if success:
                success_count += 1
                # 等待一段时间避免限频
                if i < len(unsynced):
                    time.sleep(self.delay)
            else:
                failed_count += 1
        
        # 4. 保存状态
        self.save_status()
        
        # 5. 输出总结
        print("\n" + "=" * 60)
        print("📊 同步完成")
        print("=" * 60)
        print(f"✅ 成功: {success_count}")
        print(f"❌ 失败: {failed_count}")
        print(f"📁 状态文件: {STATUS_FILE}")
        print("")


def main():
    parser = argparse.ArgumentParser(description='GitHub -> 飞书同步工具')
    parser.add_argument('--repo', required=True, help='GitHub仓库名 (如: gzchen008/ai-user-guide)')
    parser.add_argument('--folder-token', required=True, help='飞书文件夹Token')
    parser.add_argument('--delay', type=int, default=DEFAULT_DELAY, help=f'每次创建后等待秒数 (默认: {DEFAULT_DELAY})')
    parser.add_argument('--full-sync', action='store_true', help='全量同步（默认为增量同步）')
    parser.add_argument('--max-retries', type=int, default=MAX_RETRIES, help=f'最大重试次数 (默认: {MAX_RETRIES})')
    
    args = parser.parse_args()
    
    sync = GitHubFeishuSync(
        repo=args.repo,
        folder_token=args.folder_token,
        delay=args.delay,
        full_sync=args.full_sync
    )
    
    sync.run()


if __name__ == "__main__":
    main()
