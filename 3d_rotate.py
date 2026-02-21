#!/usr/bin/env python3
"""
3D Rotating Text in Terminal
按 Ctrl+C 退出
"""

import math
import time
import os
import sys

# 清屏函数
def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

# 3D 点旋转
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

# 将 3D 点投影到 2D
def project(x, y, z, distance=4):
    factor = distance / (distance + z)
    return int(x * factor * 15 + 40), int(y * factor * 8 + 12)

# 定义要显示的文字点阵
TEXT = "HELLO"

# 简单的 5x7 字体点阵
FONT = {
    'H': [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
          (1,3),(2,3),(3,3),
          (4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(4,6)],
    'E': [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
          (1,0),(2,0),(3,0),(4,0),
          (1,3),(2,3),(3,3),
          (1,6),(2,6),(3,6),(4,6)],
    'L': [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
          (1,6),(2,6),(3,6),(4,6)],
    'O': [(1,0),(2,0),(3,0),
          (0,1),(0,2),(0,3),(0,4),(0,5),
          (4,1),(4,2),(4,3),(4,4),(4,5),
          (1,6),(2,6),(3,6)],
    ' ': []
}

def get_text_points(text):
    """将文字转换为 3D 点云"""
    points = []
    x_offset = -(len(text) * 6) / 2  # 居中
    
    for i, char in enumerate(text.upper()):
        if char in FONT:
            for x, y in FONT[char]:
                # x 左右, y 上下, z 前后
                points.append((x + x_offset + i * 6, y - 3, 0))
    
    return points

def render(points, angle_x, angle_y, angle_z):
    """渲染旋转后的点云"""
    # 创建画布
    width, height = 80, 24
    screen = [[' ' for _ in range(width)] for _ in range(height)]
    z_buffer = [[-float('inf') for _ in range(width)] for _ in range(height)]
    
    # 旋转并投影所有点
    for x, y, z in points:
        rx, ry, rz = rotate_point(x, y, z, angle_x, angle_y, angle_z)
        px, py = project(rx, ry, rz)
        
        if 0 <= px < width and 0 <= py < height:
            # 简单的深度排序
            if rz > z_buffer[py][px]:
                z_buffer[py][px] = rz
                # 根据深度选择字符
                if rz > 2:
                    screen[py][px] = '@'
                elif rz > 0:
                    screen[py][px] = 'O'
                elif rz > -2:
                    screen[py][px] = 'o'
                else:
                    screen[py][px] = '.'
    
    return screen

def main():
    text = "HELLO"
    if len(sys.argv) > 1:
        text = sys.argv[1][:10]  # 限制长度
    
    points = get_text_points(text)
    angle_x, angle_y, angle_z = 0, 0, 0
    
    try:
        while True:
            clear_screen()
            
            # 渲染
            screen = render(points, angle_x, angle_y, angle_z)
            
            # 打印画布
            for row in screen:
                print(''.join(row))
            
            print(f"\n  3D Rotating: {text}")
            print("  按 Ctrl+C 退出")
            
            # 更新旋转角度
            angle_x += 0.05
            angle_y += 0.08
            angle_z += 0.03
            
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        clear_screen()
        print(f"\n再见！旋转了 {text}\n")

if __name__ == "__main__":
    main()
