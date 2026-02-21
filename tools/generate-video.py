import cv2
import numpy as np
import os

# 视频参数
WIDTH = 640
HEIGHT = 480
FPS = 10
DURATION = 5  # 秒
TOTAL_FRAMES = FPS * DURATION

# 字符集，从深到浅
CHARS = '@#%*+=-:. '

# 创建输出目录
output_dir = '/Users/cgz/.openclaw/workspace/tools'
output_file = os.path.join(output_dir, 'ascii-rotate.mp4')

def draw_spiral(frame_num):
    """绘制螺旋图案"""
    img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    img[:] = (13, 17, 23)  # 深色背景 #0d1117
    
    angle = frame_num * 0.15
    char_size = 14
    
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    
    # 绘制螺旋 ASCII
    for y in range(-15, 16):
        for x in range(-25, 26):
            r = np.sqrt(x*x + y*y)
            theta = np.arctan2(y, x) + angle
            
            # 螺旋公式
            spiral = np.sin(theta * 3 + r * 0.3) * np.cos(r * 0.1)
            
            if r < 15 and spiral > 0.3:
                idx = int((spiral + 1) * (len(CHARS) - 1) / 2)
                idx = max(0, min(len(CHARS) - 1, idx))
                char = CHARS[idx]
                
                # 计算颜色（蓝绿色调）
                brightness = int((spiral + 1) * 127 + 128)
                color = (
                    int(brightness * 0.3),  # B
                    int(brightness * 0.7),  # G
                    int(brightness * 1.0)   # R
                )
                
                # 使用 OpenCV 绘制文本
                pos_x = int(center_x + x * char_size)
                pos_y = int(center_y + y * char_size)
                cv2.putText(img, char, (pos_x, pos_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
    
    # 添加标题
    title = "WELCOME TO CODEX"
    subtitle = "AI Coding Agent"
    loading = f"Loading{' .' * ((frame_num // 5) % 4)}"
    
    # 主标题
    cv2.putText(img, title, (center_x - 140, 50), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 166, 88), 2)
    
    # 副标题
    cv2.putText(img, subtitle, (center_x - 70, 80), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (139, 148, 158), 1)
    
    # 加载提示
    cv2.putText(img, loading, (center_x - 40, HEIGHT - 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (35, 197, 94), 1)
    
    return img

# 创建视频写入器
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_file, fourcc, FPS, (WIDTH, HEIGHT))

if not out.isOpened():
    print("❌ 无法创建视频文件")
    exit(1)

print(f"🎬 正在生成视频 ({TOTAL_FRAMES} 帧)...")

# 生成每一帧
for i in range(TOTAL_FRAMES):
    frame = draw_spiral(i)
    out.write(frame)
    
    if i % 10 == 0:
        print(f"  进度: {i}/{TOTAL_FRAMES}")

out.release()

print(f"✅ 视频生成完成: {output_file}")
print(f"📁 文件大小: {os.path.getsize(output_file) / 1024:.1f} KB")