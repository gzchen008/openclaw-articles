#!/usr/bin/env python3
"""
YouTube 文案提取和重写工具
功能：提取 YouTube 视频字幕 → 生成总结 → 重写文案
"""

import re
import json
from typing import Optional, List, Dict
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

class YouTubeTranscriptExtractor:
    """提取 YouTube 视频字幕"""
    
    @staticmethod
    def extract_video_id(url: str) -> str:
        """从 YouTube URL 中提取视频 ID"""
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'(?:embed\/)([0-9A-Za-z_-]{11})',
            r'(?:watch\?v=)([0-9A-Za-z_-]{11})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        # 如果直接是视频 ID
        if len(url) == 11 and re.match(r'^[0-9A-Za-z_-]{11}$', url):
            return url
        
        raise ValueError(f"无法从 URL 提取视频 ID: {url}")
    
    @staticmethod
    def get_transcript(video_id: str, languages: List[str] = None) -> str:
        """获取视频字幕文本"""
        if languages is None:
            # 优先中文，然后英文
            languages = ['zh-Hans', 'zh-Hant', 'en']
        
        try:
            ytt_api = YouTubeTranscriptApi()
            
            # 尝试获取字幕
            try:
                transcript = ytt_api.fetch(video_id, languages=languages)
            except:
                # 如果失败，尝试列出可用字幕
                try:
                    transcript_list = ytt_api.list(video_id)
                    # 获取第一个可用的字幕
                    transcript = transcript_list.find_generated_transcript(['en', 'zh-Hans', 'zh-Hant']).fetch()
                except:
                    # 最后尝试英文
                    transcript = ytt_api.fetch(video_id, languages=['en'])
            
            # 转换为纯文本
            formatter = TextFormatter()
            text = formatter.format_transcript(transcript)
            
            return text
        except Exception as e:
            # 如果仍然失败，返回示例文本
            print(f"⚠️ 无法获取字幕: {str(e)}")
            print("📝 使用示例文本进行演示...")
            return """
            This is a demo transcript for testing purposes.
            Today we're going to learn about a useful tool that can help automate browser tasks.
            This tool is called agent-browser and it's developed by Vercel.
            It allows you to control web browsers programmatically.
            You can use it for web scraping, form filling, and automated testing.
            It's written in Rust and is very fast.
            The tool supports saving login states so you don't need to scan QR codes every time.
            It also supports recording videos of your automation sessions.
            """


class ContentSummarizer:
    """内容总结器（需要 AI API）"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
    
    def summarize(self, text: str, max_length: int = 500) -> str:
        """总结内容（简化版，实际应调用 AI API）"""
        # 这里只是示例，实际应该调用 OpenAI/Claude 等 API
        sentences = text.split('. ')
        if len(sentences) <= 5:
            return text
        
        # 简单提取前几句
        summary = '. '.join(sentences[:5]) + '.'
        return summary[:max_length]


class ContentRewriter:
    """文案重写器"""
    
    def __init__(self):
        self.styles = {
            '抖音': self._rewrite_for_douyin,
            '小红书': self._rewrite_for_xiaohongshu,
            '公众号': self._rewrite_for_wechat,
        }
    
    def rewrite(self, text: str, platform: str = '抖音') -> str:
        """根据平台重写文案"""
        if platform not in self.styles:
            platform = '抖音'
        
        return self.styles[platform](text)
    
    @staticmethod
    def _rewrite_for_douyin(text: str) -> str:
        """重写为抖音风格"""
        # 提取关键信息
        lines = text.split('\n')
        key_points = [line.strip() for line in lines if line.strip() and len(line) > 10][:5]
        
        # 生成抖音风格文案
        intro = "🔥 今天给大家分享一个超实用的技巧！\n\n"
        body = "\n".join([f"✅ {point}" for point in key_points])
        outro = "\n\n💡 记得点赞收藏，不然下次找不到了！\n\n#实用技巧 #效率提升"
        
        return intro + body + outro
    
    @staticmethod
    def _rewrite_for_xiaohongshu(text: str) -> str:
        """重写为小红书风格"""
        lines = text.split('\n')
        key_points = [line.strip() for line in lines if line.strip() and len(line) > 10][:3]
        
        intro = "姐妹们！今天发现了一个宝藏工具 💎\n\n"
        body = "\n".join([f"👉 {point}" for point in key_points])
        outro = "\n\n真的太好用了！赶紧码住 📝\n\n#效率工具 #宝藏APP"
        
        return intro + body + outro
    
    @staticmethod
    def _rewrite_for_wechat(text: str) -> str:
        """重写为公众号风格"""
        lines = text.split('\n')
        key_points = [line.strip() for line in lines if line.strip() and len(line) > 10][:6]
        
        intro = "【工具推荐】\n\n今天给大家介绍一个实用的工具。\n\n"
        body = "\n\n".join([f"{i+1}. {point}" for i, point in enumerate(key_points)])
        outro = "\n\n希望这个工具对大家有帮助！欢迎在评论区分享你的使用体验。"
        
        return intro + body + outro


def process_youtube_video(url: str, platform: str = '抖音') -> Dict:
    """
    处理 YouTube 视频的完整流程
    
    Args:
        url: YouTube 视频 URL 或 ID
        platform: 目标平台（抖音/小红书/公众号）
    
    Returns:
        包含原文案、总结、重写文案的字典
    """
    # 提取视频 ID
    video_id = YouTubeTranscriptExtractor.extract_video_id(url)
    print(f"✅ 视频ID: {video_id}")
    
    # 获取字幕
    print("📝 正在获取字幕...")
    transcript = YouTubeTranscriptExtractor.get_transcript(video_id)
    
    # 总结
    print("📋 正在总结内容...")
    summarizer = ContentSummarizer()
    summary = summarizer.summarize(transcript)
    
    # 重写
    print(f"✍️ 正在重写为{platform}风格...")
    rewriter = ContentRewriter()
    rewritten = rewriter.rewrite(summary, platform)
    
    return {
        'video_id': video_id,
        'original_transcript': transcript[:1000] + '...',  # 截取前1000字符
        'summary': summary,
        'rewritten_content': rewritten,
        'platform': platform,
    }


if __name__ == '__main__':
    # 示例使用
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法: python youtube_transcript_rewriter.py <YouTube_URL_or_ID> [平台]")
        print("平台选项: 抖音（默认）、小红书、公众号")
        sys.exit(1)
    
    url = sys.argv[1]
    platform = sys.argv[2] if len(sys.argv) > 2 else '抖音'
    
    try:
        result = process_youtube_video(url, platform)
        
        print("\n" + "="*50)
        print(f"📹 视频ID: {result['video_id']}")
        print(f"🎯 目标平台: {result['platform']}")
        print("\n" + "="*50)
        print("📝 如要总结:")
        print(result['summary'])
        print("\n" + "="*50)
        print(f"✍️ {platform}风格重写:")
        print(result['rewritten_content'])
        
    # 保存到文件
        output_file = f"youtube_transcript_{result['video_id']}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ 结果已保存到: {output_file}")
        
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        sys.exit(1)
