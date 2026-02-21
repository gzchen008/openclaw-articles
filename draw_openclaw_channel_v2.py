#!/usr/bin/env python3
"""手绘风格流程图 - OpenClaw Channel 架构（模仿手绘风格）"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import math

# 创建画布（增加高度）
width, height = 1600, 1200
img = Image.new('RGB', (width, height), '#fefefe')
draw = ImageDraw.Draw(img)

# 加载中文字体（加大）
try:
    font_title = ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc', 56)
    font_subtitle = ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc', 38)
    font_text = ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc', 28)
    font_small = ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc', 24)
    font_tiny = ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc', 20)
except:
    font_title = ImageFont.load_default()
    font_subtitle = ImageFont.load_default()
    font_text = ImageFont.load_default()
    font_small = ImageFont.load_default()
    font_tiny = ImageFont.load_default()

def sketchy_rect(x, y, w, h, fill_color, outline_color, text, text_color='#333'):
    """手绘矩形（模仿手绘风格）"""
    # 填充背景
    draw.rectangle([x, y, x+w, y+h], fill=fill_color)
    
    # 手绘边框（每条边单独画，带抖动）
    jitter = 4
    
    # 上边
    points = []
    for i in range(15):
        t = i / 14
        px = x + w * t + random.uniform(-jitter, jitter)
        py = y + random.uniform(-jitter, jitter)
        points.append((px, py))
    draw.line(points + [(x+w, y)], fill=outline_color, width=4)
    
    # 右边
    points = []
    for i in range(15):
        t = i / 14
        px = x + w + random.uniform(-jitter, jitter)
        py = y + h * t + random.uniform(-jitter, jitter)
        points.append((px, py))
    draw.line(points + [(x+w, y+h)], fill=outline_color, width=4)
    
    # 下边
    points = []
    for i in range(15):
        t = i / 14
        px = x + w * t + random.uniform(-jitter, jitter)
        py = y + h + random.uniform(-jitter, jitter)
        points.append((px, py))
    draw.line(points + [(x, y+h)], fill=outline_color, width=4)
    
    # 左边
    points = []
    for i in range(15):
        t = i / 14
        px = x + random.uniform(-jitter, jitter)
        py = y + h * t + random.uniform(-jitter, jitter)
        points.append((px, py))
    draw.line(points + [(x, y)], fill=outline_color, width=4)
    
    # 文字
    bbox = draw.textbbox((0, 0), text, font=font_text)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    draw.text((x + (w-text_w)//2, y + (h-text_h)//2 - 2), text, fill=text_color, font=font_text)

def draw_stick_figure(x, y, label, color='#333'):
    """画简笔画小人（可爱版）"""
    # 头（圆形）
    r = 25
    draw.ellipse([x-r, y-r, x+r, y+r], outline=color, width=3)
    
    # 眼睛
    draw.ellipse([x-10, y-8, x-4, y-2], fill=color)
    draw.ellipse([x+4, y-8, x+10, y-2], fill=color)
    
    # 嘴巴（微笑）
    draw.arc([x-12, y, x+12, y+15], 0, 180, fill=color, width=3)
    
    # 身体
    draw.line([x, y+r, x, y+r+50], fill=color, width=3)
    
    # 手臂
    draw.line([x-30, y+r+20, x+30, y+r+20], fill=color, width=3)
    
    # 腿
    draw.line([x, y+r+50, x-20, y+r+90], fill=color, width=3)
    draw.line([x, y+r+50, x+20, y+r+90], fill=color, width=3)
    
    # 标签
    bbox = draw.textbbox((0, 0), label, font=font_small)
    label_w = bbox[2] - bbox[0]
    draw.text((x - label_w//2, y+r+110), label, fill='#666', font=font_small)

def draw_arrow(x1, y1, x2, y2, color='#666'):
    """手绘箭头"""
    # 画弯曲的线
    points = []
    steps = 20
    for i in range(steps + 1):
        t = i / steps
        # 添加轻微弯曲
        offset = math.sin(t * math.pi) * 10
        px = x1 + (x2-x1) * t + offset * random.uniform(-0.5, 0.5)
        py = y1 + (y2-y1) * t + random.uniform(-2, 2)
        points.append((px, py))
    
    draw.line(points, fill=color, width=3)
    
    # 箭头头部
    angle = math.atan2(y2-y1, x2-x1)
    head_len = 15
    x3 = x2 - head_len * math.cos(angle - math.pi/6)
    y3 = y2 - head_len * math.sin(angle - math.pi/6)
    x4 = x2 - head_len * math.cos(angle + math.pi/6)
    y4 = y2 - head_len * math.sin(angle + math.pi/6)
    
    draw.polygon([(x2, y2), (x3, y3), (x4, y4)], fill=color)

def draw_channel_icon(x, y, name, color):
    """绘制 Channel 图标（手绘风格）"""
    # 圆形背景（带抖动）
    r = 35
    points = []
    for i in range(30):
        angle = i * 2 * math.pi / 30
        jitter = random.uniform(-3, 3)
        px = x + (r + jitter) * math.cos(angle)
        py = y + (r + jitter) * math.sin(angle)
        points.append((px, py))
    draw.polygon(points, fill=color, outline='#333', width=2)
    
    # 文字
    draw.text((x-15, y-15), name[:2], fill='white', font=font_small)

# ========== 标题 ==========
title = 'OpenClaw Channel 架构 🦞'
bbox = draw.textbbox((0, 0), title, font=font_title)
title_w = bbox[2] - bbox[0]
draw.text(((width-title_w)//2, 30), title, fill='#2c3e50', font=font_title)

# ========== 左侧：多平台 Channel ==========
draw.text((100, 120), '📱 多平台 Channel', fill='#3498db', font=font_subtitle)

# Channel 列表
channels = [
    ('WhatsApp', '#25D366'),
    ('Telegram', '#0088cc'),
    ('Discord', '#5865F2'),
    ('Signal', '#3a76f0'),
    ('Slack', '#4A154B'),
    ('iMessage', '#34C759'),
]

y_pos = 200
for i, (name, color) in enumerate(channels):
    draw_channel_icon(200, y_pos, name, color)
    draw.text((250, y_pos-15), name, fill='#333', font=font_text)
    y_pos += 100

# 省略号
draw.text((180, y_pos), '...', fill='#999', font=font_subtitle)
draw.text((100, y_pos+50), '(还有 Google Chat,', fill='#666', font=font_small)
draw.text((100, y_pos+80), 'Teams, Matrix, Zalo...)', fill='#666', font=font_small)

# ========== 中间：Gateway ==========
gateway_x = 700
sketchy_rect(gateway_x-160, 200, 320, 580, '#ffe4b5', '#e67e22', '', '#333')

# Gateway 标题
draw.text((gateway_x-90, 230), '🦞 Gateway', fill='#d35400', font=font_subtitle)
draw.text((gateway_x-110, 285), '(控制中心)', fill='#666', font=font_small)

# Gateway 功能列表（带细节）- 增加间距
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

y = 320
for func in functions:
    draw.text((gateway_x-140, y), func, fill='#333', font=font_small)
    y += 42

# ========== 右侧：Agent ==========
agent_x = 1350
sketchy_rect(agent_x-160, 200, 320, 580, '#d5f4e6', '#27ae60', '', '#333')

# Agent 标题
draw.text((agent_x-75, 230), '🤖 Agent', fill='#27ae60', font=font_subtitle)
draw.text((agent_x-100, 285), '(智能体)', fill='#666', font=font_small)

# Agent 功能列表 - 增加间距
agent_funcs = [
    '🧠 上下文加载',
    '💬 消息处理',
    '🔧 工具调用',
    '📝 记忆管理',
    '⚡ 任务执行',
]

y = 320
for func in agent_funcs:
    draw.text((agent_x-140, y), func, fill='#333', font=font_small)
    y += 48

# ========== 简笔画小人 ==========
# 主智能体小人
draw_stick_figure(150, 900, '主智能体', '#3498db')

# 子智能体小人
draw_stick_figure(1400, 900, '子智能体', '#27ae60')

# ========== 连接箭头 ==========
# Channel → Gateway
for i in range(6):
    y = 200 + i * 100
    draw_arrow(250, y, gateway_x-160, 450 + random.randint(-80, 80), '#3498db')

# Gateway → Agent
draw_arrow(gateway_x+150, 500, agent_x-160, 500, '#e67e22')

# ========== 底部：安全机制 ==========
security_y = 920
draw.text((100, security_y), '🔒 安全机制', fill='#e74c3c', font=font_subtitle)

# 安全机制说明
security_items = [
    ('dmPolicy', '私聊配对', '#e74c3c'),
    ('groupPolicy', '群聊白名单', '#e67e22'),
    ('allowFrom', '用户白名单', '#3498db'),
]

x_pos = 100
for name, desc, color in security_items:
    # 小方框
    sketchy_rect(x_pos, security_y+70, 180, 90, '#fff', color, '', '#333')
    draw.text((x_pos+20, security_y+88), name, fill=color, font=font_small)
    draw.text((x_pos+20, security_y+118), desc, fill='#666', font=font_small)
    x_pos += 220

# ========== 流程说明 ==========
draw.text((950, security_y), '💡 消息流转', fill='#9b59b6', font=font_subtitle)
draw.text((950, security_y+70), '用户消息 → Channel 接收', fill='#333', font=font_small)
draw.text((950, security_y+110), '→ Gateway 路由', fill='#333', font=font_small)
draw.text((950, security_y+150), '→ Agent 处理', fill='#333', font=font_small)
draw.text((950, security_y+190), '→ 回复返回', fill='#333', font=font_small)

# ========== 底部说明 ==========
footer = '所有 Channel 统一接口 → message tool'
bbox = draw.textbbox((0, 0), footer, font=font_text)
footer_w = bbox[2] - bbox[0]
draw.text(((width-footer_w)//2, 1150), footer, fill='#666', font=font_text)

# 保存
img.save('openclaw-channel-architecture-v2.png', 'PNG', quality=95)
print('✅ OpenClaw Channel 架构图 v2 已保存')
