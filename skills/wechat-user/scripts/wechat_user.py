#!/usr/bin/env python3
"""
微信公众号用户管理工具
支持：粉丝列表、用户信息、标签管理
"""

import os
import sys
import json
import requests
from typing import List, Dict, Any

class WeChatUser:
    """微信公众号用户管理"""
    
    BASE_URL = "https://api.weixin.qq.com/cgi-bin"
    
    def __init__(self):
        self.appid = os.environ.get("WECHAT_APPID")
        self.secret = os.environ.get("WECHAT_SECRET")
        self._token = None
        
        if not self.appid or not self.secret:
            raise ValueError("请设置 WECHAT_APPID 和 WECHAT_SECRET 环境变量")
    
    def get_token(self) -> str:
        """获取 access_token"""
        if self._token:
            return self._token
        
        url = f"{self.BASE_URL}/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.appid,
            "secret": self.secret
        }
        resp = requests.get(url, params=params, timeout=30)
        self._token = resp.json().get("access_token")
        return self._token
    
    @property
    def token(self) -> str:
        return self.get_token()
    
    def get_fans_list(self, next_openid: str = "") -> Dict[str, Any]:
        """
        获取关注者列表
        
        Args:
            next_openid: 第一个拉取的 OPENID，不填默认从头开始拉取
        
        Returns:
            {"total": 总数, "count": 本次数量, "data": {"openid": [...]}}
        """
        url = f"{self.BASE_URL}/user/get?access_token={self.token}"
        if next_openid:
            url += f"&next_openid={next_openid}"
        return requests.get(url, timeout=30).json()
    
    def get_all_fans(self) -> List[str]:
        """获取所有粉丝的 OpenID 列表"""
        all_openids = []
        next_openid = ""
        
        while True:
            result = self.get_fans_list(next_openid)
            data = result.get("data", {})
            openids = data.get("openid", [])
            
            if not openids:
                break
            
            all_openids.extend(openids)
            next_openid = result.get("next_openid", "")
            
            if not next_openid:
                break
        
        return all_openids
    
    def get_user_info(self, openid: str) -> Dict[str, Any]:
        """
        获取用户基本信息
        
        Args:
            openid: 用户的 OpenID
        
        Returns:
            用户信息（subscribe, openid, nickname, sex, city, province, country, headimgurl 等）
        """
        url = f"{self.BASE_URL}/user/info?access_token={self.token}&openid={openid}"
        return requests.get(url, timeout=30).json()
    
    def batch_get_user_info(self, openids: List[str]) -> List[Dict[str, Any]]:
        """
        批量获取用户基本信息
        
        Args:
            openids: OpenID 列表（最多100个）
        
        Returns:
            用户信息列表
        """
        url = f"{self.BASE_URL}/user/info/batchget?access_token={self.token}"
        payload = {
            "user_list": [{"openid": openid, "lang": "zh_CN"} for openid in openids[:100]]
        }
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        resp = requests.post(url, data=data, headers=headers, timeout=30)
        return resp.json().get("user_info_list", [])
    
    def update_remark(self, openid: str, remark: str) -> bool:
        """设置用户备注名"""
        url = f"{self.BASE_URL}/user/info/updateremark?access_token={self.token}"
        payload = {"openid": openid, "remark": remark}
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        resp = requests.post(url, data=data, headers=headers, timeout=30)
        return resp.json().get("errcode", 0) == 0
    
    # ===== 标签管理 =====
    
    def create_tag(self, name: str) -> Dict[str, Any]:
        """创建标签"""
        url = f"{self.BASE_URL}/tags/create?access_token={self.token}"
        payload = {"tag": {"name": name}}
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        resp = requests.post(url, data=data, headers=headers, timeout=30)
        return resp.json()
    
    def get_tags(self) -> List[Dict[str, Any]]:
        """获取标签列表"""
        url = f"{self.BASE_URL}/tags/get?access_token={self.token}"
        return requests.get(url, timeout=30).json().get("tags", [])
    
    def update_tag(self, tag_id: int, name: str) -> bool:
        """编辑标签"""
        url = f"{self.BASE_URL}/tags/update?access_token={self.token}"
        payload = {"tag": {"id": tag_id, "name": name}}
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        resp = requests.post(url, data=data, headers=headers, timeout=30)
        return resp.json().get("errcode", 0) == 0
    
    def delete_tag(self, tag_id: int) -> bool:
        """删除标签"""
        url = f"{self.BASE_URL}/tags/delete?access_token={self.token}"
        payload = {"tag": {"id": tag_id}}
        resp = requests.post(url, json=payload, timeout=30)
        return resp.json().get("errcode", 0) == 0
    
    def batch_tagging(self, tag_id: int, openids: List[str]) -> bool:
        """批量为用户打标签"""
        url = f"{self.BASE_URL}/tags/members/batchtagging?access_token={self.token}"
        payload = {"tagid": tag_id, "openid_list": openids}
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        resp = requests.post(url, data=data, headers=headers, timeout=30)
        return resp.json().get("errcode", 0) == 0
    
    def get_users_by_tag(self, tag_id: int, next_openid: str = "") -> Dict[str, Any]:
        """获取标签下粉丝列表"""
        url = f"{self.BASE_URL}/user/tag/get?access_token={self.token}"
        payload = {"tagid": tag_id, "next_openid": next_openid}
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        resp = requests.post(url, data=data, headers=headers, timeout=30)
        return resp.json()
    
    # ===== 黑名单管理 =====
    
    def get_blacklist(self, begin_openid: str = "") -> Dict[str, Any]:
        """获取黑名单列表"""
        url = f"{self.BASE_URL}/tags/members/getblacklist?access_token={self.token}"
        payload = {"begin_openid": begin_openid} if begin_openid else {}
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        resp = requests.post(url, data=data, headers=headers, timeout=30)
        return resp.json()
    
    def batch_blacklist(self, openids: List[str]) -> bool:
        """拉黑用户"""
        url = f"{self.BASE_URL}/tags/members/batchblacklist?access_token={self.token}"
        payload = {"openid_list": openids}
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        resp = requests.post(url, data=data, headers=headers, timeout=30)
        return resp.json().get("errcode", 0) == 0


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="微信公众号用户管理工具")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # fans 命令
    fans_parser = subparsers.add_parser("fans", help="获取粉丝列表")
    fans_parser.add_argument("--all", "-a", action="store_true", help="获取全部粉丝")
    
    # info 命令
    info_parser = subparsers.add_parser("info", help="获取用户信息")
    info_parser.add_argument("openid", help="用户 OpenID")
    
    # batch-info 命令
    batch_parser = subparsers.add_parser("batch-info", help="批量获取用户信息")
    batch_parser.add_argument("openids", help="OpenID 列表，逗号分隔")
    
    # tag 命令
    tag_parser = subparsers.add_parser("tag", help="标签管理")
    tag_parser.add_argument("action", choices=["create", "list", "update", "delete", "batch-tag", "users"])
    tag_parser.add_argument("--name", "-n", help="标签名称")
    tag_parser.add_argument("--tag-id", "-t", type=int, help="标签ID")
    tag_parser.add_argument("--openids", "-o", help="OpenID 列表，逗号分隔")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        user = WeChatUser()
        
        if args.command == "fans":
            if args.all:
                print("📥 获取所有粉丝...")
                openids = user.get_all_fans()
                print(f"✅ 共 {len(openids)} 位粉丝")
            else:
                result = user.get_fans_list()
                print(f"📊 粉丝数据：")
                print(f"   总数：{result.get('total', 0)}")
                print(f"   本次：{result.get('count', 0)}")
                openids = result.get("data", {}).get("openid", [])
                if openids:
                    print(f"   前5个：{openids[:5]}")
        
        elif args.command == "info":
            print(f"📥 获取用户信息：{args.openid}")
            info = user.get_user_info(args.openid)
            print(f"✅ 用户信息：")
            print(f"   昵称：{info.get('nickname', 'N/A')}")
            print(f"   性别：{['未知', '男', '女'][info.get('sex', 0)]}")
            print(f"   地区：{info.get('province', '')} {info.get('city', '')}")
            print(f"   关注时间：{info.get('subscribe_time', 'N/A')}")
        
        elif args.command == "batch-info":
            openids = args.openids.split(",")
            print(f"📥 批量获取 {len(openids)} 位用户信息...")
            users = user.batch_get_user_info(openids)
            for u in users[:5]:
                print(f"   - {u.get('nickname', 'N/A')} ({u.get('openid', '')[:10]}...)")
        
        elif args.command == "tag":
            if args.action == "list":
                print("📥 获取标签列表...")
                tags = user.get_tags()
                print(f"✅ 共 {len(tags)} 个标签：")
                for tag in tags:
                    print(f"   - [{tag['id']}] {tag['name']} ({tag.get('count', 0)}人)")
            
            elif args.action == "create":
                if not args.name:
                    print("❌ 请指定标签名称 --name")
                    return
                print(f"📥 创建标签：{args.name}")
                result = user.create_tag(args.name)
                if "tag" in result:
                    print(f"✅ 创建成功！ID: {result['tag']['id']}")
                else:
                    print(f"❌ 创建失败：{result}")
            
            elif args.action == "batch-tag":
                if not args.tag_id or not args.openids:
                    print("❌ 请指定 --tag-id 和 --openids")
                    return
                openids = args.openids.split(",")
                print(f"📥 为 {len(openids)} 位用户打标签...")
                if user.batch_tagging(args.tag_id, openids):
                    print("✅ 打标签成功！")
                else:
                    print("❌ 打标签失败")
    
    except Exception as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
