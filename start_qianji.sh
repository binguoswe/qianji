#!/bin/bash
# 启动千机项目，固定使用端口9999

echo "Starting Qianji on port 9999..."

# 激活虚拟环境
source venv/bin/activate

# 设置端口环境变量
export PORT=9999

# 启动千机服务
python -m flask run --host=0.0.0.0 --port=9999 &

echo "Qianji is now running on http://localhost:9999"
echo "Use Ctrl+C to stop the service"