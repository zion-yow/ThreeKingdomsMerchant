from game_state import state
from game_data import RETAINERS_CONFIG

def upgrade_capacity(cost=2000, add_val=10):
    """花钱升级车队规模"""
    if state.player["money"] >= cost:
        state.player["money"] -= cost
        state.player["max_capacity"] += add_val
        return True, f"升级成功！最大载重增加了 {add_val}，现为 {state.player['max_capacity']}。"
    else:
        return False, f"资金不足！需要 {cost} 金钱。"

def donate_disaster(cost=1000, gain_rep=15):
    """赈灾获取信誉"""
    if state.player["money"] >= cost:
        state.player["money"] -= cost
        state.player["reputation"] += gain_rep
        return True, f"义举动天！花费 {cost} 赈济灾民，信誉提升了 {gain_rep}。"
    else:
        return False, f"资金不足！需要 {cost} 金钱。"

def recruit_retainer(ret_id):
    """招募随从"""
    if ret_id not in RETAINERS_CONFIG:
        return False, "查无此人。"
    
    if ret_id in state.player["retainers"]:
        return False, "此人已在麾下。"
        
    cfg = RETAINERS_CONFIG[ret_id]
    cost_rep = cfg["cost"]
    
    if state.player["reputation"] >= cost_rep:
        state.player["reputation"] -= cost_rep
        state.player["retainers"].append(ret_id)
        return True, f"三顾茅庐成功！【{cfg['name']}】加入了商队。"
    else:
        return False, f"信誉不足！招募【{cfg['name']}】需要 {cost_rep} 信誉。"