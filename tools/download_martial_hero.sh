#!/bin/bash
# Martial Hero 精灵图下载和集成工具

cat << 'EOF'
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    Martial Hero 精灵图资源下载和集成指南                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

📦 资源信息
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
作者: LuizMelo
平台: itch.io
风格: 真实武术风格像素艺术
价格: 约$5-10/包

资源链接
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Martial Hero 1: https://luizmelo.itch.io/martial-hero
2. Martial Hero 2: https://luizmelo.itch.io/martial-hero-2
3. Martial Hero 3: https://luizmelo.itch.io/martial-hero-3

下载步骤
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

步骤1: 访问链接并预览
  • 打开上述链接
  • 查看预览图和动画展示
  • 确认是否满意风格

步骤2: 购买资源（如果满意）
  • 点击 "Purchase" 或 "Add to Cart"
  • 使用信用卡/PayPal支付
  • 下载ZIP文件

步骤3: 解压文件
  • 解压下载的ZIP文件
  • 找到精灵图PNG文件
  • 查看文件结构和尺寸

步骤4: 替换精灵图
  • 备份当前精灵图:
    cp -r assets/sprites assets/sprites_backup

  • 复制新精灵图:
    cp [下载路径]/hero1.png assets/sprites/default.png
    cp [下载路径]/hero2.png assets/sprites/shaolin.png
    cp [下载路径]/hero3.png assets/sprites/emei.png

  • 如果只有3个角色，武当可以复用:
    cp assets/sprites/default.png assets/sprites/wudang.png

步骤5: 检查精灵图规格
  • 验证尺寸: file assets/sprites/default.png
  • 确认格式: PNG with RGBA
  • 推荐尺寸: 512x512 或更大

步骤6: 更新代码配置

  如果精灵图尺寸不同，需要修改 src/sprite_system.py:

  # 原来: 64x64
  sprite_sheet = SpriteSheet(sprite_path, 64, 64)

  # 如果新精灵图是 128x128:
  sprite_sheet = SpriteSheet(sprite_path, 128, 128)

步骤7: 运行游戏测试
  python3 src/main.py

  检查:
  • 角色是否正常显示
  • 动画是否流畅
  • 无加载错误

步骤8: 应用调色板差异化（可选）

  如果购买的是同一角色，可以用调色板工具生成差异:
  python3 tools/regenerate_palettes_pygame.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

免费备选方案（如果预算不足）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FREE Realistic Template:
https://pixel-moon-studio.itch.io/male-realistic-pixel-art-template-sprite-pack

• 完全免费
• 写实风格模板
• 需要自定义武术服装

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

故障排除
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

问题1: 精灵图尺寸不匹配
  → 修改 sprite_system.py 中的 frame_width 和 frame_height

问题2: 动画帧数不同
  → 修改 animations_def 中的帧数配置

问题3: 精灵图加载失败
  → 使用 tools/regenerate_palettes_pygame.py 重新生成

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

执行此脚本后，请按照上述步骤完成资源集成。
EOF
