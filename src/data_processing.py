import pandas as pd
import re
import os
import logging
from src.config import PRODUCT_MAP, RANDOM_STATE

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def clean_text(text):
    """Clean the complaint narrative text."""
    if not isinstance(text, str):
        return ""
    # Lowercase
    text = text.lower()
    # Remove common boilerplate
    text = text.replace("i am writing to file a complaint", "")
    # Remove special characters while keeping numbers/punctuation
    text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', text)
    # Collapse spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def load_and_filter_data(file_path):
    """Load raw data and filter for target products."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Raw data file not found at: {file_path}")
    
    logger.info(f"Loading data from {file_path}...")
    try:
        # Load only necessary columns
        cols = ['Complaint ID', 'Product', 'Consumer complaint narrative']
        df = pd.read_csv(file_path, usecols=cols)
        
        logger.info("Filtering for target product categories...")
        df = df[df['Product'].isin(PRODUCT_MAP.keys())].copy()
        df['Product'] = df['Product'].map(PRODUCT_MAP)
        
        logger.info("Removing rows without narratives...")
        df = df.dropna(subset=['Consumer complaint narrative'])
        
        return df
    except Exception as e:
        logger.error(f"Error loading or filtering data: {e}")
        raise

def perform_stratified_sampling(df, target_size=15000):
    """Perform stratified sampling across the product categories."""
    logger.info(f"Performing stratified sampling (target: {target_size})...")
    num_products = df['Product'].nunique()
    if num_products == 0:
        raise ValueError("No products found in the dataset for sampling.")
        
    samples_per_product = target_size // num_products
    
    try:
        df_sampled = df.groupby('Product', group_keys=False).apply(
            lambda x: x.sample(n=min(len(x), samples_per_product), random_state=RANDOM_STATE)
        )
        logger.info(f"Sampled {len(df_sampled)} records.")
        return df_sampled
    except Exception as e:
        logger.error(f"Error during sampling: {e}")
        raise
