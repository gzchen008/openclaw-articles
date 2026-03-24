#!/usr/bin/env python3
"""
3D Rotating WCS - High Quality Version
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

def project(x, y, z, d=6):
    if z + d <= 0:
        z = -d + 0.1
    f = d / (d + z)
    return x * f * 2.8, y * f * 1.4

def draw_line(x0, y0, x1, y1, screen, zbuf, z, chars):
    """Bresenham画线，带深度"""
    dx, dy = abs(x1-x0), abs(y1-y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    
    while True:
        if 0 <= x0 < 80 and 0 <= y0 < 24:
            if z > zbuf[y0][x0]:
                zbuf[y0][x0] = z
                screen[y0][x0] = chars[min(int((z+3)*1.5), len(chars)-1)]
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def make_letter_points():
    """生成WCS三个字母的3D点阵"""
    points = []
    lines = []
    
    # ========== W ==========
    w_left = [(-13, y) for y in range(-7, 8, 1)]
    w_right = [(-3, y) for y in range(-7, 8, 1)]
    w_v_left = [(-11, -3), (-9, -1), (-8, 1)]
    w_v_right = [(-7, 1), (-6, -1), (-4, -3)]
    w_bottom = [(-11, 3), (-9, 4), (-7, 4), (-5, 3)]
    
    w_all = w_left + w_right + w_v_left + w_v_right + w_bottom
    
    # W的前后表面
    for x, y in w_all:
        points.append((x, y, 2.5, 'W'))
        points.append((x, y, -2.5, 'W'))
    
    # W的连接边
    for x, y in w_left + w_right:
        lines.append(((x, y, 2.5), (x, y, -2.5)))
    
    # ========== C ==========
    c_points = []
    # 上半圆弧
    for a in range(180, 361, 10):
        r = math.radians(a)
        c_points.append((2 + math.cos(r)*6, math.sin(r)*7))
    # 直边
    c_points.extend([(8, y) for y in range(6, -7, -1)])
    # 下半圆弧
    for a in range(0, 181, 10):
        r = math.radians(a)
        c_points.append((2 + math.cos(r)*6, -7 + math.sin(r)*7))
    # 内弧
    for a in range(0, 361, 15):
        r = math.radians(a)
        c_points.append((2 + math.cos(r)*3, math.sin(r)*4))
    
    for x, y in c_points:
        points.append((x, y, 2.5, 'C'))
        points.append((x, y, -2.5, 'C'))
    
    for a in range(180, 361, 20):
        r = math.radians(a)
        x, y = 2 + math.cos(r)*6, math.sin(r)*7
        lines.append(((x, y, 2.5), (x, y, -2.5)))
    
    # ========== S ==========
    s_points = []
    # 顶部
    s_points.extend([(x, 7) for x in range(9, 17)])
    # 上弧
    for a in range(90, 271, 10):
        r = math.radians(a)
        s_points.append((13 + math.cos(r)*3.5, 3.5 + math.sin(r)*3.5))
    # 中间
    s_points.extend([(x, 0) for x in range(10, 16)])
    # 下弧
    for a in range(-90, 91, 10):
        r = math.radians(a)
        s_points.append((13 + math.cos(r)*3.5, -3.5 + math.sin(r)*3.5))
    # 底部
    s_points.extend([(x, -7) for x in range(9, 17)])
    # 内部装饰
    s_points.extend([(13, 5), (13, 2), (13, -2), (13, -5), (15, 0), (11, 0)])
    
    for x, y in s_points:
        points.append((x, y, 2.5, 'S'))
        points.append((x, y, -2.5, 'S'))
    
    for x in [9, 13, 17]:
        lines.append(((x, 7, 2.5), (x, 7, -2.5)))
        lines.append(((x, -7, 2.5), (x, -7, -2.5)))
    
    return points, lines

def main():
    points, lines = make_letter_points()
    ax = ay = az = 0
    
    # 字符集：从近到远
    chars_W = ['@', 'W', 'M', 'O', 'o', '+', '=', '-', '.', ' ']
    chars_C = ['@', 'C', 'D', '0', 'c', '+', '=', '-', '.', ' ']
    chars_S = ['@', 'S', '$', '5', 's', '+', '=', '-', '.', ' ']
    
    try:
        while True:
            clear()
            
            screen = [[' ' for _ in range(80)] for _ in range(24)]
            zbuf = [[-99 for _ in range(80)] for _ in range(24)]
            
            # 绘制边（前后连接）
            for (x1, y1, z1), (x2, y2, z2) in lines:
                rx1, ry1, rz1 = rotate(x1, y1, z1, ax, ay, az)
                rx2, ry2, rz2 = rotate(x2, y2, z2, ax, ay, az)
                px1, py1 = project(rx1, ry1, rz1)
                px2, py2 = project(rx2, ry2, rz2)
                
                z_mid = (rz1 + rz2) / 2
                if z_mid > -4:
                    draw_line(int(px1+40), int(py1+12), int(px2+40), int(py2+12), 
                             screen, zbuf, z_mid, ['|', ':', '.'])
            
            # 绘制点
            for x, y, z, letter in points:
                rx, ry, rz = rotate(x, y, z, ax, ay, az)
                px, py = project(rx, ry, rz)
                ix, iy = int(px + 40), int(py + 12)
                
                if 0 <= ix < 80 and 0 <= iy < 24:
                    if rz > zbuf[iy][ix]:
                        zbuf[iy][ix] = rz
                        
                        # 根据深度选择字符
                        idx = min(max(int((rz + 4) * 1.2), 0), 9)
                        if letter == 'W':
                            screen[iy][ix] = chars_W[idx]
                        elif letter == 'C':
                            screen[iy][ix] = chars_C[idx]
                        else:
                            screen[iy][ix] = chars_S[idx]
            
            # 打印
            for row in screen:
                print(''.join(row))
            
            print(f"\n    ★ 3D WCS 立体旋转")
            print(f"    角度: X{math.degrees(ax)%360:.0f}° Y{math.degrees(ay)%360:.0f}° Z{math.degrees(az)%360:.0f}°")
            print("    Ctrl+C 退出")
            
            ay += 0.04
            ax += 0.015
            
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        clear()
        print("\n再见!\n")

if __name__ == "__main__":
    main()
