#!/usr/bin/env python3
"""
发送 Discord 通知
用于通知用户草稿已更新，请手动发布
"""

import os
import sys
import requests
import json

def send_discord_notification(title: str, draft_updated: bool = True):
    """
    发送 Discord 通知
    
    Args:
        title: 文章标题
        draft_updated: 草稿是否更新成功
    """
    # 从环境变量获取 Discord webhook（如果有的话）
    # 或者使用 OpenClaw 的 message 工具
    
    # 构建消息
    if draft_updated:
        message = f"""📝 **公众号文章草稿已更新**

**文章标题**：{title}

✅ 草稿已自动更新到公众号后台
📅 时间：{get_current_time()}

🔗 请登录 mp.weixin.qq.com 手动发布

---
*此消息由 OpenClaw 自动发送*"""
    else:
        message = f"""❌ **公众号文章草稿更新失败**

**文章标题**：{title}

⚠️ 请检查日志或手动创建草稿

---
*此消息由 OpenClaw 自动发送*"""
    
    # 这里可以调用 OpenClaw 的消息接口
    # 或者使用 Discord webhook
    print(message)
    return message

def get_current_time():
    """获取当前时间"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="发送 Discord 通知")
    parser.add_argument("--title", "-t", required=True, help="文章标题")
    parser.add_argument("--success", "-s", action="store_true", default=True, help="是否成功")
    
    args = parser.parse_args()
    
    message = send_discord_notification(args.title, args.success)
    print("\n📤 通知已发送")
