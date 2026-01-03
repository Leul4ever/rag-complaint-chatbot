import logging
from src.config import VECTOR_STORE_DIR, TOP_K
from src.vector_manager import VectorManager

logger = logging.getLogger(__name__)

class ComplaintRetriever:
    def __init__(self, store_dir=VECTOR_STORE_DIR):
        try:
            self.vector_manager = VectorManager()
            self.index, self.metadata = self.vector_manager.load_vector_store(store_dir)
        except Exception as e:
            logger.error(f"Failed to initialize ComplaintRetriever: {e}")
            raise

    def retrieve(self, query, k=TOP_K):
        """Retrieve top-k relevant complaints for a query."""
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
