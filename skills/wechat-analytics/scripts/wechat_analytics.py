#!/usr/bin/env python3
"""
微信公众号数据分析工具
支持：文章阅读数据、用户数据、选题优化建议
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from pathlib import Path

class WeChatAnalytics:
    """微信公众号数据分析"""
    
    BASE_URL = "https://api.weixin.qq.com/cgi-bin"
    
    def __init__(self):
        self.appid = os.environ.get("WECHAT_APPID")
        self.secret = os.environ.get("WECHAT_SECRET")
        self._token = None
        
        if not self.appid or not self.secret:
            raise ValueError("请设置 WECHAT_APPID 和 WECHAT_SECRET 环境变量")
    
    def get_token(self) -> str:
        """获取 access_token"""
        if self._token:
            return self._token
        
        url = f"{self.BASE_URL}/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.appid,
            "secret": self.secret
        }
        resp = requests.get(url, params=params, timeout=30)
        self._token = resp.json().get("access_token")
        return self._token
    
    @property
    def token(self) -> str:
        return self.get_token()
    
    # ===== 用户数据 =====
    
    def get_user_summary(self, begin_date: str, end_date: str) -> List[Dict]:
        """
        获取用户增减数据
        
        Args:
            begin_date: 开始日期 YYYY-MM-DD
            end_date: 结束日期 YYYY-MM-DD
        """
        url = f"{self.BASE_URL}/datacube/getusersummary?access_token={self.token}"
        payload = {"begin_date": begin_date, "end_date": end_date}
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        resp = requests.post(url, data=data, headers=headers, timeout=30)
        return resp.json().get("list", [])
    
    def get_user_cumulate(self, begin_date: str, end_date: str) -> List[Dict]:
        """获取累计用户数据"""
        url = f"{self.BASE_URL}/datacube/getusercumulate?access_token={self.token}"
        payload = {"begin_date": begin_date, "end_date": end_date}
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        resp = requests.post(url, data=data, headers=headers, timeout=30)
        return resp.json().get("list", [])
    
    # ===== 图文数据 =====
    
    def get_article_summary(self, date: str) -> List[Dict]:
        """
        获取图文群发每日数据
        
        Args:
            date: 日期 YYYY-MM-DD
        """
        url = f"{self.BASE_URL}/datacube/getarticlesummary?access_token={self.token}"
        payload = {"begin_date": date, "end_date": date}
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        resp = requests.post(url, data=data, headers=headers, timeout=30)
        return resp.json().get("list", [])
    
    def get_article_total(self, begin_date: str, end_date: str) -> List[Dict]:
        """获取图文群发总数据"""
        url = f"{self.BASE_URL}/datacube/getarticletotal?access_token={self.token}"
        payload = {"begin_date": begin_date, "end_date": end_date}
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        resp = requests.post(url, data=data, headers=headers, timeout=30)
        return resp.json().get("list", [])
    
    def get_user_read(self, begin_date: str, end_date: str) -> List[Dict]:
        """获取图文阅读概况数据"""
        url = f"{self.BASE_URL}/datacube/getuserread?access_token={self.token}"
        payload = {"begin_date": begin_date, "end_date": end_date}
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        resp = requests.post(url, data=data, headers=headers, timeout=30)
        return resp.json().get("list", [])
    
    def get_user_read_hour(self, date: str) -> List[Dict]:
        """获取图文阅读分时数据"""
        url = f"{self.BASE_URL}/datacube/getuserreadhour?access_token={self.token}"
        payload = {"begin_date": date, "end_date": date}
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        resp = requests.post(url, data=data, headers=headers, timeout=30)
        return resp.json().get("list", [])
    
    def get_user_share(self, begin_date: str, end_date: str) -> List[Dict]:
        """获取图文转发概况数据"""
        url = f"{self.BASE_URL}/datacube/getusershare?access_token={self.token}"
        payload = {"begin_date": begin_date, "end_date": end_date}
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        resp = requests.post(url, data=data, headers=headers, timeout=30)
        return resp.json().get("list", [])
    
    # ===== 分析功能 =====
    
    def analyze_best_publish_time(self, days: int = 7) -> Dict:
        """分析最佳发布时间"""
        end_date = datetime.now() - timedelta(days=1)
        begin_date = end_date - timedelta(days=days)
        
        all_hour_data = []
        current = begin_date
        while current <= end_date:
            try:
                hour_data = self.get_user_read_hour(current.strftime("%Y-%m-%d"))
                all_hour_data.extend(hour_data)
            except:
                pass
            current += timedelta(days=1)
        
        # 按小时统计阅读量
        hour_stats = {}
        for item in all_hour_data:
            ref_hour = item.get("ref_hour", 0)
            count = item.get("int_page_read_count", 0)
            hour_stats[ref_hour] = hour_stats.get(ref_hour, 0) + count
        
        # 找出阅读量最高的时段
        if hour_stats:
            best_hour = max(hour_stats, key=hour_stats.get)
            return {
                "best_hour": best_hour,
                "hour_stats": hour_stats,
                "recommendation": f"建议在 {best_hour}:00 左右发布文章"
            }
        
        return {"recommendation": "数据不足，建议在 9:00-10:00 发布"}
    
    def get_article_performance(self, days: int = 7) -> List[Dict]:
        """获取文章表现数据"""
        end_date = datetime.now() - timedelta(days=1)
        begin_date = end_date - timedelta(days=days)
        
        articles = self.get_article_total(
            begin_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d")
        )
        
        results = []
        for article in articles:
            details = article.get("details", [])
            for detail in details:
                results.append({
                    "title": article.get("title", ""),
                    "msg_id": article.get("msg_id", ""),
                    "read_count": detail.get("int_page_read_count", 0),
                    "share_count": detail.get("share_count", 0),
                    "fav_count": detail.get("add_to_fav_count", 0),
                    "read_user": detail.get("int_page_read_user", 0)
                })
        
        # 按阅读量排序
        results.sort(key=lambda x: x["read_count"], reverse=True)
        return results
    
    def generate_topic_suggestions(self, workspace_path: str = None) -> Dict:
        """
        基于历史数据生成选题建议
        
        Args:
            workspace_path: 工作区路径，用于读取历史文章
        """
        suggestions = {
            "top_performers": [],
            "topic_analysis": {},
            "recommendations": []
        }
        
        # 获取最近 30 天的文章表现
        try:
            articles = self.get_article_performance(days=30)
            suggestions["top_performers"] = articles[:5]
        except:
            pass
        
        # 分析历史文章标题关键词
        if workspace_path:
            content_plan = Path(workspace_path) / "wechat-content-plan.md"
            if content_plan.exists():
                # 读取已发布的文章
                pass
        
        # 生成建议
        suggestions["recommendations"] = [
            "📌 继续深挖 OpenClaw 实战教程",
            "📌 增加「自动化」相关内容",
            "📌 结合热点话题提升阅读量",
            "📌 多用数字和问句式标题",
            "📌 保持每天固定时间发布"
        ]
        
        return suggestions


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="微信公众号数据分析工具")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # user 命令
    user_parser = subparsers.add_parser("user", help="获取用户数据")
    user_parser.add_argument("--days", "-d", type=int, default=7, help="统计天数")
    
    # article 命令
    article_parser = subparsers.add_parser("article", help="获取文章数据")
    article_parser.add_argument("--date", "-d", help="日期 YYYY-MM-DD")
    article_parser.add_argument("--days", type=int, default=7, help="统计天数")
    
    # suggest 命令
    suggest_parser = subparsers.add_parser("suggest", help="生成选题建议")
    suggest_parser.add_argument("--workspace", "-w", help="工作区路径")
    
    # time 命令
    time_parser = subparsers.add_parser("time", help="分析最佳发布时间")
    time_parser.add_argument("--days", "-d", type=int, default=7, help="统计天数")
    
    # report 命令
    report_parser = subparsers.add_parser("report", help="生成完整报告")
    report_parser.add_argument("--days", "-d", type=int, default=7, help="统计天数")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        analytics = WeChatAnalytics()
        
        if args.command == "user":
            print(f"📥 获取用户数据（最近 {args.days} 天）...")
            
            end_date = datetime.now() - timedelta(days=1)
            begin_date = end_date - timedelta(days=args.days)
            
            # 用户增长
            summary = analytics.get_user_summary(
                begin_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d")
            )
            
            # 累计用户
            cumulate = analytics.get_user_cumulate(
                begin_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d")
            )
            
            print(f"\n📊 用户数据报告：")
            
            if summary:
                total_new = sum(s.get("new_user", 0) for s in summary)
                total_cancel = sum(s.get("cancel_user", 0) for s in summary)
                print(f"   新增用户：{total_new}")
                print(f"   取消关注：{total_cancel}")
                print(f"   净增：{total_new - total_cancel}")
            
            if cumulate:
                latest = cumulate[-1] if cumulate else {}
                print(f"   累计用户：{latest.get('cumulate_user', 'N/A')}")
        
        elif args.command == "article":
            if args.date:
                print(f"📥 获取 {args.date} 的文章数据...")
                articles = analytics.get_article_summary(args.date)
            else:
                end_date = datetime.now() - timedelta(days=1)
                begin_date = end_date - timedelta(days=args.days)
                print(f"📥 获取文章数据（最近 {args.days} 天）...")
                articles = analytics.get_article_performance(days=args.days)
            
            print(f"\n📊 文章表现：")
            for i, article in enumerate(articles[:10], 1):
                title = article.get("title", "")[:30]
                reads = article.get("read_count", article.get("int_page_read_count", 0))
                shares = article.get("share_count", 0)
                print(f"   {i}. {title}...")
                print(f"      阅读: {reads} | 分享: {shares}")
        
        elif args.command == "suggest":
            print("📥 生成选题建议...")
            suggestions = analytics.generate_topic_suggestions(args.workspace)
            
            print(f"\n📊 选题建议报告：")
            
            if suggestions.get("top_performers"):
                print(f"\n🔥 热门文章 TOP 5：")
                for i, article in enumerate(suggestions["top_performers"], 1):
                    print(f"   {i}. {article['title'][:25]}...")
                    print(f"      阅读: {article['read_count']} | 分享: {article['share_count']}")
            
            print(f"\n💡 选题建议：")
            for rec in suggestions.get("recommendations", []):
                print(f"   {rec}")
        
        elif args.command == "time":
            print(f"📥 分析最佳发布时间...")
            result = analytics.analyze_best_publish_time(args.days)
            
            print(f"\n⏰ 发布时间建议：")
            if result.get("best_hour"):
                print(f"   最佳发布时间：{result['best_hour']}:00")
            print(f"   {result.get('recommendation', '')}")
        
        elif args.command == "report":
            print(f"📥 生成完整报告（最近 {args.days} 天）...")
            
            end_date = datetime.now() - timedelta(days=1)
            begin_date = end_date - timedelta(days=args.days)
            
            # 用户数据
            cumulate = analytics.get_user_cumulate(
                begin_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d")
            )
            
            # 文章数据
            articles = analytics.get_article_performance(days=args.days)
            
            # 时间分析
            time_result = analytics.analyze_best_publish_time(args.days)
            
            print(f"\n" + "="*50)
            print(f"📊 公众号数据报告")
            print(f"   统计周期：{begin_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}")
            print("="*50)
            
            print(f"\n👥 用户数据：")
            if cumulate:
                latest = cumulate[-1]
                print(f"   累计用户：{latest.get('cumulate_user', 'N/A')}")
            
            print(f"\n📝 文章数据：")
            total_reads = sum(a.get("read_count", 0) for a in articles)
            total_shares = sum(a.get("share_count", 0) for a in articles)
            print(f"   文章数量：{len(articles)}")
            print(f"   总阅读量：{total_reads}")
            print(f"   总分享量：{total_shares}")
            
            if articles:
                print(f"   平均阅读量：{total_reads // len(articles) if articles else 0}")
            
            print(f"\n⏰ 发布建议：")
            print(f"   {time_result.get('recommendation', '')}")
            
            print(f"\n🔥 热门文章 TOP 3：")
            for i, article in enumerate(articles[:3], 1):
                print(f"   {i}. {article['title'][:25]}...")
                print(f"      阅读: {article['read_count']} | 分享: {article['share_count']}")
            
            print(f"\n" + "="*50)
    
    except Exception as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
