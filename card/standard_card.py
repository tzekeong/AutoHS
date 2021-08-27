from card.basic_card import *


# 护甲商贩
class ArmorVendor(MinionNoPoint):
    value = 2
    keep_in_hand_bool = True


# 神圣惩击
class HolySmite(SpellPointOppo):
    wait_time = 2
    spell_damage = 3
    # 加个bias,一是包含了消耗的水晶的代价，二是包含了消耗了手牌的代价
    bias = -2

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_oppo_index = -1
        best_delta_h = 0
        spell_damage = cls.get_spell_damage(state)
        for oppo_index, oppo_minion in enumerate(state.oppo_minions):

            if not oppo_minion.can_be_pointed_by_spell:
                continue

            temp_delta_h = oppo_minion.delta_h_after_damage(spell_damage) + cls.bias
            if temp_delta_h > best_delta_h:
                best_delta_h = temp_delta_h
                best_oppo_index = oppo_index

        return best_delta_h, best_oppo_index


# 倦怠光波
class WaveOfApathy(SpellNoPoint):
    wait_time = 2
    bias = -4

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        tmp = 0

        for minion in state.oppo_minions:
            tmp += minion.attack - 1

        return tmp + cls.bias,


# 噬骨殴斗者
class BonechewerBrawler(MinionNoPoint):
    value = 2
    keep_in_hand_bool = True


# 暗言术灭
class ShadowWordDeath(SpellPointOppo):
    wait_time = 1.5
    bias = -6

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_oppo_index = -1
        best_delta_h = 0

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if oppo_minion.attack < 5:
                continue
            if not oppo_minion.can_be_pointed_by_spell:
                continue

            tmp = oppo_minion.heuristic_val + cls.bias
            if tmp > best_delta_h:
                best_delta_h = tmp
                best_oppo_index = oppo_index

        return best_delta_h, best_oppo_index


# 神圣化身
class Apotheosis(SpellPointMine):
    bias = -6

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_delta_h = 0
        best_mine_index = -1

        for my_index, my_minion in enumerate(state.my_minions):
            if not my_minion.can_be_pointed_by_spell:
                continue

            tmp = cls.bias + 3 + (my_minion.health + 2) / 4 + \
                  (my_minion.attack + 1) / 2
            if my_minion.can_attack_minion:
                tmp += my_minion.attack / 4
            if tmp > best_delta_h:
                best_delta_h = tmp
                best_mine_index = my_index

        return best_delta_h, best_mine_index


# 亡首教徒
class DeathsHeadCultist(MinionNoPoint):
    value = 1
    keep_in_hand_bool = True


# 噬灵疫病
class DevouringPlague(SpellNoPoint):
    wait_time = 4
    bias = -4  # 把吸的血直接算进bias

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        curr_h = state.heuristic_value

        delta_h_sum = 0
        sample_times = 5

        for i in range(sample_times):
            tmp_state = state.copy_new_one()
            for j in range(4):
                tmp_state.random_distribute_damage(1, [i for i in range(tmp_state.oppo_minion_num)], [])

            delta_h_sum += tmp_state.heuristic_value - curr_h

        return delta_h_sum / sample_times + cls.bias,


# 狂傲的兽人
class OverconfidentOrc(MinionNoPoint):
    value = 3
    keep_in_hand_bool = True


# 神圣新星
class HolyNova(SpellNoPoint):
    bias = -8

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        return cls.bias + sum([minion.delta_h_after_damage(2)
                               for minion in state.oppo_minions]),


