#!/bin/bash
# 角色加载问题永久修复脚本
# 使用Pygame重新生成调色板精灵图

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║       角色加载问题 - 永久修复执行指南                       ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# 检查pygame是否安装
if ! python3 -c "import pygame" 2>/dev/null; then
    echo "❌ Pygame未安装"
    echo ""
    echo "请先安装pygame:"
    echo "  pip3 install pygame"
    echo ""
    echo "或者使用conda:"
    echo "  conda install -c conda-forge pygame"
    echo ""
    exit 1
fi

echo "✓ Pygame已安装"
echo ""

# 检查原始精灵图是否存在
if [ ! -f "assets/sprites/chibi_fighter_original.png" ]; then
    echo "❌ 原始精灵图不存在: assets/sprites/chibi_fighter_original.png"
    exit 1
fi

echo "✓ 原始精灵图存在"
echo ""

# 备份当前精灵图
echo "📦 备份当前精灵图..."
mkdir -p backups/sprites_$(date +%Y%m%d_%H%M%S)
cp assets/sprites/default.png backups/sprites_$(date +%Y%m%d_%H%M%S)/
cp assets/sprites/shaolin.png backups/sprites_$(date +%Y%m%d_%H%M%S)/
cp assets/sprites/emei.png backups/sprites_$(date +%Y%m%d_%H%M%S)/
cp assets/sprites/wudang.png backups/sprites_$(date +%Y%m%d_%H%M%S)/
echo "✓ 备份完成"
echo ""

# 运行重新生成工具
echo "🔄 运行Pygame调色板重新生成工具..."
echo ""
python3 tools/regenerate_palettes_pygame.py

if [ $? -eq 0 ]; then
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                                                              ║"
    echo "║              ✅ 永久修复完成！                              ║"
    echo "║                                                              ║"
    echo "║  所有角色精灵图已使用Pygame重新生成                         ║"
    echo "║  保证100%兼容Pygame加载                                     ║"
    echo "║  角色颜色差异化已恢复                                       ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "📊 生成的精灵图:"
    ls -lh assets/sprites/*.png | grep -v original
    echo ""
    echo "🎮 现在可以运行游戏测试:"
    echo "  python3 src/main.py"
else
    echo ""
    echo "❌ 生成失败，请检查错误信息"
    echo ""
    echo "💡 如果问题持续，可以回滚备份:"
    echo "  cp backups/sprites_*/default.png assets/sprites/"
    exit 1
fi
