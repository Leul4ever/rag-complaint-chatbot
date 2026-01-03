# Task 2 Report: Vector Store Setup

## 1. Stratified Sampling Strategy
To ensure the vector store is representative and computationally efficient for this phase, we implemented a stratified sampling strategy:
- **Target Sample Size**: 15,000 complaints.
- **Methodology**: The dataset was grouped by the `Product` column. We attempted to pull an equal number of records from each product category.
- **Actual Distribution**: The raw dataset was re-processed to include the following 5 balanced categories:
    - **Credit card**: 3,000 sampled.
    - **Savings account**: 3,000 sampled.
    - **Personal loan**: 3,000 sampled.
    - **Money transfers**: 3,000 sampled.
    - **Debt collection**: 3,000 sampled.
- **Result**: A total of **15,000** distinct complaints were sampled, ensuring perfectly proportional representation across all five product categories.

## 2. Text Chunking Approach
Large narratives are often ineffective when embedded as a single vector because the "meaning" gets diluted. We used the following strategy:
- **Tool**: `RecursiveCharacterTextSplitter` from LangChain.
- **Parameters**:
    - `chunk_size`: 500 characters (~80 words).
    - `chunk_overlap`: 50 characters (~10 words).
- **Justifications**:
    - **Chunk Size**: 500 characters is large enough to contain a specific grievance (e.g., "unauthorized charge on date X") but small enough to remain semantically "pure."
    - **Overlap**: 50 characters ensures that if a critical detail (like a date or amount) is split at a boundary, it appears in both chunks, preserving contextual continuity during retrieval.

## 3. Embedding Model Choice
- **Model**: `sentence-transformers/all-MiniLM-L6-v2`.
- **Justification**:
    - **Efficiency**: It is a distilled BERT-based model that is extremely fast (quantized performance) while maintaining high accuracy for semantic similarity.
    - **Compatibility**: It produces 384-dimensional vectors, which are compact and efficient for FAISS indexing.
    - **Benchmark**: This model is widely recognized as a "sweet spot" for RAG applications involving consumer text.

## 4. Modular Architecture (Higher Standards)
To ensure maintainability and robustness, the pipeline was refactored into a modular architecture:
- **`src/config.py`**: Centralized all project constants (file paths, chunk sizes, product mappings).
- **`src/data_processing.py`**: Handles all data-centric operations including loading, text cleaning, and stratified sampling. Includes defensive checks for data integrity.
- **`src/vector_manager.py`**: A class-based manager for the vector store. It handles text chunking, embedding generation using `SentenceTransformers`, and FAISS index persistence.
- **`src/create_vector_store.py`**: A clean, high-level entry point that orchestrates the entire pipeline.

### Robustness & Error Handling
- **Input Validation**: The pipeline verifies the existence of the raw dataset before processing.
- **Logging**: Integrated the `logging` module to provide real-time status updates and trace errors.
- **Exception Guards**: Added `try-except` blocks around file I/O, model loading, and indexing operations to prevent silent failures and provide descriptive error messages.

## 5. Execution Summary
- **Loaded Data**: ~9,000,000 raw complaints (filtered for 5 target products).
- **Sampled Data**: 15,000 complaints (stratified perfectly: 3,000 per product).
- **Total Chunks Generated**: 41,781.
- **Embedding Format**: 384-dimensional dense vectors using `all-MiniLM-L6-v2`.
- **Persistence**: Index saved as `vector_store/complaints.index` and metadata as `vector_store/metadata.pkl`.
