#!/usr/bin/env python3
"""
批量上传图片到微信公众号
自动替换 HTML 中的本地图片 URL 为微信 URL

使用方法：
  # 上传单张图片
  python upload_images.py image.jpg

  # 批量上传目录下所有图片
  python upload_images.py images/ --pattern "*.jpg"

  # 上传并替换 HTML 中的图片
  python upload_images.py images/ --html article.html --output article-wechat.html
"""

import os
import sys
import re
import glob
import json
import requests
from pathlib import Path
from typing import Dict, List, Tuple


class WeChatImageUploader:
    """微信图片上传器"""

    def __init__(self):
        self.appid = os.environ.get("WECHAT_APPID")
        self.secret = os.environ.get("WECHAT_SECRET")

        if not self.appid or not self.secret:
            raise ValueError("请设置 WECHAT_APPID 和 WECHAT_SECRET 环境变量")

        # 代理配置
        self.use_proxy = os.getenv("WECHAT_USE_PROXY", "true").lower() == "true"
        self.proxy_url = os.getenv("WECHAT_PROXY_URL", "http://115.191.30.195/wechat")
        self.base_url = f"{self.proxy_url}/cgi-bin" if self.use_proxy else "https://api.weixin.qq.com/cgi-bin"

        self._token = None
        self._token_file = Path("/tmp/wechat_token.json")

    def get_token(self) -> str:
        """获取 access_token"""
        # 尝试从缓存读取
        if self._token_file.exists():
            try:
                cached = json.loads(self._token_file.read_text())
                if cached.get("expires_at", 0) > int(time.time()):
                    return cached["access_token"]
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
        import time
        self._token_file.write_text(json.dumps({
            "access_token": self._token,
            "expires_at": int(time.time()) + expires_in - 300
        }))

        return self._token

    @property
    def token(self) -> str:
        if not self._token:
            return self.get_token()
        return self._token

    def upload_image(self, image_path: str) -> str:
        """
        上传图片到微信

        Args:
            image_path: 图片文件路径

        Returns:
            微信图片 URL
        """
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"图片不存在: {image_path}")

        url = f"{self.base_url}/media/uploadimg?access_token={self.token}"
        files = {"media": open(path, "rb")}
        resp = requests.post(url, files=files, timeout=60)
        data = resp.json()

        if "errcode" in data and data["errcode"] != 0:
            raise Exception(f"上传图片失败: {data.get('errmsg')}")

        return data.get("url")

    def batch_upload(self, directory: str, pattern: str = "*.jpg") -> Dict[str, str]:
        """
        批量上传图片

        Args:
            directory: 图片目录
            pattern: 文件匹配模式（默认 *.jpg）

        Returns:
            {本地路径: 微信 URL}
        """
        result = {}
        dir_path = Path(directory)

        if not dir_path.is_dir():
            raise NotADirectoryError(f"不是目录: {directory}")

        # 查找所有匹配的文件
        images = list(dir_path.glob(pattern))

        if not images:
            print(f"⚠️  未找到匹配 {pattern} 的文件")
            return result

        print(f"📤 找到 {len(images)} 张图片")

        for i, image_path in enumerate(images, 1):
            try:
                print(f"[{i}/{len(images)}] 上传: {image_path.name}")
                url = self.upload_image(str(image_path))
                result[str(image_path)] = url
                print(f"   ✅ {url[:50]}...")
            except Exception as e:
                print(f"   ❌ 失败: {e}")

        return result

    def replace_html_images(self, html_path: str, image_map: Dict[str, str], output_path: str = None) -> str:
        """
        替换 HTML 中的图片 URL

        Args:
            html_path: HTML 文件路径
            image_map: {本地路径/文件名: 微信 URL}
            output_path: 输出文件路径（默认覆盖原文件）

        Returns:
            替换后的 HTML 内容
        """
        html_file = Path(html_path)
        content = html_file.read_text(encoding="utf-8")

        # 替换图片 URL
        for local_path, wechat_url in image_map.items():
            # 尝试多种匹配方式
            patterns = [
                local_path,  # 完整路径
                Path(local_path).name,  # 文件名
                f"images/{Path(local_path).name}",  # 相对路径
            ]

            for pattern in patterns:
                if pattern in content:
                    content = content.replace(pattern, wechat_url)
                    print(f"✅ 替换: {pattern} → 微信 URL")

        # 保存文件
        output = Path(output_path) if output_path else html_file
        output.write_text(content, encoding="utf-8")
        print(f"\n💾 已保存: {output}")

        return content


def main():
    import argparse

    parser = argparse.ArgumentParser(description="批量上传图片到微信公众号")
    parser.add_argument("path", help="图片文件或目录")
    parser.add_argument("--pattern", default="*.jpg", help="文件匹配模式（默认 *.jpg）")
    parser.add_argument("--html", help="HTML 文件路径（用于替换图片 URL）")
    parser.add_argument("--output", help="输出 HTML 文件路径")
    parser.add_argument("--save-map", help="保存图片映射到 JSON 文件")

    args = parser.parse_args()

    uploader = WeChatImageUploader()
    path = Path(args.path)

    # 上传图片
    if path.is_file():
        # 单文件
        print(f"📤 上传: {path}")
        url = uploader.upload_image(str(path))
        image_map = {str(path): url}
        print(f"✅ {url}")
    elif path.is_dir():
        # 目录
        image_map = uploader.batch_upload(str(path), args.pattern)
    else:
        print(f"❌ 路径不存在: {path}")
        sys.exit(1)

    # 保存映射
    if args.save_map:
        with open(args.save_map, "w") as f:
            json.dump(image_map, f, indent=2)
        print(f"\n💾 图片映射已保存: {args.save_map}")

    # 替换 HTML
    if args.html:
        print(f"\n🔄 替换 HTML: {args.html}")
        uploader.replace_html_images(args.html, image_map, args.output)


if __name__ == "__main__":
    import time
    main()
