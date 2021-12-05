from card.basic_card import Coin
from card.standard_card import *
from card.classic_card import *
from card.hero_power_card import *

ID2CARD_DICT = {
    # 特殊项-幸运币
    "COIN": Coin,

    # 英雄技能
    "TOTEMIC_CALL": TotemicCall,
    "LESSER_HEAL": LesserHeal,
    "BALLISTA_SHOT": BallistaShot,

    # 标准模式-中立
    "SCH_713": CultNeophyte,  # 异教低阶牧师
    "YOP_032": ArmorVendor,  # 护甲商贩
    "BAR_026": DeathsHeadCultist,  # 亡首教徒
    "CS3_024": TaelanFordring,  # 泰兰·弗丁
    "EX1_110": CairneBloodhoof,  # 凯恩·血蹄
    "CORE_EX1_110": CairneBloodhoof,  # 凯恩·血蹄
    "WC_030": MutanusTheDevourer,  # 吞噬者穆坦努斯
    "BAR_077": KargalBattlescar,  # 卡加尔·战痕
    "DMF_254": CTunTheShattered,  # 克苏恩，破碎之劫
    "DMF_254t3": EyeOfCTun,   # 克苏恩之眼
    "DMF_254t4": HeartOfCTun,  # 克苏恩之心
    "DMF_254t5": BodyOfCTun,  # 克苏恩之躯
    "DMF_254t7": MawOfCTun,  # 克苏恩之口
    "SCH_428": LorekeeperPolkelt,  # 博学者普克尔特


    # 标准模式-牧师
    "CORE_CS1_130": HolySmite,  # 神圣惩击
    "CS1_130": HolySmite,  # 神圣惩击
    "SCH_250": WaveOfApathy,  # 倦怠光波
    "BT_715": BonechewerBrawler,  # 噬骨殴斗者
    "CORE_EX1_622": ShadowWordDeath,  # 暗言术:灭
    "EX1_622": ShadowWordDeath,  # 暗言术:灭
    "BT_257": Apotheosis,  # 神圣化身
    "BAR_311": DevouringPlague,  # 噬灵疫病
    "BT_730": OverconfidentOrc,  # 狂傲的兽人
    "CORE_CS1_112": HolyNova,  # 神圣新星
    "CS1_112": HolyNova,  # 神圣新星
    "YOP_006": Hysteria,  # 狂乱
    "CORE_EX1_197": ShadowWordRuin,  # 暗言术:毁
    "EX1_197": ShadowWordRuin,  # 暗言术:毁
    "WC_014": AgainstAllOdds,  # 除奇致胜
    "BT_720": RuststeedRaider,  # 锈骑劫匪
    "BT_198": SoulMirror,  # 灵魂之镜
    "DMF_053": BloodOfGhuun,  # 戈霍恩之血
    "SCH_514": RaiseDead,  # 亡者复生
    "SW_442": VoidShard,  # 虚空碎片
    "DMF_054": Insight,  # 洞察
    "DMF_054t": InsightCorrupted,  # 洞察


    # 经典模式
    "VAN_CS2_042": FireElemental,
    "VAN_EX1_562": Onyxia,
    "VAN_EX1_248": FeralSpirit,
    "VAN_EX1_246": Hex,
    "VAN_EX1_238": LightingBolt,
    "VAN_EX1_085": MindControlTech,
    "VAN_EX1_284": AzureDrake,
    "VAN_EX1_259": LightningStorm,
    "VAN_CS2_189": ElvenArcher,
    "VAN_CS2_117": EarthenRingFarseer,
    "VAN_EX1_097": Abomination,
    "VAN_NEW1_021": DoomSayer,
    "VAN_NEW1_041": StampedingKodo,
    "VAN_EX1_590": BloodKnight,
    "VAN_EX1_247": StormforgedAxe,
    "VAN_EX1_116": LeeroyJenkins,
    "VAN_EX1_567": DoomHammer,
}
