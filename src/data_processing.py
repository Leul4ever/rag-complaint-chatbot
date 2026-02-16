import pandas as pd
import re
import os
import logging
from typing import Optional, Any
from src.config import data_cfg

# Use the existing logger if possible, otherwise setup basic
logger = logging.getLogger(__name__)

def clean_text(text: Any) -> str:
    """
    Clean the complaint narrative text by removing boilerplate and normalizing whitespace.
    
    Args:
        text: The raw narrative text (might be non-string).
        
    Returns:
        The cleaned text string.
    """
    if not isinstance(text, str):
        return ""
    # Lowercase
    text = text.lower()
    # Remove common boilerplate
    text = text.replace("i am writing to file a complaint", "")
    # Remove special characters while keeping numbers/punctuation
    text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', text)
    # Remove leading punctuation that might be left over from boilerplate
    text = re.sub(r'^[.,!?\s]+', '', text)
    # Collapse spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def load_and_filter_data(file_path: str) -> pd.DataFrame:
    """
    Load raw data from CSV and filter for target product categories.
    
    Args:
        file_path: Absolute path to the raw CSV file.
        
    Returns:
        A filtered pandas DataFrame.
        
    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Raw data file not found at: {file_path}")
    
    logger.info(f"Loading data from {file_path}...")
    try:
        # Load only necessary columns to save memory
        cols = ['Complaint ID', 'Product', 'Consumer complaint narrative']
        df = pd.read_csv(file_path, usecols=cols)
        
        logger.info("Filtering for target product categories...")
        target_products = list(data_cfg.product_map.keys())
        df = df[df['Product'].isin(target_products)].copy()
        df['Product'] = df['Product'].map(data_cfg.product_map)
        
        logger.info("Removing rows without narratives...")
        df = df.dropna(subset=['Consumer complaint narrative'])
        
        return df
    except Exception as e:
        logger.error(f"Error loading or filtering data: {e}")
        raise

def perform_stratified_sampling(df: pd.DataFrame, target_size: int = data_cfg.target_sample_size) -> pd.DataFrame:
    """
    Perform stratified sampling across the product categories to ensure balanced representation.
    
    Args:
        df: The filtered DataFrame to sample from.
        target_size: The desired total number of samples.
        
    Returns:
        A sampled pandas DataFrame.
        
    Raises:
        ValueError: If no products are found in the dataset.
    """
    logger.info(f"Performing stratified sampling (target: {target_size})...")
    num_products = df['Product'].nunique()
    if num_products == 0:
        raise ValueError("No products found in the dataset for sampling.")
        
    samples_per_product = target_size // num_products
    
    try:
        df_sampled = df.groupby('Product', group_keys=False).apply(
            lambda x: x.sample(n=min(len(x), samples_per_product), random_state=data_cfg.random_state)
        )
        logger.info(f"Sampled {len(df_sampled)} records.")
        return df_sampled
    except Exception as e:
        logger.error(f"Error during sampling: {e}")
        raise
