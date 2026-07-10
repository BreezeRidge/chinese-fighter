# 紧急Bug修复指南

## 🔴 当前情况

**游戏状态**: 已启动（进程ID: 92551）  
**调试模式**: 已启用  
**等待**: 用户实机测试结果

---

## 🧪 测试步骤

**请用户执行**：

1. **确认游戏窗口**
   - 窗口标题：武林争霸 Wulin Champions
   - 尺寸：1280x720
   - 场景：水墨画风格竹林背景

2. **测试跳跃**
   - 按 **W** 键（玩家1）
   - 或按 **↑** 键（玩家2）
   - 观察：角色是否向上跳跃

3. **测试攻击**
   - 按 **F** 键（玩家1轻攻击）
   - 或按 **G** 键（玩家1重攻击）
   - 观察：角色是否有攻击动作

4. **观察血条**
   - 两个玩家互相攻击
   - 观察：血条是否减少

---

## 🔍 如果按键有反应

说明：**游戏代码正常，测试方法有问题**

**下一步**：
- 移除调试代码
- 继续正常开发

---

## 🐛 如果按键无反应

**可能原因**：

### 1. 状态机卡住
```python
# 检查：角色是否卡在某个状态
if self.state == FighterState.HIT:  # 卡在受击状态？
    # 永远不会调用 _handle_input()
```

### 2. _update_buffs() 异常
```python
# 检查：增益更新是否抛出异常
for buff_name in list(self.active_buffs.keys()):
    self.active_buffs[buff_name] -= dt  # 如果值不是数字会报错
```

### 3. 按键映射错误
```python
# 检查：pygame.K_w 是否正确映射
keys[pygame.K_w]  # 返回 False？
```

---

## 🔧 紧急修复方案

### 方案1：添加异常捕获
```python
def update(self, dt: float, keys: pygame.key.ScancodeWrapper):
    try:
        # 原有代码
        self._update_buffs(dt)
        # ...
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
```

### 方案2：强制调用 _handle_input
```python
# 移除状态机检查，直接调用
# 原代码：
# if self.state == ...
# elif ...
# else:
#     self._handle_input(dt, keys)

# 改为：
self._handle_input(dt, keys)  # 强制调用
```

### 方案3：简化 _update_buffs
```python
def _update_buffs(self, dt: float):
    """简化版，避免异常"""
    try:
        expired = []
        for name in list(self.active_buffs.keys()):
            if isinstance(self.active_buffs[name], (int, float)):
                self.active_buffs[name] -= dt
                if self.active_buffs[name] <= 0:
                    expired.append(name)
        for name in expired:
            del self.active_buffs[name]
    except:
        pass  # 忽略错误
```

---

## ⚡ 立即行动

**等待用户反馈**：
- ✅ 有反应 → 问题解决，继续开发
- ❌ 无反应 → 执行紧急修复方案

**预计修复时间**：5-10分钟

---

*生成时间: 2026/07/09 16:25*  
*优先级: 最高*
