import logging
import sys
import os

# Add the project root to sys.path to allow absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import RAW_DATA_PATH, VECTOR_STORE_DIR, TARGET_SAMPLE_SIZE
from src.data_processing import load_and_filter_data, perform_stratified_sampling, clean_text
from src.vector_manager import VectorManager

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    try:
        # 1. Load and Filter
        df = load_and_filter_data(RAW_DATA_PATH)
        
        # 2. Sample
        df_sampled = perform_stratified_sampling(df, TARGET_SAMPLE_SIZE)
        
        # 3. Clean
        logger.info("Cleaning narratives...")
        df_sampled['cleaned_narrative'] = df_sampled['Consumer complaint narrative'].apply(clean_text)
        
        # 4. Initialize Manager
        manager = VectorManager()
        
        # 5. Chunk
        chunks, metadata = manager.create_chunks(df_sampled)
        
        # 6. Embed
        embeddings = manager.generate_embeddings(chunks)
        
        # 7. Save
        manager.save_vector_store(embeddings, metadata, VECTOR_STORE_DIR)
        
        logger.info(f"Pipeline completed successfully. Vector store ready at {VECTOR_STORE_DIR}")
        
    except FileNotFoundError as e:
        logger.error(f"Configuration error: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
