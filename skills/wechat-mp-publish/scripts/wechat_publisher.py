#!/usr/bin/env python3
"""
微信公众号推文发布工具
支持：上传图片、新建草稿、发布草稿

使用前需配置环境变量：
  WECHAT_APPID - 公众号 AppID
  WECHAT_SECRET - 公众号 AppSecret
  
代理配置（默认启用）：
  WECHAT_USE_PROXY - 是否使用代理（默认 true）
  WECHAT_PROXY_URL - 代理服务器地址（默认 http://115.191.30.195/wechat）
  
  使用方式：
  原微信 API: https://api.weixin.qq.com/cgi-bin/token
  换成代理:   http://115.191.30.195/wechat/cgi-bin/token
  
  规律：把 https://api.weixin.qq.com 替换成 http://115.191.30.195/wechat 即可
"""

import os
import sys
import json
import time
import requests
from pathlib import Path
from typing import Optional, Dict, Any

class WeChatPublisher:
    """微信公众号发布器"""
    
    def __init__(self, appid: str = None, secret: str = None):
        self.appid = appid or os.environ.get("WECHAT_APPID")
        self.secret = secret or os.environ.get("WECHAT_SECRET")
        self._token = None
        self._token_file = Path("/tmp/wechat_token.json")
        
        # 代理配置（默认启用代理）
        self.use_proxy = os.getenv('WECHAT_USE_PROXY', 'true').lower() == 'true'
        self.proxy_url = os.getenv('WECHAT_PROXY_URL', 'http://115.191.30.195/wechat')
        
        # 根据代理设置选择 API 地址
        if self.use_proxy and self.proxy_url:
            # 使用代理时，代理地址已经包含了完整路径映射
            # 规律：把 https://api.weixin.qq.com 替换成 http://your-server-ip/wechat
            # 所以 base_url = http://your-server-ip/wechat/cgi-bin
            self.base_url = f"{self.proxy_url.rstrip('/')}/cgi-bin"
            print(f"✅ 使用代理: {self.base_url}")
        else:
            self.base_url = "https://api.weixin.qq.com/cgi-bin"
            print("✅ 直接连接")
        
        if not self.appid or not self.secret:
            raise ValueError("请设置 WECHAT_APPID 和 WECHAT_SECRET 环境变量")
    
    def get_access_token(self, force_refresh: bool = False) -> str:
        """获取 access_token（带缓存）"""
        # 尝试从缓存读取
        if not force_refresh and self._token_file.exists():
            try:
                cached = json.loads(self._token_file.read_text())
                if cached.get("expires_at", 0) > int(time.time()):
                    self._token = cached["access_token"]
                    return self._token
            except:
                pass
        
        # 请求新 token
        url = f"{self.base_url}/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.appid,
            "secret": self.secret
        }
        
        resp = requests.get(url, params=params, timeout=30)
        data = resp.json()
        
        if "errcode" in data:
            raise Exception(f"获取 token 失败: {data.get('errmsg')}")
        
        self._token = data["access_token"]
        expires_in = data.get("expires_in", 7200)
        
        # 缓存 token
        self._token_file.write_text(json.dumps({
            "access_token": self._token,
            "expires_at": int(time.time()) + expires_in - 300  # 提前5分钟过期
        }))
        
        return self._token
    
    @property
    def token(self) -> str:
        """获取当前 token"""
        if not self._token:
            return self.get_access_token()
        return self._token
    
    def upload_image(self, image_path: str, image_type: str = "thumb") -> Dict[str, Any]:
        """
        上传图片到微信素材库
        
        Args:
            image_path: 图片文件路径
            image_type: 素材类型 - thumb(封面缩略图64KB) / image(图文内图片)
        
        Returns:
            {"media_id": "...", "url": "..."} 
        """
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"图片不存在: {image_path}")
        
        # 图文内图片使用 uploadimg，封面使用 material/add_material
        if image_type == "image":
            url = f"{self.base_url}/media/uploadimg?access_token={self.token}"
            files = {"media": open(path, "rb")}
            resp = requests.post(url, files=files, timeout=60)
        else:
            url = f"{self.base_url}/material/add_material?access_token={self.token}&type=thumb"
            files = {"media": open(path, "rb")}
            resp = requests.post(url, files=files, timeout=60)
        
        data = resp.json()
        if "errcode" in data and data["errcode"] != 0:
            raise Exception(f"上传图片失败: {data.get('errmsg')}")
        
        return data
    
    def create_draft(
        self,
        title: str,
        content: str,
        thumb_media_id: str,
        author: str = "",
        digest: str = "",
        content_source_url: str = "",
        need_open_comment: int = 0,
        only_fans_can_comment: int = 0
    ) -> str:
        """
        新建草稿
        
        Args:
            title: 文章标题（必填，最长32字）
            content: 文章内容 HTML（必填，最长2万字符）
            thumb_media_id: 封面图 media_id（必填，永久素材）
            author: 作者（选填，最长16字）
            digest: 摘要（选填，最长128字）
            content_source_url: 阅读原文链接
            need_open_comment: 是否打开评论 0/1
            only_fans_can_comment: 是否仅粉丝可评论 0/1
        
        Returns:
            草稿 media_id
        """
        url = f"{self.base_url}/draft/add?access_token={self.token}"
        
        payload = {
            "articles": [{
                "title": title,
                "author": author,
                "digest": digest,
                "content": content,
                "content_source_url": content_source_url,
                "thumb_media_id": thumb_media_id,
                "need_open_comment": need_open_comment,
                "only_fans_can_comment": only_fans_can_comment
            }]
        }
        
        # 使用 ensure_ascii=False 避免 Unicode 转义，确保中文正常显示
        headers = {
            "Content-Type": "application/json; charset=utf-8"
        }
        json_data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        resp = requests.post(url, data=json_data, headers=headers, timeout=30)
        data = resp.json()
        
        if "errcode" in data and data["errcode"] != 0:
            raise Exception(f"创建草稿失败: {data.get('errmsg')}")
        
        return data.get("media_id")
    
    def update_draft(
        self,
        media_id: str,
        title: str,
        content: str,
        thumb_media_id: str,
        index: int = 0,
        author: str = "",
        digest: str = "",
        content_source_url: str = "",
        need_open_comment: int = 0,
        only_fans_can_comment: int = 0
    ) -> bool:
        """
        更新已有草稿
        
        Args:
            media_id: 要更新的草稿 ID（必填）
            index: 文章位置，第一篇为 0（默认）
            title: 文章标题（必填）
            content: 文章内容 HTML（必填）
            thumb_media_id: 封面图 media_id（必填）
            author: 作者
            digest: 摘要
            content_source_url: 阅读原文链接
            need_open_comment: 是否打开评论 0/1
            only_fans_can_comment: 是否仅粉丝可评论 0/1
        
        Returns:
            True 表示更新成功
        """
        url = f"{self.base_url}/draft/update?access_token={self.token}"
        
        payload = {
            "media_id": media_id,
            "index": index,
            "articles": {
                "title": title,
                "author": author,
                "digest": digest,
                "content": content,
                "content_source_url": content_source_url,
                "thumb_media_id": thumb_media_id,
                "need_open_comment": need_open_comment,
                "only_fans_can_comment": only_fans_can_comment
            }
        }
        
        headers = {"Content-Type": "application/json; charset=utf-8"}
        json_data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        resp = requests.post(url, data=json_data, headers=headers, timeout=30)
        data = resp.json()
        
        if data.get("errcode", 0) != 0:
            raise Exception(f"更新草稿失败: {data.get('errmsg')}")
        
        return True
    
    def smart_update_or_create(
        self,
        media_id: str,
        title: str,
        content: str,
        thumb_media_id: str,
        author: str = "",
        digest: str = ""
    ) -> str:
        """
        智能更新或创建草稿
        
        优先尝试更新已有草稿，如果失败则新建
        
        Args:
            media_id: 已有草稿 ID（如果为空则新建）
            title: 标题
            content: 内容
            thumb_media_id: 封面图 ID
            author: 作者
            digest: 摘要
        
        Returns:
            草稿 media_id
        """
        if media_id:
            try:
                self.update_draft(
                    media_id=media_id,
                    title=title,
                    content=content,
                    thumb_media_id=thumb_media_id,
                    author=author,
                    digest=digest
                )
                return media_id
            except Exception as e:
                # 更新失败，创建新草稿
                print(f"⚠️  更新失败，将创建新草稿: {e}")
        
        # 创建新草稿
        return self.create_draft(
            title=title,
            content=content,
            thumb_media_id=thumb_media_id,
            author=author,
            digest=digest
        )
    
    def publish(self, media_id: str) -> Dict[str, Any]:
        """
        发布草稿
        
        Args:
            media_id: 草稿的 media_id
        
        Returns:
            {"publish_id": "...", "msg_data_id": "..."}
        """
        url = f"{self.base_url}/freepublish/submit?access_token={self.token}"
        
        payload = {"media_id": media_id}
        headers = {"Content-Type": "application/json; charset=utf-8"}
        json_data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        resp = requests.post(url, data=json_data, headers=headers, timeout=30)
        data = resp.json()
        
        if data.get("errcode", 0) != 0:
            raise Exception(f"发布失败: {data.get('errmsg')}")
        
        return {
            "publish_id": data.get("publish_id"),
            "msg_data_id": data.get("msg_data_id")
        }
    
    def get_draft_list(self, offset: int = 0, count: int = 20) -> Dict[str, Any]:
        """获取草稿列表"""
        url = f"{self.base_url}/draft/batchget?access_token={self.token}"
        payload = {"offset": offset, "count": count, "no_content": 0}
        headers = {"Content-Type": "application/json; charset=utf-8"}
        json_data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        resp = requests.post(url, data=json_data, headers=headers, timeout=30)
        return resp.json()
    
    def delete_draft(self, media_id: str) -> bool:
        """删除草稿"""
        url = f"{self.base_url}/draft/delete?access_token={self.token}"
        payload = {"media_id": media_id}
        headers = {"Content-Type": "application/json; charset=utf-8"}
        json_data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        resp = requests.post(url, data=json_data, headers=headers, timeout=30)
        data = resp.json()
        return data.get("errcode", 0) == 0


