#!/bin/bash
# 武林争霸启动脚本

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
    source venv/bin/activate
    echo "安装依赖..."
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# 启动游戏
echo "启动武林争霸..."
cd src
python main.py
