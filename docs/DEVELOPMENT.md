# 开发指南 - 武林争霸

## 开发环境配置

### 1. 克隆项目（或下载源码）
```bash
cd /path/to/project
```

### 2. 创建虚拟环境
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 运行游戏
```bash
# 方式1: 使用启动脚本（推荐）
./run.sh

# 方式2: 手动运行
cd src
python main.py
```

---

## 项目架构

### 核心模块

#### `config.py` - 配置管理
- 所有游戏常量（窗口大小、角色属性、攻击参数）
- 按键映射
- 颜色定义

**设计原则**: 所有硬编码值都应提取到 config.py，方便平衡性调试。

#### `fighter.py` - 角色逻辑
- `FighterState` 枚举：角色状态机（IDLE/WALK/JUMP/ATTACK/HIT）
- `Fighter` 类：处理移动、攻击、碰撞、受击
- 关键方法：
  - `update(dt, keys)`: 每帧更新逻辑
  - `take_damage(damage, knockback)`: 受击处理
  - `_create_attack_box()`: 生成攻击判定框

**状态转换图**:
```
IDLE ──→ WALK ──→ IDLE
  │         │
  ↓         ↓
JUMP ─────→ IDLE
  │
  ↓
ATTACK_LIGHT/HEAVY ──→ IDLE
  │
  ↓ (被打)
 HIT ──→ IDLE
```

#### `main.py` - 游戏循环
- `Game` 类：管理整个游戏流程
- 主循环：事件 → 更新 → 碰撞检测 → 渲染
- UI 渲染：血条、计时器、游戏结束界面

---

## 核心系统详解

### 1. 碰撞检测系统

**两种碰撞盒**:
- `Fighter.rect`: 角色本体盒（用于受击判定和渲染）
- `Fighter.attack_box`: 攻击判定盒（只在攻击时激活）

**检测流程** (`Game.check_collisions()`):
```python
if P1.attack_box and P1.attack_box.colliderect(P2.rect):
    if P2.state != FighterState.HIT:  # 避免重复受击
        P2.take_damage(damage, knockback)
```

**为什么分离两种盒子？**
- `rect` 持久存在，代表角色占位
- `attack_box` 瞬时激活，避免"站在一起就扣血"

### 2. 状态机系统

**为什么需要状态机？**
- 防止同时执行冲突动作（如"跳跃中再次跳跃"）
- 控制行为优先级（被打时不能移动）
- 简化动画管理（每个状态对应一组动画帧）

**当前状态限制**:
```python
if self.state == FighterState.HIT:
    # 受击期间：只能播放受击动画，不接受输入
    self._update_hit_state(dt)
elif self.state in [FighterState.ATTACK_LIGHT, FighterState.ATTACK_HEAVY]:
    # 攻击期间：播放攻击动画，攻击结束后恢复 IDLE
    self._update_attack_state(dt)
else:
    # 正常状态：可以移动和攻击
    self._handle_input(dt, keys)
```

### 3. 物理系统

**重力模拟**:
```python
if self.pos_y < GROUND_Y:
    self.vel_y += GRAVITY * dt  # 加速度积分
self.pos_y += self.vel_y * dt   # 速度积分
```

**为什么使用浮点位置？**
- `self.pos_x/pos_y`: 浮点数，精确物理计算
- `self.rect`: 整数，用于渲染（像素对齐）
- 分离避免"低速移动时卡住"问题

### 4. 攻击判定时机

**当前实现**: 攻击期间每帧生成攻击盒
```python
def _update_attack_state(self, dt):
    if self.state_timer < duration:
        self._create_attack_box(...)  # 每帧重新生成
```

**优点**: 简单，适合持续性攻击（如"剑气"）  
**缺点**: 一次攻击可能击中多次

**改进方向**（Phase 2）:
- 为每次攻击添加 `hit_targets: set`
- 已击中的目标跳过伤害计算
- 实现"单次攻击只击中一次"

---

## 待优化问题

### 🐛 已知 Bug
1. **重复受击**: 攻击盒持续激活期间，同一目标会被多次击中
   - **临时方案**: 用 `FighterState.HIT` 状态避免
   - **正确方案**: 添加 `hit_targets` 集合

2. **击退无阻尼**: 重攻击击退后角色会滑行很远
   - **解决**: 添加摩擦力或手动衰减 `vel_x`

3. **空中无限跳**: 跳跃判定只检查 `pos_y >= GROUND_Y`
   - **解决**: 添加 `is_grounded` 标志

### ⚡ 性能优化
- 当前无性能问题（双角色 + 简单渲染）
- 未来添加粒子效果时考虑对象池

### 🎨 手感改进
- 攻击前摇/后摇分离（Phase 2）
- 添加攻击取消机制（轻攻击可被重攻击打断）
- 受击后无敌帧（防止无限连击）

---

## 添加新角色

### 1. 创建角色子类
```python
class ShaolinMonk(Fighter):
    def __init__(self, x, y, player_num):
        super().__init__(x, y, COLOR_SHAOLIN, player_num)
        self.speed = 280  # 比默认慢一点
        self.heavy_damage = 20  # 力量型
```

### 2. 重写特殊招式
```python
def special_attack(self):
    """少林：罗汉拳（蓄力重击）"""
    if self.state_timer > 1.0:  # 蓄力1秒
        self._create_attack_box(150, 30)  # 超大范围+伤害
```

### 3. 在 `config.py` 添加角色配置
```python
CHARACTERS = {
    "shaolin": {
        "name": "少林僧",
        "speed": 280,
        "jump": -550,
        "health": 120,
    },
    # ...
}
```

---

## 测试与调试

### 开启调试模式
在 `main.py` 的 `render()` 中取消注释：
```python
self.player1.draw_debug(self.screen)  # 绘制碰撞盒
self.player2.draw_debug(self.screen)
```

### 常用调试技巧
1. **打印状态**: 在 `Fighter.update()` 开头添加 `print(self.state)`
2. **慢动作**: 将 `FPS = 60` 改为 `FPS = 10`
3. **无敌模式**: 在 `take_damage()` 开头 `return`

### 平衡性测试清单
- [ ] 两名角色互相轻攻击，确认伤害对等
- [ ] 重攻击击退距离合理（不飞出屏幕）
- [ ] 跳跃高度能躲过地面攻击
- [ ] 99 秒时间足够打完一局

---

## 提交规范

### Commit Message 格式
```
<type>(<scope>): <subject>

[feat] 新功能
[fix] Bug修复
[refactor] 重构
[docs] 文档
[style] 代码格式
[test] 测试
[chore] 构建/工具
```

示例：
```
feat(fighter): 添加防御机制
fix(collision): 修复重复受击问题
docs(readme): 更新操作说明
```

---

## 常见问题

**Q: 为什么用 pygame-ce 而不是 pygame？**  
A: pygame-ce (Community Edition) 是 2023 年后的活跃分支，修复了大量 bug，支持 Python 3.11+。

**Q: 如何添加精灵图？**  
A: 将图片放入 `assets/sprites/`，然后：
```python
self.image = pygame.image.load("../assets/sprites/shaolin.png")
self.rect = self.image.get_rect(...)
```

**Q: 如何添加音效？**  
A: 使用 `pygame.mixer`:
```python
hit_sound = pygame.mixer.Sound("../assets/audio/hit.wav")
hit_sound.play()
```

---

*最后更新: 2026/07/09*
