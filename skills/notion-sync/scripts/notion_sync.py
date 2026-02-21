#!/usr/bin/env python3
"""
Notion 同步工具
功能：将 Markdown 文章同步到 Notion 数据库
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import List, Dict, Optional
import requests

class NotionSync:
    """Notion API 客户端"""

    def __init__(self, token: str, database_id: str):
        self.token = token
        self.database_id = database_id
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    def create_page(self, title: str, content: str, tags: List[str] = None,
                    status: str = "草稿", url: str = None) -> Dict:
        """
        创建新页面

        Args:
            title: 文章标题
            content: Markdown 内容
            tags: 标签列表
            status: 状态（草稿/已发布）
            url: 原文链接

        Returns:
            API 响应
        """
        # 将 Markdown 转换为 Notion Blocks
        blocks = self.markdown_to_blocks(content)

        # 构建页面属性
        properties = {
            "标题": {
                "title": [{"text": {"content": title}}]
            },
            "状态": {
                "select": {"name": status}
            }
        }

        # 添加标签
        if tags:
            properties["标签"] = {
                "multi_select": [{"name": tag} for tag in tags]
            }

        # 添加发布日期
        if status == "已发布":
            properties["发布日期"] = {
                "date": {"start": datetime.now().isoformat()}
            }

        # 添加链接
        if url:
            properties["链接"] = {
                "url": url
            }

        # 创建页面
        payload = {
            "parent": {"database_id": self.database_id},
            "properties": properties,
            "children": blocks
        }

        response = requests.post(
            f"{self.base_url}/pages",
            headers=self.headers,
            json=payload
        )

        if response.status_code == 200:
            print(f"✅ 页面创建成功：{title}")
            return response.json()
        else:
            print(f"❌ 创建失败：{response.text}")
            return None

    def update_page(self, page_id: str, **kwargs) -> Dict:
        """
        更新页面属性

        Args:
            page_id: 页面 ID
            **kwargs: 要更新的属性（status, tags, url）

        Returns:
            API 响应
        """
        properties = {}

        if "status" in kwargs:
            properties["状态"] = {
                "select": {"name": kwargs["status"]}
            }
            if kwargs["status"] == "已发布":
                properties["发布日期"] = {
                    "date": {"start": datetime.now().isoformat()}
                }

        if "tags" in kwargs:
            properties["标签"] = {
                "multi_select": [{"name": tag} for tag in kwargs["tags"]]
            }

        if "url" in kwargs:
            properties["链接"] = {"url": kwargs["url"]}

        payload = {"properties": properties}

        response = requests.patch(
            f"{self.base_url}/pages/{page_id}",
            headers=self.headers,
            json=payload
        )

        if response.status_code == 200:
            print(f"✅ 页面更新成功")
            return response.json()
        else:
            print(f"❌ 更新失败：{response.text}")
            return None

    def query_database(self, limit: int = 10) -> List[Dict]:
        """
        查询数据库内容

        Args:
            limit: 返回数量限制

        Returns:
            页面列表
        """
        payload = {
            "page_size": limit,
            "sorts": [{
                "timestamp": "created_time",
                "direction": "descending"
            }]
        }

        response = requests.post(
            f"{self.base_url}/databases/{self.database_id}/query",
            headers=self.headers,
            json=payload
        )

        if response.status_code == 200:
            data = response.json()
            pages = data.get("results", [])
            print(f"✅ 查询到 {len(pages)} 个页面")
            return pages
        else:
            print(f"❌ 查询失败：{response.text}")
            return []

    def markdown_to_blocks(self, markdown: str) -> List[Dict]:
        """
        将 Markdown 转换为 Notion Blocks（简化版）

        Args:
            markdown: Markdown 文本

        Returns:
            Notion Block 列表
        """
        blocks = []
        lines = markdown.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 标题
            if line.startswith('### '):
                blocks.append({
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"text": {"content": line[4:]}}]
                    }
                })
            elif line.startswith('## '):
                blocks.append({
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"text": {"content": line[3:]}}]
                    }
                })
            elif line.startswith('# '):
                blocks.append({
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [{"text": {"content": line[2:]}}]
                    }
                })
            # 无序列表
            elif line.startswith('- ') or line.startswith('* '):
                blocks.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"text": {"content": line[2:]}}]
                    }
                })
            # 有序列表
            elif line[0].isdigit() and '. ' in line:
                text = line.split('. ', 1)[1]
                blocks.append({
                    "object": "block",
                    "type": "numbered_list_item",
                    "numbered_list_item": {
                        "rich_text": [{"text": {"content": text}}]
                    }
                })
            # 代码块（简化处理）
            elif line.startswith('```'):
                continue  # 跳过代码块标记
            # 引用
            elif line.startswith('> '):
                blocks.append({
                    "object": "block",
                    "type": "quote",
                    "quote": {
                        "rich_text": [{"text": {"content": line[2:]}}]
                    }
                })
            # 普通段落
            else:
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"text": {"content": line[:2000]}}]  # Notion 单段落限制
                    }
                })

        return blocks


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="Notion 同步工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # sync 命令
    sync_parser = subparsers.add_parser("sync", help="同步文章到 Notion")
    sync_parser.add_argument("--title", required=True, help="文章标题")
    sync_parser.add_argument("--content", required=True, help="Markdown 文件路径")
    sync_parser.add_argument("--tags", help="标签（逗号分隔）")
    sync_parser.add_argument("--status", default="草稿", help="状态（草稿/已发布）")
    sync_parser.add_argument("--url", help="原文链接")

    # list 命令
    list_parser = subparsers.add_parser("list", help="查询数据库内容")
    list_parser.add_argument("--limit", type=int, default=10, help="返回数量")

    # update 命令
    update_parser = subparsers.add_parser("update", help="更新页面")
    update_parser.add_argument("--page-id", required=True, help="页面 ID")
    update_parser.add_argument("--status", help="状态（草稿/已发布）")
    update_parser.add_argument("--tags", help="标签（逗号分隔）")
    update_parser.add_argument("--url", help="链接")

    args = parser.parse_args()

    # 从环境变量读取配置
    token = os.environ.get("NOTION_TOKEN")
    database_id = os.environ.get("NOTION_DATABASE_ID")

    if not token or not database_id:
        print("❌ 错误：请设置 NOTION_TOKEN 和 NOTION_DATABASE_ID 环境变量")
        sys.exit(1)

    # 初始化客户端
    client = NotionSync(token, database_id)

    # 执行命令
    if args.command == "sync":
        # 读取 Markdown 文件
        with open(args.content, 'r', encoding='utf-8') as f:
            content = f.read()

        # 解析标签
        tags = args.tags.split(',') if args.tags else None

        # 同步
        result = client.create_page(
            title=args.title,
            content=content,
            tags=tags,
            status=args.status,
            url=args.url
        )

        if result:
            print(f"📄 页面 ID：{result['id']}")

    elif args.command == "list":
        pages = client.query_database(limit=args.limit)
        for page in pages:
            title_prop = page.get("properties", {}).get("标题", {})
            title = title_prop.get("title", [{}])[0].get("text", {}).get("content", "无标题")
            status = page.get("properties", {}).get("状态", {}).get("select", {}).get("name", "未知")
            print(f"  • {title} ({status})")

    elif args.command == "update":
        kwargs = {}
        if args.status:
            kwargs["status"] = args.status
        if args.tags:
            kwargs["tags"] = args.tags.split(',')
        if args.url:
            kwargs["url"] = args.url

        client.update_page(args.page_id, **kwargs)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
