"""
精灵图系统 - 角色动画管理
职责：加载、管理和渲染角色精灵动画
"""
import pygame
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class Animation:
    """动画数据类"""
    name: str
    frames: List[pygame.Surface]  # 帧列表
    frame_duration: float  # 每帧持续时间（秒）
    loop: bool = True  # 是否循环


class SpriteSheet:
    """精灵图管理器"""

    def __init__(self, image_path: str, frame_width: int, frame_height: int):
        """
        初始化精灵图

        Args:
            image_path: 精灵图路径
            frame_width: 单帧宽度
            frame_height: 单帧高度
        """
        import os
        self.frame_width = frame_width
        self.frame_height = frame_height

        try:
            # 检查文件是否存在
            if not os.path.exists(image_path):
                print(f"✗ 精灵图文件不存在: {image_path}")
                self.sheet = None
                return

            # 移除convert_alpha()以避免初始化顺序问题
            self.sheet = pygame.image.load(image_path)
            print(f"✓ 精灵图加载成功: {image_path}, 大小: {self.sheet.get_size()}")
        except Exception as e:
            # 如果加载失败，创建占位符
            print(f"✗ 精灵图加载失败: {image_path}, 错误: {e}")
            import traceback
            traceback.print_exc()
            self.sheet = None

    def get_frame(self, x: int, y: int) -> pygame.Surface:
        """
        从精灵图中提取单帧

        Args:
            x: 帧的X坐标（帧索引）
            y: 帧的Y坐标（行索引）

        Returns:
            单帧Surface
        """
        if self.sheet is None:
            # 返回占位符（彩色矩形）
            surface = pygame.Surface((self.frame_width, self.frame_height))
            surface.fill((200, 100, 100))
            return surface

        frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
        frame.blit(self.sheet, (0, 0),
                  (x * self.frame_width, y * self.frame_height,
                   self.frame_width, self.frame_height))
        return frame

    def get_frames(self, row: int, count: int) -> List[pygame.Surface]:
        """
        提取一行的多帧

        Args:
            row: 行索引
            count: 帧数

        Returns:
            帧列表
        """
        return [self.get_frame(i, row) for i in range(count)]


class AnimatedSprite:
    """动画精灵类"""

    def __init__(self):
        """初始化动画精灵"""
        self.animations: Dict[str, Animation] = {}
        self.current_animation: str = "idle"
        self.current_frame: int = 0
        self.frame_timer: float = 0.0
        self.facing_right: bool = True

    def add_animation(self, animation: Animation):
        """添加动画"""
        self.animations[animation.name] = animation

    def play(self, animation_name: str, reset: bool = True):
        """
        播放指定动画

        Args:
            animation_name: 动画名称
            reset: 是否重置到第一帧
        """
        if animation_name not in self.animations:
            return

        if self.current_animation != animation_name or reset:
            self.current_animation = animation_name
            self.current_frame = 0
            self.frame_timer = 0.0

    def update(self, dt: float):
        """更新动画"""
        if self.current_animation not in self.animations:
            return

        animation = self.animations[self.current_animation]
        self.frame_timer += dt

        # 切换到下一帧
        if self.frame_timer >= animation.frame_duration:
            self.frame_timer = 0.0
            self.current_frame += 1

            # 循环或停在最后一帧
            if self.current_frame >= len(animation.frames):
                if animation.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(animation.frames) - 1

    def get_current_frame(self) -> pygame.Surface:
        """获取当前帧"""
        if self.current_animation not in self.animations:
            # 返回占位符
            surface = pygame.Surface((64, 64))
            surface.fill((100, 100, 200))
            return surface

        animation = self.animations[self.current_animation]
        if not animation.frames:
            surface = pygame.Surface((64, 64))
            surface.fill((100, 200, 100))
            return surface

        frame = animation.frames[self.current_frame]

        # 水平翻转（如果面向左）
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)

        return frame


