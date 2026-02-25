#!/usr/bin/env python3
"""
Qianji Web Application - Identity Fixed Version
Forces Qji identity instead of Qwen identity
"""
import os
import sys
import json
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from flask import Flask, request, jsonify, render_template, send_from_directory
from src.core.independent_qji_identity import IndependentQjiIdentityEngine

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(project_root, 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize AI engine
print("正在加载千机AI身份修复版模型...")
ai_engine = IndependentQjiIdentityEngine()
print("千机AI身份修复版模型加载完成！")

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
            
        # Get response from Independent Qji Engine
        response = ai_engine.analyze_bazi(birth_date, birth_time, gender, location)
        
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
        
        if not message:
            return jsonify({'response': '消息不能为空'}), 400
            
        # Get conversation history (if any)
        history = data.get('history', [])
            
        # Get response from Independent Qji Engine  
        response = ai_engine.generate_response(message, history)
        
        return jsonify({'response': response})
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({'response': '抱歉，处理您的请求时出现了问题。请稍后重试。'}), 500

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory(os.path.join(project_root, 'src', 'interface', 'static'), filename)

if __name__ == '__main__':
    print("启动千机Web服务（身份修复版）...")
    print("访问地址: http://localhost:8082")
    app.run(host='127.0.0.1', port=8082, debug=False)