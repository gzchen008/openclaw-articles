# 视频生成规范

## 📐 分辨率标准

### 横屏（默认）
- **分辨率**：1920x1080 (16:9)
- **适用**：YouTube、B站、电脑播放
- **布局**：横向卡片、左右排列

### 竖屏（手机播放）
- **分辨率**：1080x1920 (9:16)
- **适用**：抖音、快手、小红书、微信视频号、Instagram Stories
- **布局**：纵向卡片、上下排列、2x2网格

## 🎬 视频结构标准

### 场景数量
- **7个场景**（标准配置）
- 封面场景：90 帧（3秒）
- 其他场景：150-180 帧（5-6秒）
- 总时长：33-34秒

### 场景顺序
1. **品牌封面** - AI工作流封面图（固定3秒）
2. **痛点场景** - 展示问题/需求
3. **功能介绍** - 核心功能说明
4. **实战案例** - 3个对比案例
5. **资源推荐** - GitHub项目/工具
6. **效率对比** - 数据可视化
7. **行动号召** - 下一步建议 + 预告

### 封面图要求
- **文件位置**：`articles/video-cover.jpg`
- **显示时长**：3秒（90帧）
- **动画效果**：淡入淡出
- **强制要求**：所有文章生成的视频必须以封面图开头

## 🎨 设计规范

### 颜色方案
- **背景色**：#1a1a1a（深黑）
- **主色**：#4CAF50（绿色）
- **强调色**：#ff6b6b（红色）
- **文字色**：#fff（白色）、#ccc（灰色）
- **卡片背景**：#2a2a2a

### 字体大小（横屏）
- 标题：60px
- 副标题：40px
- 正文：28-32px
- 小字：18-22px

### 字体大小（竖屏）
- 标题：48px
- 副标题：32px
- 正文：22-26px
- 小字：16-18px

### 动画效果
- 淡入淡出：interpolate opacity [0, 1]
- 位移动画：translateX/translateY
- 缩放动画：scale [0.8, 1]
- Spring 弹性动画：spring({fps, config})

## 📁 文件组织

### 项目结构
```
~/.openclaw/workspace/remotion/[project-name]/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts
│   ├── Root.tsx
│   └── [VideoName].tsx
└── out/
    └── video.mp4
```

### 命名规范
- **项目文件夹**：[主题]-video（如 browser-automation-video）
- **组件名**：[主题]Video（如 BrowserAutomationVideo）
- **输出文件**：video.mp4
- **最终文件**：[主题]-video[-vertical].mp4

## 🔄 工作流程

### 1. 创建项目
```bash
mkdir -p ~/.openclaw/workspace/remotion/[project-name]
# 创建 package.json、tsconfig.json、src/ 文件
```

### 2. 安装依赖
```bash
cd ~/.openclaw/workspace/remotion/[project-name]
npm install
```

### 3. 渲染视频
```bash
npm run render
```

### 4. 复制到 media 目录
```bash
cp out/video.mp4 ~/.openclaw/media/[filename].mp4
```

### 5. 发送到 Discord
```bash
# 使用 message tool
# path: ~/.openclaw/media/[filename].mp4
# target: channel:CHANNEL_ID
```

## ⚙️ 配置参数

### package.json
```json
{
  "scripts": {
    "render": "remotion render src/index.ts [CompositionName] out/video.mp4"
  }
}
```

### Root.tsx
```tsx
<Composition
  id="[CompositionName]"
  component={[VideoComponent]}
  durationInFrames={900}  // 30秒 @ 30fps
  fps={30}
  width={1920}  // 横屏
  height={1080} // 横屏
/>
```

**竖屏配置**：
```tsx
  width={1080}  // 竖屏
  height={1920} // 竖屏
```

## 📊 内容来源

### 文章转视频
- **源文件**：`articles/[date]-[title].md`
- **提取重点**：
  - 痛点（3-4个）
  - 解决方案（2-3个）
  - 实战案例（3个）
  - 数据对比（3组）
  - 行动建议（3步）

### 文字精简原则
- 每个场景核心信息不超过 5 条
- 单行文字不超过 20 字
- 使用 emoji 图标增强视觉效果
- 数字用大字号突出显示

## 🎯 质量检查

### 渲染前
- [ ] 检查 Composition id 是否正确
- [ ] 检查分辨率设置（横屏/竖屏）
- [ ] 检查所有文字内容无错误
- [ ] 检查动画时序合理

### 渲染后
- [ ] 播放视频检查流畅度
- [ ] 检查文字是否清晰可读
- [ ] 检查动画效果是否符合预期
- [ ] 检查文件大小（通常 1.5-3MB）

## 📝 模板复用

### 已有项目
- `browser-automation-video` - 浏览器自动化（横屏+竖屏）
- `meeting-minutes-video` - 会议纪要（横屏）

### 复用步骤
1. 复制整个项目文件夹
2. 修改 `src/[VideoName].tsx` 内容
3. 修改 `package.json` 名称和描述
4. 修改 `Root.tsx` 中的 Composition id
5. 运行 `npm install` 和 `npm run render`

## 🔧 常见问题

### Q: 如何调整视频时长？
A: 修改 `durationInFrames` 参数（帧数 = 秒数 × 30fps）

### Q: 如何修改动画速度？
A: 调整 `interpolate` 中的帧数范围，或修改 `delay` 值

### Q: 如何添加新场景？
A: 
1. 创建新的 Scene 组件
2. 在主组件中添加 `<Sequence>`
3. 调整后续场景的 `from` 参数

### Q: 横屏转竖屏需要改什么？
A:
1. 修改 width/height 为 1080x1920
2. 调整所有横向布局为纵向
3. 缩小字体大小
4. 调整 padding 和 margin

## 📚 参考资料

- [Remotion 官方文档](https://www.remotion.dev/docs)
- [OpenClaw 视频生成技能](../remotion/SKILL.md)
- [文章转视频最佳实践](./article-to-video-guide.md)

---

**最后更新**：2026-02-18
**维护者**：小J
