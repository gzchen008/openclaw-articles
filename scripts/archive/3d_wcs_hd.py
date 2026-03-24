#!/usr/bin/env python3
"""
3D Rotating WCS - High Density Clear Letters
高密度清晰的 WCS 字母旋转
按 Ctrl+C 退出
"""

import math
import time
import os

def clear():
    print('\033[2J\033[H', end='')

def rotate(x, y, z, ax, ay, az):
    cx, sx = math.cos(ax), math.sin(ax)
    y, z = y*cx - z*sx, y*sx + z*cx
    cy, sy = math.cos(ay), math.sin(ay)
    x, z = x*cy + z*sy, -x*sy + z*cy
    cz, sz = math.cos(az), math.sin(az)
    x, y = x*cz - y*sz, x*sz + y*cz
    return x, y, z

def project(x, y, z, d=12):
    if z + d <= 0:
        z = -d + 0.1
    f = d / (d + z)
    return x * f * 1.8, y * f * 0.9

# 颜色
CW = '\033[96m'   # 青色 W
CC = '\033[93m'   # 黄色 C  
CS = '\033[95m'   # 紫色 S
CR = '\033[0m'

def get_letter_points():
    """生成WCS三个字母的所有点"""
    all_points = []
    
    # ===== W ===== 位置偏移 (-12, 0)
    w_offset = -12
    for y in range(-7, 8, 1):  # 左竖
        for dx in range(2):  # 加粗
            all_points.append((w_offset + dx, y, 'W', CW))
    for y in range(-7, 8, 1):  # 右竖
        for dx in range(2):
            all_points.append((w_offset + 8 + dx, y, 'W', CW))
    # V形
    v_points = [(2, -5), (3, -3), (4, -1), (5, 1), (6, 2), (7, 1), (8, -1), (9, -3), (10, -5)]
    for dx, dy in v_points:
        all_points.append((w_offset + dx, dy, 'W', CW))
    # 底部
    for x in range(2, 10):
        all_points.append((w_offset + x, 3, 'W', CW))
        all_points.append((w_offset + x, 4, 'W', CW))
    # 填充内部
    for y in range(-2, 4):
        for x in range(3, 9):
            all_points.append((w_offset + x, y, 'W', CW))
    
    # ===== C ===== 位置偏移 (0, 0)
    c_offset = 0
    # 上半圆
    for angle in range(180, 361, 5):
        r = math.radians(angle)
        x = c_offset + math.cos(r) * 6
        y = math.sin(r) * 7
        all_points.append((int(x), int(y), 'C', CC))
        all_points.append((int(x), int(y)+1, 'C', CC))  # 加粗
    # 下半圆
    for angle in range(0, 181, 5):
        r = math.radians(angle)
        x = c_offset + math.cos(r) * 6
        y = -7 + math.sin(r) * 7
        all_points.append((int(x), int(y), 'C', CC))
        all_points.append((int(x), int(y)-1, 'C', CC))
    # 右边竖线
    for y in range(-6, 7):
        all_points.append((c_offset + 6, y, 'C', CC))
        all_points.append((c_offset + 7, y, 'C', CC))
    # 内部填充
    for y in range(-5, 6):
        for x in range(0, 6):
            all_points.append((c_offset + x, y, 'C', CC))
    
    # ===== S ===== 位置偏移 (12, 0)
    s_offset = 12
    # 顶部
    for x in range(0, 10):
        all_points.append((s_offset + x, 7, 'S', CS))
        all_points.append((s_offset + x, 6, 'S', CS))
    # 上弧线
    for angle in range(90, 271, 8):
        r = math.radians(angle)
        x = s_offset + 5 + math.cos(r) * 4
        y = 3 + math.sin(r) * 4
        all_points.append((int(x), int(y), 'S', CS))
        all_points.append((int(x), int(y)+1, 'S', CS))
    # 中间横
    for x in range(1, 9):
        all_points.append((s_offset + x, 0, 'S', CS))
        all_points.append((s_offset + x, 1, 'S', CS))
    # 下弧线
    for angle in range(-90, 91, 8):
        r = math.radians(angle)
        x = s_offset + 5 + math.cos(r) * 4
        y = -3 + math.sin(r) * 4
        all_points.append((int(x), int(y), 'S', CS))
        all_points.append((int(x), int(y)-1, 'S', CS))
    # 底部
    for x in range(0, 10):
        all_points.append((s_offset + x, -7, 'S', CS))
        all_points.append((s_offset + x, -6, 'S', CS))
    # 内部填充
    for y in range(-5, 6):
        for x in range(1, 9):
            if y > 1 or y < -1 or (2 < x < 7):
                all_points.append((s_offset + x, y, 'S', CS))
    
    return all_points

def main():
    points = get_letter_points()
    
    # 去重
    unique = {}
    for x, y, ch, col in points:
        unique[(x, y)] = (ch, col)
    base_points = [(x, y, ch, col) for (x, y), (ch, col) in unique.items()]
    
    ax = ay = az = 0
    
    try:
        while True:
            clear()
            
            screen = [[(' ', '') for _ in range(80)] for _ in range(24)]
            zbuf = [[-99 for _ in range(80)] for _ in range(24)]
            
            # 为所有点创建前后两面并旋转
            all_pixels = []
            for x, y, ch, col in base_points:
                # 前面 z=2
                rx, ry, rz = rotate(x, y, 2, ax, ay, az)
                px, py = project(rx, ry, rz)
                all_pixels.append((px, py, rz, ch, col))
                
                # 后面 z=-2
                rx, ry, rz = rotate(x, y, -2, ax, ay, az)
                px, py = project(rx, ry, rz)
                all_pixels.append((px, py, rz, ch.lower(), col))
            
            # 按深度排序
            all_pixels.sort(key=lambda p: p[2])
            
            # 绘制
            for px, py, rz, ch, col in all_pixels:
                ix, iy = int(px + 40), int(py + 12)
                if 0 <= ix < 80 and 0 <= iy < 24:
                    if rz > zbuf[iy][ix]:
                        zbuf[iy][ix] = rz
                        screen[iy][ix] = (ch, col)
            
            # 打印
            for row in screen:
                line = ""
                cur = ""
                for ch, col in row:
                    if col != cur:
                        line += col
                        cur = col
                    line += ch
                if cur:
                    line += CR
                print(line)
            
            print(f"\n{CW}    ★ 3D WCS 立体旋转{CR}")
            print(f"    角度: X{math.degrees(ax)%360:.0f}° Y{math.degrees(ay)%360:.0f}° Z{math.degrees(az)%360:.0f}°")
            print(f"    {CW}WWWW{CR} | {CC}CCCC{CR} | {CS}SSSS{CR}")
            print("    按 Ctrl+C 退出")
            
            ay += 0.025
            ax += 0.008
            
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        clear()
        print(f"\n{CW}W{CC}C{CS}S{CR} 再见!\n")

if __name__ == "__main__":
    main()
