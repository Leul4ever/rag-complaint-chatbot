import os

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_PATH = os.path.join(DATA_DIR, "raw", "complaints.csv")
PROCESSED_DATA_PATH = os.path.join(DATA_DIR, "processed", "complaints_processed.parquet")
VECTOR_STORE_DIR = os.path.join(BASE_DIR, "vector_store")

# Sampling Configuration
TARGET_SAMPLE_SIZE = 15000
RANDOM_STATE = 42

# Product Mapping
PRODUCT_MAP = {
    'Credit card or prepaid card': 'Credit card',
    'Checking or savings account': 'Savings account',
    'Payday loan, title loan, personal loan, or advance loan': 'Personal loan',
    'Money transfer, virtual currency, or money service': 'Money transfers',
    'Debt collection': 'Debt collection'
}

# Chunking Configuration
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Embedding Configuration
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'

# RAG Configuration
TOP_K = 5
PROMPT_TEMPLATE = """You are a financial analyst assistant for CrediTrust. Your task is to answer questions about customer complaints. Use the following retrieved complaint excerpts to formulate your answer. If the context doesn't contain the answer, state that you don't have enough information.

Context: {context}

Question: {question}

Answer:"""
