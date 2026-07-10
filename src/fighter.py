"""
角色类 - 处理战斗角色的状态、移动、攻击、碰撞
重构：使用CharacterStats数据类，提升可扩展性
v0.3.0: 添加特殊招式系统支持
v0.6.0: 添加精灵图动画系统
"""
import pygame
from enum import Enum, auto
from typing import Optional, Set
from config import CharacterStats, CHARACTERS, GRAVITY, GROUND_Y, Color, FRICTION
from special_moves import SpecialMove, SpecialMoveSystem, get_special_moves
from sprite_system import AnimatedSprite, load_character_animations


class FighterState(Enum):
    """角色状态枚举"""
    IDLE = auto()
    WALK = auto()
    JUMP = auto()
    ATTACK_LIGHT = auto()
    ATTACK_HEAVY = auto()
    SPECIAL = auto()  # 新增：特殊招式状态
    HIT = auto()
    BLOCK = auto()
    BUFF = auto()  # 新增：增益状态（金刚身、疾风步等）


class AttackBox:
    """攻击判定框类 - 封装攻击属性"""
    def __init__(self, rect: pygame.Rect, damage: int, knockback: float):
        self.rect = rect
        self.damage = damage
        self.knockback = knockback
        self.hit_targets: Set[int] = set()  # 记录已击中的目标ID，防止重复受击

    def has_hit(self, target_id: int) -> bool:
        """检查是否已击中该目标"""
        return target_id in self.hit_targets

    def mark_hit(self, target_id: int):
        """标记已击中该目标"""
        self.hit_targets.add(target_id)


