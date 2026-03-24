#!/usr/bin/env python3
"""手绘风格流程图 - OpenClaw 上下文加载顺序"""

from PIL import Image, ImageDraw, ImageFont
import random

# 创建画布
width, height = 1200, 900
img = Image.new('RGB', (width, height), 'white')
draw = ImageDraw.Draw(img)

# 尝试加载字体（系统字体）
try:
    # macOS 中文字体（支持中文和英文）
    font_title = ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', 32)
    font_subtitle = ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', 20)
    font_file = ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', 16)
    font_desc = ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', 12)
    font_note = ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', 18)
except:
    # 使用默认字体
    font_title = ImageFont.load_default()
    font_subtitle = ImageFont.load_default()
    font_file = ImageFont.load_default()
    font_desc = ImageFont.load_default()
    font_note = ImageFont.load_default()

def sketchy_rect(x, y, w, h, color, text):
    """手绘风格方框"""
    # 填充
    fill_colors = {
        'green': '#d5f4e6',
        'blue': '#d6eaf8',
        'yellow': '#fdebd0',
        'gray': '#ecf0f1',
        'orange': '#fdebd0'
    }
    fill = fill_colors.get(color, '#f0f0f0')
    draw.rectangle([x, y, x+w, y+h], fill=fill, outline=color, width=3)
    
    # 文字
    bbox = draw.textbbox((0, 0), text, font=font_file)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    draw.text((x + (w-text_w)//2, y + (h-text_h)//2 - 2), text, fill='#333', font=font_file)

def draw_arrow(x1, y1, x2, y2):
    """绘制箭头"""
    draw.line([x1, y1, x2, y2], fill='#666', width=2)
    # 箭头头部
    draw.polygon([(x2, y2), (x2-6, y2-8), (x2+6, y2-8)], fill='#666')

def draw_check_mark(x, y):
    """绿色对勾"""
    draw.line([x-10, y, x-3, y+10], fill='#27ae60', width=4)
    draw.line([x-3, y+10, x+12, y-10], fill='#27ae60', width=4)

def draw_cross_mark(x, y):
    """红色叉号"""
    draw.line([x-8, y-8, x+8, y+8], fill='#e74c3c', width=3)
    draw.line([x+8, y-8, x-8, y+8], fill='#e74c3c', width=3)

def draw_stick_figure(x, y):
    """简笔画小人"""
    # 头
    draw.ellipse([x-20, y-20, x+20, y+20], outline='#333', width=2)
    # 眼睛
    draw.ellipse([x-9, y-7, x-5, y-3], fill='#333')
    draw.ellipse([x+5, y-7, x+9, y-3], fill='#333')
    # 嘴巴
    draw.arc([x-8, y, x+8, y+10], 0, 180, fill='#333', width=2)
    # 身体
    draw.line([x, y+20, x, y+60], fill='#333', width=2)
    # 手臂
    draw.line([x-25, y+35, x+25, y+35], fill='#333', width=2)
    # 腿
    draw.line([x, y+60, x-15, y+90], fill='#333', width=2)
    draw.line([x, y+60, x+15, y+90], fill='#333', width=2)

def draw_robot(x, y):
    """机器人小人"""
    # 头（方形）
    draw.rectangle([x-20, y-20, x+20, y+20], outline='#333', width=2)
    # 眼睛
    draw.ellipse([x-9, y-7, x-5, y-3], fill='#333')
    draw.ellipse([x+5, y-7, x+9, y-3], fill='#333')
    # 嘴巴
    draw.line([x-8, y+8, x+8, y+8], fill='#333', width=2)
    # 天线
    draw.line([x, y-20, x, y-35], fill='#333', width=2)
    draw.ellipse([x-5, y-40, x+5, y-30], fill='#e74c3c')
    # 身体
    draw.rectangle([x-15, y+25, x+15, y+65], outline='#333', width=2)
    # 手臂
    draw.line([x-30, y+35, x-15, y+35], fill='#333', width=2)
    draw.line([x+15, y+35, x+30, y+35], fill='#333', width=2)
    # 腿
    draw.rectangle([x-12, y+65, x-4, y+90], outline='#333', width=2)
    draw.rectangle([x+4, y+65, x+12, y+90], outline='#333', width=2)

# 主标题
title = 'OpenClaw 上下文加载顺序 📋'
bbox = draw.textbbox((0, 0), title, font=font_title)
title_w = bbox[2] - bbox[0]
draw.text(((width-title_w)//2, 15), title, fill='#2c3e50', font=font_title)

# 中间分隔线
draw.line([600, 80, 600, 820], fill='#bdc3c7', width=2)

# ========== 左侧：主智能体 ==========
draw.text((260, 75), '主智能体 👤', fill='#3498db', font=font_subtitle)
draw_stick_figure(300, 160)

# 左侧文件列表
left_files = [
    ('AGENTS.md', 'green', '(全体通用指令)'),
    ('SOUL.md', 'blue', '(人格·规则·关系)'),
    ('TOOLS.md', 'green', '(工具定义)'),
    ('IDENTITY.md', 'yellow', '(自我介绍)'),
    ('USER.md', 'yellow', '(用户信息)'),
    ('HEARTBEAT.md', 'gray', '(定期检查)'),
    ('memory/*.md', 'orange', '(记忆)')
]

y = 270
for i, (name, color, desc) in enumerate(left_files):
    sketchy_rect(200, y, 200, 45, color, name)
    draw.text((410, y+15), desc, fill='#666', font=font_desc)
    
    if i < len(left_files) - 1:
        draw_arrow(300, y+45, 300, y+65)
    
    y += 75

# ========== 右侧：子智能体 ==========
draw.text((860, 75), '子智能体 🤖', fill='#e74c3c', font=font_subtitle)
draw_robot(900, 160)

# 右侧加载的文件
right_files = ['AGENTS.md', 'TOOLS.md']
y = 270
for i, name in enumerate(right_files):
    sketchy_rect(800, y, 200, 45, 'green', name)
    draw_check_mark(1020, y+22)
    
    if i < len(right_files) - 1:
        draw_arrow(900, y+45, 900, y+65)
    
    y += 75

# 不加载部分
y += 20
draw.text((800, y), '❌ 不加载:', fill='#e74c3c', font=font_file)
y += 35

crossed_files = ['SOUL.md', 'IDENTITY.md', 'memory/']
for name in crossed_files:
    draw.text((820, y-5), name, fill='#bdc3c7', font=font_file)
    # 划线
    text_len = len(name) * 10
    draw.line([815, y-8, 815+text_len, y-8], fill='#e74c3c', width=2)
    # 红叉
    draw_cross_mark(815+text_len+30, y-5)
    y += 35

# 底部说明
note = '💡 子智能体不注入人格(SOUL)'
bbox = draw.textbbox((0, 0), note, font=font_note)
note_w = bbox[2] - bbox[0]
note_x = (width - note_w) // 2

# 背景框
padding = 15
draw.rectangle(
    [note_x - padding, 800, note_x + note_w + padding, 850],
    fill='#ffebee', outline='#e74c3c', width=3
)
draw.text((note_x, 815), note, fill='#c0392b', font=font_note)

# 保存
img.save('openclaw-context-loading.png', 'PNG', quality=95)
print('✅ 流程图已保存为 openclaw-context-loading.png')
