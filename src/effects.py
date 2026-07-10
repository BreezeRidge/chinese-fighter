"""
攻击特效系统
职责：渲染攻击动画、粒子效果、视觉反馈
"""
import pygame
import random
from typing import List, Tuple
from config import Color


class Particle:
    """粒子类 - 用于攻击特效"""
    def __init__(self, x: float, y: float, vx: float, vy: float,
                 color: Tuple[int, int, int], lifetime: float, size: int = 3):
        self.x = x
        self.y = y
        self.vx = vx  # 水平速度
        self.vy = vy  # 垂直速度
        self.color = color
        self.lifetime = lifetime  # 生存时间（秒）
        self.max_lifetime = lifetime
        self.size = size
        self.alive = True

    def update(self, dt: float):
        """更新粒子状态"""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 500 * dt  # 重力
        self.lifetime -= dt

        if self.lifetime <= 0:
            self.alive = False

    def render(self, surface: pygame.Surface):
        """渲染粒子"""
        if not self.alive:
            return

        # 根据生命值淡出
        alpha_ratio = self.lifetime / self.max_lifetime
        alpha = int(255 * alpha_ratio)

        # 粒子大小随生命值缩小
        size = int(self.size * alpha_ratio)
        if size < 1:
            size = 1

        # 创建带透明度的粒子
        particle_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        color_with_alpha = (*self.color, alpha)
        pygame.draw.circle(particle_surf, color_with_alpha, (size, size), size)

        surface.blit(particle_surf, (int(self.x - size), int(self.y - size)))


class AttackEffect:
    """攻击特效管理器"""

    def __init__(self):
        self.particles: List[Particle] = []

    def create_hit_effect(self, x: float, y: float, direction: int, effect_type: str = "normal"):
        """
        创建击中特效

        Args:
            x, y: 击中位置
            direction: 攻击方向（1=右，-1=左）
            effect_type: 特效类型（"normal", "heavy", "special"）
        """
        if effect_type == "normal":
            self._create_normal_hit(x, y, direction)
        elif effect_type == "heavy":
            self._create_heavy_hit(x, y, direction)
        elif effect_type == "special":
            self._create_special_hit(x, y, direction)

    def _create_normal_hit(self, x: float, y: float, direction: int):
        """普通攻击特效（少量粒子）"""
        color = (255, 200, 100)  # 橙黄色
        for i in range(8):
            angle = random.uniform(-45, 45) + (0 if direction > 0 else 180)
            speed = random.uniform(100, 200)
            vx = speed * pygame.math.Vector2(1, 0).rotate(angle).x
            vy = speed * pygame.math.Vector2(1, 0).rotate(angle).y - random.uniform(50, 100)

            particle = Particle(x, y, vx, vy, color, lifetime=0.3, size=3)
            self.particles.append(particle)

    def _create_heavy_hit(self, x: float, y: float, direction: int):
        """重攻击特效（爆炸式粒子）"""
        color = (255, 100, 50)  # 红橙色
        for i in range(20):
            angle = random.uniform(-60, 60) + (0 if direction > 0 else 180)
            speed = random.uniform(200, 400)
            vx = speed * pygame.math.Vector2(1, 0).rotate(angle).x
            vy = speed * pygame.math.Vector2(1, 0).rotate(angle).y - random.uniform(100, 200)

            particle = Particle(x, y, vx, vy, color, lifetime=0.5, size=5)
            self.particles.append(particle)

    def _create_special_hit(self, x: float, y: float, direction: int):
        """特殊招式特效（华丽粒子）"""
        # 金色粒子
        color = (255, 215, 0)
        for i in range(30):
            angle = random.uniform(0, 360)
            speed = random.uniform(150, 350)
            vx = speed * pygame.math.Vector2(1, 0).rotate(angle).x
            vy = speed * pygame.math.Vector2(1, 0).rotate(angle).y

            particle = Particle(x, y, vx, vy, color, lifetime=0.8, size=6)
            self.particles.append(particle)

    def create_block_effect(self, x: float, y: float):
        """创建格挡特效（火花）"""
        color = (255, 255, 200)  # 亮黄色
        for i in range(12):
            angle = random.uniform(-90, 90)
            speed = random.uniform(100, 250)
            vx = speed * pygame.math.Vector2(1, 0).rotate(angle).x
            vy = speed * pygame.math.Vector2(1, 0).rotate(angle).y

            particle = Particle(x, y, vx, vy, color, lifetime=0.4, size=4)
            self.particles.append(particle)

    def create_buff_effect(self, x: float, y: float, buff_type: str):
        """
        创建增益特效

        Args:
            x, y: 角色中心位置
            buff_type: 增益类型（"defense", "speed", "invincible"）
        """
        if buff_type == "defense":
            color = (100, 150, 255)  # 蓝色（防御）
        elif buff_type == "speed":
            color = (100, 255, 100)  # 绿色（速度）
        elif buff_type == "invincible":
            color = (255, 255, 100)  # 金色（无敌）
        else:
            color = (200, 200, 200)

        # 环绕粒子
        for i in range(15):
            angle = (360 / 15) * i
            radius = 60
            px = x + radius * pygame.math.Vector2(1, 0).rotate(angle).x
            py = y + radius * pygame.math.Vector2(1, 0).rotate(angle).y

            # 向中心运动
            vx = -pygame.math.Vector2(1, 0).rotate(angle).x * 50
            vy = -pygame.math.Vector2(1, 0).rotate(angle).y * 50

            particle = Particle(px, py, vx, vy, color, lifetime=0.6, size=5)
            self.particles.append(particle)

    def update(self, dt: float):
        """更新所有粒子"""
        for particle in self.particles:
            particle.update(dt)

        # 移除死亡粒子
        self.particles = [p for p in self.particles if p.alive]

    def render(self, surface: pygame.Surface):
        """渲染所有粒子"""
        for particle in self.particles:
            particle.render(surface)

    def clear(self):
        """清除所有粒子"""
        self.particles.clear()


class ScreenShake:
    """屏幕震动效果"""

    def __init__(self):
        self.shake_duration = 0.0
        self.shake_intensity = 0.0
        self.offset_x = 0
        self.offset_y = 0

    def trigger(self, intensity: float, duration: float):
        """
        触发屏幕震动

        Args:
            intensity: 震动强度（像素）
            duration: 持续时间（秒）
        """
        self.shake_intensity = intensity
        self.shake_duration = duration

    def update(self, dt: float):
        """更新震动效果"""
        if self.shake_duration > 0:
            self.shake_duration -= dt

            # 随机偏移
            self.offset_x = random.randint(-int(self.shake_intensity), int(self.shake_intensity))
            self.offset_y = random.randint(-int(self.shake_intensity), int(self.shake_intensity))
        else:
            self.offset_x = 0
            self.offset_y = 0

    def get_offset(self) -> Tuple[int, int]:
        """获取当前偏移量"""
        return (self.offset_x, self.offset_y)

    def is_shaking(self) -> bool:
        """是否正在震动"""
        return self.shake_duration > 0
