import logging
import re
from typing import List, Dict, Any, Tuple
from rank_bm25 import BM25Okapi
from src.config import paths, rag_cfg
from src.vector_manager import VectorManager

logger = logging.getLogger(__name__)

class ComplaintRetriever:
    """Handles hybrid retrieval (Semantic + Keyword) of complaints."""

    def __init__(self, store_dir: str = paths.vector_store_dir):
        """
        Initialize the retriever by loading the vector store and BM25 index.
        """
        try:
            self.vector_manager = VectorManager()
            self.index, self.metadata = self.vector_manager.load_vector_store(store_dir)
            
            # Initialize BM25
            logger.info("Initializing BM25 index for hybrid search...")
            self.corpus = [m.get('original_text', '') for m in self.metadata]
            tokenized_corpus = [self._tokenize(doc) for doc in self.corpus]
            self.bm25 = BM25Okapi(tokenized_corpus)
            
        except Exception as e:
            logger.error(f"Failed to initialize ComplaintRetriever: {e}")
            raise

    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenizer for BM25."""
        return re.sub(r'[^a-zA-Z0-9\s]', '', text.lower()).split()

    def retrieve(self, query: str, k: int = rag_cfg.top_k) -> List[Dict[str, Any]]:
        """
        Retrieve top-k relevant complaints using Hybrid Search (RRF).
        """
        try:
            # 1. Semantic Search (FAISS)
            semantic_results = self.vector_manager.search(self.index, self.metadata, query, k=k*2)
            
            # 2. Keyword Search (BM25)
            tokenized_query = self._tokenize(query)
            bm25_scores = self.bm25.get_scores(tokenized_query)
            top_bm25_indices = sorted(range(len(bm25_scores)), key=lambda i: bm25_scores[i], reverse=True)[:k*2]
            
            # 3. Reciprocal Rank Fusion (RRF)
            # RRF Score = sum( 1 / (k + rank) )
            rrf_scores: Dict[int, float] = {}
            constant = 60 # Default RRF constant
            
            # Add semantic ranks
            for rank, res in enumerate(semantic_results):
                idx = self.metadata.index(res['metadata'])
                rrf_scores[idx] = rrf_scores.get(idx, 0) + 1.0 / (constant + rank + 1)
                
            # Add BM25 ranks
            for rank, idx in enumerate(top_bm25_indices):
                rrf_scores[idx] = rrf_scores.get(idx, 0) + 1.0 / (constant + rank + 1)
                
            # Sort by RRF score
            sorted_indices = sorted(rrf_scores.keys(), key=lambda i: rrf_scores[i], reverse=True)[:k]
            
            final_results = []
            for idx in sorted_indices:
                final_results.append({
                    'content': self.metadata[idx].get('original_text', ''),
                    'metadata': self.metadata[idx],
                    'score': rrf_scores[idx]
                })
                
            logger.info(f"Hybrid search returned {len(final_results)} results.")
            return final_results
            
        except Exception as e:
            logger.error(f"Error in hybrid retrieval for query '{query}': {e}")
            return []

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    retriever = ComplaintRetriever()
    test_query = "unauthorized credit card transaction"
    hits = retriever.retrieve(test_query)
    for i, hit in enumerate(hits):
        print(f"\nHit {i+1} (RRF Score: {hit['score']:.4f}):")
        print(f"ID: {hit['metadata']['complaint_id']}")
        print(f"Content: {hit['content'][:200]}...")
