#!/usr/bin/env python3
"""
Markdown 转微信公众号 HTML 工具

功能：
1. 读取 Markdown 文件
2. 转换成符合公众号规范的 HTML（处理列表、代码块、加粗等）
3. 可选：直接上传到微信草稿

使用方法：
# 仅转换
python md_to_wechat_html.py article.md -o article.html

# 转换 + 上传
python md_to_wechat_html.py article.md --upload --title "标题" --thumb cover.jpg

# 转换 + 上传 + 发布
python md_to_wechat_html.py article.md --publish --title "标题" --thumb cover.jpg
"""

import re
import sys
import argparse
from pathlib import Path


def convert_md_to_wechat_html(md_content: str, title: str = None) -> str:
    """
    将 Markdown 转换为符合微信公众号规范的 HTML
    
    Args:
        md_content: Markdown 内容
        title: 文章标题（可选，用于 H1）
    
    Returns:
        符合公众号规范的 HTML
    """
    html = md_content
    
    # 1. 移除 YAML frontmatter
    html = re.sub(r'^---\n.*?\n---\n', '', html, flags=re.DOTALL)
    
    # 2. 转换标题
    if title:
        html = re.sub(r'^# .+$', '', html, flags=re.MULTILINE)  # 移除原 H1
        html = f'<h1 style="margin-top: 0; margin-bottom: 20px; font-size: 24px; font-weight: 600; color: #24292e; text-align: center;">{title}</h1>\n\n{html}'
    
    # 转换标题（注意顺序：从高到低）
    html = re.sub(r'^#### (.+)$', r'<h4 style="margin-top: 20px; margin-bottom: 10px; font-size: 16px; font-weight: 600; color: #24292e;">\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3 style="margin-top: 24px; margin-bottom: 12px; font-size: 18px; font-weight: 600; color: #24292e; border-bottom: 1px solid #eaecef; padding-bottom: 8px;">\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2 style="margin-top: 28px; margin-bottom: 16px; font-size: 20px; font-weight: 600; color: #24292e; border-bottom: 1px solid #eaecef; padding-bottom: 8px;">\1</h2>', html, flags=re.MULTILINE)
    
    # 3. 转换引用块（高亮提示）
    # 先处理多行引用块（合并为一行）
    def replace_multiline_blockquote(match):
        lines = match.group(0).strip().split('\n')
        content_parts = []
        for line in lines:
            line = line.strip()
            if line.startswith('> '):
                content_parts.append(line[2:])
            elif line == '>':
                continue  # 跳过空引用行
        
        content = ' '.join(content_parts)
        if not content:
            return ''
        
        # 判断是否是警告类型
        if '警告' in content or '注意' in content or '⚠️' in content:
            return f'<p style="margin: 12px 0; padding: 8px; background: #fff4e6; border-left: 4px solid #f66; color: #24292e;"><strong style="font-weight: 600;">{content}</strong></p>'
        else:
            return f'<p style="margin: 12px 0; padding: 12px; background: #f1f8ff; border-left: 4px solid #0366d6; color: #24292e; font-style: italic;">{content}</p>'
    
    # 匹配连续的引用块（包括空行）
    html = re.sub(r'((?:^>.*$\n?)+)', replace_multiline_blockquote, html, flags=re.MULTILINE)
    
    # 4. 转换粗体
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong style="font-weight: 600;">\1</strong>', html)
    
    # 5. 先转换代码块（必须先于行内代码）
    def replace_code_block(match):
        lang = match.group(1) or ''
        code = match.group(2).strip()
        # 转义 HTML 特殊字符
        code = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        # 按行分割并添加样式
        lines = code.split('\n')
        code_html = '\n'.join([f'<p style="margin: 0; font-family: monospace; font-size: 14px; color: #24292e;">{line}</p>' for line in lines])
        return f'<section style="background: #f6f8fa; padding: 12px; border-radius: 6px; margin: 8px 0;">{code_html}</section>'
    
    html = re.sub(r'```(\w*)\n(.*?)```', replace_code_block, html, flags=re.DOTALL)
    
    # 6. 再转换行内代码
    html = re.sub(r'`([^`]+)`', r'<code style="background: #f6f8fa; padding: 2px 6px; border-radius: 3px; font-family: monospace; font-size: 14px;">\1</code>', html)
    
    # 7. 转换列表（使用 p 标签，避免多余黑点）
    def replace_unordered_list(match):
        items = match.group(0)
        items = re.sub(r'^- (.+)$', r'<p style="margin: 4px 0; padding-left: 20px;">• \1</p>', items, flags=re.MULTILINE)
        return items
    
    def replace_ordered_list(match):
        items = match.group(0)
        counter = [0]  # 使用列表以便在闭包中修改
        def add_number(m):
            counter[0] += 1
            return f'<p style="margin: 4px 0; padding-left: 20px;">{counter[0]}. {m.group(1)}</p>'
        items = re.sub(r'^\d+\. (.+)$', add_number, items, flags=re.MULTILINE)
        return items
    
    html = re.sub(r'((?:^- .+$\n?)+)', replace_unordered_list, html, flags=re.MULTILINE)
    html = re.sub(r'((?:^\d+\. .+$\n?)+)', replace_ordered_list, html, flags=re.MULTILINE)
    
    # 7.5. 转换 Markdown 表格
    def replace_table(match):
        table_text = match.group(0)
        lines = [line.strip() for line in table_text.strip().split('\n') if line.strip()]
        
        if len(lines) < 2:
            return table_text
        
        # 解析表头
        header_line = lines[0]
        if not header_line.startswith('|'):
            return table_text
        
        headers = [cell.strip() for cell in header_line.split('|')[1:-1]]
        
        # 跳过分隔行（第二行）
        data_lines = lines[2:] if len(lines) > 2 else []
        
        # 构建 HTML 表格
        table_html = '<table style="width: 100%; border-collapse: collapse; margin: 12px 0;">\n'
        
        # 表头
        table_html += '<thead>\n<tr>\n'
        for header in headers:
            table_html += f'<th style="background: #f6f8fa; padding: 12px; border: 1px solid #d0d7de; text-align: left; font-weight: 600;">{header}</th>\n'
        table_html += '</tr>\n</thead>\n'
        
        # 表体
        if data_lines:
            table_html += '<tbody>\n'
            for line in data_lines:
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                table_html += '<tr>\n'
                for cell in cells:
                    table_html += f'<td style="padding: 12px; border: 1px solid #d0d7de;">{cell}</td>\n'
                table_html += '</tr>\n'
            table_html += '</tbody>\n'
        
        table_html += '</table>'
        return table_html
    
    # 匹配表格（以 | 开头的连续行）
    html = re.sub(r'((?:^\|.*\|$\n?)+)', replace_table, html, flags=re.MULTILINE)
    
    # 8. 转换分隔线
    html = re.sub(r'^---$', r'<hr style="border: none; border-top: 1px solid #eaecef; margin: 24px 0;">', html, flags=re.MULTILINE)
    
    # 9. 转换链接
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" style="color: #0366d6; text-decoration: none;">\1</a>', html)
    
    # 10. 转换段落
    lines = html.split('\n')
    result = []
    
    for line in lines:
        stripped = line.strip()
        
        # 跳过已转换的标签
        if stripped.startswith('<') or not stripped:
            result.append(line)
            continue
        
        # 普通文本转段落
        result.append(f'<p style="margin: 8px 0;">{line}</p>')
    
    html = '\n'.join(result)
    
    # 11. 清理多余的空段落
    html = re.sub(r'<p style="[^"]*">\s*</p>', '', html)
    
    # 12. 包装完整的 HTML 文档
    html_template = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{title or '文章'}</title>
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; font-size: 16px; line-height: 1.6; color: #24292e; max-width: 100%; padding: 20px;">

