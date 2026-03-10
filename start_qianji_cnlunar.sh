#!/bin/bash
# 启动千机项目，使用cnlunar进行准确八字计算

echo "🚀 启动千机AI（cnlunar准确八字版）在端口9999..."
echo "✅ 千机AI已启动，访问地址: http://localhost:9999"
echo "💡 使用 Ctrl+C 停止服务"

# 激活虚拟环境
source venv/bin/activate

# 设置Flask应用和端口
export FLASK_APP=src/interface/web_app_cnlunar.py
export PORT=9999

# 启动千机服务
python -m flask run --host=0.0.0.0 --port=9999 &