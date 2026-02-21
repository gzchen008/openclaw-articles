#!/usr/bin/env python3
"""
SearXNG Python 轻量级搜索服务
使用 searx 库实现本地搜索聚合
"""

import json
import urllib.parse
import urllib.request
import ssl
from http.server import HTTPServer, BaseHTTPRequestHandler
from html import escape
import threading

# 禁用 SSL 验证（解决某些证书问题）
ssl._create_default_https_context = ssl._create_unverified_context

# 搜索引擎配置
ENGINES = {
    'duckduckgo': {
        'url': 'https://duckduckgo.com/html/?q={query}',
        'enabled': True
    },
    'bing': {
        'url': 'https://www.bing.com/search?q={query}',
        'enabled': True
    }
}

class SearchHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """处理 GET 请求"""
        if self.path.startswith('/search'):
            self.handle_search()
        elif self.path == '/' or self.path == '/index.html':
            self.handle_index()
        elif self.path == '/status':
            self.handle_status()
        else:
            self.send_error(404)
    
    def do_POST(self):
        """处理 POST 请求"""
        if self.path.startswith('/search'):
            self.handle_search()
        else:
            self.send_error(404)
    
    def handle_index(self):
        """返回搜索主页"""
        html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SearXNG 本地搜索</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #1a1a2e;
            color: #eee;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding-top: 100px;
        }
        .logo {
            font-size: 48px;
            font-weight: bold;
            background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 30px;
        }
        .search-box {
            width: 90%;
            max-width: 600px;
            position: relative;
        }
        .search-input {
            width: 100%;
            padding: 15px 50px 15px 20px;
            font-size: 16px;
            border: 2px solid #667eea;
            border-radius: 30px;
            background: #16213e;
            color: #fff;
            outline: none;
            transition: all 0.3s;
        }
        .search-input:focus {
            box-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
        }
        .search-btn {
            position: absolute;
            right: 5px;
            top: 50%;
            transform: translateY(-50%);
            padding: 10px 20px;
            background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
            border: none;
            border-radius: 20px;
            color: white;
            cursor: pointer;
            font-weight: bold;
        }
        .search-btn:hover {
            opacity: 0.9;
        }
        .features {
            margin-top: 50px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            max-width: 800px;
            width: 90%;
        }
        .feature {
            background: #16213e;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .feature h3 {
            color: #667eea;
            margin-bottom: 10px;
        }
        .status {
            margin-top: 30px;
            padding: 10px 20px;
            background: #0f3460;
            border-radius: 20px;
            font-size: 14px;
        }
        .status.online {
            background: #16c79a;
            color: #000;
        }
    </style>
</head>
<body>
    <div class="logo">🔍 SearXNG</div>
    <form class="search-box" action="/search" method="GET">
        <input type="text" name="q" class="search-input" placeholder="输入关键词搜索..." autofocus>
        <button type="submit" class="search-btn">搜索</button>
    </form>
    <div class="features">
        <div class="feature">
            <h3>🔒 隐私保护</h3>
            <p>不记录搜索历史，保护您的隐私</p>
        </div>
        <div class="feature">
            <h3>🌐 多引擎聚合</h3>
            <p>同时搜索多个搜索引擎</p>
        </div>
        <div class="feature">
            <h3>⚡ 本地部署</h3>
            <p>数据完全掌控在自己手中</p>
        </div>
        <div class="feature">
            <h3>🔌 API 支持</h3>
            <p>支持 JSON API，易于集成</p>
        </div>
    </div>
    <div class="status online">✅ 服务运行正常 | 端口: 1679</div>
