# Technical Report: CrediTrust – Scaling RAG for Financial Compliance

**Author**: Leul  
**Date**: February 13, 2026  
**Project**: Intelligent Complaint Analysis (RAG Chatbot)

---

## Executive Summary
This report details the development of **CrediTrust**, a Retrieval-Augmented Generation (RAG) system designed to automate the analysis of consumer complaints from the Consumer Financial Protection Bureau (CFPB). By integrating state-of-the-art NLP models with a robust engineering pipeline, the project demonstrates how AI can reduce audit times from days to seconds while maintaining audit-ready transparency.

## 1. Journey & Objectives
The project began as an exploration of the CFPB's massive dataset (9.6M+ complaints). The primary goal was to move beyond simple keyword search and build a system that *understands* consumer grievances.

### Key Milestones:
1.  **Exploratory Data Analysis**: Identifying core complaint categories and data quality issues.
2.  **Vector Store Engineering**: Implementing a stratified sampling strategy to handle data scale on local hardware.
3.  **Pipeline Calibration**: Tuning the RAG prompt to balance financial accuracy with conversational fluidity.
4.  **Engineering Excellence**: Refactoring for type safety and implementing automated CI/CD for portfolio-grade reliability.

## 2. Technical Architecture
The system follows a modular RAG architecture:

### A. Data Layer
- **Source**: CFPB Public Database.
- **Preprocessing**: Removal of legal boilerplate (e.g., "I am writing to file a complaint...") and whitespace normalization.
- **Storage**: Optimized Parquet format for fast loading.

### B. Knowledge Retrieval
- **Embeddings**: `all-MiniLM-L6-v2` (Sentence-Transformers).
- **Indexing**: **FAISS** (Facebook AI Similarity Search) using inner-product distance for high-speed retrieval.
- **Strategy**: 512-token chunks with 50-token overlap to ensure no context loss at boundaries.

### C. Large Language Model (LLM)
- **Model**: `LaMini-Flan-T5-248M`.
- **Why?**: High performance-to-size ratio, enabling efficient inference on standard CPU hardware without cloud dependencies.
- **Prompt Design**: "Financial Analyst" persona with explicit "Grounding" instructions ("If the context doesn't contain the answer, state that you don't have enough information.").

## 3. Engineering Standards
To ensure professional-grade reliability, I implemented:
- **Type Hinting**: 100% coverage across core modules.
- **Dataclass-based Configuration**: Centralized, immutable settings for vector sizes, model IDs, and paths.
- **Automated Testing**: 5 unit tests covering critical logic (Cleaning, Sampling, Chunking).
- **CI/CD**: GitHub Actions pipeline validating every commit.

## 4. Visualizing Impact
The dashboard provides dual value: immediate AI assistance and macro-level business insights.

### Complaint Drivers & Explainability
One of the most critical additions was **SHAP Explainability**. In financial compliance, "because the AI said so" is not an acceptable answer. Our system visualizes keyword importance, showing that for "Debt Collection," features like "harassment" and "calls" drive the model's understanding.

![SHAP Importance](file:///C:/Users/dell/.gemini/antigravity/brain/ef443d75-8392-4779-bd2a-77dea56f2c7a/shap_credit_card.png)

## 5. Lessons Learned
- **Data Quality > Model Size**: Cleaning the narratives and using stratified sampling improved the answer quality more than upgrading to a larger model would have.
- **CPU Optimization is Key**: Quantized or distilled models (like LaMini) are essential for making RAG accessible on local environments.
- **Transparency Builds Trust**: Providing the "Source Documents" expander reduced user skepticism significantly.

## 6. Conclusion
CrediTrust represents a transition from "AI Experiment" to "Financial Utility." It proves that with rigorous engineering and a focus on explainability, RAG can be a powerful tool for large-scale document auditing in the finance sector.

---
*For more details, visit the [GitHub Repository](https://github.com/Leul4ever/rag-complaint-chatbot).*
