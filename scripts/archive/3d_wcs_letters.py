#!/usr/bin/env python3
"""
3D Rotating WCS - Clear Letter Shapes
清晰的 W C S 三个大写字母旋转
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

def project(x, y, z, d=10):
    if z + d <= 0:
        z = -d + 0.1
    f = d / (d + z)
    return x * f * 2.0, y * f * 1.0

# 颜色
CW = '\033[96m'   # 青色
CC = '\033[93m'   # 黄色  
CS = '\033[95m'   # 紫色
CR = '\033[0m'

def create_letter_W():
    """创建清晰的W字母形状"""
    points = []
    # W的结构：两竖 + 中间V
    # 左竖
    for y in range(-8, 9):
        points.append((-14, y, 'W'))
    # 右竖
    for y in range(-8, 9):
        points.append((-4, y, 'W'))
    # V的左边
    points.extend([(-12, -4), (-10, -1), (-8, 2)])
    # V的右边
    points.extend([(-6, 2), (-5, -1), (-3, -4)])
    # 底部连接
    for x in range(-12, -3):
        points.append((x, 4))
    # 内部填充
    for y in range(-4, 5):
        for x in range(-13, -5):
            if abs(x + 9) + abs(y) < 6:
                points.append((x, y))
    return [(-14 + i % 5, -8 + i // 5) for i in range(90) if abs((-14 + i % 5) + 9) + abs(-8 + i // 5 - 2) < 8]

def make_clear_W():
    """清晰的W形状"""
    pts = []
    # 左竖线
    for y in range(-8, 9):
        pts.append((-13, y))
    # 右竖线
    for y in range(-8, 9):
        pts.append((-3, y))
    # 左斜线
    pts.extend([(-11, -4), (-10, -2), (-9, 0)])
    # 右斜线
    pts.extend([(-7, 0), (-6, -2), (-5, -4)])
    # 底部
    pts.extend([(-11, 3), (-10, 4), (-9, 4), (-8, 4), (-7, 4), (-6, 3)])
    # 填充内部点让形状更实
    for y in range(-3, 5):
        for x in range(-12, -4):
            if -12 <= x <= -4 and -3 <= y <= 4:
                if not (x == -8 and y > 0):  # V形缺口
                    pts.append((x, y))
    return list(set(pts))

def make_clear_C():
    """清晰的C形状"""
    pts = []
    # 上半圆
    for angle in range(180, 361, 10):
        r = math.radians(angle)
        x = 2 + math.cos(r) * 7
        y = math.sin(r) * 8
        pts.append((int(x), int(y)))
    # 右边
    for y in range(8, -9, -1):
        pts.append((9, y))
    # 下半圆
    for angle in range(0, 181, 10):
        r = math.radians(angle)
        x = 2 + math.cos(r) * 7
        y = -8 + math.sin(r) * 8
        pts.append((int(x), int(y)))
    # 内部填充
    for y in range(-6, 7):
        for x in range(0, 8):
            if (x-2)**2/36 + y**2/64 <= 0.6:
                pts.append((x, y))
    return list(set(pts))

def make_clear_S():
    """清晰的S形状"""
    pts = []
    # 顶部横
    for x in range(8, 18):
        pts.append((x, 8))
    # 上弧线
    for angle in range(90, 271, 15):
        r = math.radians(angle)
        x = 13 + math.cos(r) * 4
        y = 4 + math.sin(r) * 4
        pts.append((int(x), int(y)))
    # 中间横
    for x in range(9, 17):
        pts.append((x, 0))
    # 下弧线
    for angle in range(-90, 91, 15):
        r = math.radians(angle)
        x = 13 + math.cos(r) * 4
        y = -4 + math.sin(r) * 4
        pts.append((int(x), int(y)))
    # 底部横
    for x in range(8, 18):
        pts.append((x, -8))
    # 内部填充
    for x in range(9, 17):
        for y in [-6, -2, 2, 6]:
            pts.append((x, y))
    return list(set(pts))

def main():
    # 获取字母形状
    w_shape = make_clear_W()
    c_shape = make_clear_C()
    s_shape = make_clear_S()
    
    ax = ay = az = 0
    
    try:
        while True:
            clear()
            
            # 屏幕缓冲区
            screen = [[(' ', '') for _ in range(80)] for _ in range(24)]
            zbuf = [[-99 for _ in range(80)] for _ in range(24)]
            
            # 三个字母的配置: (形状点列表, 字符, 颜色)
            letters = [
                (w_shape, 'W', CW),
                (c_shape, 'C', CC), 
                (s_shape, 'S', CS)
            ]
            
            all_points = []
            
            # 为每个字母创建前后两面
            for shape, char, color in letters:
                for x, y in shape:
                    # 前面 (z=3)
                    all_points.append((x, y, 3, char, color))
                    # 后面 (z=-3)
                    all_points.append((x, y, -3, char.lower(), color))
            
            # 旋转所有点
            rotated = []
            for x, y, z, ch, col in all_points:
                rx, ry, rz = rotate(x, y, z, ax, ay, az)
                px, py = project(rx, ry, rz)
                rotated.append((px, py, rz, ch, col))
            
            # 按深度排序（远的先画）
            rotated.sort(key=lambda p: p[2])
            
            # 绘制到屏幕
            for px, py, rz, ch, col in rotated:
                ix, iy = int(px + 40), int(py + 12)
                if 0 <= ix < 80 and 0 <= iy < 24:
                    if rz > zbuf[iy][ix]:
                        zbuf[iy][ix] = rz
                        screen[iy][ix] = (ch, col)
            
            # 打印
            for row in screen:
                line = ""
                cur_color = ""
                for ch, col in row:
                    if col and col != cur_color:
                        line += col
                        cur_color = col
                    line += ch
                if cur_color:
                    line += CR
                print(line)
            
            # 信息
            print(f"\n{CW}    ★ 3D WCS 立体旋转{CR}")
            print(f"    角度: X{math.degrees(ax)%360:.0f}° Y{math.degrees(ay)%360:.0f}° Z{math.degrees(az)%360:.0f}°")
            print(f"    {CW}W{CR} = 青色(大写近/小写远) | {CC}C{CR} = 黄色 | {CS}S{CR} = 紫色")
            print("    按 Ctrl+C 退出")
            
            ay += 0.03
            ax += 0.01
            
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        clear()
        print(f"\n{CW}W{CC}C{CS}S{CR} 再见!\n")

if __name__ == "__main__":
    main()
