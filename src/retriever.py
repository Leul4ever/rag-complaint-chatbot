import logging
from typing import List, Dict, Any
from src.config import paths, rag_cfg
from src.vector_manager import VectorManager

logger = logging.getLogger(__name__)

class ComplaintRetriever:
    """Handles the retrieval of relevant complaints based on user queries."""

    def __init__(self, store_dir: str = paths.vector_store_dir):
        """
        Initialize the retriever by loading the vector store.
        
        Args:
            store_dir: The directory where the FAISS index and metadata are stored.
        """
        try:
            self.vector_manager = VectorManager()
            self.index, self.metadata = self.vector_manager.load_vector_store(store_dir)
        except Exception as e:
            logger.error(f"Failed to initialize ComplaintRetriever: {e}")
            raise

    def retrieve(self, query: str, k: int = rag_cfg.top_k) -> List[Dict[str, Any]]:
        """
        Retrieve top-k relevant complaints for a given query.
        
        Args:
            query: The user's query string.
            k: The number of results to retrieve.
            
        Returns:
            A list of dictionary results, each containing content and metadata.
        """
        try:
            results = self.vector_manager.search(
                self.index, 
                self.metadata, 
                query, 
                k=k
            )
            return results
        except Exception as e:
            logger.error(f"Error retrieving context for query '{query}': {e}")
            return []

if __name__ == "__main__":
    # Quick test
    logging.basicConfig(level=logging.INFO)
    retriever = ComplaintRetriever()
    test_query = "problems with credit card interest rates"
    hits = retriever.retrieve(test_query)
    for i, hit in enumerate(hits):
        print(f"\nHit {i+1} (Score: {hit['score']:.4f}):")
        print(f"ID: {hit['metadata']['complaint_id']}")
        print(f"Content: {hit['content'][:200]}...")
