#!/bin/bash
# Qianji Project Environment Setup

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install core dependencies
pip install --upgrade pip
pip install pandas numpy scikit-learn transformers torch accelerate peft bitsandbytes

# Install web framework for expert validation UI
pip install flask flask-wtf wtforms

# Install vector database clients
pip install pinecone-client weaviate-client milvus-lite

# Install classical Chinese processing
pip install jieba

echo "Environment setup complete!"
echo "To activate: source venv/bin/activate"