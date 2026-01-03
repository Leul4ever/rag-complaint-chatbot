import os
import pickle
import numpy as np
import faiss
import logging
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from src.config import CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL_NAME

logger = logging.getLogger(__name__)

class VectorManager:
    def __init__(self, model_name=EMBEDDING_MODEL_NAME):
        try:
            logger.info(f"Loading embedding model: {model_name}...")
            self.model = SentenceTransformer(model_name)
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=CHUNK_SIZE,
                chunk_overlap=CHUNK_OVERLAP
            )
        except Exception as e:
            logger.error(f"Failed to initialize VectorManager: {e}")
            raise

    def create_chunks(self, df):
        """Split narratives into chunks and prepare metadata."""
        logger.info("Chunking narratives...")
        chunks = []
        metadata = []
        
        for _, row in df.iterrows():
            narrative = row.get('cleaned_narrative', row.get('Consumer complaint narrative', ''))
            if not narrative or narrative == 'None':
                continue
            
            doc_chunks = self.text_splitter.split_text(str(narrative))
            for chunk in doc_chunks:
                chunks.append(chunk)
                metadata.append({
                    'complaint_id': row['Complaint ID'],
                    'product': row['Product'],
                    'original_text': row['Consumer complaint narrative']
                })
        
        logger.info(f"Generated {len(chunks)} chunks.")
        return chunks, metadata

    def generate_embeddings(self, chunks):
        """Generate vectors for the given text chunks."""
        logger.info("Generating embeddings...")
        try:
            embeddings = self.model.encode(chunks, show_progress_bar=True)
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise

    def save_vector_store(self, embeddings, metadata, output_dir):
        """Index embeddings in FAISS and save to disk."""
        logger.info(f"Saving vector store to {output_dir}...")
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            # Indexing
            dimension = embeddings.shape[1]
            index = faiss.IndexFlatL2(dimension)
            index.add(np.array(embeddings).astype('float32'))
            
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
