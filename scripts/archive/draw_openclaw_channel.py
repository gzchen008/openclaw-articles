#!/usr/bin/env python3
"""手绘风格流程图 - OpenClaw Channel 架构"""

from PIL import Image, ImageDraw, ImageFont
import random
import math

# 创建画布（增加高度）
width, height = 1600, 1100
img = Image.new('RGB', (width, height), '#fafafa')
draw = ImageDraw.Draw(img)

# 尝试加载中文字体（macOS）- 加大加粗
try:
    # 优先使用华文黑体（macOS 自带中文字体）
    font_title = ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc', 48)
    font_subtitle = ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc', 30)
    font_text = ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc', 22)
    font_small = ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc', 18)
    font_tiny = ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc', 16)
except:
    # 备选：PingFang
    try:
        font_title = ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', 48)
        font_subtitle = ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', 30)
        font_text = ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', 22)
        font_small = ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', 18)
        font_tiny = ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', 16)
    except:
        # 最后备选：系统默认
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_tiny = ImageFont.load_default()

def jitter(value, amount=3):
    """添加随机抖动"""
    return value + random.uniform(-amount, amount)

def sketchy_line(x1, y1, x2, y2, color='#333', width=2, jitter_amount=2):
    """手绘线条（带抖动）"""
    points = []
    steps = max(10, int(math.sqrt((x2-x1)**2 + (y2-y1)**2) / 10))
    
    for i in range(steps + 1):
        t = i / steps
        x = x1 + (x2 - x1) * t + random.uniform(-jitter_amount, jitter_amount)
        y = y1 + (y2 - y1) * t + random.uniform(-jitter_amount, jitter_amount)
        points.append((x, y))
    
    if len(points) > 1:
        draw.line(points, fill=color, width=width)

