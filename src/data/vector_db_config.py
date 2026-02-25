"""
Qianji Vector Database Configuration

This module configures the vector database for RAG (Retrieval Augmented Generation)
system using Weaviate, Pinecone, or Milvus as the backend.
"""

import os
from typing import Optional, Dict, Any

class VectorDBConfig:
    """Configuration class for vector databases."""
    
    def __init__(self):
        # Default to Weaviate for local development
        self.default_backend = "weaviate"
        
        # Weaviate configuration
        self.weaviate_config = {
            "host": "localhost",
            "port": 8080,
            "grpc_port": 50051,
            "scheme": "http"
        }
        
        # Pinecone configuration  
        self.pinecone_config = {
            "api_key": os.getenv("PINECONE_API_KEY", ""),
            "environment": os.getenv("PINECONE_ENVIRONMENT", "us-west1-gcp")
        }
        
        # Milvus configuration
        self.milvus_config = {
            "host": "localhost", 
            "port": 19530,
            "collection_name": "qianji_classics"
        }
        
    def get_config(self, backend: str = None) -> Dict[str, Any]:
        """Get configuration for specified backend."""
        backend = backend or self.default_backend
        if backend == "weaviate":
            return self.weaviate_config
        elif backend == "pinecone":
            return self.pinecone_config
        elif backend == "milvus":
            return self.milvus_config
        else:
            raise ValueError(f"Unsupported backend: {backend}")

# Initialize configuration
vector_db_config = VectorDBConfig()