# 狂乱
class Hysteria(SpellPointOppo):
    wait_time = 5
    bias = -9  # 我觉得狂乱应该要能力挽狂澜
    keep_in_hand_bool = False

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_delta_h = 0
        best_arg = 0
        sample_times = 10

        if state.oppo_minion_num == 0 or state.oppo_minion_num + state.my_minion_num == 1:
            return 0, -1

        for chosen_index, chosen_minion in enumerate(state.oppo_minions):
            if not chosen_minion.can_be_pointed_by_spell:
                continue

            delta_h_count = 0

            for i in range(sample_times):
                tmp_state = state.copy_new_one()
                tmp_chosen_index = chosen_index

                while True:
                    another_index_list = [j for j in range(tmp_state.oppo_minion_num + tmp_state.my_minion_num)]
                    another_index_list.pop(tmp_chosen_index)
                    if len(another_index_list) == 0:
                        break
                    another_index = another_index_list[random.randint(0, len(another_index_list) - 1)]

                    # print("another index: ", another_index)
                    if another_index >= tmp_state.oppo_minion_num:
                        another_minion = tmp_state.my_minions[another_index - tmp_state.oppo_minion_num]
                        if another_minion.get_damaged(chosen_minion.attack):
                            tmp_state.my_minions.pop(another_index - tmp_state.oppo_minion_num)
                    else:
                        another_minion = tmp_state.oppo_minions[another_index]
                        if another_minion.get_damaged(chosen_minion.attack):
                            tmp_state.oppo_minions.pop(another_index)
                            if another_index < tmp_chosen_index:
                                tmp_chosen_index -= 1

                    if chosen_minion.get_damaged(another_minion.attack):
                        # print("h:", tmp_state.heuristic_value, state.heuristic_value)
                        tmp_state.oppo_minions.pop(tmp_chosen_index)
                        break

                    # print("h:", tmp_state.heuristic_value, state.heuristic_value)

                delta_h_count += tmp_state.heuristic_value - state.heuristic_value

            delta_h_count /= sample_times
            # print("average delta_h:", delta_h_count)
            if delta_h_count > best_delta_h:
                best_delta_h = delta_h_count
                best_arg = chosen_index

        return best_delta_h + cls.bias, best_arg


# 暗言术毁
class ShadowWordRuin(SpellNoPoint):
    bias = -8
    keep_in_hand_bool = False

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        return cls.bias + sum([minion.heuristic_val
                               for minion in state.oppo_minions
                               if minion.attack >= 5]),


# 除奇致胜
class AgainstAllOdds(SpellNoPoint):
    bias = -9
    keep_in_hand_bool = False

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        return cls.bias + \
               sum([minion.heuristic_val
                    for minion in state.oppo_minions
                    if minion.attack % 2 == 1]) - \
               sum([minion.heuristic_val
                    for minion in state.my_minions
                    if minion.attack % 2 == 1]),


# 锈骑劫匪
class RuststeedRaider(MinionNoPoint):
    value = 3
    keep_in_hand_bool = False
    # TODO: 也许我可以为突袭随从专门写一套价值评判?


# 泰兰佛丁
class TaelanFordring(MinionNoPoint):
    value = 3
    keep_in_hand_bool = False

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        h_value = 1

        card_to_draw = ["WC_030",  # 吃手鱼
                        ]

        ctun_part = ("DMF_254t3",  # 克苏恩之眼
                     "DMF_254t4",  # 克苏恩之心
                     "DMF_254t5",  # 克苏恩之躯
                     "DMF_254t7",  # 克苏恩之口
                     )

        num_ctun_part_played = 0

        for card in state.my_minions:
            if card.card_id in ctun_part:
                num_ctun_part_played += 1

        if num_ctun_part_played >= 4:
            card_to_draw.append(
                "DMF_254"  # 克苏恩，破碎之劫
            )

        drawn_zone = state.my_graveyard + state.my_minions + state.my_hand_cards

        for card_id in card_to_draw:
            if any(card.card_id == card_id for card in drawn_zone):
                card_to_draw.remove(card_id)

        if len(card_to_draw) > 0:
            return h_value + 3,

        return h_value,


# 凯恩血蹄
class CairneBloodhoof(MinionNoPoint):
    value = 6
    keep_in_hand_bool = False


