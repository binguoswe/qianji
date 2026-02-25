"""
Expert Validation UI for Qianji AI

This module provides a web-based interface for命理 experts to review and validate
AI-generated命理分析. The UI allows experts to:
- View AI predictions and explanations
- Rate accuracy and quality
- Provide feedback and corrections
- Compare different model outputs
- Track validation history

The interface is built with Flask and includes both desktop and mobile views.
"""

from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

class ExpertValidationUI:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()
        self.validation_data_dir = "/Users/kirin/Projects/qianji/data/validation"
        os.makedirs(self.validation_data_dir, exist_ok=True)
        
    def setup_routes(self):
        """Setup Flask routes for the validation interface."""
        @self.app.route('/')
        def index():
            return render_template('validation_index.html')
            
        @self.app.route('/validate', methods=['POST'])
        def validate_prediction():
            """Handle expert validation submission."""
            data = request.json
            validation_record = {
                'timestamp': datetime.now().isoformat(),
                'ai_output': data.get('ai_output', ''),
                'expert_rating': data.get('rating', 0),
                'expert_feedback': data.get('feedback', ''),
                'corrections': data.get('corrections', []),
                'model_version': data.get('model_version', 'unknown')
            }
            
            # Save validation record
            record_id = f"validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            record_path = os.path.join(self.validation_data_dir, f"{record_id}.json")
            with open(record_path, 'w', encoding='utf-8') as f:
                json.dump(validation_record, f, ensure_ascii=False, indent=2)
                
            return jsonify({'status': 'success', 'record_id': record_id})
            
        @self.app.route('/predictions')
        def get_predictions():
            """Get pending predictions for validation."""
            # This would connect to your AI prediction queue
            # For now, return sample data
            return jsonify({
                'predictions': [
                    {
                        'id': 'pred_001',
                        'input_bazi': '甲子 乙丑 丙寅 丁卯',
                        'ai_analysis': '日主丙火生于丑月...',
                        'model_used': 'qwen-max-finetuned-v1'
                    }
                ]
            })
    
    def run(self, host='localhost', port=5001, debug=False):
        """Run the validation UI server."""
        print(f"Expert Validation UI starting on http://{host}:{port}")
        self.app.run(host=host, port=port, debug=debug)

# HTML templates would be in templates/ directory
# CSS/JS assets would be in static/ directory

if __name__ == '__main__':
    ui = ExpertValidationUI()
    ui.run(debug=True)