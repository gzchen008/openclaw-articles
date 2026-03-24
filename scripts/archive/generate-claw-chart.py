#!/usr/bin/env python3
"""
生成 Claw 家族对比图
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib import rcParams

# 设置中文字体
rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
rcParams['axes.unicode_minus'] = False

# 数据
projects = ['OpenClaw', 'ZeroClaw', 'NanoClaw', 'nanobot', 'PicoClaw', 'IronClaw', 'memU Bot', 'TrustClaw']
languages = ['Node.js', 'Rust', 'Python', 'Python', 'Go', 'Rust', 'Python', 'Cloud']

# 资源占用（相对值，0-10）
memory_usage = [10, 0.5, 3, 5, 1, 4, 6, 0]  # 0表示云托管
startup_speed = [10, 0.1, 5, 8, 1, 3, 7, 0]  # 越小越快

# Stars（千）
stars = [50, 1, 0.01, 15.4, 1.1, 0.368, 8.7, 0]

# 提供商数量
providers = [8, 22, 3, 10, 6, 5, 4, 500]

# 通道数量
channels = [5, 8, 1, 8, 2, 4, 2, 10]

# 创建图表（增大尺寸）
fig = plt.figure(figsize=(20, 15))
fig.patch.set_facecolor('#0f0f1e')

# 标题（增大字体）
fig.suptitle('Claw 家族终极对比图', fontsize=32, fontweight='bold', color='white', y=0.985)

# 创建子图
ax1 = fig.add_subplot(2, 3, 1)
ax2 = fig.add_subplot(2, 3, 2)
ax3 = fig.add_subplot(2, 3, 3)
ax4 = fig.add_subplot(2, 3, 4)
ax5 = fig.add_subplot(2, 3, 5)
ax6 = fig.add_subplot(2, 3, 6)

# 设置所有子图背景色
for ax in [ax1, ax2, ax3, ax4, ax5, ax6]:
    ax.set_facecolor('#1a1a2e')
    ax.tick_params(colors='white', labelsize=16)
    for spine in ax.spines.values():
        spine.set_color('#333355')
        spine.set_linewidth(1.5)

# 1. 内存占用对比（优化版水平条形图）
colors = ['#FF6B6B', '#4ECDC4', '#95E1D3', '#F38181', '#AA96DA', '#FFB6C1', '#C9B1FF', '#88D8B0']
y_pos = np.arange(len(projects))

# 绘制柱状图（带圆角效果）
bars = ax1.barh(y_pos, memory_usage, color=colors, alpha=0.9, 
                edgecolor='white', linewidth=2, height=0.7)

# 添加阴影效果
for bar in bars:
    bar.set_edgecolor('white')
    bar.set_linewidth(2)

ax1.set_yticks(y_pos)
ax1.set_yticklabels(projects, fontsize=18, color='white', fontweight='bold')
ax1.set_xlabel('Memory Usage (Relative)', fontsize=20, color='white', fontweight='bold')
ax1.set_title('Memory Usage', fontsize=26, fontweight='bold', color='white', pad=20)
ax1.invert_yaxis()

# 添加数值标签（更大字体）
for i, v in enumerate(memory_usage):
    if v > 0:
        label = f'{v}'
    else:
        label = 'CLOUD'
    ax1.text(v + 0.4, i, label, va='center', fontsize=16, color='white', fontweight='bold')

# 2. 启动速度对比（越小越快）
bars = ax2.barh(y_pos, startup_speed, color=colors, alpha=0.9, 
                edgecolor='white', linewidth=2, height=0.7)

ax2.set_yticks(y_pos)
ax2.set_yticklabels(projects, fontsize=18, color='white', fontweight='bold')
ax2.set_xlabel('Startup Time (Lower is Faster)', fontsize=20, color='white', fontweight='bold')
ax2.set_title('Startup Speed', fontsize=26, fontweight='bold', color='white', pad=20)
ax2.invert_yaxis()

# 添加数值标签
for i, v in enumerate(startup_speed):
    if v > 0:
        label = f'{v}'
    else:
        label = 'CLOUD'
    ax2.text(v + 0.4, i, label, va='center', fontsize=16, color='white', fontweight='bold')

# 3. GitHub Stars
bars = ax3.barh(y_pos, stars, color=colors, alpha=0.9, 
                edgecolor='white', linewidth=2, height=0.7)

ax3.set_yticks(y_pos)
ax3.set_yticklabels(projects, fontsize=18, color='white', fontweight='bold')
ax3.set_xlabel('GitHub Stars (K)', fontsize=20, color='white', fontweight='bold')
ax3.set_title('GitHub Stars', fontsize=26, fontweight='bold', color='white', pad=20)
ax3.invert_yaxis()

# 添加数值标签
for i, v in enumerate(stars):
    label = f'{v:.1f}K' if v >= 1 else f'{v}'
    ax3.text(v + 1.2, i, label, va='center', fontsize=16, color='white', fontweight='bold')

# 4. LLM 提供商支持
bars = ax4.barh(y_pos, providers, color=colors, alpha=0.9, 
                edgecolor='white', linewidth=2, height=0.7)

ax4.set_yticks(y_pos)
ax4.set_yticklabels(projects, fontsize=18, color='white', fontweight='bold')
ax4.set_xlabel('Number of Providers', fontsize=20, color='white', fontweight='bold')
ax4.set_title('LLM Providers', fontsize=26, fontweight='bold', color='white', pad=20)
ax4.invert_yaxis()

# 添加数值标签
for i, v in enumerate(providers):
    label = f'{v}+' if v < 100 else f'{v}'
    ax4.text(v + 2, i, label, va='center', fontsize=16, color='white', fontweight='bold')

# 5. 聊天通道支持
bars = ax5.barh(y_pos, channels, color=colors, alpha=0.9, 
                edgecolor='white', linewidth=2, height=0.7)

ax5.set_yticks(y_pos)
ax5.set_yticklabels(projects, fontsize=18, color='white', fontweight='bold')
ax5.set_xlabel('Number of Channels', fontsize=20, color='white', fontweight='bold')
ax5.set_title('Chat Channels', fontsize=26, fontweight='bold', color='white', pad=20)
ax5.invert_yaxis()

# 添加数值标签
for i, v in enumerate(channels):
    ax5.text(v + 0.4, i, str(v), va='center', fontsize=16, color='white', fontweight='bold')

# 6. 编程语言分布（优化饼图）
lang_count = {}
for lang in languages:
    lang_count[lang] = lang_count.get(lang, 0) + 1

lang_labels = list(lang_count.keys())
lang_values = list(lang_count.values())

wedges, texts, autotexts = ax6.pie(lang_values, labels=lang_labels, autopct='%1.0f%%',
                                     colors=['#FF6B6B', '#4ECDC4', '#95E1D3', '#AA96DA'],
                                     textprops={'fontsize': 18, 'color': 'white', 'fontweight': 'bold'},
                                     wedgeprops={'edgecolor': 'white', 'linewidth': 4},
                                     startangle=90)
for autotext in autotexts:
    autotext.set_fontsize(17)
    autotext.set_fontweight('bold')
ax6.set_title('Programming Languages', fontsize=26, fontweight='bold', color='white', pad=20)

# 调整布局
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# 添加底部说明
fig.text(0.5, 0.005, 'Data Source: 2026-02-18 GitHub & Web Search | Generated: 2026-02-18',
         ha='center', fontsize=13, color='#888888', style='italic')

# 保存图片
plt.savefig('claw-comparison-chart.png', dpi=150, bbox_inches='tight', facecolor='#0f0f1e')
print("✅ 对比图已生成: claw-comparison-chart.png")

# 显示统计信息
print("\n📊 统计信息:")
print(f"总项目数: {len(projects)}")
print(f"编程语言: {', '.join(set(languages))}")
print(f"最高 Stars: {projects[stars.index(max(stars))]} ({max(stars):.1f}K)")
print(f"最轻量: {projects[memory_usage.index(min([m for m in memory_usage if m > 0]))]}")
print(f"最快启动: {projects[startup_speed.index(min([s for s in startup_speed if s > 0]))]}")
print(f"最多提供商: {projects[providers.index(max(providers))]} ({max(providers)}+)")
print(f"最多通道: {projects[channels.index(max(channels))]} ({max(channels)} channels)")
