import json
import random
import os
import math
from game_data import CITIES_CONFIG, ITEMS_CONFIG, RETAINERS_CONFIG

SAVE_FILE = "savegame.json"

class GameState:
    def __init__(self):
        self.reset_new_game()

    def reset_new_game(self):
        """重置为新游戏状态"""
        self.start_year = 184
        self.turn_counter = 0
        
        self.player = {
            "name": "无名氏",
            "house_name": "流浪商队",
            "money": 3000,
            "reputation": 100,
            "current_city": "luo_yang",
            "inventory": {k: 0 for k in ITEMS_CONFIG.keys()},
            "max_capacity": 50,
            "retainers": [],       # 拥有的随从ID列表
            "active_retainer": None # 当前商队配置的随从ID
        }
        
        self.market_data = {}
        self.price_history = {}
        self.active_modifiers = {k: 1.0 for k in ITEMS_CONFIG.keys()}
        self.current_event = None
        
        self._init_markets()
        self._generate_pre_history()

    @property
    def current_date(self):
        return self.get_date_by_turn(self.turn_counter)

    def get_date_by_turn(self, turn):
        year = self.start_year + (turn // 4)
        season_idx = turn % 4
        season_names = ["春", "夏", "秋", "冬"]
        return f"{year}-{season_names[season_idx]}" # 简化格式以便画图

    def get_max_capacity(self):
        """计算包含随从加成后的最大载重"""
        base = self.player["max_capacity"]
        bonus = 0
        if self.player["active_retainer"]:
            ret_id = self.player["active_retainer"]
            if ret_id in RETAINERS_CONFIG:
                cfg = RETAINERS_CONFIG[ret_id]
                if cfg["effect_type"] == "capacity":
                    bonus = cfg["value"]
        return base + bonus

    def _init_markets(self):
        for city_id in CITIES_CONFIG:
            self.market_data[city_id] = {}
            self.price_history[city_id] = {}
            for item_id, props in ITEMS_CONFIG.items():
                base = props["base_price"]
                init_price = int(base * random.uniform(0.9, 1.1))
                self.market_data[city_id][item_id] = init_price
                self.price_history[city_id][item_id] = []

    def _generate_pre_history(self):
        print("[系统] 正在回溯过往行情...")
        pre_turns = 20
        
        for city_id in CITIES_CONFIG:
            for item_id in ITEMS_CONFIG:
                current = self.market_data[city_id][item_id]
                base = ITEMS_CONFIG[item_id]["base_price"]
                volatility = ITEMS_CONFIG[item_id]["volatility"]
                history = []
                temp_price = base
                for _ in range(pre_turns):
                    shock = temp_price * random.gauss(0, volatility)
                    mean_rev = (base - temp_price) * 0.1
                    temp_price = int(temp_price + shock + mean_rev)
                    temp_price = max(int(base*0.2), temp_price)
                    history.append(temp_price)
                self.price_history[city_id][item_id] = history
                self.market_data[city_id][item_id] = history[-1]

    def create_character(self, name, house_name, start_city):
        self.player["name"] = name
        self.player["house_name"] = house_name
        self.player["current_city"] = start_city

    def save_game(self):
        data = {
            "turn_counter": self.turn_counter,
            "player": self.player,
            "market_data": self.market_data,
            "price_history": self.price_history,
            "active_modifiers": self.active_modifiers,
            "current_event": self.current_event,
            "start_year": self.start_year
        }
        try:
            with open(SAVE_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True, "✅ 进度已保存。"
        except Exception as e:
            return False, f"❌ 保存失败: {e}"

    def load_game(self):
        if not os.path.exists(SAVE_FILE):
            return False, "❌ 没有找到存档文件。"
        try:
            with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.turn_counter = data["turn_counter"]
            self.player = data["player"]
            
            # 兼容性处理：补全随从字段
            if "retainers" not in self.player: self.player["retainers"] = []
            if "active_retainer" not in self.player: self.player["active_retainer"] = None
            
            self.market_data = data["market_data"]
            self.price_history = data.get("price_history", {})
            self.active_modifiers = data["active_modifiers"]
            self.current_event = data["current_event"]
            self.start_year = data.get("start_year", 184)
            if not self.price_history:
                self._init_markets()
                self._generate_pre_history()
            return True, f"✅ 成功读取商号【{self.player['house_name']}】的进度。"
        except Exception as e:
            return False, f"❌ 读取失败: {e}"

    def has_save_file(self):
        return os.path.exists(SAVE_FILE)

state = GameState()