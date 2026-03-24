#!/usr/bin/env python3
"""
3D Rotating WCS - Demo Frame
"""

import math

# 3D点旋转
def rotate_point(x, y, z, angle_x, angle_y, angle_z):
    cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)
    y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x
    
    cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
    x, z = x * cos_y + z * sin_y, -x * sin_y + z * cos_y
    
    cos_z, sin_z = math.cos(angle_z), math.sin(angle_z)
    x, y = x * cos_z - y * sin_z, x * sin_z + y * cos_z
    
    return x, y, z

def project(x, y, z, distance=8):
    if z + distance <= 0:
        z = -distance + 0.1
    factor = distance / (distance + z)
    return x * factor * 2.5, y * factor * 1.3

def build_wcs():
    points = []
    
    # W - 双层面
    w_coords = [
        (-12, 6), (-12, 4), (-12, 2), (-12, 0), (-12, -2), (-12, -4), (-12, -6),
        (-11, -4), (-10, -2), (-9, 0), (-8, 2), (-7, 3), (-6, 2),
        (-5, 0), (-4, -2), (-3, -4),
        (-2, -6), (-2, -4), (-2, -2), (-2, 0), (-2, 2), (-2, 4), (-2, 6),
        (-10, 4), (-8, 0), (-6, 0), (-4, 4),
    ]
    for x, y in w_coords:
        points.append((x, y, 2, 'W'))   # 前面
        points.append((x, y, -2, 'W'))  # 后面
    
    # C
    c_coords = []
    for angle in range(0, 181, 15):
        rad = math.radians(angle)
        x = 2 + math.cos(rad) * 5
        y = math.sin(rad) * 6
        c_coords.append((x, y))
    c_coords.extend([(7, -6), (5, -6), (3, -6), (1, -6), (-1, -6)])
    c_coords.extend([(2, 3), (2, 0), (2, -3), (4, 0)])
    for x, y in c_coords:
        points.append((x, y, 2, 'C'))
        points.append((x, y, -2, 'C'))
    
    # S
    s_coords = [(8, 6), (10, 6), (12, 6), (14, 6)]
    for angle in range(90, 271, 20):
        rad = math.radians(angle)
        x = 11 + math.cos(rad) * 3
        y = 3 + math.sin(rad) * 3
        s_coords.append((x, y))
    s_coords.extend([(10, 0), (12, 0)])
    for angle in range(-90, 91, 20):
        rad = math.radians(angle)
        x = 11 + math.cos(rad) * 3
        y = -3 + math.sin(rad) * 3
        s_coords.append((x, y))
    s_coords.extend([(8, -6), (10, -6), (12, -6)])
    s_coords.extend([(11, 4), (11, 0), (11, -4), (13, 0)])
    for x, y in s_coords:
        points.append((x, y, 2, 'S'))
        points.append((x, y, -2, 'S'))
    
    return points

def render(points, angle_x, angle_y, angle_z):
    width, height = 80, 22
    screen = [[' ' for _ in range(width)] for _ in range(height)]
    z_buffer = [[-float('inf') for _ in range(width)] for _ in range(height)]
    
    for x, y, z, letter in points:
        rx, ry, rz = rotate_point(x, y, z, angle_x, angle_y, angle_z)
        px, py = project(rx, ry, rz)
        ix, iy = int(px + width/2), int(py + height/2)
        
        if 0 <= ix < width and 0 <= iy < height:
            if rz > z_buffer[iy][ix]:
                z_buffer[iy][ix] = rz
                # 根据字母和深度选择字符
                if letter == 'W':
                    chars = ['W', 'O', 'o', '.']
                elif letter == 'C':
                    chars = ['C', '0', 'c', ',']
                else:
                    chars = ['S', '0', 's', ',']
                
                if rz > 1.5:
                    screen[iy][ix] = chars[0]
                elif rz > 0.5:
                    screen[iy][ix] = chars[1]
                elif rz > -0.5:
                    screen[iy][ix] = chars[2]
                else:
                    screen[iy][ix] = chars[3]
    
    return screen

# 渲染一帧展示
points = build_wcs()
angle_x, angle_y, angle_z = 0.3, 0.5, 0.2  # 旋转角度

screen = render(points, angle_x, angle_y, angle_z)

print("╔" + "═" * 78 + "╗")
for row in screen:
    line = ''.join(row)
    # 清理尾部空格但保留长度
    print("║" + line + "║")
print("╚" + "═" * 78 + "╝")
print("\n    ★ 3D WCS 立体文字")
print("    运行: python3 3d_wcs_shape.py  查看旋转动画")