{html}

</body>
</html>"""
    
    return html_template


def main():
    parser = argparse.ArgumentParser(description='Markdown 转微信公众号 HTML 工具')
    parser.add_argument('md_file', help='Markdown 文件路径')
    parser.add_argument('-o', '--output', help='输出 HTML 文件路径（默认：同名 .html）')
    parser.add_argument('--title', help='文章标题')
    parser.add_argument('--upload', action='store_true', help='上传到微信草稿')
    parser.add_argument('--publish', action='store_true', help='直接发布（需要先上传）')
    parser.add_argument('--thumb', help='封面图片路径')
    parser.add_argument('--author', default='小J', help='作者名')
    parser.add_argument('--digest', help='文章摘要')
    
    args = parser.parse_args()
    
    # 读取 Markdown 文件
    md_path = Path(args.md_file)
    if not md_path.exists():
        print(f"❌ 文件不存在: {args.md_file}")
        sys.exit(1)
    
    md_content = md_path.read_text(encoding='utf-8')
    
    # 提取标题（如果没有提供）
    if not args.title:
        title_match = re.search(r'^# (.+)$', md_content, re.MULTILINE)
        args.title = title_match.group(1) if title_match else md_path.stem
    
    # 转换为 HTML
    html_content = convert_md_to_wechat_html(md_content, args.title)
    
    # 保存 HTML 文件
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = md_path.with_suffix('.html')
    
    output_path.write_text(html_content, encoding='utf-8')
    print(f"✅ HTML 已保存: {output_path}")
    
    # 上传到微信
    if args.upload or args.publish:
        if not args.thumb:
            print("❌ 上传需要提供封面图片路径 (--thumb)")
            sys.exit(1)
        
        # 调用 wechat_publisher.py
        import subprocess
        
        cmd = [
            'python3', 'skills/wechat-mp-publish/scripts/wechat_publisher.py',
            'draft' if not args.publish else 'auto',
            '--title', args.title,
            '--content', str(output_path),
            '--thumb', args.thumb,
            '--author', args.author
        ]
        
        if args.digest:
            cmd.extend(['--digest', args.digest])
        
        print(f"\n📤 上传到微信...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f"❌ 上传失败:\n{result.stderr}")
            sys.exit(1)


if __name__ == '__main__':
    main()
