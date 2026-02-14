import os
import pickle
import numpy as np
import faiss
import logging
from typing import List, Dict, Tuple, Any, Optional
import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from src.config import vector_cfg

logger = logging.getLogger(__name__)

class VectorManager:
    """Manages text chunking, embedding generation, and FAISS indexing."""

    def __init__(self, model_name: str = vector_cfg.embedding_model_name):
        """
        Initialize the VectorManager with a specific embedding model.
        
        Args:
            model_name: The name of the sentence-transformers model to use.
        """
        try:
            logger.info(f"Loading embedding model: {model_name}...")
            self.model = SentenceTransformer(model_name)
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=vector_cfg.chunk_size,
                chunk_overlap=vector_cfg.chunk_overlap
            )
        except Exception as e:
            logger.error(f"Failed to initialize VectorManager: {e}")
            raise

    def create_chunks(self, df: pd.DataFrame) -> Tuple[List[str], List[Dict[str, Any]]]:
        """
        Split narratives into chunks and prepare metadata.
        
        Args:
            df: DataFrame containing consumer complaints.
            
        Returns:
            A tuple containing a list of text chunks and a list of corresponding metadata dictionaries.
        """
        logger.info("Chunking narratives...")
        chunks: List[str] = []
        metadata: List[Dict[str, Any]] = []
        
        for _, row in df.iterrows():
            narrative = row.get('cleaned_narrative', row.get('Consumer complaint narrative', ''))
            if not narrative or str(narrative).lower() == 'none':
                continue
            
            doc_chunks = self.text_splitter.split_text(str(narrative))
            for chunk in doc_chunks:
                chunks.append(chunk)
                metadata.append({
                    'complaint_id': row.get('Complaint ID'),
                    'product': row.get('Product'),
                    'original_text': row.get('Consumer complaint narrative')
                })
        
        logger.info(f"Generated {len(chunks)} chunks.")
        return chunks, metadata

    def generate_embeddings(self, chunks: List[str]) -> np.ndarray:
        """
        Generate vectors for the given text chunks.
        
        Args:
            chunks: List of text strings to embed.
            
        Returns:
            A numpy array of embeddings.
        """
        logger.info(f"Generating embeddings for {len(chunks)} chunks...")
        try:
            embeddings = self.model.encode(chunks, show_progress_bar=True)
            return np.array(embeddings)
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise

    def save_vector_store(self, embeddings: np.ndarray, metadata: List[Dict[str, Any]], output_dir: str) -> None:
        """
        Index embeddings in FAISS and save to disk.
        
        Args:
            embeddings: Numpy array of embeddings.
            metadata: List of metadata dictionaries.
            output_dir: Directory to save the index and metadata.
        """
        logger.info(f"Saving vector store to {output_dir}...")
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            # Indexing
            dimension = embeddings.shape[1]
            index = faiss.IndexFlatL2(dimension)
            index.add(embeddings.astype('float32'))
            
            # Save index
            index_path = os.path.join(output_dir, "complaints.index")
            faiss.write_index(index, index_path)
            
            # Save metadata
            metadata_path = os.path.join(output_dir, "metadata.pkl")
            with open(metadata_path, "wb") as f:
                pickle.dump(metadata, f)
                
            logger.info("Vector store persisted successfully.")
        except Exception as e:
            logger.error(f"Error saving vector store: {e}")
            raise

    def load_vector_store(self, store_dir: str) -> Tuple[faiss.Index, List[Dict[str, Any]]]:
        """
        Load FAISS index and metadata from disk.
        
        Args:
            store_dir: Directory where the store files are located.
            
        Returns:
            A tuple containing the FAISS index and the metadata list.
        """
        logger.info(f"Loading vector store from {store_dir}...")
        try:
            index_path = os.path.join(store_dir, "complaints.index")
            metadata_path = os.path.join(store_dir, "metadata.pkl")
            
            if not os.path.exists(index_path) or not os.path.exists(metadata_path):
                raise FileNotFoundError(f"Vector store files not found in {store_dir}")
                
            index = faiss.read_index(index_path)
            with open(metadata_path, "rb") as f:
                metadata = pickle.load(f)
                
            logger.info("Vector store loaded successfully.")
            return index, metadata
        except Exception as e:
            logger.error(f"Error loading vector store: {e}")
            raise

    def search(self, index: faiss.Index, metadata: List[Dict[str, Any]], query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Perform similarity search for a query string.
        
        Args:
            index: FAISS index to search.
            metadata: Metadata list associated with the index.
            query: The query string to search for.
            k: Number of nearest neighbors to retrieve.
            
        Returns:
            A list of result dictionaries containing content, metadata, and score.
        """
        logger.info(f"Searching for: {query} (k={k})")
        try:
            # Embed query
            query_vector = self.model.encode([query]).astype('float32')
            
            # Search index
            distances, indices = index.search(query_vector, k)
            
            # Retrieve results
            results = []
            for i, idx in enumerate(indices[0]):
                if idx != -1:
                    results.append({
                        'content': metadata[idx].get('original_text', ''),
                        'metadata': metadata[idx],
                        'score': float(distances[0][i])
                    })
            
            return results
        except Exception as e:
            logger.error(f"Error during search: {e}")
            raise
