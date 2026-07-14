"""
UI管理器 - 负责所有界面渲染
设计原则：分离UI逻辑，提升可维护性和视觉一致性
修复：中文显示乱码问题 - 使用系统中文字体
"""
import pygame
from typing import Optional
import sys
import os
from config import Color, WINDOW_WIDTH, WINDOW_HEIGHT


def get_chinese_font(size: int) -> pygame.font.Font:
    """
    获取支持中文的字体
    macOS/Windows/Linux 自动适配

    重要：优先使用 .ttf 单字体文件，避免使用 .ttc 集合字体。
    某些系统 .ttc 字体（如 Songti.ttc）在 macOS + SDL2_ttf 2.24 下
    存在内存管理缺陷，在持续渲染时会触发段错误(SIGSEGV)。
    详见 PERFORMANCE.md 的字体崩溃分析。
    """
    # 字体优先级：.ttf 单字体（稳定）优先，.ttc 集合字体（可能崩溃）作为兜底
    font_paths = [
        # ---- 首选：.ttf 单字体，压力测试验证稳定 ----
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",  # macOS，含中文，稳定
        # Windows .ttf 中文字体
        "C:/Windows/Fonts/simhei.ttf",  # 黑体
        "C:/Windows/Fonts/simsun.ttf",  # 宋体（部分系统为.ttf）
        # Linux .ttf/.otf 中文字体
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttf",  # 文泉驿微米黑
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.otf",

        # ---- 兜底：.ttc 集合字体（macOS 上可能不稳定，仅在无 .ttf 时使用）----
        "/System/Library/Fonts/Hiragino Sans GB.ttc",  # 冬青黑体
        "/System/Library/Fonts/STHeiti Light.ttc",  # 华文黑体
        "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",  # 文泉驿正黑
    ]

    # 尝试加载中文字体（按稳定性优先级）
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return pygame.font.Font(font_path, size)
            except Exception:
                continue

    # 回退到默认字体（不支持中文，但至少不会崩溃）
    print("警告: 未找到中文字体，使用默认字体（中文将显示为方块）")
    return pygame.font.Font(None, size)


class _CachedFont:
    """
    字体渲染缓存包装器

    关键作用：解决 SDL2_ttf 段错误崩溃(SIGSEGV)。

    问题：HUD 每帧对相同文字（角色名、血量百分比等）反复调用
    font.render()，每次都让 SDL2_ttf 分配新 Surface。在
    pygame 2.6.1 + SDL2_ttf 2.24 + Python 3.14 下，高频文字表面
    分配与特效系统的 Surface 分配交织，会触发 SDL2_ttf 堆内存
    损坏，最终在 SDL_AllocFormat 处段错误。

    修复：相同 (文字, 抗锯齿, 颜色) 只渲染一次并缓存 Surface，
    后续帧直接复用。既根治崩溃，也是标准性能优化（文字表面
    本就不应每帧重建）。详见 PERFORMANCE.md。
    """

    def __init__(self, font: pygame.font.Font):
        self._font = font
        self._cache = {}

    def render(self, text, antialias, color, background=None):
        key = (text, bool(antialias), tuple(color) if color else None,
               tuple(background) if background else None)
        cached = self._cache.get(key)
        if cached is None:
            if background is not None:
                cached = self._font.render(text, antialias, color, background)
            else:
                cached = self._font.render(text, antialias, color)
            self._cache[key] = cached
        return cached

    def __getattr__(self, name):
        # 其他方法/属性（如 get_height, size 等）委托给真实字体
        return getattr(self._font, name)


