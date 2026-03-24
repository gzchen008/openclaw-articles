#!/usr/bin/env python3
"""
3D Rotating WCS - High Clarity Version
文字始终清晰可辨的3D旋转
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

# 颜色
CW = '\033[96m'   # W - 青色
CC = '\033[93m'   # C - 黄色  
CS = '\033[95m'   # S - 紫色
CR = '\033[0m'    # 重置

# 定义每个字母的点阵 - 使用简单坐标
LETTER_W = [
    # 左竖
    (-13, 6), (-13, 4), (-13, 2), (-13, 0), (-13, -2), (-13, -4), (-13, -6),
    # 右竖  
    (-3, 6), (-3, 4), (-3, 2), (-3, 0), (-3, -2), (-3, -4), (-3, -6),
    # V形
    (-11, -2), (-10, 0), (-9, 2), (-8, 3), (-7, 2), (-6, 0), (-5, -2),
    # 底部
    (-11, 3), (-10, 4), (-9, 4), (-8, 4), (-7, 4), (-6, 3),
]

LETTER_C = []
# 上半圆弧
for a in range(180, 361, 15):
    r = math.radians(a)
    LETTER_C.append((2 + math.cos(r)*6, math.sin(r)*7))
# 右边
LETTER_C.extend([(8, 6), (8, 3), (8, 0), (8, -3), (8, -6)])
# 下半圆弧
for a in range(0, 181, 15):
    r = math.radians(a)
    LETTER_C.append((2 + math.cos(r)*6, -7 + math.sin(r)*7))

LETTER_S = []
# 顶部
for x in range(9, 17):
    LETTER_S.append((x, 7))
# 上弧
for a in range(90, 271, 20):
    r = math.radians(a)
    LETTER_S.append((13 + math.cos(r)*4, 3 + math.sin(r)*4))
# 中间
for x in range(10, 16):
    LETTER_S.append((x, 0))
# 下弧
for a in range(-90, 91, 20):
    r = math.radians(a)
    LETTER_S.append((13 + math.cos(r)*4, -3 + math.sin(r)*4))
# 底部
for x in range(9, 17):
    LETTER_S.append((x, -7))

def main():
    ax = ay = az = 0
    
    try:
        while True:
            clear()
            
            # 屏幕: (字符, 颜色)
            screen = [[(' ', '') for _ in range(80)] for _ in range(24)]
            zbuf = [[-99 for _ in range(80)] for _ in range(24)]
            
            # 处理所有字母
            letters = [
                (LETTER_W, 'W', CW, -8),
                (LETTER_C, 'C', CC, 2),
                (LETTER_S, 'S', CS, 8)
            ]
            
            for points, char, color, offset_x in letters:
                # 为每个点创建前后两面
                all_points = []
                for x, y in points:
                    # 前面
                    all_points.append((x, y, 2.5, char, color))
                    # 后面
                    all_points.append((x, y, -2.5, char, color))
                
                # 按深度排序绘制（从远到近）
                rotated = []
                for x, y, z, c, col in all_points:
                    rx, ry, rz = rotate(x, y, z, ax, ay, az)
                    px, py = project(rx, ry, rz)
                    rotated.append((px, py, rz, c, col))
                
                # 按z排序
                rotated.sort(key=lambda p: p[2])
                
                # 绘制
                for px, py, rz, c, col in rotated:
                    ix, iy = int(px + 40), int(py + 12)
                    if 0 <= ix < 80 and 0 <= iy < 24:
                        if rz > zbuf[iy][ix]:
                            zbuf[iy][ix] = rz
                            # 始终使用同一个字符，只是颜色深度变化
                            # 或者根据深度使用大小写
                            if rz > 1.5:
                                display = c  # 大写 - 近
                            elif rz > 0:
                                display = c.lower()  # 小写 - 中
                            else:
                                display = c.lower()  # 小写 - 远
                            screen[iy][ix] = (display, col)
            
            # 打印
            for row in screen:
                line = ""
                cur_color = ""
                for ch, col in row:
                    if col != cur_color:
                        line += col
                        cur_color = col
                    line += ch
                if cur_color:
                    line += CR
                print(line)
            
            print(f"\n{CW}    ★ 3D WCS 立体旋转{CR}")
            print(f"    角度: X{math.degrees(ax)%360:.0f}° Y{math.degrees(ay)%360:.0f}° Z{math.degrees(az)%360:.0f}°")
            print(f"    {CW}W{CR} = 青色 | {CC}C{CR} = 黄色 | {CS}S{CR} = 紫色")
            print("    按 Ctrl+C 退出")
            
            ay += 0.04
            ax += 0.015
            
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        clear()
        print(f"\n{CW}W{CC}C{CS}S{CR} 再见!\n")

if __name__ == "__main__":
    main()
