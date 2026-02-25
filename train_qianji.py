#!/usr/bin/env python3
"""
Training script for Qianji AI - Fine-tune Qwen Max on classical bazi texts
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.core.model_finetuning import QianjiFineTuner

def main():
    print("🚀 Starting Qianji AI training...")
    
    # Initialize the fine-tuner
    tuner = QianjiFineTuner()
    
    try:
        # Setup model with 4-bit quantization to save memory
        tuner.setup_model(use_4bit=True)
        
        # Configure LoRA parameters
        tuner.configure_lora(
            r=8,
            lora_alpha=16,
            lora_dropout=0.1,
            target_modules=["q_proj", "v_proj"]
        )
        
        # Prepare training data from classical texts
        data_path = project_root / "raw_books" / "bazi_classics"
        print(f"Loading training data from: {data_path}")
        
        # Start fine-tuning
        output_dir = project_root / "models" / "qianji-finetuned"
        tuner.start_finetuning(output_dir=str(output_dir))
        
        print("✅ Training configuration completed!")
        print("To start actual training, you need to implement the data preparation")
        print("and trainer setup in the QianjiFineTuner class.")
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()