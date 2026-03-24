#!/usr/bin/env python3
"""
外卖推荐引擎
根据用户偏好、预算、时间推荐餐厅
"""

import json
import random
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

# 数据文件路径
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
REFERENCES_DIR = SCRIPT_DIR.parent / "references"


class FoodRecommender:
    """外卖推荐引擎"""
    
    def __init__(self):
        self.preferences = self.load_preferences()
        self.chains = self.load_chains()
    
    def load_preferences(self) -> Dict:
        """加载用户偏好"""
        pref_file = DATA_DIR / "user-preferences.json"
        if pref_file.exists():
            with open(pref_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 默认偏好
            return {
                "taste_preference": ["川菜", "粤菜", "快餐"],
                "budget_range": [20, 50],
                "avoid": [],
                "favorites": []
            }
    
    def load_chains(self) -> List[Dict]:
        """加载连锁餐厅数据库"""
        chains_file = REFERENCES_DIR / "chains.md"
        # 简化版：硬编码一些常见餐厅
        return [
            {"name": "老乡鸡", "category": "中式快餐", "price": 25, "rating": 4.5},
            {"name": "真功夫", "category": "中式快餐", "price": 28, "rating": 4.3},
            {"name": "肯德基", "category": "西式快餐", "price": 35, "rating": 4.6},
            {"name": "麦当劳", "category": "西式快餐", "price": 32, "rating": 4.5},
            {"name": "黄焖鸡米饭", "category": "盖浇饭", "price": 22, "rating": 4.4},
            {"name": "重庆小面", "category": "面食", "price": 18, "rating": 4.3},
            {"name": "兰州拉面", "category": "面食", "price": 15, "rating": 4.2},
            {"name": "沙县小吃", "category": "小吃", "price": 12, "rating": 4.0},
            {"name": "必胜客", "category": "西餐", "price": 60, "rating": 4.5},
            {"name": "德克士", "category": "西式快餐", "price": 30, "rating": 4.2},
        ]
    
    def recommend(
        self,
        budget: Optional[int] = None,
        taste: Optional[str] = None,
        count: int = 3,
        random_pick: bool = False
    ) -> List[Dict]:
        """
        推荐餐厅
        
        Args:
            budget: 预算上限
            taste: 口味偏好
            count: 推荐数量
            random_pick: 是否随机选择
        
        Returns:
            推荐餐厅列表
        """
        candidates = self.chains.copy()
        
        # 筛选预算
        if budget:
            candidates = [c for c in candidates if c["price"] <= budget]
        
        # 筛选口味
        if taste:
            candidates = [c for c in candidates if taste in c["category"]]
        
        # 如果没有候选，放宽条件
        if not candidates:
            candidates = self.chains
        
        # 排序：评分高的优先
        candidates.sort(key=lambda x: x["rating"], reverse=True)
        
        # 随机选择或取前N个
        if random_pick:
            return random.sample(candidates, min(count, len(candidates)))
        else:
            return candidates[:count]
    
    def get_time_based_suggestion(self) -> str:
        """根据时间推荐"""
        hour = datetime.now().hour
        
        if 7 <= hour < 9:
            return "早餐时间！推荐：包子、豆浆、油条、煎饼果子"
        elif 11 <= hour < 13:
            return "午餐时间！推荐：盖浇饭、快餐、面条"
        elif 17 <= hour < 19:
            return "晚餐时间！推荐：正餐、聚餐、火锅"
        elif 21 <= hour < 23:
            return "夜宵时间！推荐：烧烤、小龙虾、炸鸡"
        else:
            return "非饭点时间，吃点零食？"
    
    def format_recommendation(self, restaurants: List[Dict]) -> str:
        """格式化推荐结果"""
        output = []
        for i, r in enumerate(restaurants, 1):
            output.append(
                f"{i}. {r['name']} - {r['category']} "
                f"(人均{r['price']}元，评分{r['rating']})"
            )
        return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="外卖推荐引擎")
    parser.add_argument("--budget", type=int, help="预算上限")
    parser.add_argument("--taste", type=str, help="口味偏好")
    parser.add_argument("--count", type=int, default=3, help="推荐数量")
    parser.add_argument("--random", action="store_true", help="随机推荐")
    parser.add_argument("--time", action="store_true", help="根据时间推荐")
    
    args = parser.parse_args()
    
    recommender = FoodRecommender()
    
    if args.time:
        print(recommender.get_time_based_suggestion())
        return
    
    restaurants = recommender.recommend(
        budget=args.budget,
        taste=args.taste,
        count=args.count,
        random_pick=args.random
    )
    
    print("🍜 推荐餐厅：")
    print(recommender.format_recommendation(restaurants))


if __name__ == "__main__":
    main()
