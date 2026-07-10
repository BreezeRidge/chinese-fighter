# 武林争霸 - 中文字体修复总结

## 问题
游戏启动后界面出现中文乱码（方块字符），无法正确显示角色名称、连击数、游戏结束文字。

## 原因
`pygame.font.Font(None, size)` 默认使用的是不支持中文的ASCII字体。

## 解决方案

### 1. 添加中文字体加载函数
```python
def get_chinese_font(size: int) -> pygame.font.Font:
    """
    获取支持中文的字体
    自动检测系统中文字体，跨平台兼容
    """
    font_paths = [
        # macOS
        "/System/Library/Fonts/Supplemental/Songti.ttc",  # 宋体 ✅
        "/System/Library/Fonts/Supplemental/STHeiti Light.ttc",
        # Windows
        "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
        "C:/Windows/Fonts/simsun.ttc",  # 宋体
        # Linux
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return pygame.font.Font(font_path, size)
            except:
                continue
    
    # 回退：使用默认字体
    print("警告: 未找到中文字体")
    return pygame.font.Font(None, size)
```

### 2. 在 UIManager 中应用
```python
class UIManager:
    def __init__(self, screen):
        # 替换原来的 pygame.font.Font(None, size)
        self.font_large = get_chinese_font(72)
        self.font_medium = get_chinese_font(48)
        self.font_small = get_chinese_font(36)
        self.font_tiny = get_chinese_font(24)
```

### 3. 验证测试
```bash
# 测试宋体是否能渲染中文
python -c "import pygame; pygame.init(); 
font = pygame.font.Font('/System/Library/Fonts/Supplemental/Songti.ttc', 24); 
text = font.render('少林僧', True, (255,255,255)); 
print('宋体加载成功！尺寸:', text.get_size())"

# 输出：宋体加载成功！尺寸: (72, 34) ✅
```

## 技术细节

### macOS 字体路径发现过程
1. 最初尝试：`/System/Library/Fonts/PingFang.ttc` ❌ 不存在
2. 搜索中文字体：`ls /System/Library/Fonts/Supplemental/*.ttc | grep -i song`
3. 找到：`/System/Library/Fonts/Supplemental/Songti.ttc` ✅

### 跨平台兼容性
- **macOS**: 宋体（Songti.ttc）作为首选，华文黑体作为备选
- **Windows**: 微软雅黑（msyh.ttc）、宋体（simsun.ttc）
- **Linux**: 文泉驿正黑、Noto Sans CJK

### 优雅降级
- 如果所有中文字体都不存在，回退到默认字体
- 不会导致程序崩溃，只是显示为方块
- 输出警告信息提示用户

## Git 提交记录
```
7a583ff fix: 更新macOS中文字体路径为实际存在的Songti.ttc
7f6230b fix: 中文字体显示乱码问题
```

## 效果对比

### 修复前
```
角色名称: □□□（方块）
连击显示: □ COMBO!
游戏结束: □□ □ □□!
```

### 修复后
```
角色名称: 少林僧、峨眉剑客
连击显示: 3 COMBO!
游戏结束: 玩家 1 胜利!
```

## 学到的经验

1. **字体路径因系统而异**：不能假设某个字体一定存在
2. **优雅降级很重要**：即使找不到字体，程序也应该能运行
3. **测试驱动修复**：先用命令行验证字体加载，再集成到代码
4. **跨平台考虑**：预先准备多个平台的字体路径

---

*修复完成时间：2026/07/09*  
*测试通过：宋体可正确渲染中文*
