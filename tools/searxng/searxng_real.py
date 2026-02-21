#!/usr/bin/env python3
"""
SearXNG 真实搜索版本
使用 duckduckgo-search 库获取真实搜索结果
"""

import json
import urllib.parse
import urllib.request
import ssl
from http.server import HTTPServer, BaseHTTPRequestHandler
from html import escape
import subprocess
import sys

# 尝试导入 ddgs (新版 duckduckgo_search)
try:
    from ddgs import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    # 尝试旧版
    try:
        from duckduckgo_search import DDGS
        DDGS_AVAILABLE = True
    except ImportError:
        DDGS_AVAILABLE = False
        print("⚠️  ddgs 未安装")
        print("📥 安装命令: pip3 install ddgs")

# 禁用 SSL 验证
ssl._create_default_https_context = ssl._create_unverified_context


class SearchHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/search'):
            self.handle_search()
        elif self.path == '/' or self.path == '/index.html':
            self.handle_index()
        elif self.path == '/status':
            self.handle_status()
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path.startswith('/search'):
            self.handle_search()
        else:
            self.send_error(404)
    
    def handle_index(self):
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
        .feature h3 { color: #667eea; margin-bottom: 10px; }
        .status {
            margin-top: 30px;
            padding: 10px 20px;
            background: #0f3460;
            border-radius: 20px;
            font-size: 14px;
        }
        .status.online { background: #16c79a; color: #000; }
        .notice {
            margin-top: 20px;
            padding: 15px 20px;
            background: #e94560;
            border-radius: 10px;
            font-size: 14px;
            max-width: 600px;
            text-align: center;
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
            <p>不记录搜索历史</p>
        </div>
        <div class="feature">
            <h3>🌐 多引擎聚合</h3>
            <p>DuckDuckGo 真实搜索</p>
        </div>
        <div class="feature">
            <h3>⚡ 本地部署</h3>
            <p>数据完全掌控</p>
        </div>
    </div>
    ''' + ('<div class="notice">⚠️ 当前使用模拟数据<br>安装 duckduckgo-search 获取真实结果</div>' if not DDGS_AVAILABLE else '<div class="status online">✅ 真实搜索已启用</div>') + '''
</body>
</html>'''
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def handle_status(self):
        status = {
            'status': 'ok',
            'service': 'searxng-python',
            'version': '1.1.0',
            'port': 1679,
            'real_search': DDGS_AVAILABLE,
            'engine': 'duckduckgo' if DDGS_AVAILABLE else 'mock'
        }
        self.send_json(status)
    
    def handle_search(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        
        query_list = params.get('q', [''])
        query = query_list[0]
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
                'count': len(results),
                'real_search': DDGS_AVAILABLE,
                'engine': 'duckduckgo' if (DDGS_AVAILABLE and results and results[0].get('engine') == 'duckduckgo') else 'mock'
            })
        else:
            self.send_html_results(query, results)
    
    def perform_search(self, query):
        """执行真实搜索或返回模拟数据"""
        if DDGS_AVAILABLE:
            try:
                return self.search_duckduckgo(query)
            except Exception as e:
                print(f"DuckDuckGo 搜索失败: {e}")
                return self.mock_results(query)
        else:
            return self.mock_results(query)
    
    def search_duckduckgo(self, query):
        """使用 DuckDuckGo 搜索"""
        results = []
        try:
            with DDGS(timeout=20) as ddgs:  # 增加超时时间
                for r in ddgs.text(query, max_results=10):
                    results.append({
                        'title': r['title'],
                        'url': r['href'],
                        'content': r['body'][:200] + '...' if len(r['body']) > 200 else r['body'],
                        'engine': 'duckduckgo'
                    })
        except Exception as e:
            print(f"[SearXNG] DuckDuckGo 搜索出错: {e}")
            raise  # 重新抛出，让上层处理
        return results
    
    def mock_results(self, query):
        """模拟搜索结果"""
        return [
            {
                'title': f'{query} - 搜索结果 1',
                'url': f'https://example.com/result1?q={urllib.parse.quote(query)}',
                'content': f'这是关于 "{query}" 的搜索结果描述...（⚠️ 模拟数据）',
                'engine': 'mock'
            },
            {
                'title': f'{query} - 搜索结果 2',
                'url': f'https://example.com/result2?q={urllib.parse.quote(query)}',
                'content': f'更多关于 "{query}" 的信息在这里...（⚠️ 模拟数据）',
                'engine': 'mock'
            }
        ]
    
    def send_html_results(self, query, results):
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{escape(query)} - SearXNG</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #1a1a2e; color: #eee; min-height: 100vh; padding: 20px; }}
        .header {{ display: flex; align-items: center; gap: 20px; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid #333; }}
        .logo {{ font-size: 24px; font-weight: bold; background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-decoration: none; }}
        .search-box {{ flex: 1; max-width: 600px; }}
        .search-input {{ width: 100%; padding: 10px 20px; font-size: 14px; border: 2px solid #667eea;
            border-radius: 20px; background: #16213e; color: #fff; outline: none; }}
        .results {{ max-width: 800px; margin: 0 auto; }}
        .result {{ background: #16213e; padding: 20px; margin-bottom: 15px; border-radius: 10px; border-left: 3px solid #667eea; }}
        .result h3 {{ margin-bottom: 8px; }}
        .result h3 a {{ color: #667eea; text-decoration: none; }}
        .result h3 a:hover {{ text-decoration: underline; }}
        .result .url {{ color: #16c79a; font-size: 14px; margin-bottom: 8px; }}
        .result .content {{ color: #aaa; font-size: 14px; line-height: 1.6; }}
        .result .engine {{ color: #667eea; font-size: 12px; margin-top: 8px; }}
        .info {{ text-align: center; color: #666; margin: 20px 0; }}
        .badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; margin-left: 10px; }}
        .badge.real {{ background: #16c79a; color: #000; }}
        .badge.mock {{ background: #e94560; color: #fff; }}
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
        <div class="info">找到 {len(results)} 条结果
            {'<span class="badge real">真实搜索</span>' if results and results[0].get('engine') == 'duckduckgo' else '<span class="badge mock">模拟数据</span>'}
        </div>
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
        
        html += '''    </div>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def redirect(self, url):
        self.send_response(302)
        self.send_header('Location', url)
        self.end_headers()
    
    def log_message(self, format, *args):
        print(f"[SearXNG] {self.address_string()} - {format % args}")


def run_server(port=1679):
    server = HTTPServer(('0.0.0.0', port), SearchHandler)
    print(f"🚀 SearXNG Python 服务已启动!")
    print(f"🌐 Web 界面: http://localhost:{port}")
    print(f"📡 API: http://localhost:{port}/search?q=关键词&format=json")
    print(f"✅ 真实搜索: {'已启用 (DuckDuckGo)' if DDGS_AVAILABLE else '未启用 (模拟数据)'}")
    if not DDGS_AVAILABLE:
        print(f"📥 安装真实搜索: pip3 install duckduckgo-search")
    print(f"⏹️  按 Ctrl+C 停止")
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
