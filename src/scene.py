"""
场景渲染系统
职责：绘制游戏场景背景、地面装饰、环境元素
"""
import pygame
from typing import Optional
from config import WINDOW_WIDTH, WINDOW_HEIGHT, GROUND_Y, Color


class SceneRenderer:
    """
    场景渲染器
    负责绘制水墨画风格的中式场景
    """

    def __init__(self, scene_type: str = "bamboo_forest"):
        """
        初始化场景渲染器

        Args:
            scene_type: 场景类型（"bamboo_forest", "dojo", "mountain"）
        """
        self.scene_type = scene_type
        self.parallax_offset = 0  # 视差滚动偏移量

    def draw_bamboo_forest(self, surface: pygame.Surface):
        """
        绘制竹林场景（水墨画风格）

        设计：
        - 远景：淡墨山峦
        - 中景：竹林剪影
        - 近景：竹子细节
        - 地面：青石板路
        """
        # 天空渐变（淡青色到米白）
        self._draw_sky_gradient(surface,
                               top_color=(220, 230, 235),
                               bottom_color=(240, 235, 220))

        # 远景：山峦剪影（淡墨）
        self._draw_distant_mountains(surface)

        # 中景：竹林（深墨）
        self._draw_bamboo_grove(surface)

        # 地面：青石板
        self._draw_stone_ground(surface)

        # 前景：飘落的竹叶
        self._draw_falling_leaves(surface)

    def draw_dojo(self, surface: pygame.Surface):
        """
        绘制武馆场景

        设计：
        - 背景：木质墙壁
        - 装饰：对联、匾额
        - 地面：木地板
        """
        # 墙壁（暖色调）
        wall_color = (180, 150, 120)
        pygame.draw.rect(surface, wall_color, (0, 0, WINDOW_WIDTH, GROUND_Y))

        # 木纹理（简化）
        for i in range(0, WINDOW_WIDTH, 200):
            pygame.draw.line(surface, (160, 130, 100),
                           (i, 0), (i, GROUND_Y), 2)

        # 地面：木地板
        floor_color = (140, 110, 80)
        pygame.draw.rect(surface, floor_color,
                        (0, GROUND_Y, WINDOW_WIDTH, WINDOW_HEIGHT - GROUND_Y))

        # 地板纹理
        for i in range(GROUND_Y, WINDOW_HEIGHT, 40):
            pygame.draw.line(surface, (120, 90, 60),
                           (0, i), (WINDOW_WIDTH, i), 2)

    def _draw_sky_gradient(self, surface: pygame.Surface,
                          top_color: tuple, bottom_color: tuple):
        """绘制天空渐变"""
        height = GROUND_Y
        for y in range(height):
            ratio = y / height
            r = int(top_color[0] + (bottom_color[0] - top_color[0]) * ratio)
            g = int(top_color[1] + (bottom_color[1] - top_color[1]) * ratio)
            b = int(top_color[2] + (bottom_color[2] - top_color[2]) * ratio)
            pygame.draw.line(surface, (r, g, b), (0, y), (WINDOW_WIDTH, y))

    def _draw_distant_mountains(self, surface: pygame.Surface):
        """绘制远景山峦（三角形剪影）"""
        mountain_color = (200, 210, 215)  # 淡墨色

        # 山峰1
        points1 = [
            (0, GROUND_Y - 200),
            (300, GROUND_Y - 350),
            (600, GROUND_Y - 200)
        ]
        pygame.draw.polygon(surface, mountain_color, points1)

        # 山峰2
        points2 = [
            (500, GROUND_Y - 180),
            (800, GROUND_Y - 320),
            (1100, GROUND_Y - 180)
        ]
        pygame.draw.polygon(surface, mountain_color, points2)

        # 山峰3
        points3 = [
            (900, GROUND_Y - 150),
            (1200, GROUND_Y - 280),
            (1500, GROUND_Y - 150)
        ]
        pygame.draw.polygon(surface, mountain_color, points3)

    def _draw_bamboo_grove(self, surface: pygame.Surface):
        """绘制竹林中景"""
        bamboo_color = (80, 100, 90)  # 深墨绿

        # 竹子位置（随机分布，但固定）
        bamboo_positions = [
            (150, GROUND_Y - 400, 8, 400),   # (x, y, width, height)
            (200, GROUND_Y - 420, 10, 420),
            (450, GROUND_Y - 380, 7, 380),
            (680, GROUND_Y - 410, 9, 410),
            (900, GROUND_Y - 390, 8, 390),
            (1050, GROUND_Y - 430, 10, 430),
        ]

        for x, y, width, height in bamboo_positions:
            # 竹竿
            pygame.draw.rect(surface, bamboo_color,
                           (x, y, width, height))

            # 竹节（每80像素一个）
            for node_y in range(y, y + height, 80):
                pygame.draw.line(surface, (60, 80, 70),
                               (x - 5, node_y), (x + width + 5, node_y), 3)

            # 竹叶（简化为几条线）
            leaf_color = (100, 120, 110)
            for i in range(3):
                leaf_y = y + i * 40
                # 左侧竹叶
                pygame.draw.line(surface, leaf_color,
                               (x, leaf_y), (x - 30, leaf_y - 20), 2)
                # 右侧竹叶
                pygame.draw.line(surface, leaf_color,
                               (x + width, leaf_y), (x + width + 30, leaf_y - 20), 2)

    def _draw_stone_ground(self, surface: pygame.Surface):
        """绘制青石板地面"""
        # 基础地面
        ground_color = (90, 85, 80)
        pygame.draw.rect(surface, ground_color,
                        (0, GROUND_Y, WINDOW_WIDTH, WINDOW_HEIGHT - GROUND_Y))

        # 石板纹理（矩形块）
        stone_border = (70, 65, 60)
        block_width = 120
        block_height = 40

        y_offset = GROUND_Y
        for row in range(3):
            x_offset = (row % 2) * 60  # 交错排列
            for col in range(WINDOW_WIDTH // block_width + 2):
                x = col * block_width + x_offset
                y = y_offset + row * block_height

                # 石块边框
                pygame.draw.rect(surface, stone_border,
                               (x, y, block_width - 4, block_height - 4), 2)

        # 地面装饰线（分隔线）
        pygame.draw.line(surface, (70, 65, 60),
                        (0, GROUND_Y), (WINDOW_WIDTH, GROUND_Y), 3)

    def _draw_falling_leaves(self, surface: pygame.Surface):
        """绘制飘落的竹叶（简化为小矩形）"""
        import random
        random.seed(42)  # 固定随机种子，保持一致

        leaf_color = (100, 120, 110)
        for i in range(8):
            x = random.randint(0, WINDOW_WIDTH)
            y = random.randint(0, GROUND_Y)
            # 简化为小矩形
            pygame.draw.rect(surface, leaf_color, (x, y, 6, 2))

    def render(self, surface: pygame.Surface):
        """
        渲染当前场景

        Args:
            surface: pygame.Surface 渲染目标
        """
        if self.scene_type == "bamboo_forest":
            self.draw_bamboo_forest(surface)
        elif self.scene_type == "dojo":
            self.draw_dojo(surface)
        else:
            # 默认：简单背景
            surface.fill(Color.BG)
            pygame.draw.rect(surface, Color.GROUND,
                           (0, GROUND_Y, WINDOW_WIDTH, WINDOW_HEIGHT - GROUND_Y))

    def update(self, dt: float):
        """
        更新场景动画（视差滚动等）

        Args:
            dt: delta time（秒）
        """
        # 预留：后续实现视差滚动
        pass