# 吃奖励鱼
class MutanusTheDevourer(MinionNoPoint):
    value = 5

    keep_in_hand_bool = True

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        quest_start = ("SW_028",  # 开进码头
                       "SW_031",  # 号令元素
                       "SW_039",  # 一决胜负
                       "SW_052",  # 探查内鬼
                       "SW_091",  # 恶魔之种
                       "SW_313",  # 挺身而出
                       "SW_322",  # 保卫矮人区
                       "SW_428",  # 游园迷梦
                       "SW_433",  # 寻求指引
                       "SW_450",  # 巫师的计策
                       )

        quest_complete = ("SW_028t2",  # 保证补给
                          "SW_031t2",  # 驯服火焰
                          "SW_039t3",  # 关闭传送门
                          "SW_052t2",  # 标出叛徒
                          "SW_091t3",  # 完成仪式
                          "SW_313t2",  # 为逝者复仇
                          "SW_322t2",  # 干掉他们
                          "SW_428t2",  # 野性暴朋
                          "SW_433t2",  # 照亮虚空
                          "SW_450t2",  # 抵达传送大厅
                          )

        quest_reward = ("SW_028t5",  # 船长洛卡拉
                        "SW_031t7",  # 风暴召唤者布鲁坎
                        "SW_039t3_t",  # 屠魔者库尔特鲁斯
                        "SW_052t3",  # 间谍大师斯卡布斯
                        "SW_091t4",  # 枯萎化身塔姆辛
                        "SW_313t4",  # 圣光化身凯瑞尔
                        "SW_322t4",  # 射击大师塔维什
                        "SW_428t4",  # 铁肤古夫
                        "SW_433t3",  # 圣徒泽瑞拉
                        "SW_450t4",  # 奥术师晨拥
                        )

        # 如果对手有任务
        if any(card.card_id in quest_start for card in state.oppo_graveyard):
            # 如果任务没有完成, 先不打出来
            if not any(card1.card_id in quest_complete for card1 in state.oppo_graveyard):
                return 0,
            # 如果任务完成，并且奖励还在手上, 马上打出来
            elif all(card1.card_id not in quest_reward for card1 in state.oppo_graveyard) and \
                    all(card1.card_id not in quest_reward for card1 in state.oppo_minions):
                return 1000,

        # 如果对手没有任务，或奖励已经打出来
        return 2,


# 灵魂之镜
class SoulMirror(SpellNoPoint):
    wait_time = 5
    bias = -16
    keep_in_hand_bool = False

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        copy_number = min(7 - state.my_minion_num, state.oppo_minion_num)
        h_sum = 0
        for i in range(copy_number):
            h_sum += state.oppo_minions[i].heuristic_val

        return h_sum + cls.bias,


# 戈霍恩之血
class BloodOfGhuun(MinionNoPoint):
    value = 8


# 亡者复生
class RaiseDead(SpellNoPoint):
    wait_time = 2
    bias = -4

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):

        my_graveyard_minion_num = 0
        for card in state.my_graveyard:
            if card.cardtype == CARD_MINION:
                my_graveyard_minion_num += 1

        if my_graveyard_minion_num >= 2:
            return cls.bias + 9 - state.my_hand_card_num,

        return 0,


class VoidShard(SpellPointOppo):
    wait_time = 2
    spell_damage = 4
    bias = -5

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_oppo_index = -1
        best_delta_h = 0
        spell_damage = cls.get_spell_damage(state)
        cls.bias += min(spell_damage, 30 - state.my_hero.health)

        # 看打脸会赢吗？
        if state.oppo_hero.health <= spell_damage:
            return 1000, -1

        for oppo_index, oppo_minion in enumerate(state.targetable_oppo_minions):
            temp_delta_h = oppo_minion.delta_h_after_damage(spell_damage) + cls.bias
            if temp_delta_h > best_delta_h:
                best_delta_h = temp_delta_h
                best_oppo_index = oppo_index

        temp_delta_h = state.oppo_hero.delta_h_after_damage(spell_damage) + cls.bias
        if temp_delta_h > best_delta_h:
            best_delta_h = temp_delta_h
            best_oppo_index = -1

        return best_delta_h, best_oppo_index


