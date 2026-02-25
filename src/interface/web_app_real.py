#!/usr/bin/env python3
"""
Qianji Web Application - Real AI Integration
"""
import os
import sys
import json
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from flask import Flask, request, jsonify, render_template, send_from_directory
from src.core.bazi_engine_real import BaziEngine

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(project_root, 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize AI engine
print("正在加载千机AI模型...")
bazi_engine = BaziEngine()
print("千机AI模型加载完成！")

@app.route('/')
def index():
    """Main page with dual interface (form + chat)"""
    return render_template('index_fixed.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages with real AI"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': '消息不能为空'}), 400
            
        # Process with real AI engine
        response = bazi_engine.chat_response(message)
        
        return jsonify({'response': response})
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({'error': '处理聊天消息时出现错误'}), 500

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
            return jsonify({'error': '请填写完整信息'}), 400
            
        # Format message for AI
        message = f"请分析以下八字信息：出生日期 {birth_date}，出生时间 {birth_time}，性别 {gender}，出生地点 {location}"
        response = bazi_engine.chat_response(message)
        
        return jsonify({'response': response})
    except Exception as e:
        print(f"Bazi analysis error: {e}")
        return jsonify({'error': '处理请求时出现错误，请稍后重试'}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': '没有文件上传'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '文件名为空'}), 400
            
        # Save file
        filename = f"upload_{hash(file.filename)}.tmp"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Return success
        return jsonify({'success': True, 'filename': file.filename})
    except Exception as e:
        print(f"Upload error: {e}")
        return jsonify({'error': '文件处理失败'}), 500

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory(os.path.join(project_root, 'src', 'interface', 'static'), filename)

if __name__ == '__main__':
    print("启动千机Web服务...")
    print("访问地址: http://localhost:8081")
    app.run(host='127.0.0.1', port=8081, debug=False)