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

# --- 游戏初始化与菜单流程 ---

def start_menu():
    """游戏启动菜单"""
    while True:
        clear_screen()
        print("="*40)
        print("   🗡️  三国豪商：家族兴衰录 (文字版 v0.4) 🗡️")
        print("="*40)
        print("\n1. 🏳️‍🌈  建立新商号 (开始游戏)")
        print("2. 💾  读取旧进度")
        print("q. 🚪  退出")
        
        choice = input("\n请选择: ").lower()
        
        if choice == '1':
            setup_new_game()
            start_game_loop() # 进入游戏循环
            return
        elif choice == '2':
            if state.has_save_file():
                success, msg = state.load_game()
                print(msg)
                if success:
                    input("按回车进入游戏...")
                    start_game_loop() # 进入游戏循环
                    return
                else:
                    input("按回车返回...")
            else:
                print("❌ 未找到存档文件。")
                input("按回车返回...")
        elif choice == 'q':
            sys.exit()

def setup_new_game():
    """新游戏角色创建流程"""
    clear_screen()
    print("=== 📝 登记造册 ===")
    
    name = input("请输入家主姓名 (如: 吕不韦): ").strip()
    if not name: name = "无名氏"
    
    house = input("请输入商号名称 (如: 奇货居): ").strip()
    if not house: house = "流浪商队"
    
    print("\n请选择起家之地:")
    starter_cities = ["luo_yang", "xu_chang", "ye_cheng", "jian_ye", "cheng_du"]
    for idx, cid in enumerate(starter_cities):
        city_name = CITIES_CONFIG[cid]['name']
        city_desc = CITIES_CONFIG[cid]['desc']
        print(f"{idx+1}. {city_name} - {city_desc}")
    
    city_choice = input("序号: ")
    try:
        c_idx = int(city_choice) - 1
        if 0 <= c_idx < len(starter_cities):
            start_city = starter_cities[c_idx]
        else:
            start_city = "luo_yang"
    except:
        start_city = "luo_yang"
        
    # 初始化状态
    state.reset_new_game()
    state.create_character(name, house, start_city)
    
    # 初始触发一次历史事件，设定开局环境
    market.apply_history_events()
    input("\n按回车键开启你的商业传奇...")

# --- 核心交互功能 ---

def handle_trade(is_buying=True):
    """处理买卖交互"""
    action = "买入" if is_buying else "卖出"
    keys = list(ITEMS_CONFIG.keys())
    
    clear_screen()
    print_dashboard() # 保持上下文
    print(f"\n[{action}] 选择商品:")
    
    current_city = state.player["current_city"]
    market_prices = state.market_data.get(current_city, {})
    
    for idx, k in enumerate(keys):
        curr_price = market_prices.get(k, 0)
        stock = state.player["inventory"].get(k, 0)
        print(f"{idx+1}. {ITEMS_CONFIG[k]['name']} (单价:{curr_price} | 库存:{stock})")
    
    print("0. 返回")
    
    try:
        choice = input("序号: ")
        if choice == '0': return
        
        c = int(choice) - 1
        if 0 <= c < len(keys):
            item = keys[c]
            qty_str = input(f"请输入{action}数量: ")
            if not qty_str: return
            qty = int(qty_str)
            
            if is_buying:
                ok, msg = trade.buy_item(item, qty)
            else:
                ok, msg = trade.sell_item(item, qty)
            print(f"\n>>> {msg}")
            input("按回车继续...")
    except ValueError:
        pass

def handle_travel():
    """处理移动交互"""
    curr_city_id = state.player["current_city"]
    neighbors = CITIES_CONFIG[curr_city_id]["connections"]
    
    print("\n[驿站] 选择目的地 (需耗时3个月/1回合):")
    for idx, city_id in enumerate(neighbors):
        print(f"{idx+1}. {CITIES_CONFIG[city_id]['name']}")
    print("0. 取消")
    
    try:
        choice = int(input("输入: ")) - 1
        if 0 <= choice < len(neighbors):
            target = neighbors[choice]
            print(f"\n商队启程前往 {CITIES_CONFIG[target]['name']}...")
            state.player["current_city"] = target
            
            # 移动会触发回合推进
            print("路途遥远，时光飞逝...")
            market.simulate_turn_fluctuation() 
            input("\n按回车键到达...")
        else:
            print("取消移动。")
    except ValueError:
        pass

def handle_market_analysis():
    """行情分析 (Plotext版)"""
    clear_screen()
    city_id = state.player["current_city"]
    city_name = CITIES_CONFIG[city_id]["name"]
    print(f"📈 正在分析【{city_name}】的历史行情...\n")
    
    history_data = state.price_history[city_id]
    
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

def handle_politics():
    """政治系统菜单"""
    while True:
        clear_screen()
        print("🏛️  【政治与发展】")
        print(f"💰 资金: {state.player['money']} | 📜 信誉: {state.player['reputation']}")
        print("-" * 40)
        
        upgrade_cost = 2000 + (state.player['max_capacity'] - 50) * 50
        print(f"1. 📦 扩建车队 (花费 {upgrade_cost} 金钱 -> +10 基础载重)")
        
        donate_cost = 1000
        print(f"2. 🍚 开仓赈灾 (花费 {donate_cost} 金钱 -> +15 信誉)")
        
        print("\n👲 【招募门客】 (消耗信誉)")
        recruit_map = {}
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

def handle_domestic():
    """内务系统菜单"""
    while True:
        clear_screen()
        print("🏠 【商队内务】")
        
        curr_id = state.player["active_retainer"]
        curr_name = RETAINERS_CONFIG[curr_id]["name"] if curr_id else "无"
        
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

def print_dashboard():
    """显示主界面面板"""
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

# --- 游戏主循环 ---

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
        
        if cmd == '1': handle_trade(True)
        elif cmd == '2': handle_trade(False)
        elif cmd == '3': handle_market_analysis()
        elif cmd == '4': handle_travel()
        elif cmd == '5': 
            print("\n原地休整..."); market.simulate_turn_fluctuation(); input("...")
        elif cmd == '6': handle_politics()
        elif cmd == '7': handle_domestic()
        elif cmd == '8': state.save_game(); input("保存成功...")
        elif cmd == 'q': 
            # 退出到主菜单，暂不保存
            break

# --- 程序入口 ---
if __name__ == "__main__":
    start_menu()