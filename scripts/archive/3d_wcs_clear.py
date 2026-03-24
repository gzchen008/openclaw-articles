#!/usr/bin/env python3
"""
3D Rotating WCS - Clear Text Version
文字清晰可辨的3D旋转版本
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

def project(x, y, z, d=8):
    if z + d <= 0:
        z = -d + 0.1
    f = d / (d + z)
    return x * f * 2.2, y * f * 1.1

# ANSI颜色
C_W = '\033[96m'  # 青色 W
C_C = '\033[93m'  # 黄色 C  
C_S = '\033[95m'  # 紫色 S
C_EDGE = '\033[90m'  # 灰色边框
C_RESET = '\033[0m'

def make_wcs():
    """生成WCS三个字母的3D结构"""
    objects = []  # (x, y, z, char, color)
    
    # ========== W ========== (青色)
    # W的主体结构 - 大写字母形状
    w_structure = [
        # 左竖
        (-13, -6), (-13, -4), (-13, -2), (-13, 0), (-13, 2), (-13, 4), (-13, 6),
        # 右竖
        (-3, -6), (-3, -4), (-3, -2), (-3, 0), (-3, 2), (-3, 4), (-3, 6),
        # V形中间
        (-11, -2), (-10, 0), (-9, 2), (-8, 3), (-7, 2), (-6, 0), (-5, -2),
        # 底部连接
        (-11, 3), (-10, 4), (-9, 4), (-8, 4), (-7, 4), (-6, 3),
        # 内部填充
        (-12, 0), (-11, 1), (-10, 2), (-8, 2), (-6, 1), (-4, 0),
    ]
    
    for x, y in w_structure:
        # 前面
        objects.append((x, y, 2, 'W', C_W))
        # 后面
        objects.append((x, y, -2, 'W', C_W))
    
    # W的边框连接线 (存储为元组: (p1, p2, char, color))
    for y in [-6, -2, 0, 2, 6]:
        objects.append(((-13, y, 2), (-13, y, -2), '|', C_EDGE))
        objects.append(((-3, y, 2), (-3, y, -2), '|', C_EDGE))
    
    # ========== C ========== (黄色)
    c_structure = []
    # 上半圆弧
    for angle in range(180, 361, 12):
        r = math.radians(angle)
        x = 2 + math.cos(r) * 6
        y = math.sin(r) * 7
        c_structure.append((x, y))
    # 右边
    c_structure.extend([(8, 6), (8, 2), (8, -2), (8, -6)])
    # 下半圆弧
    for angle in range(0, 181, 12):
        r = math.radians(angle)
        x = 2 + math.cos(r) * 6
        y = -7 + math.sin(r) * 7
        c_structure.append((x, y))
    # 内部
    c_structure.extend([(2, 3), (2, 0), (2, -3), (4, 4), (4, -4), (6, 0)])
    
    for x, y in c_structure:
        objects.append((x, y, 2, 'C', C_C))
        objects.append((x, y, -2, 'C', C_C))
    
    # C的边框
    for angle in [180, 225, 270, 315, 360]:
        r = math.radians(angle)
        x = 2 + math.cos(r) * 6
        y = math.sin(r) * 7 if angle <= 270 else -7
        objects.append(((x, y, 2), (x, y, -2), ':', C_EDGE))
    
    # ========== S ========== (紫色)
    s_structure = []
    # 顶部横
    for x in range(9, 17):
        s_structure.append((x, 7))
    # 上弧线
    for angle in range(90, 271, 15):
        r = math.radians(angle)
        x = 13 + math.cos(r) * 4
        y = 3 + math.sin(r) * 4
        s_structure.append((x, y))
    # 中间横
    for x in range(10, 16):
        s_structure.append((x, 0))
    # 下弧线
    for angle in range(-90, 91, 15):
        r = math.radians(angle)
        x = 13 + math.cos(r) * 4
        y = -3 + math.sin(r) * 4
        s_structure.append((x, y))
    # 底部横
    for x in range(9, 17):
        s_structure.append((x, -7))
    # 内部装饰
    s_structure.extend([(13, 5), (13, 2), (13, -2), (13, -5)])
    
    for x, y in s_structure:
        objects.append((x, y, 2, 'S', C_S))
        objects.append((x, y, -2, 'S', C_S))
    
    # S的边框
    for x in [9, 13, 17]:
        objects.append(((x, 7, 2), (x, 7, -2), ':', C_EDGE))
        objects.append(((x, -7, 2), (x, -7, -2), ':', C_EDGE))
    
    return objects

def draw_line_3d(p1, p2, screen, zbuf, char, color):
    """绘制3D线段"""
    (x1, y1, z1), (x2, y2, z2) = p1, p2
    
    # 投影
    px1, py1 = project(x1, y1, z1)
    px2, py2 = project(x2, y2, z2)
    
    x0, y0 = int(px1 + 40), int(py1 + 12)
    x1, y1 = int(px2 + 40), int(py2 + 12)
    
    dx, dy = abs(x1-x0), abs(y1-y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    
    while True:
        if 0 <= x0 < 80 and 0 <= y0 < 24:
            z = (z1 + z2) / 2
            if z > zbuf[y0][x0]:
                zbuf[y0][x0] = z
                screen[y0][x0] = (char, color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def main():
    objects = make_wcs()
    ax = ay = az = 0
    
    try:
        while True:
            clear()
            
            # 屏幕缓冲区: (字符, 颜色)
            screen = [[(' ', '') for _ in range(80)] for _ in range(24)]
            zbuf = [[-99 for _ in range(80)] for _ in range(24)]
            
            # 处理所有对象
            for obj in objects:
                # 区分点(5元素)和线段(4元素，第一个元素是元组)
                if isinstance(obj[0], tuple) and len(obj[0]) == 3 and len(obj) == 4:
                    # 点
                    x, y, z, char, color = obj
                    rx, ry, rz = rotate(x, y, z, ax, ay, az)
                    px, py = project(rx, ry, rz)
                    ix, iy = int(px + 40), int(py + 12)
                    
                    if 0 <= ix < 80 and 0 <= iy < 24:
                        if rz > zbuf[iy][ix]:
                            zbuf[iy][ix] = rz
                            # 根据深度调整字符大小写或选择
                            # 近处用大写，远处用小写，但保持同一字母
                            if rz > 2:
                                display_char = char  # 大写
                            elif rz > 0:
                                display_char = char.lower() if char != 'W' else 'w'
                            else:
                                display_char = char.lower() if char != 'W' else 'w'
                            screen[iy][ix] = (display_char, color)
                else:
                    # 线段
                    p1, p2, char, color = obj
                    # 旋转端点
                    x1, y1, z1 = p1
                    x2, y2, z2 = p2
                    rx1, ry1, rz1 = rotate(x1, y1, z1, ax, ay, az)
                    rx2, ry2, rz2 = rotate(x2, y2, z2, ax, ay, az)
                    draw_line_3d(((rx1, ry1, rz1), (rx2, ry2, rz2)), screen, zbuf, char, color)
            
            # 打印屏幕
            for row in screen:
                line = ""
                current_color = ""
                for char, color in row:
                    if color != current_color:
                        line += color
                        current_color = color
                    line += char
                if current_color:
                    line += C_RESET
                print(line)
            
            # 信息栏
            print(f"\n{C_W}    ★ 3D WCS 立体旋转{C_RESET}")
            print(f"    角度: X{math.degrees(ax)%360:.0f}° Y{math.degrees(ay)%360:.0f}° Z{math.degrees(az)%360:.0f}°")
            print(f"    {C_W}W{C_RESET} = 青色 | {C_C}C{C_RESET} = 黄色 | {C_S}S{C_RESET} = 紫色")
            print("    按 Ctrl+C 退出")
            
            ay += 0.04
            ax += 0.02
            
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        clear()
        print(f"\n{C_W}W{C_C}C{C_S}S{C_RESET} 再见!\n")

if __name__ == "__main__":
    main()