# 异教低阶牧师
class CultNeophyte(MinionNoPoint):
    value = 2


# 卡加尔·战痕
class KargalBattlescar(MinionNoPoint):
    keep_in_hand_bool = False

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        post = ("BAR_074",  # 前沿哨所
                "BAR_075",  # 十字路口哨所
                "BAR_076",  # 莫尔杉哨所
                )
        post_num = 0
        for card in state.my_graveyard:
            if card.card_id in post:
                post_num += 1

        return -2 + (post_num * 3),


# 克苏恩，破碎之劫
class CTunTheShattered(MinionNoPoint):
    bias = -11

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        hero_health = state.oppo_hero.health
        total_minion_health = 0
        for minion in state.oppo_minions:
            total_minion_health += minion.health

        if hero_health + total_minion_health <= 30:
            return 1000,

        if hero_health > 30:
            return 0,

        # 英雄死亡的可能性
        h_value = 30 * hero_health / (hero_health + total_minion_health)

        return h_value + cls.bias,


# 克苏恩之眼
class EyeOfCTun(SpellNoPoint):
    wait_time = 2
    spell_damage = 7
    bias = -6  # 把吸的血直接算进bias

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        curr_h = state.heuristic_value

        delta_h_sum = 0
        sample_times = 5

        for i in range(sample_times):
            spell_damage = cls.get_spell_damage(state)
            tmp_state = state.copy_new_one()
            for j in range(spell_damage):
                tmp_state.random_distribute_damage(1, [i for i in range(tmp_state.oppo_minion_num)], [])

            delta_h_sum += tmp_state.heuristic_value - curr_h

        return delta_h_sum / sample_times + cls.bias,


# 克苏恩之心
class HeartOfCTun(SpellNoPoint):
    wait_time = 2
    bias = -6
    spell_damage = 3

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        spell_dmg = cls.spell_damage + state.my_total_spell_power

        h_value = sum([minion.delta_h_after_damage(spell_dmg) for minion in state.oppo_minions]) - \
                  sum([minion.delta_h_after_damage(spell_dmg) for minion in state.my_minions])
        return cls.bias + h_value,


# 克苏恩之躯
class BodyOfCTun(SpellNoPoint):
    wait_time = 2

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        return 3,


# 克苏恩之口
class MawOfCTun(SpellPointOppo):
    wait_time = 2
    bias = -6

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_oppo_index = -1
        best_delta_h = 0

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_spell:
                continue
            tmp = oppo_minion.heuristic_val + cls.bias
            if tmp > best_delta_h:
                best_delta_h = tmp
                best_oppo_index = oppo_index

        return best_delta_h, best_oppo_index


# 博学者普克尔特
class LorekeeperPolkelt(MinionNoPoint):
    keep_in_hand_bool = True

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        h_value = 1

        card_to_draw = ["WC_030",  # 吃手鱼
                        ]

        ctun_part = ("DMF_254t3",  # 克苏恩之眼
                     "DMF_254t4",  # 克苏恩之心
                     "DMF_254t5",  # 克苏恩之躯
                     "DMF_254t7",  # 克苏恩之口
                     )

        num_ctun_part_played = 0

        for card in state.my_minions:
            if card.card_id in ctun_part:
                num_ctun_part_played += 1

        if num_ctun_part_played >= 4:
            card_to_draw.append(
                "DMF_254"  # 克苏恩，破碎之劫
            )

        drawn_zone = state.my_graveyard + state.my_minions + state.my_hand_cards

        for card_id in card_to_draw:
            if any(card.card_id == card_id for card in drawn_zone):
                card_to_draw.remove(card_id)

        if len(card_to_draw) > 0:
            return h_value + 3,

        return h_value,


# 洞察
class Insight(SpellNoPoint):
    wait_time = 2

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        return 0,


# 洞察(已腐蚀)
class InsightCorrupted(SpellNoPoint):
    wait_time = 2

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        return 1,
