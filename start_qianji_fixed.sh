#!/bin/bash
# 启动千机项目（修复版），固定使用端口9999

echo "🚀 启动千机AI（修复版）在端口9999..."

# 激活虚拟环境
source venv/bin/activate

# 设置Flask应用
export FLASK_APP=src/interface/web_app_fixed_realtime.py
export FLASK_ENV=production
export PORT=9999

# 启动千机服务
flask run --host=0.0.0.0 --port=9999 &

echo "✅ 千机AI已启动，访问地址: http://localhost:9999"
echo "💡 使用 Ctrl+C 停止服务"