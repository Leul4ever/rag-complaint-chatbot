import pytest
import pandas as pd
import os
import sys

# Ensure src is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_processing import clean_text, perform_stratified_sampling
from src.config import rag_cfg, vector_cfg, data_cfg
from src.vector_manager import VectorManager

def test_clean_text():
    """Test the text cleaning utility."""
    assert clean_text("I am writing to file a complaint. FIX THIS!") == ". fix this!"
    assert clean_text(123) == ""
    assert clean_text("   Hello   World   ") == "hello world"

def test_config_integrity():
    """Verify that configuration values are loaded correctly."""
    assert rag_cfg.top_k == 5
    assert vector_cfg.chunk_size == 500
    assert "Debt collection" in data_cfg.product_map.values()

def test_create_chunks_logic():
    """Test the chunking logic in VectorManager."""
    vm = VectorManager()
    df = pd.DataFrame({
        'Complaint ID': [1],
        'Product': ['Credit card'],
        'Consumer complaint narrative': ['This is a long narrative. ' * 50] # > 500 chars
    })
    chunks, metadata = vm.create_chunks(df)
    assert len(chunks) > 1
    assert metadata[0]['complaint_id'] == 1
    assert metadata[0]['product'] == 'Credit card'

def test_stratified_sampling_count():
    """Verify that stratified sampling returns expected counts."""
    df = pd.DataFrame({
        'Product': ['A'] * 10 + ['B'] * 10,
        'Consumer complaint narrative': ['text'] * 20
    })
    # data_cfg.product_map is not used in raw test df, so num_products = 2
    # target_size = 4 means 2 per product
    sampled_df = perform_stratified_sampling(df, target_size=4)
    assert len(sampled_df) == 4
    assert len(sampled_df[sampled_df['Product'] == 'A']) == 2

def test_vector_manager_initialization():
    """Ensure VectorManager initializes without error."""
    try:
        vm = VectorManager()
        assert vm.model is not None
        assert vm.text_splitter is not None
    except Exception as e:
        pytest.fail(f"VectorManager initialization failed: {e}")
