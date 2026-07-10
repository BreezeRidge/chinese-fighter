"""
AI对战系统
职责：为单人模式提供AI控制的对手
"""
import pygame
import random
from enum import Enum, auto
from typing import Optional
from fighter import Fighter, FighterState


class AIPersonality(Enum):
    """AI性格类型"""
    AGGRESSIVE = auto()  # 进攻型：频繁攻击
    DEFENSIVE = auto()   # 防守型：多格挡
    BALANCED = auto()    # 平衡型：攻防兼备


class AIDifficulty(Enum):
    """AI难度等级"""
    EASY = auto()      # 简单：反应慢，随机性高
    MEDIUM = auto()    # 中等：正常反应
    HARD = auto()      # 困难：快速反应，预判能力


class AIController:
    """
    AI控制器
    根据战斗状态决定AI的行动
    """

    def __init__(self, difficulty: AIDifficulty = AIDifficulty.MEDIUM,
                 personality: AIPersonality = AIPersonality.BALANCED):
        """
        初始化AI控制器

        Args:
            difficulty: AI难度
            personality: AI性格
        """
        self.difficulty = difficulty
        self.personality = personality

        # AI状态
        self.action_cooldown = 0.0  # 行动冷却
        self.current_action = None  # 当前行动
        self.action_duration = 0.0  # 行动持续时间

        # 难度参数
        self._set_difficulty_params()

    def _set_difficulty_params(self):
        """根据难度设置参数"""
        if self.difficulty == AIDifficulty.EASY:
            self.reaction_time = 0.5  # 反应时间（秒）
            self.attack_frequency = 0.3  # 攻击频率
            self.dodge_chance = 0.2  # 闪避概率
            self.block_chance = 0.3  # 格挡概率
            self.special_move_chance = 0.1  # 使用特殊招式概率
        elif self.difficulty == AIDifficulty.MEDIUM:
            self.reaction_time = 0.3
            self.attack_frequency = 0.5
            self.dodge_chance = 0.4
            self.block_chance = 0.5
            self.special_move_chance = 0.3
        else:  # HARD
            self.reaction_time = 0.15
            self.attack_frequency = 0.7
            self.dodge_chance = 0.6
            self.block_chance = 0.7
            self.special_move_chance = 0.5

    def update(self, dt: float, ai_fighter: Fighter, opponent: Fighter) -> dict:
        """
        更新AI决策

        Args:
            dt: delta time
            ai_fighter: AI控制的角色
            opponent: 对手

        Returns:
            按键状态字典 {"left": bool, "right": bool, ...}
        """
        # 更新冷却
        self.action_cooldown = max(0, self.action_cooldown - dt)

        # 初始化按键状态
        keys_state = {
            "left": False,
            "right": False,
            "jump": False,
            "attack_light": False,
            "attack_heavy": False,
            "block": False,
            "special_1": False,
            "special_2": False,
        }

        # 如果在冷却中，返回空操作
        if self.action_cooldown > 0:
            return keys_state

        # AI决策逻辑
        distance = abs(ai_fighter.pos_x - opponent.pos_x)

        # 1. 威胁检测：对手正在攻击
        if opponent.state in [FighterState.ATTACK_LIGHT, FighterState.ATTACK_HEAVY, FighterState.SPECIAL]:
            if distance < 150:
                # 尝试格挡或闪避
                if random.random() < self.block_chance:
                    keys_state["block"] = True
                    self._set_action_cooldown(0.3)
                    return keys_state
                elif random.random() < self.dodge_chance:
                    # 后退
                    keys_state["left" if ai_fighter.facing_right else "right"] = True
                    self._set_action_cooldown(0.2)
                    return keys_state

        # 2. 距离判断
        if distance > 200:
            # 远距离：接近对手
            return self._approach_opponent(ai_fighter, opponent)
        elif distance > 100:
            # 中距离：根据性格决定
            if self.personality == AIPersonality.AGGRESSIVE:
                return self._decide_attack(ai_fighter, opponent, keys_state)
            elif self.personality == AIPersonality.DEFENSIVE:
                if random.random() < 0.5:
                    return self._approach_opponent(ai_fighter, opponent)
                else:
                    keys_state["block"] = True
                    self._set_action_cooldown(0.3)
                    return keys_state
            else:  # BALANCED
                if random.random() < self.attack_frequency:
                    return self._decide_attack(ai_fighter, opponent, keys_state)
                else:
                    return self._approach_opponent(ai_fighter, opponent)
        else:
            # 近距离：攻击或格挡
            return self._decide_attack(ai_fighter, opponent, keys_state)

    def _approach_opponent(self, ai_fighter: Fighter, opponent: Fighter) -> dict:
        """接近对手"""
        keys_state = {k: False for k in ["left", "right", "jump", "attack_light",
                                        "attack_heavy", "block", "special_1", "special_2"]}

        if ai_fighter.pos_x < opponent.pos_x:
            keys_state["right"] = True
        else:
            keys_state["left"] = True

        # 偶尔跳跃接近
        if random.random() < 0.1:
            keys_state["jump"] = True

        self._set_action_cooldown(0.1)
        return keys_state

    def _decide_attack(self, ai_fighter: Fighter, opponent: Fighter, keys_state: dict) -> dict:
        """决定攻击方式"""
        # 重置所有按键
        for key in keys_state:
            keys_state[key] = False

        # 优先使用特殊招式（如果可用）
        if random.random() < self.special_move_chance:
            if random.random() < 0.5:
                keys_state["special_1"] = True
                self._set_action_cooldown(0.5)
                return keys_state
            else:
                keys_state["special_2"] = True
                self._set_action_cooldown(0.5)
                return keys_state

        # 选择攻击类型
        if self.personality == AIPersonality.AGGRESSIVE:
            # 进攻型：70%重攻击
            if random.random() < 0.7:
                keys_state["attack_heavy"] = True
                self._set_action_cooldown(0.5)
            else:
                keys_state["attack_light"] = True
                self._set_action_cooldown(0.3)
        elif self.personality == AIPersonality.DEFENSIVE:
            # 防守型：主要轻攻击
            if random.random() < 0.8:
                keys_state["attack_light"] = True
                self._set_action_cooldown(0.3)
            else:
                keys_state["attack_heavy"] = True
                self._set_action_cooldown(0.5)
        else:  # BALANCED
            if random.random() < 0.5:
                keys_state["attack_light"] = True
                self._set_action_cooldown(0.3)
            else:
                keys_state["attack_heavy"] = True
                self._set_action_cooldown(0.5)

        return keys_state

    def _set_action_cooldown(self, duration: float):
        """设置行动冷却"""
        self.action_cooldown = duration * (1.0 / self.reaction_time)


