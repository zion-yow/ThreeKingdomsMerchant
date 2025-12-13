import random
import math
from game_state import state
from game_data import ITEMS_CONFIG, HISTORY_TIMELINE

def apply_history_events():
    """检查并应用当前时间的历史事件"""
    
    # --- 修复：直接通过回合数计算年份和季节，不再依赖字符串解析 ---
    # 这样无论 UI 显示格式怎么变（"184年" 或 "184-Spring"），逻辑都不会崩
    year = state.start_year + (state.turn_counter // 4)
    season_idx = state.turn_counter % 4
    # --------------------------------------------------------
    
    # 重置修正系数
    state.active_modifiers = {k: 1.0 for k in ITEMS_CONFIG.keys()}
    state.current_event = None
    
    if year in HISTORY_TIMELINE and season_idx in HISTORY_TIMELINE[year]:
        event = HISTORY_TIMELINE[year][season_idx]
        state.current_event = event
        
        if "modifiers" in event:
            for item, mod in event["modifiers"].items():
                state.active_modifiers[item] = mod
        
        if "impact" in event:
            impact = event["impact"]
            impact_msgs = []
            if "money_pct" in impact:
                loss = int(state.player["money"] * impact["money_pct"])
                if loss > 0:
                    state.player["money"] -= loss
                    impact_msgs.append(f"💸 损失资金 {loss}")
            if "inventory_pct" in impact:
                loss_pct = impact["inventory_pct"]
                total_loss = 0
                for iid, count in state.player["inventory"].items():
                    if count > 0:
                        l = math.ceil(count * loss_pct)
                        state.player["inventory"][iid] = max(0, count - l)
                        total_loss += l
                if total_loss > 0:
                    impact_msgs.append(f"🔥 损失货物 {total_loss}")
            if "reputation" in impact:
                state.player["reputation"] = max(0, state.player["reputation"] + impact["reputation"])
                impact_msgs.append(f"📉 信誉变动 {impact['reputation']}")
            
            if impact_msgs:
                state.current_event["impact_desc"] = " | ".join(impact_msgs)

def simulate_turn_fluctuation():
    """模拟回合结束时的市场波动，并记录历史"""
    
    state.turn_counter += 1
    apply_history_events()
    
    for city_id in state.market_data:
        for item_id in state.market_data[city_id]:
            if item_id not in ITEMS_CONFIG: continue

            current_price = state.market_data[city_id].get(item_id, ITEMS_CONFIG[item_id]["base_price"])
            base_price = ITEMS_CONFIG[item_id]["base_price"]
            volatility = ITEMS_CONFIG[item_id]["volatility"]
            
            mean_reversion = (base_price - current_price) * 0.1
            random_shock = current_price * random.gauss(0, volatility)
            
            temp_price = current_price + mean_reversion + random_shock
            hist_mod = state.active_modifiers.get(item_id, 1.0)
            
            final_price = int(temp_price * hist_mod)
            final_price = max(int(base_price * 0.1), final_price)
            
            # 更新市场价格
            state.market_data[city_id][item_id] = final_price
            
            # --- 记录历史 ---
            if item_id not in state.price_history[city_id]:
                state.price_history[city_id][item_id] = []
            
            state.price_history[city_id][item_id].append(final_price)