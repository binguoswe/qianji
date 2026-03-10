#!/usr/bin/env python3
"""
Qianji Web Application - Real-time Date with Simple Engine
"""
import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from flask import Flask, request, jsonify, render_template, send_from_directory
from src.core.independent_qji_simple import IndependentQjiEngine

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(project_root, 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize AI engine
print("正在加载千机AI模型...")
ai_engine = IndependentQjiEngine()
print("千机AI模型加载完成！")

@app.route('/')
def index():
    """Main page with persistent chat interface"""
    return render_template('index_persistent.html')

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

@app.route('/current-date', methods=['GET'])
def current_date():
    """Get current date information for debugging"""
    try:
        now = datetime.now()
        current_date = now.strftime("%Y年%m月%d日")
        current_weekday = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][now.weekday()]
        
        # Get lunar date using the engine's method
        lunar_info = ai_engine.get_current_lunar_date()
        
        return jsonify({
            'solar_date': current_date,
            'weekday': current_weekday,
            'lunar_info': lunar_info
        })
    except Exception as e:
        print(f"Current date error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory(os.path.join(project_root, 'src', 'interface', 'static'), filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 9999))
    print(f"启动千机Web服务（实时日期）...")
    print(f"访问地址: http://localhost:{port}")
    app.run(host='127.0.0.1', port=port, debug=False)