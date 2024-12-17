import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for managing environment variables."""
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
    PINECONE_CLOUD = os.getenv("PINECONE_CLOUD", "aws")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "hr-chatbot-index")
    PINECONE_DIMENSION = int(os.getenv("PINECONE_DIMENSION", 1024))
    EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "BAAI/bge-large-en")
    LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "llama3-70b-8192")
    ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "http://localhost:9200")
    ELASTICSEARCH_USERNAME = os.getenv("ELASTICSEARCH_USERNAME", "elastic")
    ELASTICSEARCH_PASSWORD = os.getenv("ELASTICSEARCH_PASSWORD", "password")
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))
    TOP_P = float(os.getenv("TOP_P", "0.3"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))