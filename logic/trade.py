from game_state import state
from game_data import ITEMS_CONFIG, RETAINERS_CONFIG

def get_current_city_prices():
    city_id = state.player["current_city"]
    return state.market_data.get(city_id, {})

def get_retainer_buff():
    """获取当前激活随从的Buff类型和数值"""
    rid = state.player["active_retainer"]
    if rid and rid in RETAINERS_CONFIG:
        return RETAINERS_CONFIG[rid]["effect_type"], RETAINERS_CONFIG[rid]["value"]
    return None, 0

def buy_item(item_id, quantity):
    if quantity <= 0: return False, "数量必须大于0"
    
    market_prices = get_current_city_prices()
    if item_id not in market_prices: return False, "该商品此处不贩售"
        
    unit_price = market_prices[item_id]
    
    # --- 随从折扣逻辑 ---
    buff_type, buff_val = get_retainer_buff()
    discount_msg = ""
    if buff_type == "discount":
        discount = int(unit_price * buff_val)
        unit_price -= discount
        discount_msg = f"(随从折扣 -{discount})"
    # ------------------

    total_cost = unit_price * quantity
    
    if state.player["money"] < total_cost:
        return False, f"资金不足！需要 {total_cost}，拥有 {state.player['money']}"
    
    # 使用动态计算的最大载重
    current_load = sum(state.player["inventory"].values())
    max_cap = state.get_max_capacity()
    
    if current_load + quantity > max_cap:
        return False, f"商队载重已满！(上限 {max_cap})"
        
    state.player["money"] -= total_cost
    state.player["inventory"][item_id] += quantity
    return True, f"成功买入 {ITEMS_CONFIG[item_id]['name']} {quantity} {ITEMS_CONFIG[item_id]['unit']} {discount_msg}"

def sell_item(item_id, quantity):
    if quantity <= 0: return False, "数量必须大于0"
    if state.player["inventory"].get(item_id, 0) < quantity:
        return False, "库存不足！"
        
    market_prices = get_current_city_prices()
    unit_price = market_prices[item_id]
    
    # --- 随从溢价逻辑 ---
    buff_type, buff_val = get_retainer_buff()
    premium_msg = ""
    if buff_type == "premium":
        extra = int(unit_price * buff_val)
        unit_price += extra
        premium_msg = f"(随从溢价 +{extra})"
    # ------------------
    
    total_revenue = unit_price * quantity
    
    state.player["money"] += total_revenue
    state.player["inventory"][item_id] -= quantity
    return True, f"成功卖出 {ITEMS_CONFIG[item_id]['name']} {quantity} {ITEMS_CONFIG[item_id]['unit']}，获利 {total_revenue} {premium_msg}"