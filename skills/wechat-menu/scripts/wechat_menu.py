#!/usr/bin/env python3
"""
微信公众号菜单管理工具
支持：创建、查询、删除自定义菜单
"""

import os
import sys
import json
import requests
from pathlib import Path
from typing import Dict, Any, List

class WeChatMenu:
    """微信公众号菜单管理"""
    
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
    
    def create_menu(self, menu_data: Dict[str, Any]) -> bool:
        """
        创建自定义菜单
        
        Args:
            menu_data: 菜单数据
        
        Returns:
            是否成功
        """
        url = f"{self.BASE_URL}/menu/create?access_token={self.token}"
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = json.dumps(menu_data, ensure_ascii=False).encode('utf-8')
        resp = requests.post(url, data=data, headers=headers, timeout=30)
        result = resp.json()
        
        if result.get("errcode", 0) == 0:
            return True
        else:
            raise Exception(f"创建菜单失败: {result.get('errmsg')}")
    
    def get_menu(self) -> Dict[str, Any]:
        """获取自定义菜单配置"""
        url = f"{self.BASE_URL}/menu/get?access_token={self.token}"
        return requests.get(url, timeout=30).json()
    
    def get_current_menu(self) -> Dict[str, Any]:
        """获取当前使用的菜单配置"""
        url = f"{self.BASE_URL}/get_current_selfmenu_info?access_token={self.token}"
        return requests.get(url, timeout=30).json()
    
    def delete_menu(self) -> bool:
        """删除自定义菜单"""
        url = f"{self.BASE_URL}/menu/delete?access_token={self.token}"
        resp = requests.get(url, timeout=30)
        return resp.json().get("errcode", 0) == 0
    
    def create_conditional_menu(self, menu_data: Dict[str, Any]) -> str:
        """
        创建个性化菜单
        
        Args:
            menu_data: 包含 matchrule 的菜单数据
        
        Returns:
            菜单 ID
        """
        url = f"{self.BASE_URL}/menu/addconditional?access_token={self.token}"
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = json.dumps(menu_data, ensure_ascii=False).encode('utf-8')
        resp = requests.post(url, data=data, headers=headers, timeout=30)
        result = resp.json()
        
        if "menuid" in result:
            return result["menuid"]
        else:
            raise Exception(f"创建个性化菜单失败: {result.get('errmsg')}")
    
    def delete_conditional_menu(self, menu_id: str) -> bool:
        """删除个性化菜单"""
        url = f"{self.BASE_URL}/menu/delconditional?access_token={self.token}"
        payload = {"menuid": menu_id}
        resp = requests.post(url, json=payload, timeout=30)
        return resp.json().get("errcode", 0) == 0
    
    def try_match_menu(self, user_id: str) -> Dict[str, Any]:
        """测试个性化菜单匹配结果"""
        url = f"{self.BASE_URL}/menu/trymatch?access_token={self.token}"
        payload = {"user_id": user_id}
        resp = requests.post(url, json=payload, timeout=30)
        return resp.json()


def create_simple_menu(buttons: List[str]) -> Dict[str, Any]:
    """
    创建简单菜单
    
    Args:
        buttons: 按钮列表，格式 "名称|URL" 或 "名称|click:KEY"
    
    Returns:
        菜单数据
    """
    menu_buttons = []
    
    for btn in buttons:
        if "|" not in btn:
            continue
        
        parts = btn.split("|", 1)
        name = parts[0]
        action = parts[1]
        
        if action.startswith("http"):
            button = {"type": "view", "name": name, "url": action}
        elif action.startswith("click:"):
            button = {"type": "click", "name": name, "key": action[6:]}
        elif action.startswith("miniprogram:"):
            # 小程序格式: miniprogram:appid:page:path
            parts = action.split(":")
            button = {
                "type": "miniprogram",
                "name": name,
                "url": "https://example.com",
                "appid": parts[1] if len(parts) > 1 else "",
                "pagepath": parts[2] if len(parts) > 2 else ""
            }
        else:
            button = {"type": "view", "name": name, "url": action}
        
        menu_buttons.append(button)
    
    return {"button": menu_buttons}


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="微信公众号菜单管理工具")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # get 命令
    get_parser = subparsers.add_parser("get", help="获取当前菜单")
    
    # create 命令
    create_parser = subparsers.add_parser("create", help="创建菜单")
    create_parser.add_argument("file", help="菜单 JSON 文件路径")
    
    # quick-create 命令
    quick_parser = subparsers.add_parser("quick-create", help="快速创建简单菜单")
    quick_parser.add_argument("--btn1", help="按钮1：名称|URL")
    quick_parser.add_argument("--btn2", help="按钮2：名称|URL")
    quick_parser.add_argument("--btn3", help="按钮3：名称|URL")
    
    # delete 命令
    delete_parser = subparsers.add_parser("delete", help="删除菜单")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        menu = WeChatMenu()
        
        if args.command == "get":
            print("📥 获取当前菜单...")
            result = menu.get_current_menu()
            
            if "selfmenu_info" in result:
                buttons = result["selfmenu_info"].get("button", [])
                print(f"✅ 当前菜单：")
                for i, btn in enumerate(buttons, 1):
                    name = btn.get("name", "N/A")
                    btn_type = btn.get("type", "N/A")
                    print(f"   {i}. {name} ({btn_type})")
                    
                    if "sub_button" in btn:
                        for j, sub in enumerate(btn["sub_button"].get("list", []), 1):
                            print(f"      {j}. {sub.get('name', 'N/A')}")
            else:
                print(f"❌ 获取失败：{result}")
        
        elif args.command == "create":
            print(f"📥 从文件创建菜单：{args.file}")
            
            file_path = Path(args.file)
            if not file_path.exists():
                print(f"❌ 文件不存在：{args.file}")
                return
            
            menu_data = json.loads(file_path.read_text(encoding="utf-8"))
            
            if menu.create_menu(menu_data):
                print("✅ 菜单创建成功！")
            else:
                print("❌ 菜单创建失败")
        
        elif args.command == "quick-create":
            buttons = [b for b in [args.btn1, args.btn2, args.btn3] if b]
            
            if not buttons:
                print("❌ 请至少指定一个按钮")
                return
            
            print(f"📥 创建简单菜单（{len(buttons)} 个按钮）...")
            menu_data = create_simple_menu(buttons)
            
            if menu.create_menu(menu_data):
                print("✅ 菜单创建成功！")
                print("   按钮：")
                for btn in menu_data["button"]:
                    print(f"   - {btn['name']}")
            else:
                print("❌ 菜单创建失败")
        
        elif args.command == "delete":
            print("📥 删除菜单...")
            if menu.delete_menu():
                print("✅ 菜单删除成功！")
            else:
                print("❌ 菜单删除失败")
    
    except Exception as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
