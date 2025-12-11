# 静态配置数据文件

# --- 商品数据 (10种) ---
ITEMS_CONFIG = {
    "grain":     {"name": "粮草", "base_price": 20, "volatility": 0.25, "unit": "石"},
    "wood":      {"name": "木材", "base_price": 40, "volatility": 0.15, "unit": "方"},
    "iron":      {"name": "铁锭", "base_price": 100, "volatility": 0.2, "unit": "钧"},
    "salt":      {"name": "食盐", "base_price": 150, "volatility": 0.1, "unit": "引"},
    "tea":       {"name": "茶叶", "base_price": 180, "volatility": 0.3, "unit": "饼"},
    "silk":      {"name": "丝绸", "base_price": 300, "volatility": 0.4, "unit": "匹"},
    "wine":      {"name": "美酒", "base_price": 350, "volatility": 0.35, "unit": "坛"},
    "horse":     {"name": "战马", "base_price": 600, "volatility": 0.5, "unit": "匹"},
    "porcelain": {"name": "瓷器", "base_price": 800, "volatility": 0.4, "unit": "件"},
    "jade":      {"name": "玉石", "base_price": 1200, "volatility": 0.6, "unit": "枚"}
}

# --- 随从数据 (新增) ---
# effect_type: 
#   'discount': 买入折扣 (0.1 = 便宜10%)
#   'premium': 卖出溢价 (0.1 = 多卖10%)
#   'capacity': 增加载重 (绝对值)
RETAINERS_CONFIG = {
    "r_guanjia": {"name": "老管家", "cost": 100, "desc": "家族旧部，擅长打理行装。", "effect_type": "capacity", "value": 20},
    "r_scholar": {"name": "落魄书生", "cost": 300, "desc": "能言善辩，讨价还价。", "effect_type": "discount", "value": 0.1},
    "r_merchant": {"name": "西域胡商", "cost": 500, "desc": "精通鉴宝，卖出高价。", "effect_type": "premium", "value": 0.15},
    "r_guard":    {"name": "退伍老兵", "cost": 200, "desc": "身强力壮，增加大量负重。", "effect_type": "capacity", "value": 50},
    "r_beauty":   {"name": "绝世名伶", "cost": 1000, "desc": "倾国倾城，此时无声胜有声。", "effect_type": "discount", "value": 0.2}
}

# --- 城市数据 (15个) ---
CITIES_CONFIG = {
    "luo_yang":  {"name": "洛阳", "connections": ["chang_an", "xu_chang", "ye_cheng", "wan_cheng"], "desc": "天下之中，命途多舛的帝都。"},
    "chang_an":  {"name": "长安", "connections": ["luo_yang", "wu_wei", "han_zhong"], "desc": "西京古都，扼守关中。"},
    "xu_chang":  {"name": "许昌", "connections": ["luo_yang", "wan_cheng", "xiao_pei", "shou_chun"], "desc": "曹魏龙兴之地，屯田中心。"},
    "ye_cheng":  {"name": "邺城", "connections": ["luo_yang", "bei_ping", "xiao_pei"], "desc": "河北重镇，袁绍基业所在。"},
    "bei_ping":  {"name": "北平", "connections": ["ye_cheng"], "desc": "幽州苦寒之地，产良马。"},
    "wu_wei":    {"name": "武威", "connections": ["chang_an"], "desc": "凉州门户，羌汉杂居。"},
    "xiao_pei":  {"name": "小沛", "connections": ["xu_chang", "ye_cheng", "xia_pi"], "desc": "徐州要冲，四战之地。"},
    "xia_pi":    {"name": "下邳", "connections": ["xiao_pei", "shou_chun"], "desc": "徐州富庶大城。"},
    "shou_chun": {"name": "寿春", "connections": ["xu_chang", "xia_pi", "jian_ye", "lu_jiang"], "desc": "淮南都会，袁术称帝处。"},
    "wan_cheng": {"name": "宛城", "connections": ["luo_yang", "xu_chang", "xiang_yang"], "desc": "南阳大郡，冶铁中心。"},
    "xiang_yang": {"name": "襄阳", "connections": ["wan_cheng", "jiang_ling"], "desc": "荆州治所，人杰地灵。"},
    "jiang_ling": {"name": "江陵", "connections": ["xiang_yang", "chai_sang", "cheng_du"], "desc": "南郡重镇，兵家必争。"},
    "chai_sang":  {"name": "柴桑", "connections": ["jiang_ling", "jian_ye", "lu_jiang"], "desc": "东吴水军基地，赤壁前哨。"},
    "jian_ye":   {"name": "建业", "connections": ["shou_chun", "chai_sang"], "desc": "江东虎踞龙盘之地。"},
    "lu_jiang":  {"name": "庐江", "connections": ["shou_chun", "chai_sang"], "desc": "江淮之间，乔氏故里。"},
    "han_zhong": {"name": "汉中", "connections": ["chang_an", "cheng_du"], "desc": "益州咽喉，天师道场。"},
    "cheng_du":  {"name": "成都", "connections": ["han_zhong", "jiang_ling"], "desc": "天府之国，沃野千里。"}
}

