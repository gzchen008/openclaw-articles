---
name: remotion
description: Generate videos programmatically using Remotion - a React-based video creation framework. Use when users want to create videos from code, animations, product demos, explainer videos, or any programmatic video generation task. Supports creating video templates, rendering MP4/GIF, and customizing animations with React components.
---

# Remotion - 程序化视频生成

用代码生成视频。基于 React + TypeScript，适合制作产品介绍、教程、数据可视化动画等。

## 快速开始

### 1. 初始化 Remotion 项目

```bash
# 创建新项目
npm init video@latest

# 或克隆模板
git clone https://github.com/remotion-dev/template-hello-world.git my-video
```

### 2. 核心概念

| 概念 | 说明 | 示例 |
|------|------|------|
| `Composition` | 视频片段定义 | 设置视频尺寸、FPS、时长 |
| `useCurrentFrame()` | 获取当前帧号 | 实现帧动画 |
| `useVideoConfig()` | 视频配置 | fps, width, height, durationInFrames |
| `Sequence` | 时间线控制 | 控制片段开始时间和持续时长 |
| `interpolate()` | 插值动画 | 数值/颜色过渡动画 |
| `spring()` | 弹性动画 | 自然的弹性效果 |

### 3. 开发工作流

```bash
# 1. 启动开发服务器（实时预览）
npm run dev

# 2. 渲染视频（导出 MP4）
npx remotion render src/index.ts MyComposition output.mp4

# 3. 渲染 GIF
npx remotion render src/index.ts MyComposition output.gif --codec=gif

# 4. 渲染图片序列
npx remotion render src/index.ts MyComposition frames/ --sequence
```

## 常用视频模板

### 产品介绍视频 (Product Demo)

适用于展示产品功能、操作流程。

```tsx
// src/ProductDemo.tsx
import { useCurrentFrame, useVideoConfig, interpolate } from 'remotion';

export const ProductDemo: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  
  // 进度 0-1
  const progress = frame / durationInFrames;
  
  return (
    <div style={{
      width: '100%',
      height: '100%',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: 'system-ui',
    }}>
      <div style={{
        opacity: interpolate(frame, [0, 30], [0, 1]),
        transform: `translateY(${interpolate(frame, [0, 30], [50, 0])}px)`,
      }}>
        <h1 style={{ color: 'white', fontSize: 60 }}>OpenClaw</h1>
        <p style={{ color: 'white', fontSize: 24 }}>AI驱动的自动化助手</p>
      </div>
    </div>
  );
};
```

### 文字动画视频 (Typography)

适合社交媒体、标题动画。

```tsx
// src/TypeAnimation.tsx
import { useCurrentFrame, spring, useVideoConfig } from 'remotion';

export const TypeAnimation: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  const scale = spring({
    frame,
    fps,
    config: { damping: 10, stiffness: 100 },
  });
  
  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      height: '100%',
      backgroundColor: '#1a1a1a',
    }}>
      <h1 style={{
        color: 'white',
        fontSize: 80,
        transform: `scale(${scale})`,
      }}>
        {text}
      </h1>
    </div>
  );
};
```

### 分镜序列 (Storyboard)

多场景连续播放。

```tsx
// src/Storyboard.tsx
import { Sequence } from 'remotion';
import { IntroScene } from './scenes/IntroScene';
import { FeatureScene } from './scenes/FeatureScene';
import { OutroScene } from './scenes/OutroScene';

export const Storyboard: React.FC = () => {
  return (
    <>
      <Sequence from={0} durationInFrames={90}>
        <IntroScene />
      </Sequence>
      <Sequence from={90} durationInFrames={120}>
        <FeatureScene />
      </Sequence>
      <Sequence from={210} durationInFrames={60}>
        <OutroScene />
      </Sequence>
    </>
  );
};
```

## OpenClaw 介绍视频模板

见 `assets/openclaw-intro/` 目录，包含完整的产品介绍视频模板：

```
assets/openclaw-intro/
├── src/
│   ├── index.ts          # 入口文件
│   ├── Root.tsx          # 根组件
│   ├── compositions/     # 视频片段
│   │   ├── Intro.tsx     # 开场 (0-5s)
│   │   ├── PainPoint.tsx # 痛点场景 (5-15s)
│   │   ├── Solution.tsx  # 解决方案 (15-35s)
│   │   ├── Features.tsx  # 功能展示 (35-60s)
│   │   └── CTA.tsx       # 行动号召 (60-75s)
│   ├── components/       # 可复用组件
│   │   ├── TextReveal.tsx
│   │   ├── CodeBlock.tsx
│   │   └── Logo.tsx
│   └── styles/           # 样式
├── public/               # 静态资源
│   ├── logo.png
│   └── screenshots/
└── package.json
```

### 使用模板

```bash
# 1. 复制模板到工作目录
cp -r ~/.openclaw/skills/remotion/assets/openclaw-intro ./my-video

# 2. 安装依赖
cd my-video && npm install

# 3. 预览
npm run dev

# 4. 渲染（约 2-3 分钟）
npx remotion render src/index.tsx OpenClawIntro openclaw-intro.mp4
```

## 脚本工具

### `scripts/init-project.sh`

快速初始化 Remotion 项目。

```bash
# 创建项目
~/.openclaw/skills/remotion/scripts/init-project.sh my-video

# 使用模板
~/.openclaw/skills/remotion/scripts/init-project.sh my-video --template openclaw-intro
```

### `scripts/render.sh`

渲染视频（支持常用参数）。

```bash
# 基本用法
~/.openclaw/skills/remotion/scripts/render.sh MyComposition output.mp4

# 指定帧范围
~/.openclaw/skills/remotion/scripts/render.sh MyComposition output.mp4 --frames 0-150

# 降低质量快速预览
~/.openclaw/skills/remotion/scripts/render.sh MyComposition preview.mp4 --quality low
```

## 常用动画效果

### 淡入淡出

```tsx
const opacity = interpolate(frame, [0, 30, 150, 180], [0, 1, 1, 0]);
```

### 滑动进入

```tsx
const translateX = interpolate(frame, [0, 30], [-100, 0]);
```

### 打字机效果

```tsx
const charsToShow = Math.floor(frame / 3);
const displayText = fullText.slice(0, charsToShow);
```

### 弹性缩放

```tsx
const scale = spring({ frame, fps, config: { mass: 1, damping: 10 } });
```

## 视频规格建议

| 用途 | 分辨率 | FPS | 时长 |
|------|--------|-----|------|
| 抖音/小红书 | 1080×1920 | 30 | 15-60s |
| YouTube | 1920×1080 | 30/60 | 1-3min |
| Twitter/X | 1280×720 | 30 | < 2min |
| GIF 动画 | 480×270 | 15 | < 10s |

## 参考文档

详细 API 文档和进阶用法见 `references/` 目录：

- `references/animation.md` - 动画技巧
- `references/components.md` - 组件库
- `references/deployment.md` - 部署到云端渲染

## 学习资源

- 官方文档: https://www.remotion.dev/docs
- 示例项目: https://github.com/remotion-dev/remotion/tree/main/packages/example
- 社区模板: https://github.com/remotion-dev/template-*
