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

## 4. Vector Store Implementation
- **Library**: FAISS (Facebook AI Similarity Search).
- **Metadata Management**:
    - Crucially, we do not just store the vector. We maintain a separate `metadata.pkl` mapping that links each vector index to:
        - `Complaint ID`: To trace back to the original database record.
        - `Product`: For category-specific filtering if needed later.
        - `Original Text`: To provide the LLM with the raw context for generation.

## 5. Execution Summary
- **Loaded Data**: ~9,000,000 raw complaints (filtered for 5 target products).
- **Sampled Data**: 15,000 complaints (stratified perfectly: 3,000 per product).
- **Total Chunks Generated**: 41,781.
- **Embedding Format**: 384-dimensional dense vectors.
- **Persistence**: Refreshed index saved as `vector_store/complaints.index` and metadata as `vector_store/metadata.pkl`.
