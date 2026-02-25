#!/usr/bin/env python3
"""
Qianji Web Application - Simple Conversation Manager
"""
import os
import sys
import json
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from flask import Flask, request, jsonify, render_template, send_from_directory
from src.core.simple_conversation import SimpleConversationManager

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(project_root, 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize conversation manager
print("正在加载千机AI模型...")
conversation_manager = SimpleConversationManager()
print("千机AI模型加载完成！")

@app.route('/')
def index():
    """Main page with dual interface (form + chat)"""
    return render_template('index.html')

@app.route('/bazi', methods=['POST'])
def bazi_analysis():
    """Handle quick bazi analysis from form"""
    try:
        data = request.get_json()
        birth_date = data.get('birthDate')
        birth_time = data.get('birthTime') 
        gender = data.get('gender')
        location = data.get('location')
        
        if not all([birth_date, birth_time, gender, location]):
            return jsonify({'response': '请填写完整的八字信息'}), 400
            
        # Create detailed bazi analysis message
        bazi_message = f"请为我详细分析这个八字：出生日期 {birth_date}，出生时间 {birth_time}，性别 {gender}，出生地点 {location}。需要包含四柱排盘、格局分析、用神选择、大运流年和具体的人生建议。"
        
        # Get response from conversation manager
        response = conversation_manager.get_response(bazi_message)
        
        return jsonify({'response': response})
    except Exception as e:
        print(f"Bazi analysis error: {e}")
        return jsonify({'response': '抱歉，处理您的请求时出现了问题。请稍后重试。'}), 500

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages with AI"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        conversation_id = data.get('conversation_id', None)
        history = data.get('history', [])
        
        if not message:
            return jsonify({'response': '消息不能为空'}), 400
            
        # Get contextual response from conversation manager
        response = conversation_manager.get_response(message, conversation_id, history)
        
        return jsonify({'response': response})
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({'response': '抱歉，处理您的请求时出现了问题。请稍后重试。'}), 500

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory(os.path.join(project_root, 'src', 'interface', 'static'), filename)

if __name__ == '__main__':
    print("启动千机Web服务...")
    print("访问地址: http://localhost:8081")
    app.run(host='127.0.0.1', port=8081, debug=False)