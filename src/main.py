"""
武林争霸 - 主程序
重构：模块化设计，UI组件分离，提升可读性
v0.3.0: 特殊招式系统
v0.4.0: 场景美术升级 + 粒子特效
v0.5.0: 音效系统
"""
import pygame
import sys
from fighter import Fighter, FighterState
from config import *
from ui import UIManager
from scene import SceneRenderer
from effects import AttackEffect, ScreenShake
from sound import get_sound_manager  # 新增：音效系统


class GameState:
    """游戏状态枚举"""
    MENU = "menu"
    CHARACTER_SELECT = "character_select"
    FIGHTING = "fighting"
    ROUND_END = "round_end"


class Game:
    """
    游戏主类
    职责：游戏循环、状态管理、碰撞检测
    """

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # UI管理器
        self.ui = UIManager(self.screen)

        # 场景渲染器
        self.scene = SceneRenderer("bamboo_forest")  # 默认竹林场景

        # 特效系统
        self.effects = AttackEffect()
        self.screen_shake = ScreenShake()

        # 音效系统
        self.sound = get_sound_manager()

        # 游戏状态
        self.state = GameState.FIGHTING  # 暂时直接进入战斗，后续添加菜单
        self.round_time = ROUND_TIME
        self.game_over = False
        self.winner = None

        # 创建角色（后续改为角色选择界面）
        self._init_fighters("default", "default")

    def _init_fighters(self, p1_char: str, p2_char: str):
        """初始化双方角色"""
        self.player1 = Fighter(200, GROUND_Y, p1_char, player_num=1)
        self.player2 = Fighter(WINDOW_WIDTH - 200, GROUND_Y, p2_char, player_num=2)

    # ========================================================================
    # 主游戏循环
    # ========================================================================

    def run(self):
        """游戏主循环"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            self.handle_events()

            if self.state == GameState.FIGHTING and not self.game_over:
                self.update(dt)
                self.check_collisions()
                self.check_win_condition()

            self.render()

        pygame.quit()
        sys.exit()

    def handle_events(self):
        """事件处理"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)

    def _handle_keydown(self, key: int):
        """按键按下处理"""
        if key == pygame.K_ESCAPE:
            self.running = False
        elif key == pygame.K_r and self.game_over:
            self.reset_game()
        elif key == pygame.K_F1:
            # 调试：切换角色组合
            self._init_fighters("shaolin", "emei")
        elif key == pygame.K_F2:
            self._init_fighters("emei", "shaolin")
        elif key == pygame.K_F3:
            # 新增：武当 vs 少林
            self._init_fighters("wudang", "shaolin")
        elif key == pygame.K_F4:
            # 新增：武当 vs 峨眉
            self._init_fighters("wudang", "emei")

    # ========================================================================
    # 游戏逻辑
    # ========================================================================

    def update(self, dt: float):
        """更新游戏逻辑"""
        keys = pygame.key.get_pressed()

        # 更新角色
        self.player1.update(dt, keys)
        self.player2.update(dt, keys)

        # 更新特效
        self.effects.update(dt)
        self.screen_shake.update(dt)

        # 更新计时器
        self.round_time -= dt
        if self.round_time <= 0:
            self.round_time = 0
            self._time_out_end()

    def check_collisions(self):
        """检测攻击碰撞"""
        # P1 攻击 P2
        if self.player1.can_hit(self.player2):
            self.player1.hit(self.player2)
            self._trigger_hit_effects(self.player1, self.player2)

        # P2 攻击 P1
        if self.player2.can_hit(self.player1):
            self.player2.hit(self.player1)
            self._trigger_hit_effects(self.player2, self.player1)

    def _trigger_hit_effects(self, attacker: Fighter, defender: Fighter):
        """触发击中特效"""
        # 计算击中位置
        hit_x = defender.rect.centerx
        hit_y = defender.rect.centery

        # 根据攻击类型选择特效和音效
        if attacker.state == FighterState.SPECIAL:
            self.effects.create_hit_effect(hit_x, hit_y,
                                          1 if attacker.facing_right else -1,
                                          "special")
            self.screen_shake.trigger(intensity=8, duration=0.2)
            self.sound.play_hit_sound("special")  # ⭐ 音效
        elif attacker.state == FighterState.ATTACK_HEAVY:
            self.effects.create_hit_effect(hit_x, hit_y,
                                          1 if attacker.facing_right else -1,
                                          "heavy")
            self.screen_shake.trigger(intensity=5, duration=0.15)
            self.sound.play_hit_sound("heavy")  # ⭐ 音效
        else:
            self.effects.create_hit_effect(hit_x, hit_y,
                                          1 if attacker.facing_right else -1,
                                          "normal")
            self.sound.play_hit_sound("light")  # ⭐ 音效

        # 格挡特效和音效
        if defender.state == FighterState.BLOCK:
            self.effects.create_block_effect(hit_x, hit_y)
            self.sound.play_block_sound()  # ⭐ 音效

    def check_win_condition(self):
        """检查胜负条件"""
        if self.player1.health <= 0:
            self._end_game(winner=2)
        elif self.player2.health <= 0:
            self._end_game(winner=1)

    def _time_out_end(self):
        """时间到判定"""
        self.game_over = True
        if self.player1.health > self.player2.health:
            self.winner = 1
        elif self.player2.health > self.player1.health:
            self.winner = 2
        else:
            self.winner = 0  # 平局

    def _end_game(self, winner: int):
        """游戏结束"""
        self.game_over = True
        self.winner = winner
        self.sound.play_ko_sound()  # ⭐ KO音效

    def reset_game(self):
        """重置游戏"""
        # 重新创建角色（保留当前选择）
        p1_char = "shaolin" if "少林" in self.player1.stats.name else "default"
        p2_char = "emei" if "峨眉" in self.player2.stats.name else "default"
        self._init_fighters(p1_char, p2_char)

        self.round_time = ROUND_TIME
        self.game_over = False
        self.winner = None

    # ========================================================================
    # 渲染
    # ========================================================================

    def render(self):
        """渲染画面"""
        # 场景背景（替换纯色背景）
        self.scene.render(self.screen)

        # 粒子特效（在角色后面）
        self.effects.render(self.screen)

        # 角色
        shake_offset = self.screen_shake.get_offset()
        self.screen.blit(self.player1.image,
                        (self.player1.rect.x + shake_offset[0],
                         self.player1.rect.y + shake_offset[1]))
        self.screen.blit(self.player2.image,
                        (self.player2.rect.x + shake_offset[0],
                         self.player2.rect.y + shake_offset[1]))

        # 调试模式（按F3切换）
        if hasattr(self, 'debug_mode') and self.debug_mode:
            self.player1.draw_debug(self.screen)
            self.player2.draw_debug(self.screen)

        # UI
        self.ui.draw_hud(
            self.player1.stats.name,
            self.player1.get_health_percentage(),
            self.player1.combo_count,
            self.player2.stats.name,
            self.player2.get_health_percentage(),
            self.player2.combo_count,
            int(self.round_time)
        )

        # 游戏结束界面
        if self.game_over:
            self.ui.draw_game_over(self.winner)

        pygame.display.flip()

    def _draw_ground(self):
        """绘制地面"""
        pygame.draw.rect(
            self.screen,
            Color.GROUND,
            (0, GROUND_Y, WINDOW_WIDTH, WINDOW_HEIGHT - GROUND_Y)
        )

        # 地面装饰线
        pygame.draw.line(
            self.screen,
            (70, 60, 50),
            (0, GROUND_Y),
            (WINDOW_WIDTH, GROUND_Y),
            3
        )


if __name__ == "__main__":
    game = Game()
    game.run()
