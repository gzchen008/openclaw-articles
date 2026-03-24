#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
珩珩满月宴邀请函生成器
"""

from PIL import Image, ImageDraw, ImageFont
import os

# 图片尺寸 (竖版，适合分享)
WIDTH = 800
HEIGHT = 1400
BG_COLOR = '#FFF5F5'  # 淡粉色背景

def hex_to_rgb(hex_color):
    """将十六进制颜色转换为 RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def draw_rounded_rect(draw, coords, radius, fill):
    """绘制圆角矩形"""
    x1, y1, x2, y2 = coords
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    draw.pieslice([x1, y1, x1 + 2*radius, y1 + 2*radius], 180, 270, fill=fill)
    draw.pieslice([x2 - 2*radius, y1, x2, y1 + 2*radius], 270, 360, fill=fill)
    draw.pieslice([x1, y2 - 2*radius, x1 + 2*radius, y2], 90, 180, fill=fill)
    draw.pieslice([x2 - 2*radius, y2 - 2*radius, x2, y2], 0, 90, fill=fill)

def get_font(size):
    """获取字体，优先使用 PingFang SC"""
    font_names = [
        'PingFang SC',
        'PingFang-SC-Regular',
        'Hiragino Sans GB',
        'STHeiti',
        'Arial Unicode MS',
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/STHeiti Light.ttc',
    ]
    
    for font_name in font_names:
        try:
            if font_name.startswith('/'):
                return ImageFont.truetype(font_name, size)
            else:
                return ImageFont.truetype(font_name, size)
        except:
            continue
    
    # 降级到默认字体
    return ImageFont.load_default()

def create_invitation():
    """创建邀请函图片"""
    # 创建图片
    img = Image.new('RGB', (WIDTH, HEIGHT), hex_to_rgb(BG_COLOR))
    draw = ImageDraw.Draw(img)
    
    # 字体
    title_font = get_font(48)
    subtitle_font = get_font(20)
    body_font = get_font(24)
    label_font = get_font(18)
    small_font = get_font(16)
    
    # 颜色
    pink = hex_to_rgb('#FF69B4')
    dark_pink = hex_to_rgb('#FF1493')
    gray = hex_to_rgb('#666666')
    light_pink = hex_to_rgb('#FFE4E1')
    
    y = 40
    
    # 标题
    title = "👶 珩珩满月宴"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = bbox[2] - bbox[0]
    draw.text(((WIDTH - title_width) // 2, y), title, fill=dark_pink, font=title_font)
    y += 60
    
    # 副标题
    subtitle = "FULL MOON CELEBRATION"
    bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = bbox[2] - bbox[0]
    draw.text(((WIDTH - subtitle_width) // 2, y), subtitle, fill=pink, font=subtitle_font)
    y += 50
    
    # 分隔线
    draw.rectangle([100, y, WIDTH - 100, y + 2], fill=light_pink)
    y += 30
    
    # 开场白
    greeting_lines = [
        "亲爱的家人们、朋友们：",
        "",
        "时光飞逝，转眼间我们的小宝贝",
        "珩珩 已经满月啦！🎉",
        "",
        "感谢这一个月来大家的关心与祝福，",
        "小珩珩在满满的爱意中健康成长，",
        "每天都给我们带来新的惊喜和快乐～",
        "",
        "为庆祝这个特别的日子，",
        "我们诚挚地邀请您一起来分享这份喜悦！"
    ]
    
    for line in greeting_lines:
        bbox = draw.textbbox((0, 0), line, font=body_font)
        line_width = bbox[2] - bbox[0]
        draw.text(((WIDTH - line_width) // 2, y), line, fill=gray, font=body_font)
        y += 32
    
    y += 20
    
    # 宴会信息卡片
    card_y = y
    card_height = 140
    draw_rounded_rect(draw, [50, card_y, WIDTH - 50, card_y + card_height], 20, hex_to_rgb('#FFFFFF'))
    
    # 时间
    info_y = card_y + 25
    draw.text((80, info_y), "📅 时间", fill=pink, font=label_font)
    draw.text((200, info_y), "2026年3月25日（周三）18:30", fill=gray, font=label_font)
    
    # 地点
    info_y += 40
    draw.text((80, info_y), "📍 地点", fill=pink, font=label_font)
    draw.text((200, info_y), "阜沙卫民市场旁 贵福西上街 42号", fill=gray, font=label_font)
    
    y = card_y + card_height + 30
    
    # 宝宝小档案
    baby_card_y = y
    baby_card_height = 120
    draw_rounded_rect(draw, [50, baby_card_y, WIDTH - 50, baby_card_y + baby_card_height], 20, light_pink)
    
    draw.text((80, baby_card_y + 15), "👶 宝宝小档案", fill=dark_pink, font=label_font)
    
    baby_info_y = baby_card_y + 50
    baby_items = [
        ("💝", "小名：珩珩"),
        ("👦", "性别：男宝"),
        ("💕", "特点：像爸爸妈妈")
    ]
    
    item_x = 100
    for icon, text in baby_items:
        draw.text((item_x, baby_info_y), f"{icon} {text}", fill=gray, font=small_font)
        item_x += 230
    
    y = baby_card_y + baby_card_height + 30
    
    # 宴会亮点
    draw.text((80, y), "✨ 宴会亮点", fill=dark_pink, font=label_font)
    y += 35
    
    highlights = [
        ("📸", "留影区", "记录与珩珩的美好瞬间"),
        ("🍬", "零食区", "大小朋友都能享受的美味")
    ]
    
    for icon, title, desc in highlights:
        draw.text((100, y), f"{icon} {title}", fill=pink, font=label_font)
        draw.text((100, y + 25), f"   {desc}", fill=gray, font=small_font)
        y += 60
    
    y += 10
    
    # 温馨提示
    draw.text((80, y), "💕 温馨提示", fill=dark_pink, font=label_font)
    y += 35
    
    tips = [
        "• 宴会设有宝宝专区，欢迎带小朋友一起来玩",
        "• 如有饮食禁忌，请提前告知我们"
    ]
    
    for tip in tips:
        draw.text((100, y), tip, fill=gray, font=small_font)
        y += 28
    
    y += 30
    
    # 结尾
    closing = "期待与您相聚，一起见证珩珩的成长！"
    bbox = draw.textbbox((0, 0), closing, font=body_font)
    closing_width = bbox[2] - bbox[0]
    draw.text(((WIDTH - closing_width) // 2, y), closing, fill=pink, font=body_font)
    y += 40
    
    # 署名
    signature = "👶 珩珩一家 敬邀"
    bbox = draw.textbbox((0, 0), signature, font=label_font)
    sig_width = bbox[2] - bbox[0]
    draw.text(((WIDTH - sig_width) // 2, y), signature, fill=gray, font=label_font)
    
    # 保存图片
    output_path = os.path.expanduser('~/.openclaw/workspace/hengheng-invitation.png')
    img.save(output_path, 'PNG', quality=95)
    print(f"✅ 邀请函已生成: {output_path}")
    return output_path

if __name__ == '__main__':
    create_invitation()
