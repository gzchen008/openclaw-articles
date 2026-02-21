#!/usr/bin/env python3
"""生成智能家居文章的三张图片"""

from PIL import Image, ImageDraw, ImageFont
import os

# 图片尺寸
WIDTH = 1080
HEIGHT = 1080

# 颜色方案
COLORS = {
    1: {"gradient": [(102, 126, 234), (118, 75, 162)]},
    2: {"gradient": [(240, 147, 251), (245, 87, 108)]},
    3: {"gradient": [(79, 172, 254), (0, 242, 254)]},
}

def create_gradient_background(width, height, color1, color2):
    """创建渐变背景"""
    img = Image.new('RGBA', (width, height))
    pixels = img.load()
    for y in range(height):
        r = int(color1[0] + (color2[0] - color1[0]) * y / height)
        g = int(color1[1] + (color2[1] - color1[1]) * y / height)
        b = int(color1[2] + (color2[2] - color1[2]) * y / height)
        for x in range(width):
            pixels[x, y] = (r, g, b, 255)
    return img

def get_font(size):
    """获取字体"""
    try:
        return ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", size)
    except:
        return ImageFont.load_default()

def draw_rounded_rect(overlay, bbox, radius, fill):
    """绘制圆角矩形"""
    x1, y1, x2, y2 = bbox
    draw = ImageDraw.Draw(overlay)
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    draw.ellipse([x1, y1, x1 + radius * 2, y1 + radius * 2], fill=fill)
    draw.ellipse([x2 - radius * 2, y1, x2, y1 + radius * 2], fill=fill)
    draw.ellipse([x1, y2 - radius * 2, x1 + radius * 2, y2], fill=fill)
    draw.ellipse([x2 - radius * 2, y2 - radius * 2, x2, y2], fill=fill)

def create_card(card_num, subtitle, title, items):
    """创建卡片"""
    colors = COLORS[card_num]
    img = create_gradient_background(WIDTH, HEIGHT, colors["gradient"][0], colors["gradient"][1])
    draw = ImageDraw.Draw(img)

    # 字体
    font_subtitle = get_font(48)
    font_title = get_font(72)
    font_item_title = get_font(40)
    font_item_desc = get_font(30)

    # 副标题
    draw.text((80, 80), subtitle, font=font_subtitle, fill=(255, 255, 255, 230))

    # 主标题（分两行）
    if len(title) > 8:
        mid = len(title) // 2
        draw.text((80, 160), title[:mid], font=font_title, fill=(255, 255, 255))
        draw.text((80, 250), title[mid:], font=font_title, fill=(255, 255, 255))
        start_y = 380
    else:
        draw.text((80, 160), title, font=font_title, fill=(255, 255, 255))
        start_y = 300

    # 项目列表
    y = start_y
    item_height = 140
    for item_title, item_desc in items:
        # 创建半透明覆盖层
        overlay = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
        draw_rounded_rect(overlay, [80, y, 1000, y + item_height], 20, (255, 255, 255, 50))

        # 合并图层
        img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img)

        # 标题
        draw.text((120, y + 20), item_title, font=font_item_title, fill=(255, 255, 255))

        # 描述
        draw.text((120, y + 80), item_desc, font=font_item_desc, fill=(255, 255, 255, 220))

        y += item_height + 30

    return img

def main():
    """生成三张图片"""
    output_dir = "/Users/cgz/.openclaw/workspace/articles"

    # 卡片1
    print("生成图片 1/3...")
    items1 = [
        ("🗣️ 自然语言控制", "说什么都能听懂，不再受固定指令限制"),
        ("🤖 智能场景推荐", "AI 根据你的习惯，自动设计自动化规则"),
        ("🏠 统一管理", "一个入口控制所有品牌设备"),
        ("💡 主动建议", "AI 会主动提出优化方案，省电又省心"),
    ]
    img1 = create_card(1, "OpenClaw 智能家居", "为什么需要AI + 智能家居？", items1)
    img1.save(os.path.join(output_dir, "smart-home-card-1.png"), "PNG")
    print("✅ smart-home-card-1.png")

    # 卡片2
    print("生成图片 2/3...")
    items2 = [
        ("1️⃣ 安装 Home Assistant", "Docker 一键部署，或用树莓派"),
        ("2️⃣ 接入智能设备", "支持 2000+ 设备，小米/涂鸦都行"),
        ("3️⃣ 配置 OpenClaw", "通过 REST API 或 Skills 封装"),
        ("4️⃣ 创建智能场景", "回家模式、睡眠模式、电影模式"),
        ("5️⃣ 开始语音控制", "说一句话，全屋响应"),
    ]
    img2 = create_card(2, "5 分钟上手", "配置步骤", items2)
    img2.save(os.path.join(output_dir, "smart-home-card-2.png"), "PNG")
    print("✅ smart-home-card-2.png")

    # 卡片3
    print("生成图片 3/3...")
    items3 = [
        ("🎤 语音控制", "早上好 → 打开窗帘、启动咖啡机"),
        ("📊 能耗监控", "「这个月电费多少？」AI 帮你分析"),
        ("🔔 智能提醒", "检测暴雨自动关窗，会议前唤醒"),
        ("🌍 远程控制", "出差在外也能控制家里设备"),
    ]
    img3 = create_card(3, "进阶玩法", "更多可能", items3)
    img3.save(os.path.join(output_dir, "smart-home-card-3.png"), "PNG")
    print("✅ smart-home-card-3.png")

    print("\n🎉 三张图片生成完成！")

if __name__ == "__main__":
    main()