class Fighter(pygame.sprite.Sprite):
    """
    格斗角色基类
    设计原则：
    1. 数据驱动 - 角色属性通过CharacterStats配置
    2. 状态机 - 明确的状态转换逻辑
    3. 浮点精度 - 位置用float，渲染用int
    4. 单一职责 - 每个方法只做一件事
    """

    _id_counter = 0  # 类变量：为每个实例分配唯一ID

    def __init__(self, x: float, y: float, character_key: str, player_num: int):
        """
        初始化角色

        Args:
            x, y: 初始位置
            character_key: 角色键名（如 "shaolin", "emei"）
            player_num: 玩家编号（1或2）
        """
        super().__init__()

        # 分配唯一ID
        self.id = Fighter._id_counter
        Fighter._id_counter += 1

        # 加载角色配置
        self.stats = CHARACTERS.get(character_key, CHARACTERS["default"])
        self.player_num = player_num

        # 位置与速度（浮点数精度）
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.vel_x = 0.0
        self.vel_y = 0.0

        # 角色属性
        self.health = self.stats.max_health
        self.facing_right = (player_num == 1)  # P1面向右，P2面向左

        # 状态管理
        self.state = FighterState.IDLE
        self.state_timer = 0.0
        self.attack_cooldown = 0.0

        # 连击系统
        self.combo_count = 0
        self.combo_timer = 0.0

        # 特殊招式系统
        self.character_key = character_key
        self.special_moves = get_special_moves(character_key)
        self.special_move_system = SpecialMoveSystem()
        self.active_special: Optional[SpecialMove] = None  # 当前激活的特殊招式

        # 增益状态（buff）
        self.active_buffs = {}  # {buff_name: remaining_time}

        # 精灵图动画系统
        self.sprite = load_character_animations(character_key)
        self.sprite.facing_right = self.facing_right

        # 渲染（使用精灵图）
        self.image = self.sprite.get_current_frame()
        self.rect = self.image.get_rect(bottomleft=(int(self.pos_x), int(self.pos_y)))

        # 攻击判定
        self.attack_box: Optional[AttackBox] = None

    def _create_character_surface(self) -> pygame.Surface:
        """创建角色渲染表面（临时色块，后期替换为精灵图）"""
        surface = pygame.Surface((self.stats.width, self.stats.height))

        # 根据玩家编号选择颜色
        color = Color.PLAYER1 if self.player_num == 1 else Color.PLAYER2
        surface.fill(color)

        # 绘制角色名称（临时标识）
        font = pygame.font.Font(None, 20)
        name_text = font.render(self.stats.name, True, Color.TEXT_PRIMARY)
        name_rect = name_text.get_rect(center=(self.stats.width // 2, 10))
        surface.blit(name_text, name_rect)

        return surface

    # ========================================================================
    # 主更新逻辑
    # ========================================================================

    def update(self, dt: float, keys: pygame.key.ScancodeWrapper):
        """
        每帧更新

        Args:
            dt: delta time（秒）
            keys: 按键状态
        """
        # 更新计时器
        self.state_timer += dt
        self.attack_cooldown = max(0, self.attack_cooldown - dt)
        self.combo_timer = max(0, self.combo_timer - dt)

        # 更新特殊招式冷却
        self.special_move_system.update(dt)

        # 更新增益效果 - 添加异常捕获
        try:
            self._update_buffs(dt)
        except Exception as e:
            print(f"[ERROR] _update_buffs: {e}")
            self.active_buffs.clear()  # 清空错误的buff

        # 连击超时重置
        if self.combo_timer == 0:
            self.combo_count = 0

        # 状态机分发 - 简化逻辑，优先处理输入
        if self.state == FighterState.HIT:
            self._update_hit_state(dt)
        elif self.state == FighterState.BLOCK:
            self._update_block_state(dt, keys)
        elif self.state == FighterState.SPECIAL:
            self._update_special_state(dt)
        elif self.state in [FighterState.ATTACK_LIGHT, FighterState.ATTACK_HEAVY]:
            self._update_attack_state(dt)
        else:
            # 默认状态：处理输入
            try:
                self._handle_input(dt, keys)
            except Exception as e:
                print(f"[ERROR] _handle_input: {e}")
                import traceback
                traceback.print_exc()

        # 物理更新
        self._apply_physics(dt)
        self._apply_friction()

        # 更新精灵动画
        self.sprite.update(dt)
        self.sprite.facing_right = self.facing_right
        self._update_sprite_animation()

        # 更新渲染图像
        self.image = self.sprite.get_current_frame()

        # 同步渲染位置
        self.rect.bottomleft = (int(self.pos_x), int(self.pos_y))

    def _apply_physics(self, dt: float):
        """应用物理模拟（重力、速度、边界）"""
        # 应用重力
        if self.pos_y < GROUND_Y:
            self.vel_y += GRAVITY * dt

        # 先应用速度（关键：在边界检查之前）
        self.pos_x += self.vel_x * dt
        self.pos_y += self.vel_y * dt

        # 地面碰撞检测（在应用速度之后）
        if self.pos_y >= GROUND_Y:
            self.pos_y = GROUND_Y
            self.vel_y = 0
            if self.state == FighterState.JUMP:
                self.state = FighterState.IDLE

        # 边界限制
        half_width = self.stats.width // 2
        self.pos_x = max(half_width, min(1280 - half_width, self.pos_x))

    def _apply_friction(self):
        """应用地面摩擦力"""
        if self.pos_y >= GROUND_Y and self.state not in [FighterState.ATTACK_LIGHT, FighterState.ATTACK_HEAVY]:
            self.vel_x *= FRICTION

    # ========================================================================
    # 输入处理
    # ========================================================================

    def _handle_input(self, dt: float, keys: pygame.key.ScancodeWrapper):
        """处理玩家输入"""
        from config import Controls

        # 选择按键映射
        if self.player_num == 1:
            left, right, jump = pygame.K_a, pygame.K_d, pygame.K_w
            light, heavy, block = pygame.K_f, pygame.K_g, pygame.K_h
        else:
            left, right, jump = pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP
            light, heavy, block = pygame.K_j, pygame.K_k, pygame.K_l

        # 格挡（最高优先级，直接返回）
        if keys[block]:
            self.state = FighterState.BLOCK
            self.vel_x = 0
            return

        # 跳跃（优先级高于移动）
        if keys[jump] and self.pos_y >= GROUND_Y:
            self.vel_y = self.stats.jump_velocity
            self.state = FighterState.JUMP

        # 水平移动（只在地面上时才能改变 IDLE/WALK 状态）
        move_input = 0
        if keys[left]:
            move_input = -1
            self.facing_right = False
        elif keys[right]:
            move_input = 1
            self.facing_right = True

        self.vel_x = move_input * self.stats.move_speed

        # 应用增益效果的速度修正
        if "speed_boost" in self.active_buffs:
            self.vel_x *= (1 + self.active_buffs["speed_boost"])
        if "speed_penalty" in self.active_buffs:
            self.vel_x *= (1 + self.active_buffs["speed_penalty"])

        # 只有在地面上且不在跳跃状态时才更新 IDLE/WALK 状态
        if self.pos_y >= GROUND_Y and self.state != FighterState.JUMP:
            if move_input != 0:
                self.state = FighterState.WALK
            else:
                self.state = FighterState.IDLE

        # 攻击
        if self.attack_cooldown <= 0:
            if keys[light]:
                self._start_attack(light=True)
            elif keys[heavy]:
                self._start_attack(light=False)

        # 特殊招式（Q/E键）
        for special_move in self.special_moves:
            if keys[special_move.key] and self.special_move_system.can_use(special_move):
                self._use_special_move(special_move)

    # ========================================================================
    # 攻击系统
    # ========================================================================

    def _start_attack(self, light: bool):
        """
        开始攻击

        Args:
            light: True=轻攻击, False=重攻击
        """
        if light:
            self.state = FighterState.ATTACK_LIGHT
            self.state_timer = 0
            self.attack_cooldown = self.stats.light_duration + 0.1
            self._create_attack_box(
                self.stats.light_range,
                self.stats.light_damage,
                0  # 轻攻击无击退
            )
        else:
            self.state = FighterState.ATTACK_HEAVY
            self.state_timer = 0
            self.attack_cooldown = self.stats.heavy_duration + 0.1
            self._create_attack_box(
                self.stats.heavy_range,
                self.stats.heavy_damage,
                self.stats.heavy_knockback
            )

    def _create_attack_box(self, range_px: int, damage: int, knockback: float):
        """创建攻击判定框"""
        if self.facing_right:
            attack_x = self.pos_x + self.stats.width // 2
        else:
            attack_x = self.pos_x - range_px

        rect = pygame.Rect(
            attack_x,
            self.pos_y - self.stats.height,
            range_px,
            self.stats.height
        )

        self.attack_box = AttackBox(rect, damage, knockback)

    def _update_attack_state(self, dt: float):
        """更新攻击状态"""
        duration = (self.stats.light_duration if self.state == FighterState.ATTACK_LIGHT
                   else self.stats.heavy_duration)

        if self.state_timer >= duration:
            self.state = FighterState.IDLE
            self.state_timer = 0
            self.attack_box = None
        else:
            # 持续更新攻击框位置（角色可能在移动）
            if self.attack_box:
                if self.facing_right:
                    self.attack_box.rect.x = self.pos_x + self.stats.width // 2
                else:
                    range_px = self.attack_box.rect.width
                    self.attack_box.rect.x = self.pos_x - range_px

    # ========================================================================
    # 受击与防御系统
    # ========================================================================

    def take_damage(self, damage: int, knockback_direction: float):
        """
        受到伤害

        Args:
            damage: 伤害值
            knockback_direction: 击退方向（1=右，-1=左）
        """
        # 无敌状态免疫伤害
        if self.is_invincible():
            return

        # 增益效果减伤
        damage_reduction = self.get_damage_reduction()
        if damage_reduction > 0:
            damage = int(damage * (1 - damage_reduction))

        # 格挡减伤
        if self.state == FighterState.BLOCK:
            damage = int(damage * (1 - self.stats.block_reduction))
            knockback_direction *= 0.5  # 格挡减少击退

            # 太极气盾反伤
            if "reflect_damage" in self.active_buffs:
                # 这里需要通过游戏主循环处理反伤，暂时标记
                self.active_buffs["pending_reflect"] = damage * self.active_buffs["reflect_damage"]

        self.health = max(0, self.health - damage)
        self.state = FighterState.HIT
        self.state_timer = 0

        # 击退效果
        if knockback_direction != 0:
            self.vel_x = knockback_direction

        # 重置连击
        self.combo_count = 0

    def _update_hit_state(self, dt: float):
        """更新受击状态"""
        if self.state_timer >= self.stats.hit_stun_duration:
            self.state = FighterState.IDLE
            self.state_timer = 0

    def _update_block_state(self, dt: float, keys: pygame.key.ScancodeWrapper):
        """更新格挡状态"""
        block_key = pygame.K_h if self.player_num == 1 else pygame.K_l

        if not keys[block_key]:
            self.state = FighterState.IDLE

    # ========================================================================
    # 特殊招式系统
    # ========================================================================

    def _use_special_move(self, special_move: SpecialMove):
        """
        使用特殊招式

        Args:
            special_move: 特殊招式对象
        """
        # 启动冷却
        self.special_move_system.use(special_move)
        self.active_special = special_move
        self.state_timer = 0

        # 根据招式类型执行不同效果
        if special_move.damage > 0:
            # 攻击型招式
            self.state = FighterState.SPECIAL
            self._create_attack_box(
                special_move.range,
                special_move.damage,
                special_move.knockback
            )
        else:
            # 增益型招式
            self.state = FighterState.BUFF
            self._apply_special_buff(special_move)

    def _update_special_state(self, dt: float):
        """更新特殊招式状态"""
        if not self.active_special:
            self.state = FighterState.IDLE
            return

        if self.state_timer >= self.active_special.duration:
            self.state = FighterState.IDLE
            self.state_timer = 0
            self.attack_box = None
            self.active_special = None
        else:
            # 持续更新攻击框位置
            if self.attack_box:
                if self.facing_right:
                    self.attack_box.rect.x = self.pos_x + self.stats.width // 2
                else:
                    range_px = self.attack_box.rect.width
                    self.attack_box.rect.x = self.pos_x - range_px

    def _apply_special_buff(self, special_move: SpecialMove):
        """
        应用特殊招式增益效果

        Args:
            special_move: 特殊招式对象
        """
        from buff_effects import (
            apply_shaolin_body_buff,
            apply_emei_speed_buff,
            apply_wudang_shield_buff
        )

        # 根据角色和招式名称应用对应增益
        if self.character_key == "shaolin" and special_move.name == "金刚身":
            apply_shaolin_body_buff(self)
        elif self.character_key == "emei" and special_move.name == "疾风步":
            apply_emei_speed_buff(self)
        elif self.character_key == "wudang" and special_move.name == "太极气盾":
            apply_wudang_shield_buff(self)
        elif special_move.name == "闪避":
            # 默认角色的闪避
            self.active_buffs["invincible"] = special_move.duration

    def _update_buffs(self, dt: float):
        """更新所有增益效果"""
        if not self.active_buffs:
            return

        # 更新所有增益的剩余时间
        expired_buffs = []
        for buff_name in list(self.active_buffs.keys()):
            buff_value = self.active_buffs[buff_name]

            # 只处理数值型的buff（时间）
            if isinstance(buff_value, (int, float)) and buff_value > 0:
                self.active_buffs[buff_name] = buff_value - dt
                if self.active_buffs[buff_name] <= 0:
                    expired_buffs.append(buff_name)

        # 移除过期增益
        for buff_name in expired_buffs:
            del self.active_buffs[buff_name]

    def get_effective_move_speed(self) -> float:
        """获取考虑增益后的实际移动速度"""
        speed = self.stats.move_speed

        # 金刚身减速
        if "speed_penalty" in self.active_buffs:
            speed *= (1 + self.active_buffs["speed_penalty"])

        # 疾风步加速
        if "speed_boost" in self.active_buffs:
            speed *= (1 + self.active_buffs["speed_boost"])

        return speed

    def get_damage_reduction(self) -> float:
        """获取当前伤害减免比例（0-1）"""
        reduction = 0.0

        # 金刚身减伤
        if "damage_reduction" in self.active_buffs:
            reduction = max(reduction, self.active_buffs["damage_reduction"])

        return reduction

    def is_invincible(self) -> bool:
        """检查是否处于无敌状态"""
        return "invincible" in self.active_buffs

    def _update_sprite_animation(self):
        """根据当前状态更新精灵动画"""
        # 状态到动画的映射
        state_to_anim = {
            FighterState.IDLE: "idle",
            FighterState.WALK: "walk",
            FighterState.JUMP: "jump",
            FighterState.ATTACK_LIGHT: "attack_light",
            FighterState.ATTACK_HEAVY: "attack_heavy",
            FighterState.HIT: "hit",
            FighterState.BLOCK: "idle",  # 暂时使用idle
            FighterState.SPECIAL: "attack_heavy",  # 暂时使用重攻击
            FighterState.BUFF: "idle",
        }

        animation_name = state_to_anim.get(self.state, "idle")
        self.sprite.play(animation_name, reset=False)

    # ========================================================================
    # 碰撞检测辅助
    # ========================================================================

    def can_hit(self, other: 'Fighter') -> bool:
        """检查是否可以击中目标"""
        if not self.attack_box:
            return False
        if not self.attack_box.rect.colliderect(other.rect):
            return False
        if self.attack_box.has_hit(other.id):
            return False
        if other.state == FighterState.HIT:  # 额外保护
            return False
        return True

    def hit(self, other: 'Fighter'):
        """执行击中逻辑"""
        if not self.attack_box:
            return

        direction = 1 if self.facing_right else -1
        other.take_damage(self.attack_box.damage, direction * self.attack_box.knockback)
        self.attack_box.mark_hit(other.id)

        # 连击计数
        self.combo_count += 1
        self.combo_timer = 0.8  # 连击超时

    # ========================================================================
    # 调试与渲染
    # ========================================================================

    def draw_debug(self, surface: pygame.Surface):
        """绘制调试信息（碰撞盒）"""
        # 角色盒
        pygame.draw.rect(surface, Color.DEBUG_HITBOX, self.rect, 2)

        # 攻击盒
        if self.attack_box:
            pygame.draw.rect(surface, Color.DEBUG_ATTACKBOX, self.attack_box.rect, 2)

        # 状态文字
        font = pygame.font.Font(None, 16)
        state_text = font.render(f"{self.state.name} Combo:{self.combo_count}",
                                True, Color.TEXT_PRIMARY)
        surface.blit(state_text, (self.rect.x, self.rect.y - 20))

    def get_health_percentage(self) -> float:
        """获取血量百分比（0-1）"""
        return self.health / self.stats.max_health