def sketchy_rect(x, y, w, h, fill_color, outline_color, text, text_color='#333'):
    """手绘矩形框"""
    # 填充
    draw.rectangle([x, y, x+w, y+h], fill=fill_color)
    
    # 手绘边框（4条独立线段）
    jitter_amount = 3
    # 上边
    sketchy_line(x, y, x+w, y, outline_color, 3, jitter_amount)
    # 右边
    sketchy_line(x+w, y, x+w, y+h, outline_color, 3, jitter_amount)
    # 下边
    sketchy_line(x, y+h, x+w, y+h, outline_color, 3, jitter_amount)
    # 左边
    sketchy_line(x, y, x, y+h, outline_color, 3, jitter_amount)
    
    # 文字
    bbox = draw.textbbox((0, 0), text, font=font_text)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    draw.text((x + (w-text_w)//2, y + (h-text_h)//2 - 2), text, fill=text_color, font=font_text)

def draw_arrow(x1, y1, x2, y2, color='#666'):
    """绘制箭头"""
    sketchy_line(x1, y1, x2, y2, color, 2)
    # 箭头头部
    angle = math.atan2(y2-y1, x2-x1)
    head_len = 12
    x3 = x2 - head_len * math.cos(angle - math.pi/6)
    y3 = y2 - head_len * math.sin(angle - math.pi/6)
    x4 = x2 - head_len * math.cos(angle + math.pi/6)
    y4 = y2 - head_len * math.sin(angle + math.pi/6)
    draw.polygon([(x2, y2), (x3, y3), (x4, y4)], fill=color)

def draw_channel_icon(x, y, name, color):
    """绘制 Channel 图标（简化版）"""
    # 圆形背景
    draw.ellipse([x-30, y-30, x+30, y+30], fill=color, outline='#333', width=2)
    # 文字
    draw.text((x-12, y-10), name, fill='white', font=font_small)

# ========== 标题 ==========
title = 'OpenClaw Channel 架构 🦞'
bbox = draw.textbbox((0, 0), title, font=font_title)
title_w = bbox[2] - bbox[0]
draw.text(((width-title_w)//2, 20), title, fill='#2c3e50', font=font_title)

# ========== 左侧：多平台 Channel ==========
draw.text((80, 100), '📱 多平台 Channel', fill='#3498db', font=font_subtitle)

# Channel 列表
channels = [
    ('WhatsApp', '#25D366'),
    ('Telegram', '#0088cc'),
    ('Discord', '#5865F2'),
    ('Signal', '#3a76f0'),
    ('Slack', '#4A154B'),
    ('iMessage', '#34C759'),
]

y_pos = 160
for i, (name, color) in enumerate(channels):
    draw_channel_icon(150, y_pos, name[:2], color)
    draw.text((190, y_pos-12), name, fill='#333', font=font_text)
    y_pos += 70

# 省略号
draw.text((130, y_pos), '...', fill='#999', font=font_subtitle)
draw.text((80, y_pos+40), '(还有 Google Chat,', fill='#666', font=font_small)
draw.text((80, y_pos+65), 'Teams, Matrix, Zalo...)', fill='#666', font=font_small)

# ========== 中间：Gateway ==========
gateway_x = 650
sketchy_rect(gateway_x-140, 220, 280, 520, '#ffe4b5', '#e67e22', '', '#333')

# Gateway 标题
draw.text((gateway_x-60, 220), '🦞 Gateway', fill='#d35400', font=font_subtitle)
draw.text((gateway_x-80, 260), '(控制中心)', fill='#666', font=font_small)

# Gateway 功能列表（扩展会话管理细节）
functions = [
    '✅ Channel 连接管理',
    '✅ 消息路由分发',
    '✅ 权限验证',
    '',
    '📝 会话管理细节：',
    '  • main (主会话)',
    '  • isolated (隔离会话)',
    '  • sub-agent (子智能体)',
    '  • dmScope (私聊范围)',
    '  • 会话持久化',
    '',
    '✅ 事件调度',
]
y = 290
for func in functions:
    draw.text((gateway_x-110, y), func, fill='#333', font=font_small)
    y += 32

# ========== 右侧：Agent ==========
agent_x = 1280
sketchy_rect(agent_x-140, 220, 280, 520, '#d5f4e6', '#27ae60', '', '#333')

# Agent 标题
draw.text((agent_x-50, 220), '🤖 Agent', fill='#27ae60', font=font_subtitle)
draw.text((agent_x-70, 260), '(智能体)', fill='#666', font=font_small)

# Agent 功能列表
agent_funcs = [
    '🧠 上下文加载',
    '💬 消息处理',
    '🔧 工具调用',
    '📝 记忆管理',
    '⚡ 任务执行',
]
y = 310
for func in agent_funcs:
    draw.text((agent_x-100, y), func, fill='#333', font=font_small)
    y += 35

# ========== 连接箭头 ==========
# Channel → Gateway
for i in range(6):
    y = 160 + i * 70
    draw_arrow(190, y, gateway_x-150, 400 + random.randint(-50, 50), '#3498db')

# Gateway → Agent
draw_arrow(gateway_x+140, 480, agent_x-150, 480, '#e67e22')

# ========== 底部：安全机制 ==========
security_y = 850
draw.text((80, security_y), '🔒 安全机制', fill='#e74c3c', font=font_subtitle)

# 安全机制说明
security_items = [
    ('dmPolicy', '私聊配对', '#e74c3c'),
    ('groupPolicy', '群聊白名单', '#e67e22'),
    ('allowFrom', '用户白名单', '#3498db'),
]

x_pos = 80
for name, desc, color in security_items:
    # 小方框
    sketchy_rect(x_pos, security_y+50, 160, 70, '#fff', color, '', '#333')
    draw.text((x_pos+15, security_y+62), name, fill=color, font=font_small)
    draw.text((x_pos+15, security_y+88), desc, fill='#666', font=font_small)
    x_pos += 200

# ========== 流程说明 ==========
draw.text((850, security_y), '💡 消息流转', fill='#9b59b6', font=font_subtitle)
draw.text((850, security_y+50), '用户消息 → Channel 接收', fill='#333', font=font_small)
draw.text((850, security_y+80), '→ Gateway 路由', fill='#333', font=font_small)
draw.text((850, security_y+110), '→ Agent 处理', fill='#333', font=font_small)
draw.text((850, security_y+140), '→ 回复返回', fill='#333', font=font_small)

# ========== 底部说明 ==========
footer = '所有 Channel 统一接口 → message tool'
bbox = draw.textbbox((0, 0), footer, font=font_text)
footer_w = bbox[2] - bbox[0]
draw.text(((width-footer_w)//2, 1050), footer, fill='#666', font=font_text)

# 保存
img.save('openclaw-channel-architecture.png', 'PNG', quality=95)
print('✅ OpenClaw Channel 架构图已保存为 openclaw-channel-architecture.png')
