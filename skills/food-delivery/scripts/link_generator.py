#!/usr/bin/env python3
"""
外卖平台链接生成器
生成美团、饿了么、大众点评的搜索链接
"""

import urllib.parse
from typing import Dict


class LinkGenerator:
    """外卖平台链接生成器"""
    
    @staticmethod
    def meituan_search(keyword: str) -> str:
        """生成美团外卖搜索链接"""
        encoded = urllib.parse.quote(keyword)
        return f"https://waimai.meituan.com/search?keyword={encoded}"
    
    @staticmethod
    def eleme_search(keyword: str) -> str:
        """生成饿了么搜索链接"""
        encoded = urllib.parse.quote(keyword)
        return f"https://www.ele.me/search?keyword={encoded}"
    
    @staticmethod
    def dianping_search(keyword: str) -> str:
        """生成大众点评搜索链接"""
        encoded = urllib.parse.quote(keyword)
        return f"https://www.dianping.com/search?keyword={encoded}"
    
    @staticmethod
    def generate_all_links(keyword: str) -> Dict[str, str]:
        """生成所有平台链接"""
        return {
            "美团外卖": LinkGenerator.meituan_search(keyword),
            "饿了么": LinkGenerator.eleme_search(keyword),
            "大众点评": LinkGenerator.dianping_search(keyword)
        }
    
    @staticmethod
    def format_links(keyword: str) -> str:
        """格式化链接为Markdown"""
        links = LinkGenerator.generate_all_links(keyword)
        output = [f"🔗 搜索「{keyword}」："]
        for platform, url in links.items():
            output.append(f"- [{platform}]({url})")
        return "\n".join(output)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="外卖平台链接生成器")
    parser.add_argument("keyword", help="搜索关键词")
    parser.add_argument("--platform", choices=["meituan", "eleme", "dianping", "all"], 
                       default="all", help="平台选择")
    
    args = parser.parse_args()
    
    if args.platform == "all":
        print(LinkGenerator.format_links(args.keyword))
    elif args.platform == "meituan":
        print(LinkGenerator.meituan_search(args.keyword))
    elif args.platform == "eleme":
        print(LinkGenerator.eleme_search(args.keyword))
    elif args.platform == "dianping":
        print(LinkGenerator.dianping_search(args.keyword))


if __name__ == "__main__":
    main()
