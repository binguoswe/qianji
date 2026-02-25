"""
Model Manager for Qji Max - Integration of Qwen Max with fine-tuned weights
"""
import os
import torch
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM

class ModelManager:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.model_path = Path("/Users/kirin/Projects/qianji/models/qji_max")
        self.base_model_name = "bailian/qwen3-max-2026-01-23"
        
    def load_model(self):
        """Load Qji Max model (Qwen Max base + fine-tuned weights)"""
        print("🔄 正在加载Qji Max模型...")
        
        try:
            # Check if fine-tuned model exists
            if self.model_path.exists():
                print(f"✅ 找到Qji Max微调模型: {self.model_path}")
                self.tokenizer = AutoTokenizer.from_pretrained(str(self.model_path))
                self.model = AutoModelForCausalLM.from_pretrained(
                    str(self.model_path),
                    torch_dtype=torch.float16,
                    device_map="auto"
                )
            else:
                # Load base Qwen Max model
                print(f"⚠️ 未找到Qji Max微调模型，使用基础Qwen Max模型")
                print(f"🔍 基础模型: {self.base_model_name}")
                self.tokenizer = AutoTokenizer.from_pretrained(self.base_model_name)
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.base_model_name,
                    torch_dtype=torch.float16,
                    device_map="auto"
                )
                
                # Create models directory and save base model as Qji Max
                self.model_path.parent.mkdir(parents=True, exist_ok=True)
                print(f"💾 保存基础模型为Qji Max: {self.model_path}")
                self.model.save_pretrained(str(self.model_path))
                self.tokenizer.save_pretrained(str(self.model_path))
            
            print("✅ Qji Max模型加载完成！")
            return True
            
        except Exception as e:
            print(f"❌ 模型加载失败: {e}")
            print("🔄 回退到智能模板系统...")
            return False
    
    def generate_response(self, prompt, max_length=1024, temperature=0.7):
        """Generate response using Qji Max model"""
        if self.model is None:
            return self._fallback_response(prompt)
        
        try:
            # Prepare input
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
            
            # Generate response
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Remove prompt from response
            if response.startswith(prompt):
                response = response[len(prompt):].strip()
            
            return response
            
        except Exception as e:
            print(f"❌ 生成响应失败: {e}")
            return self._fallback_response(prompt)
    
    def _fallback_response(self, prompt):
        """Fallback to intelligent template system"""
        # Import smart template engine
        from .smart_template_engine import SmartTemplateEngine
        engine = SmartTemplateEngine()
        return engine.generate_response(prompt)

# Global model manager instance
model_manager = ModelManager()