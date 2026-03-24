#!/usr/bin/env python3
"""
微信公众号草稿管理脚本
支持：创建新草稿、更新现有草稿
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error

# 微信公众号配置
APPID = os.environ.get("WECHAT_APPID", "wx9aa62d3e2bbd457a")
SECRET = os.environ.get("WECHAT_SECRET", "0d740d847430bd0a3a0b92a019f51f42")

# 固定封面图
THUMB_MEDIA_ID = "Sgs1hrgsJnAqIX94EoxAiNKZV3aIkaiHaO-BxJAzU0HrGitHNxAU2MGiKD6-H61W"

# 状态文件
DRAFT_STATE_FILE = os.path.expanduser("~/.openclaw/workspace/articles/.draft-state.json")


def get_access_token():
    """获取 access_token"""
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={SECRET}"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            if "access_token" in data:
                return data["access_token"]
            else:
                print(f"获取 access_token 失败: {data}", file=sys.stderr)
                return None
    except Exception as e:
        print(f"请求失败: {e}", file=sys.stderr)
        return None


def load_draft_state():
    """加载草稿状态"""
    if os.path.exists(DRAFT_STATE_FILE):
        try:
            with open(DRAFT_STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {}


def save_draft_state(state):
    """保存草稿状态"""
    os.makedirs(os.path.dirname(DRAFT_STATE_FILE), exist_ok=True)
    with open(DRAFT_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def update_draft(token, media_id, title, content):
    """更新草稿"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/update?access_token={token}"
    payload = {
        "media_id": media_id,
        "index": 0,
        "articles": {
            "title": title,
            "content": content,
            "thumb_media_id": THUMB_MEDIA_ID,
            "need_open_comment": 0,
            "fans_only": 0
        }
    }
    
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json; charset=utf-8"})
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("errcode", 0) == 0, result
    except Exception as e:
        return False, {"error": str(e)}


def add_draft(token, title, content):
    """创建新草稿"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
    payload = {
        "articles": [{
            "title": title,
            "content": content,
            "thumb_media_id": THUMB_MEDIA_ID,
            "need_open_comment": 0,
            "fans_only": 0
        }]
    }
    
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json; charset=utf-8"})
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            if "media_id" in result:
                return True, result
            return False, result
    except Exception as e:
        return False, {"error": str(e)}


def main():
    if len(sys.argv) < 3:
        print("用法: python wechat_draft.py <标题> <HTML文件路径>", file=sys.stderr)
        sys.exit(1)
    
    title = sys.argv[1]
    html_file = sys.argv[2]
    
    # 读取 HTML 内容
    if not os.path.exists(html_file):
        print(f"文件不存在: {html_file}", file=sys.stderr)
        sys.exit(1)
    
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 获取 access_token
    token = get_access_token()
    if not token:
        print("获取 access_token 失败", file=sys.stderr)
        sys.exit(1)
    
    print(f"✅ 获取 access_token 成功")
    
    # 加载草稿状态
    state = load_draft_state()
    media_id = state.get("media_id")
    
    # 尝试更新草稿
    if media_id:
        print(f"🔄 尝试更新草稿: {media_id}")
        success, result = update_draft(token, media_id, title, content)
        if success:
            print(f"✅ 更新草稿成功!")
            # 更新状态
            state["media_id"] = media_id
            state["title"] = title
            state["updated_at"] = __import__("datetime").datetime.now().isoformat()
            save_draft_state(state)
            print(f"📝 草稿 ID: {media_id}")
            sys.exit(0)
        else:
            print(f"⚠️ 更新失败: {result}")
            print("📝 将创建新草稿...")
    
    # 创建新草稿
    print(f"🆕 创建新草稿: {title}")
    success, result = add_draft(token, title, content)
    if success:
        new_media_id = result["media_id"]
        print(f"✅ 创建草稿成功!")
        # 保存状态
        state["media_id"] = new_media_id
        state["title"] = title
        state["created_at"] = __import__("datetime").datetime.now().isoformat()
        state["thumb_media_id"] = THUMB_MEDIA_ID
        save_draft_state(state)
        print(f"📝 草稿 ID: {new_media_id}")
    else:
        print(f"❌ 创建草稿失败: {result}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