# --- 历史时间线 (保持不变) ---
HISTORY_TIMELINE = {
    184: {
        0: {
            "title": "黄巾起义", 
            "desc": "苍天已死，黄天当立。道路阻隔，盗匪横行。", 
            "modifiers": {"grain": 2.5, "salt": 1.5},
            "impact": {"money_pct": 0.05, "reputation": -5}
        },
        2: {
            "title": "黄巾转战", 
            "desc": "战火波及豫州、冀州，流民抢夺物资。", 
            "modifiers": {"grain": 2.0, "iron": 1.3},
            "impact": {"inventory_pct": 0.1}
        },
    },
    185: {
        0: {
            "title": "凉州兵变", 
            "desc": "韩遂、边章乱西凉。丝绸之路断绝。", 
            "modifiers": {"horse": 2.0, "silk": 0.5, "tea": 1.2},
            "impact": {"reputation": -5}
        },
    },
    187: {
        1: {
            "title": "张纯叛乱", 
            "desc": "幽州张纯勾结乌桓。北方局势不稳。", 
            "modifiers": {"horse": 1.5, "wood": 1.2}
        },
    },
    189: {
        1: {
            "title": "灵帝驾崩", 
            "desc": "少帝即位，十常侍乱政。京师混乱。", 
            "modifiers": {"jade": 0.8, "porcelain": 0.8},
            "impact": {"reputation": -10}
        },
        2: {
            "title": "董卓入京", 
            "desc": "董卓纵兵劫掠，向富户征收重税。", 
            "modifiers": {"grain": 1.5, "horse": 0.6, "silk": 0.4},
            "impact": {"money_pct": 0.20, "reputation": -10}
        },
    },
    190: {
        0: {
            "title": "诸侯讨董", 
            "desc": "十八路诸侯征集粮饷，强征商队物资。", 
            "modifiers": {"iron": 2.5, "grain": 2.0, "wood": 1.5},
            "impact": {"inventory_pct": 0.15}
        },
        1: {
            "title": "火烧洛阳", 
            "desc": "洛阳化为焦土，无数商铺积蓄毁于一旦。", 
            "modifiers": {"grain": 5.0, "salt": 3.0, "porcelain": 2.0},
            "impact": {"money_pct": 0.1, "inventory_pct": 0.2, "reputation": -20}
        },
    },
    191: {
        1: {
            "title": "界桥之战", 
            "desc": "公孙瓒与袁绍争夺冀州。", 
            "modifiers": {"horse": 1.5, "iron": 1.2}
        },
    },
    192: {
        1: {
            "title": "董卓伏诛", 
            "desc": "长安陷入李傕郭汜之乱，城中抢劫成风。", 
            "modifiers": {"grain": 2.0, "jade": 0.5},
            "impact": {"money_pct": 0.1}
        },
    },
    193: {
        2: {
            "title": "曹操攻徐", 
            "desc": "曹操攻打陶谦，所过之处多有杀戮。", 
            "modifiers": {"grain": 3.0, "wood": 1.5},
            "impact": {"inventory_pct": 0.1, "reputation": -5}
        },
    },
    194: {
        1: {
            "title": "蝗灾大起", 
            "desc": "关中大旱并发蝗灾，人相食。生存极度艰难。", 
            "modifiers": {"grain": 10.0, "tea": 0.5, "wine": 0.5},
            "impact": {"inventory_pct": 0.3, "reputation": -15}
        },
    },
    195: {
        3: {
            "title": "天子东归", 
            "desc": "献帝逃离长安，沿途需索无度。", 
            "modifiers": {"jade": 1.5},
            "impact": {"money_pct": 0.05}
        },
    },
    196: {
        2: {
            "title": "迁都许昌", 
            "desc": "曹操开始屯田，局势稍定。", 
            "modifiers": {"grain": 0.8, "iron": 1.2},
            "impact": {"reputation": 10}
        },
    },
    197: {
        0: {
            "title": "袁术称帝", 
            "desc": "袁术在寿春横征暴敛，以供挥霍。", 
            "modifiers": {"wine": 2.0, "silk": 2.0, "jade": 2.0},
            "impact": {"money_pct": 0.15, "reputation": -5}
        },
    },
    198: {
        3: {
            "title": "白门楼", 
            "desc": "吕布殒命。徐州商路重开。", 
            "modifiers": {"horse": 0.8}
        },
    },
    200: {
        0: {
            "title": "衣带诏", 
            "desc": "朝廷清洗反曹势力，人人自危。", 
            "modifiers": {"iron": 1.5},
            "impact": {"reputation": -10}
        },
        2: {
            "title": "官渡之战", 
            "desc": "两军对垒，征发民夫商队运粮。", 
            "modifiers": {"grain": 3.0, "iron": 2.0, "wood": 1.5},
            "impact": {"inventory_pct": 0.1}
        },
    },
    202: {
        1: {
            "title": "袁绍病亡", 
            "desc": "袁氏诸子内斗，河北混乱。", 
            "modifiers": {"salt": 1.3},
            "impact": {"money_pct": 0.05}
        },
    },
    207: {
        2: {
            "title": "北征乌桓", 
            "desc": "曹操远征，征调大量马匹。", 
            "modifiers": {"horse": 1.5, "wood": 1.2},
            "impact": {"reputation": 5}
        },
        3: {
            "title": "三顾茅庐", 
            "desc": "天下士人传为美谈。", 
            "modifiers": {"tea": 1.5}
        },
    },
    208: {
        2: {
            "title": "长坂坡", 
            "desc": "曹操南下，百姓流离失所。", 
            "modifiers": {"iron": 1.5, "grain": 1.5},
            "impact": {"inventory_pct": 0.2, "money_pct": 0.1}
        },
        3: {
            "title": "赤壁之战", 
            "desc": "大战在即，东吴征调民船。", 
            "modifiers": {"wood": 3.0, "iron": 2.0, "wine": 1.5},
            "impact": {"money_pct": 0.1}
        },
    }
}