#!/usr/bin/env python3
"""
测试已发布文章接口
"""

import sys
sys.path.insert(0, '/Users/cgz/.openclaw/workspace/skills/wechat-mp-publish/scripts')

from wechat_publisher import WeChatPublisher
import json

def test_published_articles():
    """测试获取已发布文章"""
    print("=" * 60)
    print("测试：获取已发布文章列表")
    print("=" * 60)
    
    try:
        publisher = WeChatPublisher()
        
        # 测试接口
        url = f"{publisher.BASE_URL}/freepublish/get?access_token={publisher.token}"
        
        import requests
        payload = {
            "offset": 0,
            "count": 10,
            "no_content": 1  # 不返回内容，只返回元信息
        }
        
        print(f"\n📤 请求: {url}")
        print(f"📦 参数: {json.dumps(payload, indent=2)}")
        
        resp = requests.post(url, json=payload, timeout=30)
        data = resp.json()
        
        print(f"\n📥 响应:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        # 分析结果
        print("\n" + "=" * 60)
        if "errcode" in data:
            if data["errcode"] == 0:
                print("✅ 成功！可以获取已发布文章列表")
                print(f"   总数: {data.get('total_count', 0)}")
            elif data["errcode"] == 48001:
                print("❌ 无权限（48001）")
                print("   个人账号无法使用此接口")
            else:
                print(f"⚠️  错误: {data.get('errmsg')}")
        else:
            print("✅ 成功获取数据")
            
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

def test_article_detail(article_id=None):
    """测试获取文章详情"""
    print("\n" + "=" * 60)
    print("测试：获取文章详情（getarticle）")
    print("=" * 60)
    
    if not article_id:
        print("⚠️  需要 article_id 参数")
        return
    
    try:
        publisher = WeChatPublisher()
        
        url = f"{publisher.BASE_URL}/freepublish/getarticle?access_token={publisher.token}"
        payload = {"article_id": article_id}
        
        print(f"\n📤 请求: {url}")
        print(f"📦 参数: {json.dumps(payload, indent=2)}")
        
        import requests
        resp = requests.post(url, json=payload, timeout=30)
        data = resp.json()
        
        print(f"\n📥 响应:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        # 分析结果
        print("\n" + "=" * 60)
        if "errcode" in data:
            if data["errcode"] == 0:
                print("✅ 成功！可以获取文章详情")
            elif data["errcode"] == 48001:
                print("❌ 无权限（48001）")
                print("   个人账号无法使用此接口")
            else:
                print(f"⚠️  错误: {data.get('errmsg')}")
        else:
            print("✅ 成功获取数据")
            
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

def test_article_stats():
    """测试获取图文统计（肯定失败，但确认一下）"""
    print("\n" + "=" * 60)
    print("测试：获取图文统计（datacube）")
    print("=" * 60)
    
    try:
        publisher = WeChatPublisher()
        
        url = f"{publisher.BASE_URL}/datacube/getarticlesummary?access_token={publisher.token}"
        
        import requests
        from datetime import datetime, timedelta
        
        # 获取昨天的日期
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        payload = {
            "begin_date": yesterday,
            "end_date": yesterday
        }
        
        print(f"\n📤 请求: {url}")
        print(f"📦 参数: {json.dumps(payload, indent=2)}")
        
        resp = requests.post(url, json=payload, timeout=30)
        data = resp.json()
        
        print(f"\n📥 响应:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        # 分析结果
        print("\n" + "=" * 60)
        if "errcode" in data:
            if data["errcode"] == 48001:
                print("❌ 无权限（48001）- 符合预期")
                print("   个人账号无法获取统计数据")
            else:
                print(f"⚠️  错误: {data.get('errmsg')}")
        else:
            print("✅ 意外成功！可以获取统计数据")
            
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🔍 微信公众号接口测试")
    print("=" * 60)
    print("测试账号类型：个人订阅号")
    print("=" * 60)
    
    # 测试 1: 已发布文章列表
    test_published_articles()
    
    # 测试 2: 图文统计（预期失败）
    test_article_stats()
    
    # 如果需要测试文章详情，需要先获取 article_id
    # test_article_detail("ARTICLE_ID_HERE")
    
    print("\n" + "=" * 60)
    print("🏁 测试完成")
    print("=" * 60)
