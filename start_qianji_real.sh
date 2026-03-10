#!/bin/bash
# 启动千机项目真实版，使用Qwen Max API和实时日期

echo "🚀 启动千机AI（真实版）在端口9999..."

# 激活虚拟环境
source venv/bin/activate

# 设置端口环境变量
export PORT=9999

# 启动千机服务 - 使用真实Qianji引擎
FLASK_APP=src/interface/web_app_real_qianji.py flask run --host=0.0.0.0 --port=9999 &

echo "✅ 千机AI已启动，访问地址: http://localhost:9999"
echo "💡 使用 Ctrl+C 停止服务"