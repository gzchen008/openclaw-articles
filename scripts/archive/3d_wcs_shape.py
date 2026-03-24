#!/usr/bin/env python3
"""
3D Rotating WCS with Real 3D Shape
按 Ctrl+C 退出
"""

import math
import time
import os
import sys

# 清屏
def clear_screen():
    print('\033[2J\033[H', end='')

def rotate_point(x, y, z, angle_x, angle_y, angle_z):
    # X轴旋转
    cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)
    y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x
    
    # Y轴旋转
    cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
    x, z = x * cos_y + z * sin_y, -x * sin_y + z * cos_y
    
    # Z轴旋转
    cos_z, sin_z = math.cos(angle_z), math.sin(angle_z)
    x, y = x * cos_z - y * sin_z, x * sin_z + y * cos_z
    
    return x, y, z

def project(x, y, z, distance=8):
    """3D透视投影"""
    if z + distance <= 0:
        z = -distance + 0.1
    factor = distance / (distance + z)
    return x * factor * 2.5, y * factor * 1.3

# 构建真正的3D文字 - 有厚度的WCS
def build_wcs_3d():
    """构建WCS三个字母的3D点云，带厚度"""
    all_points = []
    edges = []  # 存储边用于画线
    
    # W - 更复杂的3D形状
    w_points_front = []
    w_points_back = []
    
    # W的前表面 (z = 2)
    w_front = [
        # 左竖
        (-12, 6, 2), (-12, 4, 2), (-12, 2, 2), (-12, 0, 2), (-12, -2, 2), (-12, -4, 2), (-12, -6, 2),
        # 左斜下
        (-11, -4, 2), (-10, -2, 2), (-9, 0, 2),
        # V底部
        (-8, 2, 2), (-7, 3, 2), (-6, 2, 2),
        # 右斜上
        (-5, 0, 2), (-4, -2, 2), (-3, -4, 2),
        # 右竖
        (-2, -6, 2), (-2, -4, 2), (-2, -2, 2), (-2, 0, 2), (-2, 2, 2), (-2, 4, 2), (-2, 6, 2),
        # 内部填充
        (-10, 4, 2), (-8, 0, 2), (-6, 0, 2), (-4, 4, 2),
    ]
    
    # W的后表面 (z = -2)
    w_back = [(x, y, -2) for x, y, z in w_front]
    
    # W的连接边
    w_edges = []
    for i in range(len(w_front)):
        # 前后连接
        w_edges.append((w_front[i], w_back[i]))
    
    all_points.extend(w_front)
    all_points.extend(w_back)
    edges.extend(w_edges)
    
    # C - 弧形3D
    c_front = []
    # 上半圆
    for angle in range(0, 181, 15):
        rad = math.radians(angle)
        x = 2 + math.cos(rad) * 5
        y = math.sin(rad) * 6
        c_front.append((x, y, 2))
    # 底部
    c_front.extend([(7, -6, 2), (5, -6, 2), (3, -6, 2), (1, -6, 2), (-1, -6, 2)])
    # 内部
    c_front.extend([(2, 3, 2), (2, 0, 2), (2, -3, 2), (4, 0, 2)])
    
    c_back = [(x, y, -2) for x, y, z in c_front]
    c_edges = [(c_front[i], c_back[i]) for i in range(min(len(c_front), len(c_back)))]
    
    all_points.extend(c_front)
    all_points.extend(c_back)
    edges.extend(c_edges)
    
    # S - 3D曲线
    s_front = []
    # 顶部横
    s_front.extend([(8, 6, 2), (10, 6, 2), (12, 6, 2), (14, 6, 2)])
    # 上半弧
    for angle in range(90, 271, 20):
        rad = math.radians(angle)
        x = 11 + math.cos(rad) * 3
        y = 3 + math.sin(rad) * 3
        s_front.append((x, y, 2))
    # 中间
    s_front.extend([(10, 0, 2), (12, 0, 2)])
    # 下半弧
    for angle in range(-90, 91, 20):
        rad = math.radians(angle)
        x = 11 + math.cos(rad) * 3
        y = -3 + math.sin(rad) * 3
        s_front.append((x, y, 2))
    # 底部横
    s_front.extend([(8, -6, 2), (10, -6, 2), (12, -6, 2)])
    # 内部
    s_front.extend([(11, 4, 2), (11, 0, 2), (11, -4, 2), (13, 0, 2)])
    
    s_back = [(x, y, -2) for x, y, z in s_front]
    s_edges = [(s_front[i], s_back[i]) for i in range(min(len(s_front), len(s_back)))]
    
    all_points.extend(s_front)
    all_points.extend(s_back)
    edges.extend(s_edges)
    
    return all_points, edges

