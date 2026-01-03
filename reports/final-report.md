# Final Project Report: Intelligent Complaint Analysis RAG System

## 1. Executive Summary
The **Intelligent Complaint Analysis System** is a Retrieval-Augmented Generation (RAG) platform designed to help financial analysts navigate millions of consumer complaints from the CFPB database. By combining high-speed semantic search (FAISS) with specialized local LLMs (LaMini-Flan-T5), the system provides grounded, cited answers to complex consumer grievance queries through a modern web interface.

## 2. Methodology & Technical Implementation

### Phase 1: Data Preprocessing & EDA
- **Dataset**: 9.6M records from the CFPB Consumer Complaint Database.
- **Filtering**: Focused on 5 core products: *Credit Card, Debt Collection, Personal Loan, Savings Account, Money Transfers*.
- **Cleaning**: Implemented a robust text cleaning pipeline (boilerplate removal, normalization, special character filtering).
- **Outcome**: Reduced 6GB of raw data to a clean, analysis-ready format.

### Phase 2: Vector Store Development
- **Sampling**: Stratified balanced sampling of 15,000 complaints (3,000 per product) to ensure representativeness.
- **Embeddings**: Utilized `all-MiniLM-L6-v2` (384-dimensional) for efficient semantic representation.
- **Store**: Built a FAISS-CPU vector index containing ~42,000 text chunks with 50-character overlap for contextual continuity.

### Phase 3: RAG Core Logic
- **Architecture**: Modular Python-based pipeline.
- **Retriever**: Hybrid manager that performs top-K similarity searches.
- **Generator**: `MBZUAI/LaMini-Flan-T5-248M` selected for local CPU performance.
- **Prompting**: Designed a "CrediTrust Analyst" persona that strictly adheres to retrieved context and refuses to hallucinate.

### Phase 4: User Interface
- **Technology**: Streamlit.
- **Experience**: Chat-based interface with simulated streaming.
- **Trust Features**: Expandable citations for every AI response, showing direct evidence from the vector store.

## 3. Key Findings & Performance
- **Accuracy**: Qualitative evaluation shows high precision in identifying specific financial grievances (e.g., unauthorized charges, reward catch-22s).
- **Efficiency**: Modular architecture allows for fast startup and low-memory inference on standard hardware.
- **Compliance**: The strict grounding in retrieved documents ensures the system remains a reliable assistant for financial professionals.

## 4. Visual Evidence
- **Interactive Chat**: 
![Chat Interface Overview](/reports/figures/ui_screenshot_chat.png) *(Note: Placeholder for actual user screenshot)*
- **Source Citations**: 
![Citations Detail](/reports/figures/ui_screenshot_citations.png) *(Note: Placeholder for actual user screenshot)*

## 5. Conclusion & Future Roadmap
The project successfully demonstrates the utility of RAG in the financial domain. Future improvements include:
- **Scaling**: Indexing the full 9.6M dataset using a cloud-native vector store (e.g., Pinecone/Milvus).
- **Advanced RAG**: Implementing "Reranking" for improved precision.
- **Analytics**: Adding structured data dashboards alongside the chat interface.

---
**Project Delivered**: January 3, 2026
**Lead AI Assistant**
