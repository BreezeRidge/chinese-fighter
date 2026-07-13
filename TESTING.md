# 测试指南 - Cat Fighter精灵图集成

## 已完成修复（2026-07-09）

### 问题1：精灵图显示异常
**现象**：一个方框显示多个角色在跑
**原因**：精灵图帧大小配置错误（64x64 vs 实际50x50）
**修复**：`src/sprite_system.py:242` 改为 `SpriteSheet(sprite_path, 50, 50)`

### 问题2：碰撞检查不合理  
**现象**：碰撞盒与角色实际显示不匹配
**原因**：config.py中角色尺寸仍为旧值（60-65宽 × 95-105高）
**修复**：所有角色改为 `width=50, height=50` 匹配Cat Fighter精灵图

## Cat Fighter精灵图规格

```
文件大小：500x500 像素
帧布局：10列 × 10行
每帧大小：50x50 像素
总帧数：100帧
```

### 动画映射（10行）
- 第1行：待机 (idle)
- 第2行：奔跑 (walk)  
- 第3行：跳跃 (jump)
- 第4行：轻攻击 (attack_light)
- 第5行：重攻击 (attack_heavy)
- 第6行：受击 (hit)
- 第7-10行：备用扩展

## 测试步骤

### 1. 启动游戏
```bash
cd /Users/rookie/todo/python/chinese-fighter
source venv/bin/activate
python src/main.py
```

### 2. 检查项目

#### 2.1 精灵显示 ✓
- [ ] 角色显示为单个完整的猫武士形象
- [ ] 不再出现"多个角色在一个框"的情况
- [ ] 动画播放流畅（待机、行走、跳跃、攻击）

#### 2.2 碰撞检测 ✓
- [ ] 攻击判定准确（击中显示在正确位置）
- [ ] 角色之间不会穿透
- [ ] 攻击范围与视觉表现一致

#### 2.3 角色动作
测试所有状态的动画：
- [ ] **待机**：角色站立时播放第1行动画
- [ ] **行走**：按A/D或方向键移动时播放第2行
- [ ] **跳跃**：按W/↑时播放第3行
- [ ] **轻攻击**：按F/J时播放第4行
- [ ] **重攻击**：按G/K时播放第5行
- [ ] **受击**：被攻击时播放第6行

#### 2.4 四个角色差异
当前所有角色使用同一套动画，仅颜色不同：
- [ ] default.png（玩家1默认）
- [ ] shaolin.png（少林僧）
- [ ] emei.png（峨眉剑客）
- [ ] wudang.png（武当道士）

### 3. 操作测试

**玩家1（左侧）**
- 移动：A（左）D（右）W（跳）
- 攻击：F（轻）G（重）H（格挡）
- 特殊：Q/E

**玩家2（右侧）**
- 移动：←（左）→（右）↑（跳）
- 攻击：J（轻）K（重）L（格挡）
- 特殊：I/O

## 已知问题

### 警告信息（不影响游戏）
```
objc[...]: Class SDL_* is implemented in both...
```
这是SDL2库重复加载的警告，不影响游戏运行。

### 待优化项
1. 四个角色当前使用相同精灵图（可通过调色或替换资源差异化）
2. 格挡状态暂时使用idle动画
3. 特殊招式动画需要进一步调优

## 提交记录

```
49fbc04 - fix: 修正所有角色碰撞盒尺寸匹配Cat Fighter精灵图
- config.py: 所有角色 width/height 改为 50
- sprite_system.py: 帧大小从64改为50
```

## 资源归属

**Cat Fighter Sprite**
- 来源：OpenGameArt.org
- 作者：dogchicken
- 许可：CC-BY 3.0
- 链接：https://opengameart.org/content/cat-fighter-sprite-sheet

备份位置：`assets/sprites_backup_catfighter/`
