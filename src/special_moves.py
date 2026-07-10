"""
特殊招式系统
设计原则：每个角色拥有独特的特殊招式，增加战斗深度
"""
from dataclasses import dataclass
from typing import Callable
import pygame


@dataclass
class SpecialMove:
    """
    特殊招式数据类

    Attributes:
        name: 招式名称
        key: 触发按键（pygame.K_*）
        cooldown: 冷却时间（秒）
        damage: 伤害值
        range: 攻击范围（像素）
        duration: 动画持续时间（秒）
        knockback: 击退力度
        cost: 能量消耗（预留，后续实现能量系统）
        description: 招式描述
    """
    name: str
    key: int
    cooldown: float
    damage: int
    range: int
    duration: float
    knockback: float
    cost: int = 0
    description: str = ""


class SpecialMoveSystem:
    """
    特殊招式管理系统
    职责：管理每个角色的特殊招式库，处理冷却时间
    """

    def __init__(self):
        # 招式冷却计时器 {招式名: 剩余冷却时间}
        self.cooldowns = {}

    def can_use(self, move: SpecialMove) -> bool:
        """检查招式是否可用（冷却完成）"""
        return self.cooldowns.get(move.name, 0) <= 0

    def use(self, move: SpecialMove):
        """使用招式（启动冷却）"""
        self.cooldowns[move.name] = move.cooldown

    def update(self, dt: float):
        """更新所有招式冷却时间"""
        for name in list(self.cooldowns.keys()):
            self.cooldowns[name] = max(0, self.cooldowns[name] - dt)

    def get_cooldown_percent(self, move: SpecialMove) -> float:
        """获取招式冷却百分比（0-1，0=可用，1=刚使用）"""
        if move.cooldown == 0:
            return 0
        return self.cooldowns.get(move.name, 0) / move.cooldown


# ============================================================================
# 角色特殊招式定义
# ============================================================================

# 少林僧 - 力量型
SHAOLIN_SPECIAL_1 = SpecialMove(
    name="罗汉拳",
    key=pygame.K_q,  # Q键
    cooldown=5.0,
    damage=25,
    range=120,
    duration=0.6,
    knockback=300,
    cost=30,
    description="蓄力重击，造成巨额伤害和击退"
)

SHAOLIN_SPECIAL_2 = SpecialMove(
    name="金刚身",
    key=pygame.K_e,  # E键
    cooldown=8.0,
    damage=0,
    range=0,
    duration=3.0,  # 持续3秒
    knockback=0,
    cost=50,
    description="3秒内受到伤害减少70%，移动速度-30%"
)

# 峨眉剑客 - 速度型
EMEI_SPECIAL_1 = SpecialMove(
    name="飞燕斩",
    key=pygame.K_q,
    cooldown=4.0,
    damage=18,
    range=150,
    duration=0.3,
    knockback=100,
    cost=25,
    description="快速前冲斩击，超远攻击范围"
)

EMEI_SPECIAL_2 = SpecialMove(
    name="疾风步",
    key=pygame.K_e,
    cooldown=6.0,
    damage=0,
    range=0,
    duration=2.0,  # 持续2秒
    knockback=0,
    cost=35,
    description="2秒内移动速度+100%，攻击速度+50%"
)

# 武当道士 - 防御型（新角色）
WUDANG_SPECIAL_1 = SpecialMove(
    name="太极推手",
    key=pygame.K_q,
    cooldown=5.0,
    damage=10,
    range=100,
    duration=0.4,
    knockback=400,  # 超强击退
    cost=30,
    description="四两拨千斤，低伤害但超强击退"
)

WUDANG_SPECIAL_2 = SpecialMove(
    name="太极气盾",
    key=pygame.K_e,
    cooldown=10.0,
    damage=0,
    range=0,
    duration=4.0,  # 持续4秒
    knockback=0,
    cost=60,
    description="4秒内格挡成功时反弹50%伤害给攻击者"
)

# 默认角色（无特殊招式）
DEFAULT_SPECIAL_1 = SpecialMove(
    name="普通重击",
    key=pygame.K_q,
    cooldown=3.0,
    damage=20,
    range=110,
    duration=0.5,
    knockback=150,
    cost=20,
    description="增强版重攻击"
)

DEFAULT_SPECIAL_2 = SpecialMove(
    name="闪避",
    key=pygame.K_e,
    cooldown=5.0,
    damage=0,
    range=0,
    duration=0.5,
    knockback=0,
    cost=25,
    description="短暂无敌"
)


# 角色招式映射表
CHARACTER_SPECIAL_MOVES = {
    "default": [DEFAULT_SPECIAL_1, DEFAULT_SPECIAL_2],
    "shaolin": [SHAOLIN_SPECIAL_1, SHAOLIN_SPECIAL_2],
    "emei": [EMEI_SPECIAL_1, EMEI_SPECIAL_2],
    "wudang": [WUDANG_SPECIAL_1, WUDANG_SPECIAL_2],
}


def get_special_moves(character_key: str) -> list[SpecialMove]:
    """
    获取角色的特殊招式列表

    Args:
        character_key: 角色键名（如 "shaolin", "emei"）

    Returns:
        包含2个特殊招式的列表
    """
    return CHARACTER_SPECIAL_MOVES.get(character_key, CHARACTER_SPECIAL_MOVES["default"])