def draw_line(p1, p2, screen, z_buffer, char='#'):
    """在屏幕上画线"""
    x0, y0, z0 = p1
    x1, y1, z1 = p2
    
    # 投影到2D
    px0, py0 = project(x0, y0, z0)
    px1, py1 = project(x1, y1, z1)
    
    # Bresenham画线
    dx = abs(int(px1 - px0))
    dy = abs(int(py1 - py0))
    sx = 1 if px0 < px1 else -1
    sy = 1 if py0 < py1 else -1
    err = dx - dy
    
    x, y = int(px0), int(py0)
    
    while True:
        if 0 <= x < 80 and 0 <= y < 24:
            # 计算该点的平均深度
            z = (z0 + z1) / 2
            if z > z_buffer[y][x]:
                z_buffer[y][x] = z
                # 根据深度选择字符
                if z > 1:
                    screen[y][x] = '@'
                elif z > 0:
                    screen[y][x] = 'O'
                elif z > -1:
                    screen[y][x] = 'o'
                else:
                    screen[y][x] = '.'
        
        if x == int(px1) and y == int(py1):
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy

def render(points, edges, angle_x, angle_y, angle_z):
    """渲染3D场景"""
    width, height = 80, 24
    screen = [[' ' for _ in range(width)] for _ in range(height)]
    z_buffer = [[-float('inf') for _ in range(width)] for _ in range(height)]
    
    # 旋转所有点
    rotated_points = []
    for x, y, z in points:
        rx, ry, rz = rotate_point(x, y, z, angle_x, angle_y, angle_z)
        rotated_points.append((rx, ry, rz))
    
    # 画边（连接线）
    for (p1_idx, p2_idx) in [(i, i) for i in range(len(edges))] if not edges else []:
        pass
    
    # 直接画所有旋转后的边
    # 首先找出应该连接的边
    for i in range(0, len(rotated_points), 2):
        if i + 1 < len(rotated_points):
            # 前后对应的点连线
            p1 = rotated_points[i]
            p2 = rotated_points[i + 1]
            draw_line(p1, p2, screen, z_buffer, '|')
    
    # 绘制所有点
    for x, y, z in rotated_points:
        px, py = project(x, y, z)
        ix, iy = int(px + width/2), int(py + height/2)
        if 0 <= ix < width and 0 <= iy < height:
            if z > z_buffer[iy][ix]:
                z_buffer[iy][ix] = z
                # 根据深度选择字符
                if z > 2:
                    screen[iy][ix] = '@'
                elif z > 1:
                    screen[iy][ix] = 'O'
                elif z > 0:
                    screen[iy][ix] = 'o'
                elif z > -1:
                    screen[iy][ix] = '*'
                else:
                    screen[iy][ix] = '.'
    
    return screen

def main():
    points, edges = build_wcs_3d()
    
    angle_x, angle_y, angle_z = 0, 0, 0
    
    try:
        while True:
            clear_screen()
            
            # 渲染
            screen = render(points, edges, angle_x, angle_y, angle_z)
            
            # 打印
            for row in screen:
                print(''.join(row))
            
            # 信息
            print(f"\n  ★ 3D Rotating: WCS")
            print(f"  ↺ X:{math.degrees(angle_x)%360:.0f}° Y:{math.degrees(angle_y)%360:.0f}° Z:{math.degrees(angle_z)%360:.0f}°")
            print("  按 Ctrl+C 退出")
            
            # 旋转
            angle_y += 0.05
            angle_x += 0.02
            
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        clear_screen()
        print("\n再见！\n")

if __name__ == "__main__":
    main()
