#!/usr/bin/env python3
"""
生成 Claw 家族对比图 - 手机竖版
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

# 设置中文字体
rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
rcParams['axes.unicode_minus'] = False

# 数据
projects = ['OpenClaw', 'ZeroClaw', 'NanoClaw', 'nanobot', 'PicoClaw', 'IronClaw', 'memU Bot', 'TrustClaw']

# 资源占用（相对值，0-10）
memory_usage = [10, 0.5, 3, 5, 1, 4, 6, 0]
startup_speed = [10, 0.1, 5, 8, 1, 3, 7, 0]
stars = [50, 1, 0.01, 15.4, 1.1, 0.368, 8.7, 0]
providers = [8, 22, 3, 10, 6, 5, 4, 500]
channels = [5, 8, 1, 8, 2, 4, 2, 10]

# 创建图表（竖版）
fig = plt.figure(figsize=(10, 16))
fig.patch.set_facecolor('#0f0f1e')

# 标题
fig.suptitle('Claw Family Comparison', fontsize=28, fontweight='bold', color='white', y=0.97)

# 创建垂直堆叠的子图
ax1 = fig.add_subplot(3, 2, 1)
ax2 = fig.add_subplot(3, 2, 2)
ax3 = fig.add_subplot(3, 2, 3)
ax4 = fig.add_subplot(3, 2, 4)
ax5 = fig.add_subplot(3, 2, 5)
ax6 = fig.add_subplot(3, 2, 6)

# 设置所有子图背景色
for ax in [ax1, ax2, ax3, ax4, ax5, ax6]:
    ax.set_facecolor('#1a1a2e')
    ax.tick_params(colors='white', labelsize=11)
    for spine in ax.spines.values():
        spine.set_color('#333355')
        spine.set_linewidth(1.5)

# 颜色方案
colors = ['#FF6B6B', '#4ECDC4', '#95E1D3', '#F38181', '#AA96DA', '#FFB6C1', '#C9B1FF', '#88D8B0']

y_pos = np.arange(len(projects))

# 1. 内存占用
bars1 = ax1.barh(y_pos, memory_usage, color=colors, alpha=0.9, edgecolor='white', linewidth=1.5, height=0.6)
ax1.set_yticks(y_pos)
ax1.set_yticklabels(projects, fontsize=12, color='white', fontweight='bold')
ax1.set_xlabel('Memory', fontsize=14, color='white', fontweight='bold')
ax1.set_title('Memory Usage', fontsize=16, fontweight='bold', color='white', pad=10)
ax1.invert_yaxis()

for i, v in enumerate(memory_usage):
    label = 'CLOUD' if v == 0 else str(v)
    ax1.text(v + 0.3, i, label, va='center', fontsize=11, color='white', fontweight='bold')

# 2. 启动速度
bars2 = ax2.barh(y_pos, startup_speed, color=colors, alpha=0.9, edgecolor='white', linewidth=1.5, height=0.6)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(projects, fontsize=12, color='white', fontweight='bold')
ax2.set_xlabel('Speed (Lower=Faster)', fontsize=14, color='white', fontweight='bold')
ax2.set_title('Startup Speed', fontsize=16, fontweight='bold', color='white', pad=10)
ax2.invert_yaxis()

for i, v in enumerate(startup_speed):
    label = 'CLOUD' if v == 0 else str(v)
    ax2.text(v + 0.3, i, label, va='center', fontsize=11, color='white', fontweight='bold')

# 3. GitHub Stars
bars3 = ax3.barh(y_pos, stars, color=colors, alpha=0.9, edgecolor='white', linewidth=1.5, height=0.6)
ax3.set_yticks(y_pos)
ax3.set_yticklabels(projects, fontsize=12, color='white', fontweight='bold')
ax3.set_xlabel('Stars (K)', fontsize=14, color='white', fontweight='bold')
ax3.set_title('GitHub Stars', fontsize=16, fontweight='bold', color='white', pad=10)
ax3.invert_yaxis()

for i, v in enumerate(stars):
    label = f'{v:.1f}K' if v >= 1 else f'{v}'
    ax3.text(v + 1, i, label, va='center', fontsize=11, color='white', fontweight='bold')

# 4. LLM 提供商
bars4 = ax4.barh(y_pos, providers, color=colors, alpha=0.9, edgecolor='white', linewidth=1.5, height=0.6)
ax4.set_yticks(y_pos)
ax4.set_yticklabels(projects, fontsize=12, color='white', fontweight='bold')
ax4.set_xlabel('Providers', fontsize=14, color='white', fontweight='bold')
ax4.set_title('LLM Providers', fontsize=16, fontweight='bold', color='white', pad=10)
ax4.invert_yaxis()

for i, v in enumerate(providers):
    label = f'{v}+' if v < 100 else str(v)
    ax4.text(v + 2, i, label, va='center', fontsize=11, color='white', fontweight='bold')

# 5. 聊天通道
bars5 = ax5.barh(y_pos, channels, color=colors, alpha=0.9, edgecolor='white', linewidth=1.5, height=0.6)
ax5.set_yticks(y_pos)
ax5.set_yticklabels(projects, fontsize=12, color='white', fontweight='bold')
ax5.set_xlabel('Channels', fontsize=14, color='white', fontweight='bold')
ax5.set_title('Chat Channels', fontsize=16, fontweight='bold', color='white', pad=10)
ax5.invert_yaxis()

for i, v in enumerate(channels):
    ax5.text(v + 0.3, i, str(v), va='center', fontsize=11, color='white', fontweight='bold')

# 6. 快速推荐
ax6.axis('off')
ax6.text(0.5, 0.95, 'Quick Recommendations', fontsize=18, fontweight='bold', 
         color='white', ha='center', va='top', transform=ax6.transAxes)

recommendations = [
    ('Most Features:', 'OpenClaw'),
    ('Ultra Light:', 'ZeroClaw / PicoClaw'),
    ('Best Security:', 'IronClaw'),
    ('Easiest Setup:', 'TrustClaw'),
    ('Multi-Channel:', 'nanobot'),
    ('Long-Running:', 'memU Bot'),
]

y_start = 0.82
for i, (label, value) in enumerate(recommendations):
    y_pos_text = y_start - (i * 0.12)
    ax6.text(0.1, y_pos_text, label, fontsize=13, color='#888888', 
             fontweight='bold', transform=ax6.transAxes, va='center')
    ax6.text(0.45, y_pos_text, value, fontsize=13, color='white',
             fontweight='bold', transform=ax6.transAxes, va='center')

# 添加底部说明
fig.text(0.5, 0.01, 'Data: 2026-02-18 | Generated by Clawra', 
         ha='center', fontsize=11, color='#666666', style='italic')

# 调整布局
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# 保存图片（手机竖版，较低 DPI）
plt.savefig('claw-comparison-mobile.png', dpi=100, bbox_inches='tight', facecolor='#0f0f1e')
print("✅ 手机竖版对比图已生成: claw-comparison-mobile.png")
print(f"📐 分辨率: 约 {1000}x{1600}")
