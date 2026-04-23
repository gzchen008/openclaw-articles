#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号草稿创建脚本
"""

import json
import requests
import sys
from datetime import datetime

# 微信公众号配置
APPID = "wx9aa62d3e2bbd457a"
SECRET = "0d740d847430bd0a3a0b92a019f51f42"
THUMB_MEDIA_ID = "Sgs1hrgsJnAqIX94EoxAiNKZV3aIkaiHaO-BxJAzU0HrGitHNxAU2MGiKD6-H61W"

def get_access_token():
    """获取 access_token"""
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={SECRET}"
    response = requests.get(url)
    data = response.json()
    if "access_token" in data:
        return data["access_token"]
    else:
        print(f"获取 access_token 失败: {data}")
        sys.exit(1)

def create_draft(access_token, title, content, thumb_media_id):
    """创建草稿"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    
    payload = {
        "articles": [{
            "title": title,
            "content": content,
            "thumb_media_id": thumb_media_id,
            "author": "",
            "digest": "",
            "content_source_url": "",
            "need_open_comment": 0,
            "only_fans_can_comment": 0
        }]
    }
    
    headers = {"Content-Type": "application/json; charset=utf-8"}
    json_data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    
    response = requests.post(url, data=json_data, headers=headers)
    data = response.json()
    
    if "media_id" in data:
        return data["media_id"]
    else:
        print(f"创建草稿失败: {data}")
        sys.exit(1)

def save_draft_state(media_id, title, content_file):
    """保存草稿状态"""
    state = {
        "last_updated": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "title": title,
        "media_id": media_id,
        "thumb_media_id": THUMB_MEDIA_ID,
        "content_file": content_file
    }
    
    with open(".draft-state.json", "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    
    print(f"草稿状态已保存: {media_id}")

def main():
    if len(sys.argv) < 3:
        print("用法: python3 create_draft.py <标题> <HTML文件路径>")
        sys.exit(1)
    
    title = sys.argv[1]
    html_file = sys.argv[2]
    
    # 读取 HTML 内容
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    print(f"正在创建草稿: {title}")
    
    # 获取 access_token
    access_token = get_access_token()
    print(f"获取 access_token 成功")
    
    # 创建草稿
    media_id = create_draft(access_token, title, content, THUMB_MEDIA_ID)
    print(f"草稿创建成功: {media_id}")
    
    # 保存草稿状态
    save_draft_state(media_id, title, html_file)
    
    print(f"\n✅ 草稿已创建！")
    print(f"标题: {title}")
    print(f"草稿 ID: {media_id}")
    print(f"\n请登录公众号后台手动发布")

if __name__ == "__main__":
    main()
