import os
import sys
import pandas as pd
from game_state import state
from game_data import CITIES_CONFIG, ITEMS_CONFIG, RETAINERS_CONFIG
from logic import market, trade, politics

# 尝试导入 plotext
try:
    import plotext as plt
    HAS_PLOTEXT = True
except ImportError:
    HAS_PLOTEXT = False

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# --- 行情分析 (Plotext版) ---
def handle_market_analysis():
    clear_screen()
    city_id = state.player["current_city"]
    city_name = CITIES_CONFIG[city_id]["name"]
    print(f"📈 正在分析【{city_name}】的历史行情...\n")
    
    history_data = state.price_history[city_id]
    
    # 交互循环
    while True:
        print("请选择要查看的商品走势:")
        items = list(ITEMS_CONFIG.keys())
        for idx, k in enumerate(items):
            print(f"{idx+1}. {ITEMS_CONFIG[k]['name']}", end="  ")
            if (idx+1) % 5 == 0: print()
        print("\n0. 返回上一级")
        
        choice = input("\n选项: ")
        if choice == '0': break
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(items):
                item_id = items[idx]
                item_name = ITEMS_CONFIG[item_id]["name"]
                
                prices = history_data[item_id]
                
                # 准备时间轴数据 (取最近30个点)
                display_count = 30
                prices_show = prices[-display_count:]
                
                # 生成时间标签 (倒推)
                curr_turn = state.turn_counter
                turns = range(curr_turn - len(prices_show) + 1, curr_turn + 1)
                labels = [state.get_date_by_turn(t) for t in turns]
                
                if HAS_PLOTEXT:
                    plt.clf()
                    plt.title(f"{city_name} - {item_name} 价格走势")
                    plt.plot(labels, prices_show, marker="dot", color="green")
                    plt.theme("dark") # 适应深色终端
                    plt.xlabel("时间")
                    plt.ylabel("价格")
                    # 标记当前点
                    plt.scatter([labels[-1]], [prices_show[-1]], color="red", label=f"当前: {prices_show[-1]}")
                    plt.show()
                else:
                    print("⚠️ 未检测到 plotext 库，显示简易表格。请运行 pip install plotext 获取最佳体验。")
                    df = pd.DataFrame({"时间": labels, "价格": prices_show})
                    print(df.to_string())
                
                input("\n按回车查看其他商品...")
                clear_screen()
        except ValueError:
            pass

# --- 政治系统菜单 ---
def handle_politics():
    while True:
        clear_screen()
        print("🏛️  【政治与发展】")
        print(f"💰 资金: {state.player['money']} | 📜 信誉: {state.player['reputation']}")
        print("-" * 40)
        
        # 升级选项
        upgrade_cost = 2000 + (state.player['max_capacity'] - 50) * 50 # 越升越贵
        print(f"1. 📦 扩建车队 (花费 {upgrade_cost} 金钱 -> +10 基础载重)")
        
        # 赈灾选项
        donate_cost = 1000
        print(f"2. 🍚 开仓赈灾 (花费 {donate_cost} 金钱 -> +15 信誉)")
        
        # 招募列表
        print("\n👲 【招募门客】 (消耗信誉)")
        recruit_map = {} # 映射序号到ID
        counter = 3
        for rid, cfg in RETAINERS_CONFIG.items():
            status = "✅已招募" if rid in state.player["retainers"] else f"需 {cfg['cost']} 信誉"
            if rid not in state.player["retainers"]:
                print(f"{counter}. {cfg['name']} ({status}) - {cfg['desc']}")
                recruit_map[str(counter)] = rid
                counter += 1
            else:
                 print(f"   {cfg['name']} (已在麾下)")
        
        print("\n0. 返回")
        choice = input("选项: ")
        
        if choice == '0': return
        elif choice == '1':
            ok, msg = politics.upgrade_capacity(upgrade_cost, 10)
            print(f"\n{msg}"); input("...")
        elif choice == '2':
            ok, msg = politics.donate_disaster(donate_cost, 15)
            print(f"\n{msg}"); input("...")
        elif choice in recruit_map:
            ok, msg = politics.recruit_retainer(recruit_map[choice])
            print(f"\n{msg}"); input("...")

