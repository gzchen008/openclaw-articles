#!/usr/bin/env python3
"""
3D Rotating WCS Text with Shape
按 Ctrl+C 退出
"""

import math
import time
import os
import sys

# ANSI 颜色代码
COLORS = {
    'reset': '\033[0m',
    'red': '\033[91m',
    'green': '\033[92m', 
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'bold': '\033[1m'
}

def clear_screen():
    print('\033[2J\033[H', end='')

def rotate_point(x, y, z, angle_x, angle_y, angle_z):
    # 绕 X 轴旋转
    cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)
    y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x
    
    # 绕 Y 轴旋转
    cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
    x, z = x * cos_y + z * sin_y, -x * sin_y + z * cos_y
    
    # 绕 Z 轴旋转
    cos_z, sin_z = math.cos(angle_z), math.sin(angle_z)
    x, y = x * cos_z - y * sin_z, x * sin_z + y * cos_z
    
    return x, y, z

def project(x, y, z, distance=6):
    """透视投影"""
    if z + distance <= 0:
        z = -distance + 0.1
    factor = distance / (distance + z)
    return x * factor * 2.2, y * factor * 1.1

# 改进的 7x9 字体 - 更美观的 W、C、S
FONT = {
    'W': [
        # 外框
        (0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),
        (6,0),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7),(6,8),
        # 中间V形
        (1,7),(2,6),(3,5),(4,6),(5,7),
        # 底部横线
        (0,8),(1,8),(2,8),(3,8),(4,8),(5,8),(6,8),
        # 内部填充点增加立体感
        (0,4),(6,4),(3,6),
    ],
    'C': [
        # 上半圆弧
        (1,0),(2,0),(3,0),(4,0),(5,0),
        (0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),
        # 下半圆弧  
        (1,8),(2,8),(3,8),(4,8),(5,8),
        (6,1),(6,7),
        # 内部点
        (1,2),(1,6),(5,2),(5,6),(3,4),
    ],
    'S': [
        # 顶部横
        (1,0),(2,0),(3,0),(4,0),(5,0),(6,0),
        # 上半部分
        (0,1),(0,2),(0,3),(1,3),(2,3),(3,3),(4,3),
        (5,4),(6,5),(6,6),
        # 下半部分
        (5,7),(4,8),(3,8),(2,8),(1,8),(0,7),(0,6),
        # 中间连接线
        (3,4),(3,5),(2,5),(4,4),
        # 内部点
        (2,1),(4,1),(3,6),(1,7),(5,2),
    ]
}

def get_text_points(text="WCS"):
    """生成3D文字点云，添加厚度"""
    points = []
    colors = []
    x_offset = -(len(text) * 9) / 2
    
    color_map = [COLORS['cyan'], COLORS['magenta'], COLORS['yellow']]
    
    for i, char in enumerate(text.upper()):
        if char in FONT:
            base_color = color_map[i % len(color_map)]
            # 为每个字符创建多层厚度
            for layer in range(3):  # 3层厚度
                z = layer * 1.5 - 1.5  # -1.5, 0, 1.5
                for x, y in FONT[char]:
                    px = x + x_offset + i * 9
                    py = y - 4
                    # 添加一些随机点让形状更立体
                    points.append((px, py, z))
                    colors.append(base_color)
                    
            # 添加连接前后的边线点
            for x, y in FONT[char]:
                if (x, y) in [(0,0), (3,4), (6,8)]:  # 关键点
                    for z in [-1.5, 1.5]:
                        px = x + x_offset + i * 9
                        py = y - 4
                        points.append((px, py, z))
                        colors.append(COLORS['white'])
    
    return points, colors

def draw_line(x0, y0, x1, y1, screen, z_buffer, char='*', z=0):
    """Bresenham 画线算法"""
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    
    while True:
        if 0 <= x0 < 80 and 0 <= y0 < 24:
            if z > z_buffer[y0][x0]:
                z_buffer[y0][x0] = z
                screen[y0][x0] = char
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def render(points, colors, angle_x, angle_y, angle_z, frame):
    """渲染旋转后的3D文字"""
    width, height = 80, 24
    screen = [[' ' for _ in range(width)] for _ in range(height)]
    z_buffer = [[-float('inf') for _ in range(width)] for _ in range(height)]
    color_buffer = [['' for _ in range(width)] for _ in range(height)]
    
    rotated_points = []
    
    # 旋转所有点
    for (x, y, z), color in zip(points, colors):
        rx, ry, rz = rotate_point(x, y, z, angle_x, angle_y, angle_z)
        px, py = project(rx, ry, rz)
        rotated_points.append((px, py, rz, color))
    
    # 按深度排序（从远到近）
    rotated_points.sort(key=lambda p: p[2])
    
    # 绘制点
    for px, py, rz, color in rotated_points:
        ix, iy = int(px + width/2), int(py + height/2)
        if 0 <= ix < width and 0 <= iy < height:
            if rz > z_buffer[iy][ix]:
                z_buffer[iy][ix] = rz
                # 根据深度选择字符
                if rz > 2:
                    char = '@'
                elif rz > 0:
                    char = 'O'
                elif rz > -2:
                    char = 'o'
                else:
                    char = '.'
                screen[iy][ix] = char
                color_buffer[iy][ix] = color
    
    # 添加发光效果 - 在亮点周围添加暗淡的点
    glow_screen = [row[:] for row in screen]
    for y in range(1, height-1):
        for x in range(1, width-1):
            if screen[y][x] in ['@', 'O']:
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nx, ny = x+dx, y+dy
                    if screen[ny][nx] == ' ':
                        glow_screen[ny][nx] = '·'
                        color_buffer[ny][nx] = COLORS['blue']
    
    return glow_screen, color_buffer

def main():
    text = "WCS"
    points, colors = get_text_points(text)
    
    angle_x, angle_y, angle_z = 0, 0, 0
    frame = 0
    
    try:
        while True:
            clear_screen()
            
            # 渲染
            screen, color_buffer = render(points, colors, angle_x, angle_y, angle_z, frame)
            
            # 打印带颜色的画面
            for y, (row, color_row) in enumerate(zip(screen, color_buffer)):
                line = ""
                current_color = ""
                for x, (char, color) in enumerate(zip(row, color_row)):
                    if color and color != current_color:
                        line += color
                        current_color = color
                    line += char
                if current_color:
                    line += COLORS['reset']
                print(line)
            
            # 底部信息
            print(f"\n{COLORS['green']}  ★ 3D Rotating: {COLORS['bold']}{text}{COLORS['reset']}")
            print(f"{COLORS['cyan']}  ↺ X:{math.degrees(angle_x)%360:.0f}° Y:{math.degrees(angle_y)%360:.0f}° Z:{math.degrees(angle_z)%360:.0f}°{COLORS['reset']}")
            print(f"{COLORS['yellow']}  按 Ctrl+C 退出{COLORS['reset']}")
            
            # 更新旋转角度 - 更流畅的旋转
            angle_y += 0.06  # 主要绕Y轴旋转
            angle_x += 0.02  # 轻微X轴旋转
            angle_z += 0.01  # 轻微Z轴旋转
            
            frame += 1
            time.sleep(0.04)
            
    except KeyboardInterrupt:
        clear_screen()
        print(f"\n{COLORS['green']}再见！{COLORS['reset']}\n")

if __name__ == "__main__":
    main()
