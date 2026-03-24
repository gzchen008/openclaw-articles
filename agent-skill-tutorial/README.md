# Agent Skill Tutorial - Remotion Video

使用 Remotion 制作的 Agent Skill 编写教程视频（90秒）

## 项目结构

```
agent-skill-tutorial/
├── src/
│   ├── index.ts                    # 入口文件
│   ├── Root.tsx                    # Remotion 根组件
│   ├── AgentSkillTutorial.tsx      # 主视频组件
│   └── scenes/
│       ├── TitleScene.tsx          # 场景1: 开场标题
│       ├── ConceptScene.tsx        # 场景2: 核心概念
│       ├── CreateSkillScene.tsx    # 场景3: 创建 Skill
│       ├── ThreeLayersScene.tsx    # 场景4: 三层架构
│       ├── ReferenceScene.tsx      # 场景5: Reference 示例
│       ├── ScriptScene.tsx         # 场景6: Script 示例
│       ├── MCPCompareScene.tsx     # 场景7: MCP 对比
│       └── EndScene.tsx            # 场景8: 结尾
├── package.json
├── remotion.config.ts
└── README.md
```

## 安装

```bash
cd ~/.openclaw/workspace/agent-skill-tutorial
npm install
```

## 运行

### 1. 启动开发服务器

```bash
npm start
```

浏览器会自动打开 Remotion Studio，可以实时预览视频。

### 2. 渲染视频

```bash
npm run build
```

视频会保存到 `out/video.mp4`

## 视频信息

- **时长**: 90 秒（2700 帧）
- **分辨率**: 1920x1080 (16:9)
- **帧率**: 30 FPS
- **格式**: MP4

## 场景时长

| 场景 | 时长 | 内容 |
|------|------|------|
| 1. 开场标题 | 0-3秒 | Logo + 标题 |
| 2. 核心概念 | 3-8秒 | 什么是 Agent Skill |
| 3. 创建 Skill | 8-18秒 | skill.md 创建步骤 |
| 4. 三层架构 | 18-35秒 | 渐进式披露机制 |
| 5. Reference | 35-50秒 | 条件读取示例 |
| 6. Script | 50-65秒 | 自动执行代码 |
| 7. MCP 对比 | 65-80秒 | MCP vs Skill |
| 8. 结尾 | 80-90秒 | 引导关注 |

## 自定义

### 修改颜色

编辑各场景文件中的颜色值：
- 主色调: `#667eea` (紫色)
- 次色调: `#764ba2` (深紫)
- 强调色: `#f093fb` (粉紫)
- 背景色: `#1a1a2e` (深蓝)

### 修改文字

编辑各场景文件中的文本内容。

### 调整时长

在 `AgentSkillTutorial.tsx` 中修改 `durationInFrames` 参数。

### 添加背景音乐

```tsx
import { Audio } from "remotion";

// 在组件中添加
<Audio src="/path/to/music.mp3" />
```

### 添加配音

```tsx
import { Audio } from "remotion";

// 在对应场景添加
<Audio src="/path/to/voiceover.mp3" />
```

## 导出其他格式

### GIF

```bash
npx remotion render AgentSkillTutorial out/video.gif --codec gif
```

### WebM

```bash
npx remotion render AgentSkillTutorial out/video.webm --codec vp8
```

### 竖屏版本（9:16）

修改 `Root.tsx`:

```tsx
<Composition
  id="AgentSkillTutorial"
  component={AgentSkillTutorial}
  durationInFrames={5400}
  fps={30}
  width={1080}   // 改为 1080
  height={1920}  // 改为 1920
/>
```

## 技术栈

- **Remotion 4.0**: React 视频生成框架
- **React 18**: UI 组件
- **TypeScript**: 类型安全

## 常见问题

### Q: 如何添加新的场景？

1. 在 `src/scenes/` 创建新的场景组件
2. 在 `AgentSkillTutorial.tsx` 中导入并添加 `<Sequence>`
3. 调整时间轴和时长

### Q: 如何添加过渡效果？

使用 Remotion 的 `interpolate` 和 `spring` 函数：

```tsx
const opacity = interpolate(frame, [0, 30], [0, 1]);

const scale = spring({
  frame,
  fps: 30,
  config: {
    damping: 100,
    stiffness: 200,
  },
});
```

### Q: 如何导出为抖音格式？

修改分辨率为 1080x1920，时长控制在 60 秒内。

## 许可证

MIT

---

**制作时间**: 2026-03-08
**作者**: 小J (OpenClaw Agent)
