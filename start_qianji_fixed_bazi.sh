#!/bin/bash
# 启动千机项目（修复八字计算版本），固定使用端口9999

echo "🚀 启动千机AI（修复八字计算版）在端口9999..."
echo "✅ 千机AI已启动，访问地址: http://localhost:9999"
echo "💡 使用 Ctrl+C 停止服务"

# 激活虚拟环境
source venv/bin/activate

# 设置端口环境变量
export PORT=9999

# 启动千机服务（修复八字计算版本）
python -m flask --app src.interface.web_app_fixed_bazi run --host=0.0.0.0 --port=9999