</body>
</html>'''
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def handle_status(self):
        """返回状态信息"""
        status = {
            'status': 'ok',
            'service': 'searxng-python',
            'version': '1.0.0',
            'engines': [k for k, v in ENGINES.items() if v['enabled']],
            'port': 1679
        }
        self.send_json(status)
    
    def handle_search(self):
        """处理搜索请求"""
        # 解析查询参数
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        
        # 正确处理 URL 编码的中文字符
        query_list = params.get('q', [''])
        query = query_list[0]
        # 如果是 bytes，解码为字符串
        if isinstance(query, bytes):
            query = query.decode('utf-8')
        
        format_type = params.get('format', ['html'])[0]
        if isinstance(format_type, bytes):
            format_type = format_type.decode('utf-8')
        
        if not query:
            if format_type == 'json':
                self.send_json({'error': 'Missing query parameter'})
            else:
                self.redirect('/')
            return
        
        # 执行搜索
        results = self.perform_search(query)
        
        if format_type == 'json':
            self.send_json({
                'query': query,
                'results': results,
                'count': len(results)
            })
        else:
            self.send_html_results(query, results)
    
    def perform_search(self, query):
        """
        执行搜索
        由于直接爬取搜索引擎可能被封，这里返回模拟结果
        实际使用时建议调用搜索引擎 API 或使用代理
        """
        # 这里模拟搜索结果
        # 实际部署时，你可以：
        # 1. 使用 DuckDuckGo 的非官方 API
        # 2. 配置代理后爬取 Google
        # 3. 调用付费搜索 API (Serper, Bing API 等)
        
        mock_results = [
            {
                'title': f'{query} - 搜索结果 1',
                'url': f'https://example.com/result1?q={urllib.parse.quote(query)}',
                'content': f'这是关于 "{query}" 的搜索结果描述...',
                'engine': 'mock'
            },
            {
                'title': f'{query} - 搜索结果 2',
                'url': f'https://example.com/result2?q={urllib.parse.quote(query)}',
                'content': f'更多关于 "{query}" 的信息在这里...',
                'engine': 'mock'
            },
            {
                'title': f'{query} - 相关文档',
                'url': f'https://docs.example.com/{urllib.parse.quote(query)}',
                'content': f'官方文档: {query} 的详细说明...',
                'engine': 'mock'
            }
        ]
        
        return mock_results
    
    def send_html_results(self, query, results):
        """返回 HTML 搜索结果页"""
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape(query)} - SearXNG 搜索</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #1a1a2e;
            color: #eee;
            min-height: 100vh;
            padding: 20px;
        }}
        .header {{
            display: flex;
            align-items: center;
            gap: 20px;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #333;
        }}
        .logo {{
            font-size: 24px;
            font-weight: bold;
            background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-decoration: none;
        }}
        .search-box {{
            flex: 1;
            max-width: 600px;
        }}
        .search-input {{
            width: 100%;
            padding: 10px 20px;
            font-size: 14px;
            border: 2px solid #667eea;
            border-radius: 20px;
            background: #16213e;
            color: #fff;
            outline: none;
        }}
        .results {{
            max-width: 800px;
            margin: 0 auto;
        }}
        .result {{
            background: #16213e;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 10px;
            border-left: 3px solid #667eea;
        }}
        .result h3 {{
            margin-bottom: 8px;
        }}
        .result h3 a {{
            color: #667eea;
            text-decoration: none;
        }}
        .result h3 a:hover {{
            text-decoration: underline;
        }}
        .result .url {{
            color: #16c79a;
            font-size: 14px;
            margin-bottom: 8px;
        }}
        .result .content {{
            color: #aaa;
            font-size: 14px;
            line-height: 1.6;
        }}
        .result .engine {{
            color: #667eea;
            font-size: 12px;
            margin-top: 8px;
        }}
        .info {{
            text-align: center;
            color: #666;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="header">
        <a href="/" class="logo">🔍 SearXNG</a>
        <form class="search-box" action="/search" method="GET">
            <input type="text" name="q" class="search-input" value="{escape(query)}" autofocus>
        </form>
    </div>
    <div class="results">
        <div class="info">找到 {len(results)} 条结果</div>
'''
        
        for r in results:
            html += f'''
        <div class="result">
            <h3><a href="{escape(r['url'])}" target="_blank">{escape(r['title'])}</a></h3>
            <div class="url">{escape(r['url'])}</div>
            <div class="content">{escape(r['content'])}</div>
            <div class="engine">🔍 来源: {escape(r['engine'])}</div>
        </div>
'''
        
        html += '''
    </div>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def send_json(self, data):
        """返回 JSON 响应"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def redirect(self, url):
        """重定向"""
        self.send_response(302)
        self.send_header('Location', url)
        self.end_headers()
    
    def log_message(self, format, *args):
        """自定义日志"""
        print(f"[SearXNG] {self.address_string()} - {format % args}")


def run_server(port=1679):
    """启动服务器"""
    server = HTTPServer(('0.0.0.0', port), SearchHandler)
    print(f"🚀 SearXNG Python 服务已启动!")
    print(f"🌐 Web 界面: http://localhost:{port}")
    print(f"📡 API 地址: http://localhost:{port}/search?q=关键词&format=json")
    print(f"📊 状态检查: http://localhost:{port}/status")
    print(f"⏹️  按 Ctrl+C 停止服务")
    print()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹️  服务已停止")
        server.shutdown()


if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 1679
    run_server(port)
