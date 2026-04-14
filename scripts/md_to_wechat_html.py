#!/usr/bin/env python3
"""
Markdown 转微信公众号 HTML 转换器
"""
import re
import sys
from pathlib import Path


def convert_markdown_to_wechat_html(md_content: str) -> str:
    """将 Markdown 转换为微信公众号兼容的 HTML"""
    
    # 移除 YAML front matter
    md_content = re.sub(r'^---\n.*?\n---\n', '', md_content, flags=re.DOTALL)
    
    # 处理标题（紧凑间距）
    md_content = re.sub(r'^### (.+)$', r'<h3 style="font-size: 16px; font-weight: bold; margin: 16px 0 8px 0; color: #333;">\1</h3>', md_content, flags=re.MULTILINE)
    md_content = re.sub(r'^## (.+)$', r'<h2 style="font-size: 18px; font-weight: bold; margin: 20px 0 10px 0; color: #1a1a1a;">\1</h2>', md_content, flags=re.MULTILINE)
    md_content = re.sub(r'^# (.+)$', r'<h1 style="font-size: 22px; font-weight: bold; margin: 0 0 12px 0; color: #000; text-align: center;">\1</h1>', md_content, flags=re.MULTILINE)
    
    # 处理引用块（紧凑样式）
    md_content = re.sub(r'^> (.+)$', r'<blockquote style="background: #f8f9fa; border-left: 3px solid #4a90e2; padding: 8px 12px; margin: 10px 0; color: #555; font-size: 14px;">\1</blockquote>', md_content, flags=re.MULTILINE)
    
    # 处理粗体
    md_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', md_content)
    
    # 处理行内代码
    md_content = re.sub(r'`(.+?)`', r'<code style="background: #f5f5f5; padding: 2px 4px; border-radius: 2px; font-family: monospace; font-size: 13px; color: #e83e8c;">\1</code>', md_content)
    
    # 处理代码块（紧凑样式）
    md_content = re.sub(r'```(\w+)?\n(.*?)\n```', r'<pre style="background: #282c34; color: #abb2bf; padding: 12px; border-radius: 4px; overflow-x: auto; margin: 10px 0; font-size: 13px; line-height: 1.5;"><code>\2</code></pre>', md_content, flags=re.DOTALL)
    
    # 处理列表项（紧凑间距，去掉黑点）
    md_content = re.sub(r'^- (.+)$', r'<p style="padding-left: 16px; margin: 4px 0; font-size: 15px; line-height: 1.6;">\1</p>', md_content, flags=re.MULTILINE)
    md_content = re.sub(r'^(\d+)\. (.+)$', r'<p style="padding-left: 16px; margin: 4px 0; font-size: 15px; line-height: 1.6;">\1. \2</p>', md_content, flags=re.MULTILINE)
    
    # 处理表格（简化为段落）
    lines = md_content.split('\n')
    in_table = False
    table_lines = []
    result_lines = []
    
    for line in lines:
        if '|' in line and not line.strip().startswith('<'):
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(line)
        else:
            if in_table:
                # 转换表格
                if table_lines:
                    result_lines.append('<div style="background: #f9f9f9; padding: 8px 12px; border-radius: 4px; margin: 8px 0; font-size: 14px; line-height: 1.5;">')
                    for tl in table_lines:
                        if not re.match(r'^\s*\|[-:]+\|', tl):
                            cells = [c.strip() for c in tl.split('|') if c.strip()]
                            if cells:
                                result_lines.append(' • '.join(cells))
                    result_lines.append('</div>')
                in_table = False
                table_lines = []
            result_lines.append(line)
    
    md_content = '\n'.join(result_lines)
    
    # 处理水平线
    md_content = re.sub(r'^---$', r'<hr style="border: none; border-top: 1px solid #e0e0e0; margin: 24px 0;">', md_content, flags=re.MULTILINE)
    
    # 处理段落
    paragraphs = md_content.split('\n\n')
    html_paragraphs = []
    
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        
        # 如果已经是 HTML 标签，保持原样
        if p.startswith('<'):
            html_paragraphs.append(p)
        else:
            # 否则包装成段落（紧凑间距）
            html_paragraphs.append(f'<p style="margin: 8px 0; font-size: 15px; line-height: 1.6; color: #333;">{p}</p>')
    
    html_content = '\n\n'.join(html_paragraphs)
    
    # 包装完整 HTML
    full_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文章</title>
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; line-height: 1.8; color: #333; padding: 20px; max-width: 100%; margin: 0 auto;">
{html_content}
</body>
</html>'''
    
    return full_html


def main():
    if len(sys.argv) < 2:
        print("用法: python md_to_wechat_html.py <markdown_file>")
        sys.exit(1)
    
    md_file = Path(sys.argv[1])
    if not md_file.exists():
        print(f"文件不存在: {md_file}")
        sys.exit(1)
    
    md_content = md_file.read_text(encoding='utf-8')
    html_content = convert_markdown_to_wechat_html(md_content)
    
    # 保存 HTML 文件
    html_file = md_file.with_suffix('.html')
    html_file.write_text(html_content, encoding='utf-8')
    
    print(f"✅ HTML 文件已生成: {html_file}")
    print(f"   文件大小: {len(html_content)} 字符")


if __name__ == '__main__':
    main()
