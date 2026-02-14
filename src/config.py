import os
from dataclasses import dataclass, field
from typing import Dict

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@dataclass(frozen=True)
class PathConfig:
    data_dir: str = os.path.join(BASE_DIR, "data")
    raw_data_path: str = os.path.join(BASE_DIR, "data", "raw", "complaints.csv")
    processed_data_path: str = os.path.join(BASE_DIR, "data", "processed", "complaints_processed.parquet")
    vector_store_dir: str = os.path.join(BASE_DIR, "vector_store")

@dataclass(frozen=True)
class DataConfig:
    target_sample_size: int = 15000
    random_state: int = 42
    product_map: Dict[str, str] = field(default_factory=lambda: {
        'Credit card or prepaid card': 'Credit card',
        'Checking or savings account': 'Savings account',
        'Payday loan, title loan, personal loan, or advance loan': 'Personal loan',
        'Money transfer, virtual currency, or money service': 'Money transfers',
        'Debt collection': 'Debt collection'
    })

@dataclass(frozen=True)
class VectorConfig:
    chunk_size: int = 500
    chunk_overlap: int = 50
    embedding_model_name: str = 'all-MiniLM-L6-v2'

@dataclass(frozen=True)
class RAGConfig:
    top_k: int = 5
    model_id: str = "MBZUAI/LaMini-Flan-T5-248M"
    prompt_template: str = """You are a financial analyst assistant for CrediTrust. Your task is to answer questions about customer complaints. Use the following retrieved complaint excerpts to formulate your answer. If the context doesn't contain the answer, state that you don't have enough information.

Context: {context}

Question: {question}

Answer:"""

# Instantiate configs for structured access
paths = PathConfig()
data_cfg = DataConfig()
vector_cfg = VectorConfig()
rag_cfg = RAGConfig()

# Backward compatibility exports
BASE_DIR = paths.data_dir
DATA_DIR = paths.data_dir
RAW_DATA_PATH = paths.raw_data_path
PROCESSED_DATA_PATH = paths.processed_data_path
VECTOR_STORE_DIR = paths.vector_store_dir
TARGET_SAMPLE_SIZE = data_cfg.target_sample_size
RANDOM_STATE = data_cfg.random_state
PRODUCT_MAP = data_cfg.product_map
CHUNK_SIZE = vector_cfg.chunk_size
CHUNK_OVERLAP = vector_cfg.chunk_overlap
EMBEDDING_MODEL_NAME = vector_cfg.embedding_model_name
TOP_K = rag_cfg.top_k
PROMPT_TEMPLATE = rag_cfg.prompt_template
MODEL_ID = rag_cfg.model_id
