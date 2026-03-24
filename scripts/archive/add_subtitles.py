import subprocess
import os

# 视频文件路径
video_path = os.path.expanduser("~/.openclaw/workspace/agent-browser-intro.mp4")
output_path = os.path.expanduser("~/.openclaw/workspace/agent-browser-with-subtitles.mp4")

# 字幕列表 (时间, 文本)
subtitles = [
    (0, 4, "大家好！今天介绍 agent-browser 项目"),
    (4, 8, "Vercel 官方开源，Star 8.6k"),
    (8, 13, "Rust 编写的浏览器自动化 CLI"),
    (13, 18, "核心功能：快照、点击、填表、录屏"),
    (18, 23, "支持保存登录态，下次不用扫码"),
    (23, 28, "安装：npm install -g agent-browser"),
    (28, 33, "适合自动化测试、爬虫、RPA"),
    (33, 38, "GitHub: vercel-labs/agent-browser"),
    (38, 40, "记得点赞关注！"),
]

# 构建 drawtext 滤镜
filters = []
for start, end, text in subtitles:
    # 转义特殊字符
    text_escaped = text.replace(":", "\\:").replace("'", "'")
    filter_str = f"drawtext=text='{text_escaped}':fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=28:fontcolor=white:x=(w-text_w)/2:y=h-th-80:shadowcolor=black:shadowx=2:shadowy=2:enable='between(t,{start},{end})'"
    filters.append(filter_str)

# 合并所有滤镜
filter_complex = ",".join(filters)

# 构建 ffmpeg 命令
cmd = [
    "ffmpeg", "-i", video_path,
    "-vf", filter_complex,
    "-c:a", "copy",
    output_path, "-y"
]

print("执行命令...")
print("滤镜数量:", len(filters))

# 执行
result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0:
    print("✅ 字幕添加成功")
    print(f"输出文件: {output_path}")
    print(f"文件大小: {os.path.getsize(output_path) / 1024:.1f} KB")
else:
    print("❌ 失败")
    print(result.stderr[-500:])