class UIManager:
    """
    UI管理器类
    职责：血条、计时器、连击数、游戏结束界面等所有UI渲染
    """

    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        # 字体（使用中文字体）
        # 用 _CachedFont 包装：缓存文字表面，避免每帧重复 render 触发
        # SDL2_ttf 段错误崩溃（详见 _CachedFont 文档字符串）
        self.font_large = _CachedFont(get_chinese_font(72))
        self.font_medium = _CachedFont(get_chinese_font(48))
        self.font_small = _CachedFont(get_chinese_font(36))
        self.font_tiny = _CachedFont(get_chinese_font(24))

        # UI常量
        self.margin = 40
        self.bar_width = 400
        self.bar_height = 30

    # ========================================================================
    # HUD（抬头显示）
    # ========================================================================

    def draw_hud(
        self,
        p1_name: str,
        p1_health_percent: float,
        p1_combo: int,
        p2_name: str,
        p2_health_percent: float,
        p2_combo: int,
        timer: int
    ):
        """
        绘制战斗HUD

        Args:
            p1_name: 玩家1角色名
            p1_health_percent: 玩家1血量百分比（0-1）
            p1_combo: 玩家1连击数
            p2_name: 玩家2角色名
            p2_health_percent: 玩家2血量百分比（0-1）
            p2_combo: 玩家2连击数
            timer: 倒计时秒数
        """
        # 玩家1血条（左上）
        self._draw_health_bar(
            self.margin,
            self.margin,
            self.bar_width,
            self.bar_height,
            p1_health_percent,
            flipped=False,
            player_name=p1_name
        )

        # 玩家2血条（右上，镜像）
        self._draw_health_bar(
            WINDOW_WIDTH - self.margin - self.bar_width,
            self.margin,
            self.bar_width,
            self.bar_height,
            p2_health_percent,
            flipped=True,
            player_name=p2_name
        )

        # 连击数显示
        if p1_combo > 1:
            self._draw_combo_counter(self.margin, self.margin + 50, p1_combo)
        if p2_combo > 1:
            self._draw_combo_counter(
                WINDOW_WIDTH - self.margin - 100,
                self.margin + 50,
                p2_combo
            )

        # 倒计时（中上）
        self._draw_timer(timer)

    def _draw_health_bar(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        health_percent: float,
        flipped: bool,
        player_name: str
    ):
        """
        绘制精美血条

        Args:
            x, y: 左上角位置
            width, height: 血条尺寸
            health_percent: 血量百分比（0-1）
            flipped: 是否镜像（P2从右向左减少）
            player_name: 角色名称
        """
        # 背景
        bg_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, Color.HP_BG, bg_rect, border_radius=5)

        # 血量
        filled_width = int(width * health_percent)
        if filled_width > 0:
            if flipped:
                hp_x = x + (width - filled_width)
            else:
                hp_x = x

            # 血量颜色渐变（低血变暗）
            hp_color = self._get_health_color(health_percent)
            hp_rect = pygame.Rect(hp_x, y, filled_width, height)
            pygame.draw.rect(self.screen, hp_color, hp_rect, border_radius=5)

        # 边框
        pygame.draw.rect(self.screen, Color.TEXT_PRIMARY, bg_rect, 3, border_radius=5)

        # 角色名称（血条上方）
        name_surface = self.font_tiny.render(player_name, True, Color.TEXT_PRIMARY)
        name_x = x if not flipped else x + width - name_surface.get_width()
        self.screen.blit(name_surface, (name_x, y - 25))

        # 血量数值（显示百分比）
        hp_text = f"{int(health_percent * 100)}%"
        hp_surface = self.font_tiny.render(hp_text, True, Color.TEXT_PRIMARY)
        hp_text_x = x + width // 2 - hp_surface.get_width() // 2
        self.screen.blit(hp_surface, (hp_text_x, y + 5))

    def _get_health_color(self, health_percent: float) -> tuple:
        """根据血量百分比返回颜色（渐变效果）"""
        if health_percent > 0.5:
            return Color.HP_FULL
        elif health_percent > 0.2:
            # 黄色警告区
            return (220, 180, 50)
        else:
            return Color.HP_LOW

    def _draw_combo_counter(self, x: int, y: int, combo: int):
        """
        绘制连击数

        Args:
            x, y: 位置
            combo: 连击数
        """
        # 连击文字（金色强调）
        combo_text = f"{combo} COMBO!"
        combo_surface = self.font_small.render(combo_text, True, Color.TEXT_GOLD)

        # 文字阴影效果
        shadow_surface = self.font_small.render(combo_text, True, Color.TEXT_SHADOW)
        self.screen.blit(shadow_surface, (x + 2, y + 2))
        self.screen.blit(combo_surface, (x, y))

    def _draw_timer(self, seconds: int):
        """
        绘制倒计时

        Args:
            seconds: 剩余秒数
        """
        timer_text = str(seconds)
        timer_surface = self.font_large.render(timer_text, True, Color.TEXT_PRIMARY)
        timer_rect = timer_surface.get_rect(center=(WINDOW_WIDTH // 2, 60))

        # 背景框
        bg_rect = timer_rect.inflate(40, 20)
        pygame.draw.rect(self.screen, Color.UI_BG, bg_rect, border_radius=10)

        # 时间紧迫警告（最后10秒红色）
        if seconds <= 10:
            pygame.draw.rect(self.screen, (200, 50, 50), bg_rect, 3, border_radius=10)

        self.screen.blit(timer_surface, timer_rect)

    # ========================================================================
    # 游戏结束界面
    # ========================================================================

    def draw_game_over(self, winner: Optional[int]):
        """
        绘制游戏结束界面

        Args:
            winner: 胜利者（1=P1, 2=P2, 0=平局, None=无）
        """
        # 半透明黑色遮罩
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # 胜利文字
        if winner == 0:
            result_text = "平局 DRAW"
            text_color = Color.TEXT_PRIMARY
        elif winner is not None:
            result_text = f"玩家 {winner} 胜利!"
            text_color = Color.TEXT_GOLD
        else:
            result_text = "游戏结束"
            text_color = Color.TEXT_PRIMARY

        # 主文字（带阴影）
        self._draw_text_with_shadow(
            result_text,
            self.font_large,
            text_color,
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)
        )

        # 提示文字
        hint_text = "按 R 重新开始 | ESC 退出"
        hint_surface = self.font_small.render(hint_text, True, Color.TEXT_PRIMARY)
        hint_rect = hint_surface.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)
        )
        self.screen.blit(hint_surface, hint_rect)

        # 调试提示（按F1/F2/F3/F4切换角色）
        debug_hint = "F1-F4:切换角色 | F5:AI模式 | F6:AI难度 | F7:AI性格"
        debug_surface = self.font_tiny.render(debug_hint, True, (150, 150, 150))
        debug_rect = debug_surface.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100)
        )
        self.screen.blit(debug_surface, debug_rect)

    def _draw_text_with_shadow(
        self,
        text: str,
        font: pygame.font.Font,
        color: tuple,
        center: tuple
    ):
        """
        绘制带阴影的文字

        Args:
            text: 文字内容
            font: 字体
            color: 文字颜色
            center: 中心位置
        """
        # 阴影
        shadow_surface = font.render(text, True, Color.TEXT_SHADOW)
        shadow_rect = shadow_surface.get_rect(center=(center[0] + 4, center[1] + 4))
        self.screen.blit(shadow_surface, shadow_rect)

        # 主文字
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=center)
        self.screen.blit(text_surface, text_rect)

    # ========================================================================
    # 调试信息
    # ========================================================================

    def draw_debug_info(self, fps: float, state: str):
        """
        绘制调试信息（FPS、游戏状态等）

        Args:
            fps: 当前帧率
            state: 游戏状态
        """
        debug_lines = [
            f"FPS: {int(fps)}",
            f"State: {state}",
        ]

        y_offset = WINDOW_HEIGHT - 80
        for line in debug_lines:
            debug_surface = self.font_tiny.render(line, True, (255, 255, 0))
            self.screen.blit(debug_surface, (10, y_offset))
            y_offset += 20
