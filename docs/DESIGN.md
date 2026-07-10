# 中式格斗游戏设计文档
**项目名称**: 武林争霸 (Wulin Champions)  
**类型**: 2D 横版格斗游戏  
**风格**: 中国武术 + 水墨画风

---

## 核心概念

### 主题定位
- **中式元素**: 中国武术流派（少林、武当、峨眉、华山）
- **美术风格**: 水墨画风格 + 传统配色（朱红、墨黑、青绿）
- **音乐音效**: 古筝、二胡、锣鼓（后期）
- **故事背景**: 武林大会，各派高手争夺"天下第一"

### 游戏机制（MVP 阶段）
1. **1v1 对战**: 两名玩家控制角色对战
2. **基础操作**:
   - 移动: 左/右方向键
   - 跳跃: 上键
   - 轻攻击: J 键
   - 重攻击: K 键
   - 防御: L 键
3. **战斗系统**:
   - 血量条: 每人 100 HP
   - 连击系统: 轻→轻→重（3连击）
   - 硬直/受击: 被打后短暂无法行动
   - 击飞效果: 重攻击击飞对手
4. **胜负判定**:
   - 血量归零失败
   - 时间限制 99 秒（超时血多方胜）

---

## 技术架构

### 核心类设计
```python
Fighter (角色基类)
├── position: (x, y) 位置
├── velocity: (vx, vy) 速度
├── health: int 血量
├── state: IDLE | WALK | JUMP | ATTACK | HIT | BLOCK
├── facing: LEFT | RIGHT 朝向
├── hitbox: Rect 受击区
├── attackbox: Rect 攻击区（攻击时激活）
└── methods:
    - update(dt, input)
    - attack_light()
    - attack_heavy()
    - take_damage(amount)
    - check_collision(other)

Game (游戏管理)
├── player1: Fighter
├── player2: Fighter
├── timer: float 倒计时
├── state: MENU | FIGHT | ROUND_END
└── methods:
    - handle_collisions()
    - check_win_condition()
    - render_ui()
```

### 开发路线图

**Phase 1: 核心战斗系统（当前）**
- [ ] 角色移动 + 跳跃（重力）
- [ ] 基础攻击（轻/重）
- [ ] 碰撞检测（hitbox vs attackbox）
- [ ] 血量系统
- [ ] 简单 UI（血条、计时器）

**Phase 2: 战斗手感**
- [ ] 攻击硬直（攻击动画期间不可移动）
- [ ] 受击硬直（被打后后退 + 短暂无法行动）
- [ ] 连击判定（combo counter）
- [ ] 防御机制（格挡减伤）

**Phase 3: 角色差异化**
- [ ] 第一个角色：少林僧（平衡型）
- [ ] 第二个角色：峨眉剑客（速度型）
- [ ] 特殊招式（每人 1-2 个）

**Phase 4: 完善体验**
- [ ] 角色选择界面
- [ ] 场景背景（竹林、武馆）
- [ ] 音效（攻击音、受击音）
- [ ] 胜利/失败动画

---

## 美术资源需求

### 临时方案（Prototype）
- 使用色块矩形代表角色（红 vs 蓝）
- 纯色背景
- 系统字体显示 UI

### 最终方案（待实现）
- 像素风格精灵图（64x64 每帧）
- 水墨画风格背景
- 中文像素字体（如思源黑体）

---

## 参考作品
- **Street Fighter II**: 经典格斗游戏手感
- **拳皇 (KOF)**: 连招系统
- **侍魂**: 武器格斗 + 东方美学
- **Pygame 格斗教程**: [Real Python Fighting Game](https://realpython.com/)

---

*创建日期: 2026/07/09*  
*当前阶段: Phase 1 - 核心战斗系统*
