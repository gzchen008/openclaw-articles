#!/usr/bin/env python3
"""
更新现有草稿
"""

import sys
sys.path.insert(0, '/Users/cgz/.openclaw/workspace/skills/wechat-mp-publish')

from scripts.wechat_publisher import WeChatPublisher
import json

# 读取草稿 ID
with open('/Users/cgz/.openclaw/workspace/articles/.draft-state.json', 'r') as f:
    draft_state = json.load(f)
    draft_id = draft_state['last_draft_id']

# 读取 HTML 内容
with open('/Users/cgz/.openclaw/workspace/articles/claw-family-comparison.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 初始化 publisher
publisher = WeChatPublisher()

# 封面 ID
thumb_media_id = "Sgs1hrgsJnAqIX94EoxAiIi0abxAD3Ie6G3Dj1COv_XH3DYup5AzxiYShV2ymhZX"

# 更新草稿
print(f"📝 更新草稿: {draft_id}")
try:
    result = publisher.update_draft(
        media_id=draft_id,
        title="🔥 Claw 家族大盘点：8 个 AI 助手框架全面对比",
        content=content,
        thumb_media_id=thumb_media_id
    )
    print("✅ 草稿更新成功！")
    print(f"   草稿 ID: {draft_id}")
except Exception as e:
    print(f"❌ 更新失败: {e}")
    print("💡 尝试创建新草稿...")
    # 如果更新失败，创建新草稿
    result = publisher.create_draft(
        title="🔥 Claw 家族大盘点：8 个 AI 助手框架全面对比",
        content=content,
        thumb_media_id=thumb_media_id
    )
    print(f"✅ 新草稿创建成功！")
    print(f"   草稿 ID: {result['media_id']}")
    
    # 保存新草稿 ID
    draft_state['last_draft_id'] = result['media_id']
    draft_state['last_updated'] = "2026-02-18T08:30:00Z"
    with open('/Users/cgz/.openclaw/workspace/articles/.draft-state.json', 'w') as f:
        json.dump(draft_state, f, indent=2, ensure_ascii=False)
