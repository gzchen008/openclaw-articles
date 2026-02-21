#!/usr/bin/env python3
"""
Notion 配置助手
帮助用户快速配置 Notion Integration
"""

import os
import json
import subprocess

def print_banner():
    """打印欢迎信息"""
    print("""
╔═══════════════════════════════════════════╗
║   📝 Notion 同步配置助手                  ║
║   小J 帮你快速配置 Notion Integration     ║
╚═══════════════════════════════════════════╝
""")

def check_existing_config():
    """检查现有配置"""
    token = os.environ.get("NOTION_TOKEN")
    database_id = os.environ.get("NOTION_DATABASE_ID")

    if token and database_id:
        print("✅ 检测到现有配置：")
        print(f"  • NOTION_TOKEN: {token[:20]}...")
        print(f"  • NOTION_DATABASE_ID: {database_id}")
        return True
    return False

def guide_setup():
    """引导用户设置"""
    print("\n📋 配置步骤：\n")

    print("【步骤 1】创建 Notion Integration")
    print("  1. 访问：https://www.notion.so/my-integrations")
    print("  2. 点击 'New integration'")
    print("  3. 填写名称（如：OpenClaw Sync）")
    print("  4. 复制 Internal Integration Token（以 secret_ 开头）\n")

    token = input("👉 请粘贴你的 Notion Token: ").strip()

    if not token.startswith("secret_"):
        print("⚠️  Token 格式不正确，应该以 'secret_' 开头")
        return None, None

    print("\n【步骤 2】创建 Notion 数据库")
    print("  1. 在 Notion 中创建新页面")
    print("  2. 添加数据库（表格视图）")
    print("  3. 添加以下列：")
    print("     • 标题（Title）- 默认列")
    print("     • 状态（Select）：草稿 / 已发布")
    print("     • 标签（Multi-select）")
    print("     • 发布日期（Date）")
    print("     • 链接（URL）")
    print("  4. 复制数据库 ID：")
    print("     URL 格式：https://www.notion.so/workspace/[DATABASE_ID]?v=...")
    print("     复制 [DATABASE_ID] 部分（32位字符串）\n")

    database_id = input("👉 请粘贴数据库 ID: ").strip()

    if len(database_id) != 32:
        print("⚠️  数据库 ID 应该是 32 位字符串")
        return None, None

    print("\n【步骤 3】分享数据库给 Integration")
    print("  1. 打开你的数据库页面")
    print("  2. 点击右上角 '...' → 'Add connections'")
    print("  3. 选择你创建的 Integration\n")

    return token, database_id

def save_config(token: str, database_id: str):
    """保存配置到 OpenClaw"""
    print("\n💾 保存配置到 OpenClaw...\n")

    # 构建配置
    config = {
        "env": {
            "NOTION_TOKEN": token,
            "NOTION_DATABASE_ID": database_id
        }
    }

    print("将要执行的命令：")
    print("openclaw gateway config.patch")
    print("\n配置内容：")
    print(json.dumps(config, indent=2, ensure_ascii=False))

    confirm = input("\n✅ 确认配置？(y/n): ").strip().lower()

    if confirm == 'y':
        # 保存到临时文件
        config_file = "/tmp/notion_config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f)

        print("\n✅ 配置已保存！")
        print("\n📝 接下来请运行：")
        print(f"  openclaw gateway config.patch < {config_file}")
        print("  或者手动添加到 ~/.openclaw/openclaw.json")
    else:
        print("❌ 已取消")

def test_connection(token: str, database_id: str):
    """测试连接"""
    print("\n🔍 测试连接...\n")

    try:
        import requests

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

        response = requests.get(
            f"https://api.notion.com/v1/databases/{database_id}",
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            print("✅ 连接成功！")
            print(f"  • 数据库名称：{data.get('title', [{}])[0].get('text', {}).get('content', '未命名')}")
            return True
        else:
            print(f"❌ 连接失败：{response.text}")
            return False

    except Exception as e:
        print(f"❌ 测试失败：{e}")
        return False

def main():
    """主函数"""
    print_banner()

    # 检查现有配置
    if check_existing_config():
        print("\n是否要更新配置？(y/n)")
        if input().strip().lower() != 'y':
            print("✅ 保持现有配置")
            return

    # 引导设置
    token, database_id = guide_setup()

    if not token or not database_id:
        print("\n❌ 配置失败，请重试")
        return

    # 测试连接
    if test_connection(token, database_id):
        # 保存配置
        save_config(token, database_id)
    else:
        print("\n❌ 连接测试失败，请检查：")
        print("  1. Token 是否正确")
        print("  2. 数据库 ID 是否正确")
        print("  3. 是否已分享数据库给 Integration")

if __name__ == "__main__":
    main()
