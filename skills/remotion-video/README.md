# Remotion Video Skill

Remotion 视频生成技能 - 使用 React 组件生成专业视频。

## 安装

```bash
# 安装 Remotion CLI
npm install -g @remotion/cli

# 或使用项目本地安装
cd ~/.openclaw/workspace/skills/remotion-video
npm install
```

## 使用方法

### 1. 从文本生成视频

```bash
./scripts/generate.sh --title "视频标题" --content "内容文本" --output video.mp4
```

### 2. 从文章生成视频

```bash
./scripts/generate.sh --article /path/to/article.md --output video.mp4
```

### 3. 使用配置文件

```bash
# 创建视频配置
cp templates/example-config.json my-video-config.json

# 编辑配置
# ...

# 生成视频
./scripts/generate.sh --config my-video-config.json --output video.mp4
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--title` | 视频标题 | 必填 |
| `--content` | 文本内容 | 可选 |
| `--article` | Markdown 文章路径 | 可选 |
| `--output` | 输出文件路径 | `out/video.mp4` |
| `--format` | `vertical` 或 `horizontal` | `vertical` |
| `--duration` | 每个场景时长（秒） | `5` |
| `--cover` | 封面图片路径 | 可选 |

## 场景类型

### 1. 封面场景 (cover)

```json
{
  "type": "cover",
  "title": "标题",
  "data": { "subtitle": "副标题" },
  "duration": 3
}
```

### 2. 文本场景 (text)

```json
{
  "type": "text",
  "title": "标题",
  "data": {
    "lines": ["第一行", "第二行", "第三行"]
  },
  "duration": 5
}
```

### 3. 卡片场景 (card)

```json
{
  "type": "card",
  "title": "标题",
  "data": {
    "cards": [
      { "title": "卡片1", "content": "内容1", "color": "#4CAF50" },
      { "title": "卡片2", "content": "内容2", "color": "#2196F3" }
    ]
  },
  "duration": 5
}
```

### 4. 对比场景 (comparison)

```json
{
  "type": "comparison",
  "title": "对比标题",
  "data": {
    "comparisons": [
      { "left": "旧方案问题", "right": "新方案优势" }
    ]
  },
  "duration": 5
}
```

### 5. CTA 场景 (cta)

```json
{
  "type": "cta",
  "title": "行动号召",
  "data": {
    "steps": ["步骤1", "步骤2", "步骤3"]
  },
  "duration": 5
}
```

## 动画规则

⚠️ **重要** - 遵循以下规则避免渲染问题：

1. **只使用 opacity 淡入**：元素出现时 `opacity: 0 → 1`
2. **禁止位置动画**：`translateY`/`translateX` 会导致遮挡
3. **禁止缩放动画**：`scale` 会导致边界问题
4. **固定位置**：所有元素位置不变，只改透明度
5. **居中对齐**：使用 `justifyContent: 'center'` + `alignItems: 'center'`

## 常见问题

### Chrome Headless Shell 下载慢

使用系统 Chrome：

```bash
export REMOTION_CHROME_EXECUTABLE="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
```

### WebSocket 错误

降低并发：

```bash
npx remotion render src/index.ts Video out/video.mp4 --concurrency 1
```

### staticFile() 错误

静态文件放在 `public/` 目录，不要用相对路径：

```tsx
// ❌ 错误
<Img src={staticFile('../../../articles/cover.jpg')} />

// ✅ 正确
<Img src={staticFile('cover.jpg')} />
```

## 文件结构

```
skills/remotion-video/
├── SKILL.md                    # 技能说明
├── README.md                   # 本文件
├── scripts/
│   └── generate.sh             # 生成脚本
├── templates/
│   ├── VideoTemplate.tsx       # 视频组件模板
│   └── example-config.json     # 示例配置
└── src/                        # 源代码
```

---

**创建日期**：2026-03-09
**作者**：小J
