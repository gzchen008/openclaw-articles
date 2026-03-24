---
name: remotion-video
description: Generate videos from text/articles using Remotion (React-based video renderer). Supports vertical (9:16) and horizontal (16:9) formats.
homepage: https://remotion.dev
metadata:
  openclaw:
    emoji: "🎬"
    requires:
      bins: ["node", "npx"]
    install:
      - id: remotion-cli
        kind: npm
        package: "@remotion/cli"
        label: "Install Remotion CLI"
---

# Remotion Video Skill

Generate professional videos from text or articles using Remotion.

## Quick Start

### Generate video from text

```bash
{baseDir}/scripts/generate.sh --title "标题" --content "内容文本" --output video.mp4
```

### Generate video from article

```bash
{baseDir}/scripts/generate.sh --article /path/to/article.md --output video.mp4
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--title` | Video title | Required |
| `--content` | Text content | Optional |
| `--article` | Path to markdown article | Optional |
| `--output` | Output file path | `out/video.mp4` |
| `--format` | `vertical` (9:16) or `horizontal` (16:9) | `vertical` |
| `--duration` | Duration per scene (seconds) | `5` |
| `--cover` | Path to cover image | Optional |

## Templates

### Vertical Video (9:16)
- Resolution: 1080x1920
- Best for: TikTok, Instagram Reels, YouTube Shorts, WeChat Video

### Horizontal Video (16:9)
- Resolution: 1920x1080
- Best for: YouTube, Bilibili, Presentations

## Scene Structure

Default video structure (7 scenes, ~33 seconds):

1. **Cover** (3s) - Brand/title card
2. **Pain Point** (5s) - Problem statement
3. **Concept** (5s) - Core concept introduction
4. **Solutions** (5s) - Multiple solutions
5. **Comparison** (5s) - Data comparison
6. **Code** (5s) - Technical implementation
7. **CTA** (5s) - Call to action

## Animation Rules

⚠️ **Important** - Follow these rules to avoid rendering issues:

1. **Only use opacity fade-in**: Elements appear with `opacity: 0 → 1`
2. **No position animations**: Avoid `translateY`/`translateX` (causes overlapping)
3. **No scale animations**: Avoid `scale` (causes boundary issues)
4. **Fixed positions**: All elements stay in place, only opacity changes
5. **Center everything**: Use `justifyContent: 'center'` + `alignItems: 'center'`

## Project Structure

```
~/.openclaw/workspace/remotion/[project-name]/
├── package.json
├── tsconfig.json
├── public/
│   └── cover.jpg          # Cover image
├── src/
│   ├── index.ts
│   ├── Root.tsx
│   └── Video.tsx          # Main video component
└── out/
    └── video.mp4
```

## Examples

### Generate promotional video

```bash
{baseDir}/scripts/generate.sh \
  --title "OpenClaw: AI Agent Framework" \
  --content "痛点:AI开发复杂|方案:OpenClaw简化|效果:效率提升10倍" \
  --format vertical \
  --output openclaw-promo.mp4
```

### Generate tutorial video from article

```bash
{baseDir}/scripts/generate.sh \
  --article articles/2026-03-09-openclaw-context-engine.md \
  --format vertical \
  --output context-engine-tutorial.mp4
```

## Troubleshooting

### Chrome Headless Shell download slow

Use system Chrome instead:

```bash
export REMOTION_CHROME_EXECUTABLE="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
```

### Rendering fails with WebSocket error

Reduce concurrency:

```bash
npx remotion render src/index.ts Video out/video.mp4 --concurrency 1
```

### staticFile() error

Put static files in `public/` folder, not relative paths:

```tsx
// ❌ Wrong
<Img src={staticFile('../../../articles/cover.jpg')} />

// ✅ Correct
<Img src={staticFile('cover.jpg')} />
```

## Dependencies

- Node.js 18+
- Remotion 4.0+
- Chrome/Chromium (for rendering)

---

**Created**: 2026-03-09
**Author**: 小J
