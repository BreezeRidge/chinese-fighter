"""
游戏常量配置
所有硬编码值集中管理，方便调试和平衡性调整
"""
from dataclasses import dataclass
from typing import Tuple

# ============================================================================
# 窗口与显示
# ============================================================================
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60
TITLE = "武林争霸 Wulin Champions"

# ============================================================================
# 游戏规则
# ============================================================================
ROUND_TIME = 99  # 回合时间（秒）
GRAVITY = 2000  # 重力加速度（像素/秒²）
GROUND_Y = 600  # 地面Y坐标

# ============================================================================
# 角色基础属性
# ============================================================================
@dataclass
class CharacterStats:
    """角色属性数据类"""
    name: str
    max_health: int
    move_speed: float  # 像素/秒
    jump_velocity: float  # 初始跳跃速度（向上为负）
    width: int
    height: int

    # 攻击属性
    light_damage: int
    light_range: int
    light_duration: float  # 秒

    heavy_damage: int
    heavy_range: int
    heavy_duration: float
    heavy_knockback: float  # 击退速度（像素/秒）

    # 战斗机制
    hit_stun_duration: float  # 受击硬直
    block_reduction: float  # 格挡减伤比例（0-1）


# 预设角色配置
DEFAULT_FIGHTER = CharacterStats(
    name="默认角色",
    max_health=100,
    move_speed=300,
    jump_velocity=-600,
    width=60,
    height=100,
    light_damage=5,
    light_range=80,
    light_duration=0.2,
    heavy_damage=15,
    heavy_range=100,
    heavy_duration=0.4,
    heavy_knockback=200,
    hit_stun_duration=0.3,
    block_reduction=0.5,
)

SHAOLIN_MONK = CharacterStats(
    name="少林僧",
    max_health=120,  # 血厚
    move_speed=280,  # 速度慢
    jump_velocity=-550,
    width=65,
    height=105,
    light_damage=6,
    light_range=75,
    light_duration=0.25,
    heavy_damage=20,  # 重攻击伤害高
    heavy_range=90,
    heavy_duration=0.5,
    heavy_knockback=250,
    hit_stun_duration=0.3,
    block_reduction=0.6,  # 格挡效果好
)

EMEI_SWORDSMAN = CharacterStats(
    name="峨眉剑客",
    max_health=85,  # 血薄
    move_speed=350,  # 速度快
    jump_velocity=-650,
    width=55,
    height=95,
    light_damage=4,
    light_range=100,  # 剑的攻击范围远
    light_duration=0.15,  # 攻击快
    heavy_damage=12,
    heavy_range=120,
    heavy_duration=0.3,
    heavy_knockback=150,
    hit_stun_duration=0.25,
    block_reduction=0.4,
)

# 角色选择字典
CHARACTERS = {
    "default": DEFAULT_FIGHTER,
    "shaolin": SHAOLIN_MONK,
    "emei": EMEI_SWORDSMAN,
}

# ============================================================================
# 战斗机制
# ============================================================================
ATTACK_COOLDOWN = 0.1  # 攻击间隔（秒）
COMBO_TIMEOUT = 0.8  # 连击超时（秒）
FRICTION = 0.85  # 地面摩擦力（每帧速度衰减）

# ============================================================================
# 视觉设计 - 中式配色
# ============================================================================
# 传统中国色彩参考：
# 朱红（Vermilion）、墨黑（Ink Black）、青绿（Celadon）、
# 金黄（Imperial Gold）、米白（Rice White）

class Color:
    """颜色常量类"""
    # 背景
    BG = (240, 235, 220)  # 宣纸米白
    GROUND = (90, 75, 60)  # 青砖灰褐

    # 玩家颜色（临时，后期替换为精灵图）
    PLAYER1 = (200, 50, 50)  # 朱红
    PLAYER2 = (50, 100, 150)  # 青蓝

    # UI颜色
    UI_BG = (40, 40, 40)  # 深灰背景
    HP_FULL = (220, 50, 50)  # 满血红
    HP_LOW = (180, 30, 30)  # 低血暗红
    HP_BG = (60, 60, 60)  # 血条背景

    TEXT_PRIMARY = (255, 255, 255)  # 主文字白色
    TEXT_GOLD = (255, 215, 0)  # 金色强调
    TEXT_SHADOW = (0, 0, 0)  # 文字阴影

    # 调试颜色
    DEBUG_HITBOX = (0, 255, 0)  # 绿色受击盒
    DEBUG_ATTACKBOX = (255, 0, 0)  # 红色攻击盒

# ============================================================================
# 按键映射
# ============================================================================
class Controls:
    """按键配置类"""
    # 玩家1（左侧）- WASD + FGH
    P1_LEFT = 'a'
    P1_RIGHT = 'd'
    P1_JUMP = 'w'
    P1_LIGHT = 'f'
    P1_HEAVY = 'g'
    P1_BLOCK = 'h'

    # 玩家2（右侧）- 方向键 + JKL
    P2_LEFT = 'left'
    P2_RIGHT = 'right'
    P2_JUMP = 'up'
    P2_LIGHT = 'j'
    P2_HEAVY = 'k'
    P2_BLOCK = 'l'

# ============================================================================
# 资源路径（为后续资产加载预留）
# ============================================================================
class Paths:
    """资源路径常量"""
    ASSETS = "../assets"
    SPRITES = f"{ASSETS}/sprites"
    AUDIO = f"{ASSETS}/audio"
    FONTS = f"{ASSETS}/fonts"

    # 角色精灵图（待添加）
    SHAOLIN_SPRITE = f"{SPRITES}/shaolin.png"
    EMEI_SPRITE = f"{SPRITES}/emei.png"

    # 音效（待添加）
    SOUND_HIT = f"{AUDIO}/hit.wav"
    SOUND_BLOCK = f"{AUDIO}/block.wav"
    SOUND_JUMP = f"{AUDIO}/jump.wav"