class AIKeyWrapper:
    """
    AI按键包装器
    将AI决策转换为pygame按键格式
    """

    def __init__(self, ai_controller: AIController, ai_fighter: Fighter, opponent: Fighter):
        """
        初始化AI按键包装器

        Args:
            ai_controller: AI控制器
            ai_fighter: AI控制的角色
            opponent: 对手
        """
        self.ai_controller = ai_controller
        self.ai_fighter = ai_fighter
        self.opponent = opponent
        self.keys_state = {}

    def update(self, dt: float):
        """更新AI决策"""
        self.keys_state = self.ai_controller.update(dt, self.ai_fighter, self.opponent)

    def __getitem__(self, key: int) -> bool:
        """
        实现pygame按键接口

        Args:
            key: pygame按键常量

        Returns:
            是否按下
        """
        # 映射pygame按键到AI决策
        key_mapping = {
            pygame.K_LEFT: "left",
            pygame.K_RIGHT: "right",
            pygame.K_UP: "jump",
            pygame.K_j: "attack_light",
            pygame.K_k: "attack_heavy",
            pygame.K_l: "block",
            pygame.K_q: "special_1",
            pygame.K_e: "special_2",
        }

        action = key_mapping.get(key)
        if action:
            return self.keys_state.get(action, False)

        return False


def create_ai_opponent(difficulty: AIDifficulty = AIDifficulty.MEDIUM,
                      personality: AIPersonality = AIPersonality.BALANCED,
                      character_key: str = "shaolin") -> tuple:
    """
    创建AI对手

    Args:
        difficulty: AI难度
        personality: AI性格
        character_key: 角色类型

    Returns:
        (Fighter, AIController) 元组
    """
    from config import GROUND_Y

    # 创建AI角色
    ai_fighter = Fighter(800, GROUND_Y, character_key, 2)

    # 创建AI控制器
    ai_controller = AIController(difficulty, personality)

    return ai_fighter, ai_controller
