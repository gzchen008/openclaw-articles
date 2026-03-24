#!/usr/bin/env python3
"""
多源网络搜索工具
支持多个免费搜索 API，自动降级
"""

import sys
import json
import urllib.request
import urllib.parse
import urllib.error
from typing import List, Dict, Optional
import time

class WebSearchResult:
    def __init__(self, title: str, url: str, snippet: str, source: str):
        self.title = title
        self.url = url
        self.snippet = snippet
        self.source = source
    
    def to_dict(self):
        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
            "source": self.source
        }

def search_duckduckgo(query: str, max_results: int = 5) -> List[WebSearchResult]:
    """
    DuckDuckGo Instant Answer API
    完全免费，无需 API key
    限制：主要返回即时答案，不是完整搜索结果
    """
    try:
        url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&no_html=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        results = []
        
        # 相关主题
        if data.get('RelatedTopics'):
            for topic in data['RelatedTopics'][:max_results]:
                if isinstance(topic, dict) and 'Text' in topic and 'FirstURL' in topic:
                    results.append(WebSearchResult(
                        title=topic.get('Text', '').split(' - ')[0] if ' - ' in topic.get('Text', '') else topic.get('Text', '')[:50],
                        url=topic.get('FirstURL', ''),
                        snippet=topic.get('Text', ''),
                        source='DuckDuckGo'
                    ))
        
        # 抽象结果
        if data.get('Abstract'):
            results.insert(0, WebSearchResult(
                title=data.get('Heading', query),
                url=data.get('AbstractURL', ''),
                snippet=data.get('Abstract', ''),
                source='DuckDuckGo'
            ))
        
        return results[:max_results]
    
    except Exception as e:
        print(f"DuckDuckGo 搜索失败: {e}", file=sys.stderr)
        return []

def get_wikipedia_summary(title: str, lang: str = "en") -> str:
    """获取 Wikipedia 页面摘要"""
    try:
        summary_url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}"
        req = urllib.request.Request(summary_url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('extract', '')
    except:
        return ""

def search_wikipedia(query: str, max_results: int = 3, lang: str = "en") -> List[WebSearchResult]:
    """
    Wikipedia API
    完全免费，适合查知识和定义
    支持多语言（en, zh, ja, ko等）
    """
    try:
        # 1. 先搜索文章列表
        search_url = f"https://{lang}.wikipedia.org/w/api.php?action=opensearch&search={urllib.parse.quote(query)}&limit={max_results}&format=json"
        req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        # opensearch 返回格式: [query, [titles], [descriptions], [urls]]
        if len(data) >= 2 and data[1]:
            results = []
            for i, title in enumerate(data[1][:max_results]):
                # 获取摘要
                snippet = data[2][i] if (len(data) > 2 and len(data[2]) > i and data[2][i]) else get_wikipedia_summary(title, lang)
                
                results.append(WebSearchResult(
                    title=title,
                    url=data[3][i] if len(data[3]) > i else f"https://{lang}.wikipedia.org/wiki/{urllib.parse.quote(title)}",
                    snippet=snippet,
                    source=f'Wikipedia ({lang})'
                ))
            return results
        
        return []
    
    except Exception as e:
        print(f"Wikipedia 搜索失败: {e}", file=sys.stderr)
        return []

def search_searx(query: str, max_results: int = 5, instance: str = "https://searx.be") -> List[WebSearchResult]:
    """
    SearXNG 公共实例
    开源搜索引擎聚合器
    """
    try:
        url = f"{instance}/search?q={urllib.parse.quote(query)}&format=json"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        results = []
        for item in data.get('results', [])[:max_results]:
            results.append(WebSearchResult(
                title=item.get('title', ''),
                url=item.get('url', ''),
                snippet=item.get('content', ''),
                source=f'SearX ({instance})'
            ))
        
        return results
    
    except Exception as e:
        print(f"SearX 搜索失败: {e}", file=sys.stderr)
        return []

def detect_language(query: str) -> str:
    """检测查询语言，返回 Wikipedia 语言代码"""
    # 检测中文字符
    if any('\u4e00' <= char <= '\u9fff' for char in query):
        return "zh"
    # 检测日文
    elif any('\u3040' <= char <= '\u309f' or '\u30a0' <= char <= '\u30ff' for char in query):
        return "ja"
    # 检测韩文
    elif any('\uac00' <= char <= '\ud7af' for char in query):
        return "ko"
    # 默认英文
    return "en"

def multi_search(query: str, max_results: int = 10) -> List[WebSearchResult]:
    """
    多源搜索，自动降级
    """
    all_results = []
    lang = detect_language(query)
    
    # 1. 尝试 DuckDuckGo（英文查询）
    if lang == "en":
        print("🔍 尝试 DuckDuckGo...", file=sys.stderr)
        ddg_results = search_duckduckgo(query, max_results=5)
        all_results.extend(ddg_results)
    
    # 2. 尝试 Wikipedia（自动检测语言）
    print(f"🔍 尝试 Wikipedia ({lang})...", file=sys.stderr)
    wiki_results = search_wikipedia(query, max_results=3, lang=lang)
    all_results.extend(wiki_results)
    
    # 3. 尝试 SearXNG（如果前两个都没结果）
    if len(all_results) == 0:
        print("🔍 尝试 SearXNG...", file=sys.stderr)
        searx_results = search_searx(query, max_results=max_results)
        all_results.extend(searx_results)
        
        # 如果第一个实例失败，尝试其他实例
        if len(searx_results) == 0:
            for instance in ["https://search.bus-hit.me", "https://searx.fmac.xyz"]:
                print(f"🔍 尝试 SearXNG 备用实例 {instance}...", file=sys.stderr)
                searx_results = search_searx(query, max_results=max_results, instance=instance)
                if searx_results:
                    all_results.extend(searx_results)
                    break
    
    return all_results[:max_results]

def format_output(results: List[WebSearchResult], format_type: str = "text"):
    """格式化输出"""
    if format_type == "json":
        return json.dumps([r.to_dict() for r in results], ensure_ascii=False, indent=2)
    
    # 文本格式
    output = []
    for i, result in enumerate(results, 1):
        output.append(f"\n{i}. {result.title}")
        output.append(f"   URL: {result.url}")
        output.append(f"   摘要: {result.snippet[:200]}..." if len(result.snippet) > 200 else f"   摘要: {result.snippet}")
        output.append(f"   来源: {result.source}")
    
    return "\n".join(output)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='多源网络搜索工具')
    parser.add_argument('query', help='搜索关键词')
    parser.add_argument('-n', '--number', type=int, default=10, help='结果数量（默认10）')
    parser.add_argument('-f', '--format', choices=['text', 'json'], default='text', help='输出格式')
    parser.add_argument('-s', '--source', choices=['duckduckgo', 'wikipedia', 'searx', 'all'], 
                       default='all', help='搜索源（默认all）')
    
    args = parser.parse_args()
    
    # 执行搜索
    if args.source == 'all':
        results = multi_search(args.query, args.number)
    elif args.source == 'duckduckgo':
        results = search_duckduckgo(args.query, args.number)
    elif args.source == 'wikipedia':
        results = search_wikipedia(args.query, args.number)
    elif args.source == 'searx':
        results = search_searx(args.query, args.number)
    
    # 输出结果
    if results:
        print(format_output(results, args.format))
    else:
        print("未找到结果", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