def create_placeholder_spritesheet(character_name: str, color: tuple) -> SpriteSheet:
    """
    创建占位符精灵图（用于开发阶段）

    Args:
        character_name: 角色名称
        color: 角色颜色

    Returns:
        SpriteSheet对象
    """
    # 创建临时精灵图（64x64像素）
    sheet_width = 64 * 8  # 8帧
    sheet_height = 64 * 6  # 6个动画
    sheet = pygame.Surface((sheet_width, sheet_height), pygame.SRCALPHA)

    font = pygame.font.Font(None, 12)

    # 为每个动画绘制占位符
    animations = ["idle", "walk", "jump", "attack_light", "attack_heavy", "hit"]

    for row, anim_name in enumerate(animations):
        for col in range(8):
            x = col * 64
            y = row * 64

            # 绘制矩形
            rect = pygame.Rect(x, y, 64, 64)
            pygame.draw.rect(sheet, color, rect)
            pygame.draw.rect(sheet, (255, 255, 255), rect, 2)

            # 绘制文字
            text = font.render(f"{anim_name[:4]}{col}", True, (255, 255, 255))
            text_rect = text.get_rect(center=(x + 32, y + 32))
            sheet.blit(text, text_rect)

    # 保存到内存（不保存到磁盘）
    # 创建SpriteSheet对象
    sprite_sheet = SpriteSheet.__new__(SpriteSheet)
    sprite_sheet.sheet = sheet
    sprite_sheet.frame_width = 64
    sprite_sheet.frame_height = 64

    return sprite_sheet


def load_character_animations(character_key: str) -> AnimatedSprite:
    """
    加载角色动画

    Args:
        character_key: 角色键名（"shaolin", "emei", "wudang"）

    Returns:
        AnimatedSprite对象
    """
    import os
    sprite = AnimatedSprite()

    # 定义角色颜色（占位符使用）
    colors = {
        "default": (150, 150, 150),
        "shaolin": (200, 100, 50),
        "emei": (100, 150, 200),
        "wudang": (150, 200, 100),
    }

    color = colors.get(character_key, colors["default"])

    # 构建正确的路径（相对于项目根目录）
    # main.py在src/目录下运行，需要回到上级目录
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sprite_path = os.path.join(base_path, "assets", "sprites", f"{character_key}.png")

    print(f"[DEBUG] 尝试加载精灵图: {sprite_path}")
    print(f"[DEBUG] 文件存在: {os.path.exists(sprite_path)}")

    # 尝试加载精灵图（如果不存在则使用占位符）
    try:
        sprite_sheet = SpriteSheet(sprite_path, 50, 50)
    except:
        # 创建占位符精灵图
        print(f"[DEBUG] 使用占位符精灵图: {character_key}")
        sprite_sheet = create_placeholder_spritesheet(character_key, color)

    # 定义动画（支持新的8帧高质量精灵图）
    animations_def = {
        "idle": (0, 8, 0.15),         # 行0，8帧，0.15秒/帧 (更流畅)
        "walk": (1, 8, 0.08),         # 行1，8帧，0.08秒/帧 (更流畅)
        "dash": (2, 8, 0.06),         # 行2，8帧，0.06秒/帧 (冲刺动画-快速)
        "jump": (3, 8, 0.12),         # 行3，8帧，0.12秒/帧
        "attack_light": (4, 8, 0.08), # 行4，8帧，0.08秒/帧 (攻击1)
        "attack_heavy": (5, 8, 0.1),  # 行5，8帧，0.1秒/帧 (攻击2)
        "hit": (6, 8, 0.08),          # 行6，8帧，0.08秒/帧 (受伤)
        "charge": (7, 8, 0.12),       # 行7，8帧，0.12秒/帧 (蓄力动画-爆气)
    }

    # 加载所有动画
    for anim_name, (row, count, duration) in animations_def.items():
        frames = sprite_sheet.get_frames(row, count)
        animation = Animation(
            name=anim_name,
            frames=frames,
            frame_duration=duration,
            loop=(anim_name not in ["attack_light", "attack_heavy", "hit"])
        )
        sprite.add_animation(animation)

    # 默认播放idle动画
    sprite.play("idle")

    return sprite