def main():
    """命令行入口"""
    import argparse
    import time
    
    parser = argparse.ArgumentParser(description="微信公众号推文发布工具")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # upload 命令
    upload_parser = subparsers.add_parser("upload", help="上传图片")
    upload_parser.add_argument("image", help="图片路径")
    upload_parser.add_argument("--type", "-t", default="thumb", choices=["thumb", "image"],
                               help="素材类型: thumb(封面) / image(图文内)")
    
    # draft 命令
    draft_parser = subparsers.add_parser("draft", help="新建草稿")
    draft_parser.add_argument("--title", "-t", required=True, help="文章标题")
    draft_parser.add_argument("--content", "-c", required=True, help="文章内容（HTML或文件路径）")
    draft_parser.add_argument("--thumb", "-th", required=True, help="封面图 media_id 或文件路径")
    draft_parser.add_argument("--author", "-a", default="", help="作者")
    draft_parser.add_argument("--digest", "-d", default="", help="摘要")
    draft_parser.add_argument("--source-url", "-s", default="", help="阅读原文链接")
    draft_parser.add_argument("--update", "-u", help="更新已有草稿的 media_id（提供则更新，否则新建）")
    
    # publish 命令
    publish_parser = subparsers.add_parser("publish", help="发布草稿")
    publish_parser.add_argument("media_id", help="草稿 media_id")
    
    # auto 命令（一键发布）
    auto_parser = subparsers.add_parser("auto", help="一键发布（上传封面+建草稿+发布）")
    auto_parser.add_argument("--title", "-t", required=True, help="文章标题")
    auto_parser.add_argument("--content", "-c", required=True, help="文章内容（HTML或文件路径）")
    auto_parser.add_argument("--thumb", "-th", required=True, help="封面图路径")
    auto_parser.add_argument("--author", "-a", default="", help="作者")
    auto_parser.add_argument("--digest", "-d", default="", help="摘要")
    auto_parser.add_argument("--source-url", "-s", default="", help="阅读原文链接")
    auto_parser.add_argument("--dry-run", action="store_true", help="只创建草稿不发布")
    auto_parser.add_argument("--update", "-u", help="更新已有草稿的 media_id")
    
    # list 命令
    list_parser = subparsers.add_parser("list", help="列出草稿")
    list_parser.add_argument("--count", "-n", type=int, default=10, help="数量")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        publisher = WeChatPublisher()
        
        if args.command == "upload":
            print(f"📤 上传图片: {args.image}")
            result = publisher.upload_image(args.image, args.type)
            print(f"✅ 上传成功!")
            print(f"   media_id: {result.get('media_id')}")
            if result.get('url'):
                print(f"   url: {result.get('url')}")
        
        elif args.command == "draft":
            # 处理内容（可能是文件）
            content = args.content
            if Path(args.content).exists():
                content = Path(args.content).read_text(encoding="utf-8")
            
            # 处理封面（可能是文件路径或 media_id）
            thumb_id = args.thumb
            if Path(args.thumb).exists():
                print(f"📤 上传封面图: {args.thumb}")
                result = publisher.upload_image(args.thumb, "thumb")
                thumb_id = result["media_id"]
                print(f"   media_id: {thumb_id}")
            
            # 使用智能更新或创建
            action = "更新" if args.update else "创建"
            print(f"📝 {action}草稿: {args.title}")
            
            if args.update:
                # 更新模式
                publisher.update_draft(
                    media_id=args.update,
                    title=args.title,
                    content=content,
                    thumb_media_id=thumb_id,
                    author=args.author,
                    digest=args.digest,
                    content_source_url=args.source_url
                )
                media_id = args.update
                print(f"✅ 草稿更新成功!")
            else:
                # 创建模式
                media_id = publisher.create_draft(
                    title=args.title,
                    content=content,
                    thumb_media_id=thumb_id,
                    author=args.author,
                    digest=args.digest,
                    content_source_url=args.source_url
                )
                print(f"✅ 草稿创建成功!")
            
            print(f"   media_id: {media_id}")
        
        elif args.command == "publish":
            print(f"🚀 发布草稿: {args.media_id}")
            result = publisher.publish(args.media_id)
            print(f"✅ 发布成功!")
            print(f"   publish_id: {result['publish_id']}")
            print(f"   msg_data_id: {result['msg_data_id']}")
        
        elif args.command == "auto":
            # 读取内容
            content = args.content
            if Path(args.content).exists():
                content = Path(args.content).read_text(encoding="utf-8")
            
            # 1. 上传封面
            print(f"📤 步骤1: 上传封面图")
            thumb_result = publisher.upload_image(args.thumb, "thumb")
            thumb_id = thumb_result["media_id"]
            print(f"   ✅ media_id: {thumb_id}")
            
            # 2. 创建或更新草稿
            if args.update:
                print(f"📝 步骤2: 更新草稿")
                publisher.update_draft(
                    media_id=args.update,
                    title=args.title,
                    content=content,
                    thumb_media_id=thumb_id,
                    author=args.author,
                    digest=args.digest
                )
                media_id = args.update
                print(f"   ✅ 已更新: {media_id}")
            else:
                print(f"📝 步骤2: 创建草稿")
                media_id = publisher.create_draft(
                    title=args.title,
                    content=content,
                    thumb_media_id=thumb_id,
                    author=args.author,
                    digest=args.digest,
                    content_source_url=args.source_url
                )
                print(f"   ✅ media_id: {media_id}")
            
            if args.dry_run:
                print(f"\n⏸️  Dry-run 模式，跳过发布")
                print(f"   草稿 media_id: {media_id}")
                return
            
            # 3. 发布
            print(f"🚀 步骤3: 发布草稿")
            result = publisher.publish(media_id)
            print(f"   ✅ publish_id: {result['publish_id']}")
            print(f"\n🎉 全部完成!")
        
        elif args.command == "list":
            result = publisher.get_draft_list(count=args.count)
            items = result.get("item", [])
            print(f"📋 草稿列表 (共 {result.get('total_count', 0)} 篇)")
            print("-" * 50)
            for item in items:
                for article in item.get("content", {}).get("news_item", []):
                    print(f"  • {article.get('title')}")
                    print(f"    media_id: {item.get('media_id')}")
                    print()
    
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
