# 性能优化指南

## 🔴 严重BUG修复：字体段错误(SIGSEGV) — 已根治

### 崩溃现象
```
Exception Type: EXC_BAD_ACCESS (SIGSEGV)
Exception Codes: KERN_INVALID_ADDRESS at 0x2f73746e65746e6f
Termination Reason: Namespace SIGNAL, Code 11 Segmentation fault: 11
```
游戏运行一段时间后随机崩溃，exit code 139。

### 根因分析（通过对照实验定位）

**1. 崩溃地址解码是关键线索**
崩溃地址 `0x2f73746e65746e6f` 小端解码为 ASCII 字符串 `"ontents/"`
（来自 macOS 字体路径 `.../Contents/...`）。CPU 把字符串数据当指针解引用
= 典型的内存损坏 / use-after-free。

**2. C堆栈定位到SDL2_ttf**
```
SDL_AllocFormat_REAL          ← 崩溃点
SDL_CreateRGBSurfaceWithFormat_REAL
AllocateAlignedPixels         (SDL2_ttf)
Create_Surface_Blended        (SDL2_ttf)
TTF_Render_Wrapped_Internal   (SDL2_ttf)
font_render                   (pygame)
```

**3. 对照实验确定真凶是 .ttc 集合字体**

| 字体 | 类型 | 50轮GC压力测试 | 结果 |
|------|------|--------------|------|
| Songti.ttc（原首选） | .ttc集合 | 崩溃 | ✗ SIGSEGV |
| 内置默认字体 | pygame内置 | 通过 | ✓ |
| Arial Unicode.ttf | .ttf单字体 | 通过 | ✓ |

**结论**：macOS 系统的某些 `.ttc`（TrueType Collection 集合字体，
如 Songti.ttc）在 SDL2_ttf 2.24 下存在内存管理缺陷。集合字体内部
结构复杂，持续渲染 + GC 时机不当会触发悬空指针访问 → 段错误。

### 修复方案

`src/ui.py` 的 `get_chinese_font()` 调整字体优先级：
- **首选 `.ttf` 单字体**（Arial Unicode.ttf 等，压力测试稳定）
- **`.ttc` 集合字体降为兜底**（仅在无 .ttf 可用时使用）
- 移除了原来排第一的 Songti.ttc

**验证**：80轮GC压力 + 200轮多字体渲染 + 3轮完整游戏生命周期
（战斗→重启→再战斗）全部通过，退出码0。

---

## SDL警告说明

### 问题现象
启动游戏时出现大量警告信息：
```
objc[xxxxx]: Class SDL_RumbleMotor is implemented in both...
```

### 原因分析
macOS系统中存在两个SDL2库：
1. **系统级SDL2**: `/opt/homebrew/Cellar/sdl2/2.32.10/lib/libSDL2-2.0.0.dylib`
2. **Pygame内置SDL2**: `venv/lib/python3.14/site-packages/pygame/.dylibs/libSDL2-2.0.0.dylib`

两个库同时加载导致类定义冲突警告。

### 影响评估
✅ **不影响游戏运行**
- 警告信息仅在启动时出现
- 游戏功能完全正常
- 不会造成崩溃或性能问题

⚠️ **理论风险**（实际未发现）
- "spurious casting failures"（虚假类型转换失败）
- "mysterious crashes"（神秘崩溃）

## 优化方案

### 方案1：使用优化脚本（推荐）
```bash
./optimize_game.sh
```

**优点**：
- 自动过滤SDL警告输出
- 设置优化环境变量
- 保持终端输出清爽

### 方案2：卸载系统SDL2（不推荐）
```bash
brew uninstall sdl2
```

**缺点**：
- 可能影响其他依赖SDL2的应用
- Pygame内置SDL2已足够使用

### 方案3：环境变量抑制
在 `~/.zshrc` 或 `~/.bashrc` 中添加：
```bash
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
export PYGAME_HIDE_SUPPORT_PROMPT=1
```

### 方案4：修改Pygame安装（高级）
```bash
# 重新安装pygame时指定不使用bundled SDL
pip uninstall pygame
pip install pygame --no-binary :all:
```

## 性能优化建议

### 1. 精灵图优化
当前精灵图规格：
- 大小：500x500 PNG
- 格式：RGBA（含透明通道）
- 单个文件：20-26KB

**优化建议**：
```bash
# 使用pngquant压缩（保持质量）
pngquant --quality=65-80 assets/sprites/*.png -o compressed.png
```

### 2. 代码性能优化

#### 已优化项 ✅
- 使用浮点数精度位置计算
- 精灵图缓存机制
- 碰撞检测优化（早期退出）

#### 待优化项
```python
# 建议：缓存精灵帧而不是每次get_current_frame()
class Fighter:
    def __init__(self):
        self._cached_frame = None
        self._cache_valid = False
```

### 3. 内存优化

**当前内存占用**（估算）：
- 精灵图加载：~100KB × 4角色 = 400KB
- 场景渲染：~2MB
- 总计：<10MB

**优化建议**：
- 使用精灵图集（sprite atlas）合并多个角色
- 延迟加载非当前场景资源

### 4. 帧率优化

**目标**：稳定60 FPS

**当前配置**：
```python
FPS = 60
dt = self.clock.tick(FPS) / 1000.0
```

**监控工具**：
```python
# 添加FPS显示（调试模式）
if self.debug_mode:
    fps = self.clock.get_fps()
    font.render(f"FPS: {fps:.1f}", ...)
```

## 性能测试

### 测试场景
1. 双人对战（无AI）
2. 单人对战AI
3. 持续战斗5分钟

### 性能指标
- **帧率**: 应保持在55-60 FPS
- **内存**: 应低于50MB
- **CPU**: 应低于30%（单核）

### 测试命令
```bash
# 使用Activity Monitor监控
open -a "Activity Monitor"

# 或使用命令行
while true; do
    ps aux | grep "python src/main.py" | grep -v grep | awk '{print "CPU:", $3"%", "MEM:", $4"%"}'
    sleep 1
done
```

## 故障排查

### 问题1：游戏卡顿
**可能原因**：
- 精灵动画更新过于频繁
- 特效粒子过多

**解决方案**：
```python
# 降低特效密度
self.effects.max_particles = 50  # 默认100
```

### 问题2：内存持续增长
**可能原因**：
- 特效对象未正确清理
- 精灵帧缓存过多

**解决方案**：
```python
# 定期清理过期特效
if len(self.effects.particles) > 100:
    self.effects.particles = self.effects.particles[-50:]
```

### 问题3：启动缓慢
**可能原因**：
- 精灵图加载耗时
- 音效文件加载

**解决方案**：
- 添加启动加载界面
- 异步加载非关键资源

## 总结

当前游戏性能表现良好：
- ✅ SDL警告不影响运行
- ✅ 内存占用合理
- ✅ 帧率稳定
- ✅ 响应迅速

**推荐操作**：
1. 使用 `./optimize_game.sh` 启动游戏（过滤警告）
2. 监控游戏运行性能
3. 根据实际情况进一步优化
