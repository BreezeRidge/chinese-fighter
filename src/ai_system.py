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

        # 连段系统状态
        self.combo_step = 0          # 当前连段步骤（0=未开始）
        self.combo_window = 0.0      # 连段确认窗口剩余时间
        self._prev_opp_health = None # 上一帧对手血量（用于命中确认）

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

        # 更新连段窗口计时
        self.combo_window = max(0, self.combo_window - dt)
        if self.combo_window <= 0:
            self.combo_step = 0  # 窗口过期，连段中断

        # 命中确认：对手掉血 => 上一次攻击命中，可推进连段
        opp_hp = opponent.health
        just_hit = (self._prev_opp_health is not None
                    and opp_hp < self._prev_opp_health)
        self._prev_opp_health = opp_hp

        # 如果在冷却中，返回空操作
        if self.action_cooldown > 0:
            return keys_state

        distance = abs(ai_fighter.pos_x - opponent.pos_x)
        light_range = ai_fighter.stats.light_range
        heavy_range = ai_fighter.stats.heavy_range

        # 血量态势：落后时更激进，领先时更稳健
        hp_ratio = ai_fighter.health / ai_fighter.stats.max_health
        opp_hp_ratio = opp_hp / opponent.stats.max_health
        losing = hp_ratio < opp_hp_ratio - 0.15

        # ============ 优先级1：命中确认后的连段追击 ============
        # 刚打中或对手处于硬直，是格斗AI最该压迫的窗口。
        opp_stunned = opponent.state == FighterState.HIT
        if (just_hit or opp_stunned) and distance < heavy_range + 20:
            self.combo_step += 1
            self.combo_window = 0.45  # 保持连段意图
            return self._combo_attack(ai_fighter, opponent, keys_state)

        # ============ 优先级2：威胁检测——对手正在攻击 ============
        opp_attacking = opponent.state in [
            FighterState.ATTACK_LIGHT, FighterState.ATTACK_HEAVY, FighterState.SPECIAL
        ]
        if opp_attacking and distance < heavy_range + 30:
            # 落后时倾向闪避后反击而非被动格挡
            if losing and random.random() < self.dodge_chance:
                keys_state["left" if ai_fighter.facing_right else "right"] = True
                self._set_action_cooldown(0.6)
                return keys_state
            if random.random() < self.block_chance:
                keys_state["block"] = True
                self._set_action_cooldown(1.0)
                return keys_state
            if random.random() < self.dodge_chance:
                keys_state["left" if ai_fighter.facing_right else "right"] = True
                self._set_action_cooldown(0.6)
                return keys_state

        # ============ 优先级3：特殊招式（真实就绪时才放） ============
        if self._try_special(ai_fighter, opponent, distance, keys_state, losing):
            return keys_state

        # ============ 优先级4：基于攻击范围的距离决策 ============
        if distance <= light_range:
            # 已进入攻击范围：直接攻击
            return self._decide_attack(ai_fighter, opponent, keys_state)
        elif distance <= heavy_range + 30:
            # 边缘距离：进攻型/落后时直接重击进场，否则微调走位
            if self.personality == AIPersonality.AGGRESSIVE or losing:
                return self._decide_attack(ai_fighter, opponent, keys_state)
            if self.personality == AIPersonality.DEFENSIVE and random.random() < 0.4:
                keys_state["block"] = True
                self._set_action_cooldown(0.8)
                return keys_state
            return self._approach_opponent(ai_fighter, opponent)
        else:
            # 远距离：接近对手
            return self._approach_opponent(ai_fighter, opponent)

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

        # 攻击后冷却缩短，让AI能连续压迫（追击靠连段窗口衔接）
        # 选择攻击类型
        if self.personality == AIPersonality.AGGRESSIVE:
            # 进攻型：70%重攻击
            if random.random() < 0.7:
                keys_state["attack_heavy"] = True
                self._set_action_cooldown(0.9)
            else:
                keys_state["attack_light"] = True
                self._set_action_cooldown(0.5)
        elif self.personality == AIPersonality.DEFENSIVE:
            # 防守型：主要轻攻击（快速、破绽小）
            if random.random() < 0.8:
                keys_state["attack_light"] = True
                self._set_action_cooldown(0.5)
            else:
                keys_state["attack_heavy"] = True
                self._set_action_cooldown(0.9)
        else:  # BALANCED
            if random.random() < 0.5:
                keys_state["attack_light"] = True
                self._set_action_cooldown(0.5)
            else:
                keys_state["attack_heavy"] = True
                self._set_action_cooldown(0.9)

        return keys_state

    def _combo_attack(self, ai_fighter: Fighter, opponent: Fighter, keys_state: dict) -> dict:
        """
        连段追击：对手处于硬直/刚被命中时使用。
        套路——轻攻击起手确认命中，第2、3段接重攻击收尾，
        制造真实的连段压迫感，而非单发后撤。
        """
        for key in keys_state:
            keys_state[key] = False

        # 面向对手，避免打空
        if ai_fighter.pos_x < opponent.pos_x:
            keys_state["right"] = True
        else:
            keys_state["left"] = True

        if self.combo_step >= 3:
            # 第3段：重攻击/特殊收尾，然后重置连段
            keys_state["attack_heavy"] = True
            keys_state["right" if ai_fighter.pos_x < opponent.pos_x else "left"] = False
            self.combo_step = 0
            self._set_action_cooldown(0.8)
        elif self.combo_step == 2:
            keys_state["attack_heavy"] = True
            self._set_action_cooldown(0.7)
        else:
            # 起手用轻攻击，快且好确认
            keys_state["attack_light"] = True
            self._set_action_cooldown(0.4)
        return keys_state

    def _try_special(self, ai_fighter: Fighter, opponent: Fighter,
                     distance: float, keys_state: dict, losing: bool) -> bool:
        """
        尝试使用特殊招式——只在招式真实冷却完毕时才放，避免空按浪费决策帧。
        落后时提高使用意愿。返回是否决定使用。
        """
        moves = getattr(ai_fighter, "special_moves", None)
        system = getattr(ai_fighter, "special_move_system", None)
        if not moves or system is None:
            return False

        # 找出当前真正可用的招式
        ready = [m for m in moves if system.can_use(m)]
        if not ready:
            return False

        # 使用意愿：基础概率 + 落后加成
        chance = self.special_move_chance + (0.25 if losing else 0.0)
        if random.random() > chance:
            return False

        # 近距离才放（多数招式需贴身），远距离留着
        if distance > ai_fighter.stats.heavy_range + 60:
            return False

        # special_1 对应第一个招式键，special_2 对应第二个
        idx = 0 if len(ready) == 1 else random.randint(0, 1)
        keys_state["special_1" if idx == 0 else "special_2"] = True
        self._set_action_cooldown(1.2)
        return True

    def _set_action_cooldown(self, duration: float):
        """
        设置行动冷却。

        修复：旧公式 duration * (1/reaction_time) 会让反应快的HARD
        (reaction_time=0.15) 冷却被放大6.67倍，难度越高反而越迟钝。
        现在以 reaction_time 作为基础间隔，duration 只做微调缩放。
        """
        self.action_cooldown = self.reaction_time * duration


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
