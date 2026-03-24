#!/usr/bin/env python3
"""
订单记录追踪器
记录历史订单，分析用户偏好
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from collections import Counter


DATA_DIR = Path(__file__).parent.parent / "data"


class OrderTracker:
    """订单记录追踪器"""
    
    def __init__(self):
        self.history_file = DATA_DIR / "order-history.json"
        self.history = self.load_history()
    
    def load_history(self) -> List[Dict]:
        """加载订单历史"""
        if self.history_file.exists():
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return []
    
    def save_history(self):
        """保存订单历史"""
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def add_order(
        self,
        restaurant: str,
        dishes: List[str],
        price: float,
        platform: str = "unknown",
        rating: Optional[int] = None
    ):
        """添加订单记录"""
        order = {
            "timestamp": datetime.now().isoformat(),
            "restaurant": restaurant,
            "dishes": dishes,
            "price": price,
            "platform": platform,
            "rating": rating
        }
        self.history.append(order)
        self.save_history()
        print(f"✅ 已记录订单：{restaurant} - {price}元")
    
    def analyze_preferences(self) -> Dict:
        """分析用户偏好"""
        if not self.history:
            return {"error": "暂无订单记录"}
        
        # 统计餐厅
        restaurants = [o["restaurant"] for o in self.history]
        top_restaurants = Counter(restaurants).most_common(5)
        
        # 统计菜品
        all_dishes = []
        for o in self.history:
            all_dishes.extend(o["dishes"])
        top_dishes = Counter(all_dishes).most_common(5)
        
        # 统计平台
        platforms = [o["platform"] for o in self.history]
        platform_usage = Counter(platforms)
        
        # 平均价格
        avg_price = sum(o["price"] for o in self.history) / len(self.history)
        
        return {
            "total_orders": len(self.history),
            "top_restaurants": top_restaurants,
            "top_dishes": top_dishes,
            "platform_usage": dict(platform_usage),
            "average_price": round(avg_price, 2)
        }
    
    def get_recent_orders(self, days: int = 7) -> List[Dict]:
        """获取最近N天的订单"""
        from datetime import timedelta
        
        cutoff = datetime.now() - timedelta(days=days)
        recent = []
        
        for order in self.history:
            order_time = datetime.fromisoformat(order["timestamp"])
            if order_time > cutoff:
                recent.append(order)
        
        return recent
    
    def avoid_duplicates(self, days: int = 3) -> List[str]:
        """获取最近吃过的餐厅（避免重复）"""
        recent = self.get_recent_orders(days)
        return list(set(o["restaurant"] for o in recent))


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="订单记录追踪器")
    parser.add_argument("--add", nargs=4, metavar=("餐厅", "菜品", "价格", "平台"),
                       help="添加订单")
    parser.add_argument("--analyze", action="store_true", help="分析偏好")
    parser.add_argument("--recent", type=int, metavar="DAYS", help="查看最近N天订单")
    parser.add_argument("--avoid", type=int, metavar="DAYS", help="最近N天吃过的餐厅")
    
    args = parser.parse_args()
    
    tracker = OrderTracker()
    
    if args.add:
        restaurant, dishes_str, price, platform = args.add
        dishes = [d.strip() for d in dishes_str.split(",")]
        tracker.add_order(restaurant, dishes, float(price), platform)
    
    elif args.analyze:
        prefs = tracker.analyze_preferences()
        print(json.dumps(prefs, ensure_ascii=False, indent=2))
    
    elif args.recent:
        recent = tracker.get_recent_orders(args.recent)
        print(f"最近{args.recent}天订单（{len(recent)}单）：")
        for order in recent:
            print(f"- {order['timestamp'][:10]} {order['restaurant']} {order['price']}元")
    
    elif args.avoid:
        restaurants = tracker.avoid_duplicates(args.avoid)
        print(f"最近{args.avoid}天吃过的餐厅：")
        for r in restaurants:
            print(f"- {r}")


if __name__ == "__main__":
    main()