# --- 内务系统菜单 ---
def handle_domestic():
    while True:
        clear_screen()
        print("🏠 【商队内务】")
        
        # 显示当前随从
        curr_id = state.player["active_retainer"]
        curr_name = RETAINERS_CONFIG[curr_id]["name"] if curr_id else "无"
        
        # 效果描述
        buff_desc = "无加成"
        if curr_id:
            cfg = RETAINERS_CONFIG[curr_id]
            if cfg['effect_type'] == 'discount': buff_desc = f"买入折扣 {int(cfg['value']*100)}%"
            elif cfg['effect_type'] == 'premium': buff_desc = f"卖出溢价 {int(cfg['value']*100)}%"
            elif cfg['effect_type'] == 'capacity': buff_desc = f"额外载重 +{cfg['value']}"
            
        print(f"当前随从: 【{curr_name}】 ({buff_desc})")
        print(f"当前载重: {state.get_max_capacity()} (基础 {state.player['max_capacity']})")
        print("-" * 40)
        
        owned = state.player["retainers"]
        if not owned:
            print("你还没有任何随从，请去政治菜单招募。")
        else:
            print("可指派随从:")
            opt_map = {}
            for idx, rid in enumerate(owned):
                cfg = RETAINERS_CONFIG[rid]
                mark = "★" if rid == curr_id else " "
                print(f"{idx+1}. {mark} {cfg['name']} [{cfg['effect_type']}]")
                opt_map[str(idx+1)] = rid
            
            print("\nu. 解除随从")
        
        print("0. 返回")
        choice = input("选项: ")
        
        if choice == '0': return
        elif choice == 'u':
            state.player["active_retainer"] = None
            print("已解除随从配置。"); input("...")
        elif choice in opt_map:
            rid = opt_map[choice]
            state.player["active_retainer"] = rid
            print(f"已指派 {RETAINERS_CONFIG[rid]['name']} 负责商队事务。"); input("...")

# --- 主界面 UI 微调 ---
def print_dashboard():
    curr_city_id = state.player["current_city"]
    curr_city_name = CITIES_CONFIG[curr_city_id]["name"]
    date_str = state.current_date
    
    print("\n" + "="*50)
    print(f"🚩 商号: {state.player['house_name']} | 👤 家主: {state.player['name']}")
    print(f"📅 时间: 东汉 {date_str} | 📍 位置: {curr_city_name}")
    
    if state.current_event:
        print("🔥 [天下大势] " + state.current_event["title"])
    
    print("-" * 50)
    print(f"💰 资金: {state.player['money']}    | 📜 信誉: {state.player['reputation']}")
    
    # 显示随从带来的额外载重
    max_cap = state.get_max_capacity()
    print(f"📦 载重: {sum(state.player['inventory'].values())}/{max_cap}")
    
    inv_list = [f"{ITEMS_CONFIG[k]['name']}:{v}" for k, v in state.player["inventory"].items() if v > 0]
    print(f"📦 货物: {'  '.join(inv_list) if inv_list else '空'}")
    print("-" * 50)
    
    print(f"【{curr_city_name} 现货挂牌】")
    print(f"{'商品':<8}{'当前价格':<10}{'趋势'}")
    prices = state.market_data[curr_city_id]
    history = state.price_history[curr_city_id]
    
    for item_id, price in prices.items():
        item = ITEMS_CONFIG[item_id]
        last_price = history[item_id][-2] if len(history[item_id]) >= 2 else price
        
        trend = " -- "
        if price > last_price * 1.1: trend = "📈 涨"
        elif price > last_price:     trend = "🔺 微涨"
        elif price < last_price * 0.9: trend = "📉 跌"
        elif price < last_price:     trend = "🔻 微跌"
        
        event_mark = ""
        current_mod = state.active_modifiers.get(item_id, 1.0)
        if current_mod > 1.2: event_mark = "🔥(紧缺)"
        elif current_mod < 0.8: event_mark = "❄️(滞销)"
        
        print(f"{item['name']:<8}{price:<10}{trend} {event_mark}")
    print("="*50)

# --- 游戏循环 ---
def start_game_loop():
    while True:
        clear_screen()
        print_dashboard()
        
        print("\n[商业]")
        print("1. 🛒 买入  2. 💰 卖出  3. 📈 打听行情(K线图)")
        print("[行动]")
        print("4. 🐎 前往他城  5. 💤 原地休整")
        print("[管理]")
        print("6. 🏛️ 政治与招募  7. 🏠 商队内务  8. 💾 保存进度  q. 退出")
        
        cmd = input("指令: ").lower()
        
        if cmd == '1': trade.handle_trade_ui(True) # 注意：这里你需要把 main 里原本的 handle_trade 改个名或者移到 trade.py
        elif cmd == '2': trade.handle_trade_ui(False)
        elif cmd == '3': handle_market_analysis()
        elif cmd == '4': 
            # (这里省略 handle_travel 代码，保持原样即可)
            # 为节省篇幅，假设 handle_travel 就在下面或已定义
            handle_travel()
        elif cmd == '5': 
            print("\n原地休整..."); market.simulate_turn_fluctuation(); input("...")
        elif cmd == '6': handle_politics()
        elif cmd == '7': handle_domestic()
        elif cmd == '8': state.save_game(); input("保存成功...")
        elif cmd == 'q': break

# 为兼容性，将 main.py 里原来的 handle_trade 简单封装一下或直接使用
# 建议将 UI 交互函数保留在 main.py，调用 logic 层的函数
def handle_trade_wrapper(is_buying):
    # 这里复制之前 main.py 的 handle_trade 逻辑即可
    from main import handle_trade # 如果有定义
    handle_trade(is_buying)

# ... (保留原有的 handle_travel, handle_trade, start_menu 等函数) ...

if __name__ == "__main__":
    # from main import start_menu
    start_menu()