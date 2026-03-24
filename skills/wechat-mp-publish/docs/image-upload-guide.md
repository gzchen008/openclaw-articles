# 微信公众号图片上传完整指南

## 📌 核心规则

**⚠️ 所有文章中的图片 URL 必须来自微信服务器！**

外部 URL（GitHub、图床、CDN）会被微信过滤，导致图片无法显示。

## 🚀 快速开始

### 1. 上传单张图片

```bash
cd /Users/cgz/.openclaw/workspace

# 上传图片
python skills/wechat-mp-publish/scripts/wechat_publisher.py upload image.jpg --type image

# 返回示例：
# ✅ 上传成功!
#    url: http://mmbiz.qpic.cn/sz_mmbiz_jpg/...
```

### 2. 批量上传图片

```bash
# 上传目录下所有 JPG 图片
python skills/wechat-mp-publish/scripts/upload_images.py images/ --pattern "*.jpg"

# 输出：
# 📤 找到 5 张图片
# [1/5] 上传: image1.jpg
#    ✅ http://mmbiz.qpic.cn/...
# [2/5] 上传: image2.jpg
#    ✅ http://mmbiz.qpic.cn/...
```

### 3. 替换 HTML 中的图片 URL

```bash
# 上传图片 + 替换 HTML
python skills/wechat-mp-publish/scripts/upload_images.py images/ \
  --html article.html \
  --output article-wechat.html \
  --save-map image-map.json

# 输出：
# 📤 找到 5 张图片
# [1/5] 上传: image1.jpg
#    ✅ http://mmbiz.qpic.cn/...
# ...
# 🔄 替换 HTML: article.html
# ✅ 替换: image1.jpg → 微信 URL
# 💾 已保存: article-wechat.html
```

## 📋 图片要求

### 文件格式

| 格式 | 支持 | 推荐场景 |
|------|------|----------|
| JPG | ✅ | 照片、截图、复杂图片 |
| PNG | ✅ | 图表、Logo、透明背景 |
| GIF | ✅ | 动图（但会被转为静态图） |
| WebP | ❌ | 不支持 |

### 文件大小

| 类型 | 限制 | 建议 |
|------|------|------|
| thumb（封面） | 64KB | 压缩到 < 50KB |
| image（内容） | 无明确限制 | 建议 < 1MB |

### 图片尺寸

| 场景 | 推荐尺寸 | 说明 |
|------|----------|------|
| 文章内容图 | 900px 宽 | 适配手机屏幕 |
| 封面图 | 900x383px（2.35:1） | 公众号推荐比例 |
| Logo/图标 | 200x200px | 正方形 |

## 🔧 工具命令

### wechat_publisher.py

```bash
# 上传图文内图片（文章内容中的图片）
python scripts/wechat_publisher.py upload image.jpg --type image

# 上传封面缩略图（用于草稿封面）
python scripts/wechat_publisher.py upload cover.jpg --type thumb

# 查看帮助
python scripts/wechat_publisher.py upload --help
```

### upload_images.py（批量工具）

```bash
# 上传单张图片
python scripts/upload_images.py image.jpg

# 批量上传（按模式匹配）
python scripts/upload_images.py images/ --pattern "*.png"

# 上传 + 替换 HTML
python scripts/upload_images.py images/ \
  --html article.html \
  --output article-wechat.html

# 保存图片映射
python scripts/upload_images.py images/ \
  --save-map image-map.json
```

## 📝 HTML 图片使用

### 标准格式

```html
<img src="http://mmbiz.qpic.cn/sz_mmbiz_jpg/..."
     style="max-width: 100%; display: block; margin: 16px auto;"
     alt="图片描述" />
```

### 带标题的图片

```html
<figure style="text-align: center; margin: 20px 0;">
  <img src="http://mmbiz.qpic.cn/..." style="max-width: 100%;" />
  <p style="font-size: 14px; color: #666; margin-top: 8px;">图片说明文字</p>
</figure>
```

