#!/bin/bash
# 千机AI v1.0 推送到GitHub脚本

echo "🚀 正在推送千机AI v1.0到GitHub..."

# 确保在正确的目录
cd /Users/kirin/Projects/qianji

# 添加远程仓库（如果还没有）
git remote add origin https://github.com/binguoswe/qianji.git 2>/dev/null || true

# 推送主分支和标签
git push -u origin main --tags

echo "✅ 千机AI v1.0已成功推送到GitHub！"
echo "仓库地址: https://github.com/binguoswe/qianji"