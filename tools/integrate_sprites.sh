#!/bin/bash
# 角色精灵图自动集成工具

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║    角色精灵图自动集成工具                                   ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# 检查参数
if [ $# -eq 0 ]; then
    echo "使用方法:"
    echo "  ./tools/integrate_sprites.sh <ZIP文件路径>"
    echo ""
    echo "示例:"
    echo "  ./tools/integrate_sprites.sh ~/Downloads/template.zip"
    echo ""
    echo "推荐资源:"
    echo "  1. FREE Realistic Template"
    echo "     https://pixel-moon-studio.itch.io/male-realistic-pixel-art-template-sprite-pack"
    echo ""
    echo "  2. Kenney Platformer Pack"
    echo "     https://kenney.nl/assets/platformer-pack-redux"
    exit 1
fi

ZIP_FILE="$1"

# 检查文件是否存在
if [ ! -f "$ZIP_FILE" ]; then
    echo "✗ 文件不存在: $ZIP_FILE"
    exit 1
fi

echo "✓ 找到ZIP文件: $ZIP_FILE"
echo ""

# 创建临时目录
TEMP_DIR="/tmp/sprite_extract_$$"
mkdir -p "$TEMP_DIR"
echo "✓ 创建临时目录: $TEMP_DIR"

# 解压
echo "解压中..."
unzip -q "$ZIP_FILE" -d "$TEMP_DIR"
if [ $? -eq 0 ]; then
    echo "✓ 解压完成"
else
    echo "✗ 解压失败"
    exit 1
fi

# 查找PNG文件
echo ""
echo "查找精灵图文件..."
PNG_FILES=$(find "$TEMP_DIR" -name "*.png" -type f)
PNG_COUNT=$(echo "$PNG_FILES" | wc -l | tr -d ' ')

echo "✓ 找到 $PNG_COUNT 个PNG文件"

if [ $PNG_COUNT -eq 0 ]; then
    echo "✗ 未找到PNG文件"
    exit 1
fi

# 显示前10个文件
echo ""
echo "文件列表（前10个）:"
echo "$PNG_FILES" | head -10 | nl

# 备份现有精灵图
echo ""
echo "备份现有精灵图..."
BACKUP_DIR="assets/sprites_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp assets/sprites/*.png "$BACKUP_DIR/" 2>/dev/null
echo "✓ 备份完成: $BACKUP_DIR"

# 选择精灵图
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "选择集成方式:"
echo "  1. 自动选择（使用前4个PNG文件）"
echo "  2. 手动指定文件"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
read -p "选择 (1/2) [1]: " CHOICE
CHOICE=${CHOICE:-1}

if [ "$CHOICE" = "1" ]; then
    # 自动选择前4个
    CHARACTERS=("default" "shaolin" "emei" "wudang")
    INDEX=0

    echo ""
    echo "开始集成..."
    echo "$PNG_FILES" | head -4 | while read -r PNG_FILE; do
        if [ $INDEX -lt 4 ]; then
            CHAR=${CHARACTERS[$INDEX]}
            DEST="assets/sprites/${CHAR}.png"
            cp "$PNG_FILE" "$DEST"
            echo "✓ $CHAR.png <- $(basename "$PNG_FILE")"
            INDEX=$((INDEX + 1))
        fi
    done

    echo ""
    echo "✓ 自动集成完成！"
else
    echo ""
    echo "请手动复制文件到 assets/sprites/ 目录："
    echo "  - default.png"
    echo "  - shaolin.png"
    echo "  - emei.png"
    echo "  - wudang.png"
    echo ""
    echo "文件位于: $TEMP_DIR"
    echo "（临时目录不会自动删除，请手动操作后删除）"
    exit 0
fi

# 验证
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "验证集成结果:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ls -lh assets/sprites/*.png | grep -v original

# 清理
echo ""
read -p "是否删除临时目录? (y/n) [y]: " CLEANUP
CLEANUP=${CLEANUP:-y}
if [ "$CLEANUP" = "y" ]; then
    rm -rf "$TEMP_DIR"
    echo "✓ 临时目录已删除"
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║    ✅ 精灵图集成完成！                                      ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "下一步:"
echo "  1. 测试游戏: python3 src/main.py"
echo "  2. 如需颜色差异化，运行:"
echo "     python3 tools/regenerate_palettes_pygame.py"
