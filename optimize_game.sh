#!/bin/bash
# 游戏性能优化脚本
# 用途: 解决SDL警告、优化资源加载

echo "=========================================="
echo "武林争霸 - 性能优化"
echo "=========================================="
echo ""

# 1. 设置环境变量抑制SDL警告（保留音频功能）
export PYGAME_HIDE_SUPPORT_PROMPT=1
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

# 2. 检查Python版本
echo "🔍 检查环境..."
python3 --version

# 3. 激活虚拟环境
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "✓ 虚拟环境已激活"
else
    echo "✗ 未找到虚拟环境，请先运行: python3 -m venv venv"
    exit 1
fi

# 4. 启动游戏（过滤SDL警告）
echo ""
echo "🎮 启动游戏（已优化输出）..."
echo "   - SDL警告已抑制"
echo "   - 按ESC退出游戏"
echo ""

# 启动游戏，过滤objc和SDL警告
python src/main.py 2>&1 | grep -v "objc\|Class SDL\|spurious casting"
