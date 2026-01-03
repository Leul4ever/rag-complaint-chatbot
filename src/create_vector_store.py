import os
import re
import pickle
import numpy as np
import pandas as pd
import faiss
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

def clean_text(text):
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

def run_task_2_pipeline(raw_data_path, vector_store_dir, target_sample_size=15000):
    """
    Load raw data, filter for 5 products, clean, sample, chunk, and index.
    """
    print(f"Loading raw data from {raw_data_path} (this may take a while)...")
    # We load only necessary columns to save memory
    cols = ['Complaint ID', 'Product', 'Consumer complaint narrative']
    df = pd.read_csv(raw_data_path, usecols=cols)
    
    # Define the 5 target products (Mapping to the newer CFPB names)
    product_map = {
        'Credit card or prepaid card': 'Credit card',
        'Checking or savings account': 'Savings account',
        'Payday loan, title loan, personal loan, or advance loan': 'Personal loan',
        'Money transfer, virtual currency, or money service': 'Money transfers',
        'Debt collection': 'Debt collection'
    }
    
    # Filter for these products
    print("Filtering for 5 target product categories...")
    df = df[df['Product'].isin(product_map.keys())].copy()
    
    # Standardize product names
    df['Product'] = df['Product'].map(product_map)
    
    # Drop rows without narratives
    print("Cleaning and filtering narratives...")
    df = df.dropna(subset=['Consumer complaint narrative'])
    
    # Sample before cleaning to save time (stratified)
    print("Performing stratified sampling (3,000 per product if available)...")
    samples_per_product = target_sample_size // 5
    df_sampled = df.groupby('Product', group_keys=False).apply(
        lambda x: x.sample(n=min(len(x), samples_per_product), random_state=42)
    )
    
    print(f"Sampled {len(df_sampled)} records.")
    print("Distribution:\n", df_sampled['Product'].value_counts())

    # Clean text
    print("Pre-processing text...")
    df_sampled['cleaned_narrative'] = df_sampled['Consumer complaint narrative'].apply(clean_text)

    # 2. Text Chunking
    print("Chunking narratives...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )

    chunks = []
    metadata = []

    for idx, row in df_sampled.iterrows():
        narrative = row['cleaned_narrative']
        if not narrative:
            continue
        
        doc_chunks = text_splitter.split_text(narrative)
        for chunk in doc_chunks:
            chunks.append(chunk)
            metadata.append({
                'complaint_id': row['Complaint ID'],
                'product': row['Product'],
                'original_text': row['Consumer complaint narrative']
            })
    
    print(f"Generated {len(chunks)} chunks.")

    # 3. Embedding Generation
    print("Loading model and generating embeddings...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(chunks, show_progress_bar=True)

    # 4. Indexing (FAISS)
    print("Indexing in FAISS...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))

    # 5. Persistence
    os.makedirs(vector_store_dir, exist_ok=True)
    faiss.write_index(index, os.path.join(vector_store_dir, "complaints.index"))
    with open(os.path.join(vector_store_dir, "metadata.pkl"), "wb") as f:
        pickle.dump(metadata, f)
    
    print(f"SUCCESS: Vector store refreshed at {vector_store_dir}")

if __name__ == "__main__":
    RAW_DATA = "data/raw/complaints.csv"
    VECTOR_DIR = "vector_store"
    run_task_2_pipeline(RAW_DATA, VECTOR_DIR)
