"""
特殊招式系统 - 增益效果处理
武当道士、少林僧、峨眉剑客的特殊能力实现
"""

# 增益效果类型
class BuffType:
    """增益效果类型枚举"""
    DEFENSE = "defense"  # 防御增强（金刚身、太极气盾）
    SPEED = "speed"      # 速度增强（疾风步）
    INVINCIBLE = "invincible"  # 无敌（闪避）
    REFLECT = "reflect"  # 反伤（太极气盾）


def apply_wudang_shield_buff(fighter):
    """武当道士 - 太极气盾效果"""
    fighter.active_buffs["太极气盾"] = 4.0  # 持续4秒
    fighter.active_buffs["reflect_damage"] = 0.5  # 反伤50%


def apply_shaolin_body_buff(fighter):
    """少林僧 - 金刚身效果"""
    fighter.active_buffs["金刚身"] = 3.0  # 持续3秒
    fighter.active_buffs["damage_reduction"] = 0.7  # 减伤70%
    fighter.active_buffs["speed_penalty"] = -0.3  # 速度减少30%


def apply_emei_speed_buff(fighter):
    """峨眉剑客 - 疾风步效果"""
    fighter.active_buffs["疾风步"] = 2.0  # 持续2秒
    fighter.active_buffs["speed_boost"] = 1.0  # 速度提升100%
    fighter.active_buffs["attack_speed_boost"] = 0.5  # 攻击速度提升50%