### 多图排版

```html
<div style="display: flex; gap: 8px; margin: 16px 0;">
  <img src="..." style="flex: 1; max-width: 50%;" />
  <img src="..." style="flex: 1; max-width: 50%;" />
</div>
```

## ⚠️ 常见问题

### 1. 图片上传失败

**错误**: `invalid credential, access_token is invalid`

**解决**:
```bash
# 删除 token 缓存
rm -f /tmp/wechat_token.json

# 重新上传
python scripts/wechat_publisher.py upload image.jpg --type image
```

### 2. 图片太大

**错误**: `file size exceed`

**解决**:
```bash
# 使用 ImageMagick 压缩
convert input.jpg -resize 900x -quality 85 output.jpg

# 或使用 Python PIL
from PIL import Image
img = Image.open("input.jpg")
img.thumbnail((900, 2000))
img.save("output.jpg", quality=85)
```

### 3. 图片显示不出来

**原因**:
1. 使用了外部 URL（GitHub、图床）
2. 图片 URL 未替换
3. 图片上传失败

**检查清单**:
```bash
# 1. 检查 HTML 中的图片 URL
grep -o 'src="[^"]*"' article.html | grep -v mmbiz.qpic.cn

# 2. 检查图片映射
cat image-map.json

# 3. 验证图片 URL
curl -I "http://mmbiz.qpic.cn/..."
```

## 🔄 完整工作流

### 手动流程

```bash
# 1. 准备图片
mkdir -p images
# 放入图片文件

# 2. 上传图片
python scripts/upload_images.py images/ --save-map image-map.json

# 3. 检查映射
cat image-map.json

# 4. 替换 HTML
python scripts/upload_images.py images/ \
  --html article.html \
  --output article-wechat.html

# 5. 创建草稿
python scripts/wechat_publisher.py draft \
  --title "标题" \
  --content article-wechat.html \
  --thumb cover.jpg
```

### 自动化流程（Python）

```python
import os
from pathlib import Path
from wechat_publisher import WeChatPublisher

# 初始化
publisher = WeChatPublisher()

# 1. 上传图片
image_dir = Path("images")
image_map = {}

for image_path in image_dir.glob("*.jpg"):
    print(f"上传: {image_path.name}")
    url = publisher.upload_image(str(image_path), "image")
    image_map[image_path.name] = url
    print(f"  ✅ {url[:50]}...")

# 2. 替换 HTML
html_file = Path("article.html")
content = html_file.read_text(encoding="utf-8")

for filename, url in image_map.items():
    content = content.replace(filename, url)

# 3. 保存
output_file = Path("article-wechat.html")
output_file.write_text(content, encoding="utf-8")

# 4. 上传封面
cover_url = publisher.upload_image("cover.jpg", "thumb")
media_id = cover_url["media_id"]

# 5. 创建草稿
draft_id = publisher.create_draft(
    title="标题",
    content=content,
    thumb_media_id=media_id
)

print(f"✅ 草稿创建成功: {draft_id}")
```

## 📊 性能优化

### 批量上传优化

```bash
# 并发上传（使用 GNU Parallel）
ls images/*.jpg | parallel -j 3 \
  python scripts/wechat_publisher.py upload {} --type image
```

### 图片压缩

```bash
# 批量压缩（ImageMagick）
mkdir -p compressed
for img in images/*.jpg; do
  convert "$img" -resize 900x -quality 85 "compressed/$(basename $img)"
done
```

### 缓存管理

```bash
# 查看 token 缓存
cat /tmp/wechat_token.json

# 清除缓存（如果 token 失效）
rm -f /tmp/wechat_token.json
```

## 📚 相关文档

- [SKILL.md](../SKILL.md) - 技能主文档
- [wechat_publisher.py](../scripts/wechat_publisher.py) - 发布脚本
- [upload_images.py](../scripts/upload_images.py) - 批量上传工具

---

**最后更新**: 2026-03-10
**维护者**: 小J
