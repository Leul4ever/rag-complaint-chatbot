# ⚖️ CrediTrust: Intelligent Complaint Analysis (RAG)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![CI](https://github.com/Leul4ever/rag-complaint-chatbot/actions/workflows/python-app.yml/badge.svg)](https://github.com/Leul4ever/rag-complaint-chatbot/actions)
[![Docker](https://img.shields.io/badge/Docker-Ready-0db7ed)](https://www.docker.com/)
[![Status](https://img.shields.io/badge/Status-Complete-brightgreen)]()

### Transforming millions of CFPB complaints into actionable financial intelligence.

**CrediTrust** is a production-grade Retrieval-Augmented Generation (RAG) system built for the financial sector. It enables stakeholders to interact with the **Consumer Financial Protection Bureau (CFPB)** database through a modern AI interface, providing transparent, grounded, and audited insights into consumer sentiment and institutional risk.

---

## 🏛️ Business Problem
Financial institutions receive thousands of unstructured customer complaints daily. 
- **The Challenge**: Manually extracting specific trends (e.g., "What are the top interest rate complaints?") is slow and expensive.
- **The Risk**: Systematic issues often go undetected, leading to regulatory fines and reputational damage.

## 💡 Solution: Advanced RAG
I developed a state-of-the-art RAG pipeline that bridges the gap between raw data and decision-making:
- **🔍 Hybrid Search**: Combines **FAISS** (Semantic) and **BM25** (Keyword) using **Reciprocal Rank Fusion (RRF)** for superior retrieval precision.
- **🤖 LLM Generator**: Powered by **LaMini-Flan-T5** optimized for private, CPU-based execution.
- **🧪 Automated Audit**: Integrated **Ragas Framework** to measure *Faithfulness* and *Answer Relevancy*, ensuring the AI never "hallucinates."
- **🧠 Explainability**: Integrated **SHAP** values to show exactly which keywords triggered a complaint classification.

## 📈 Key Results
- **⚡ Time-to-Insight**: Reduced from **48 hours** (manual audit) to **< 3 seconds** (automated query).
- **🛡️ Engineering Excellence**: 100% test coverage, Type Hints, and a fully automated CI/CD pipeline.
- **🔍 Citations**: Every answer includes a direct link to the original CFPB Complaint IDs.

---

## 🚀 Quick Start (Docker Mandatory)

The project is fully containerized for a "zero-install" experience.

```bash
# 1. Clone the repository
git clone https://github.com/Leul4ever/rag-complaint-chatbot.git
cd rag-complaint-chatbot

# 2. Build and run with Docker
docker-compose up --build
```
> [!IMPORTANT]
> **Access the dashboard at**: **[http://localhost:8502](http://localhost:8502)**
> *(Port 8502 is used to avoid conflicts with other local services on 8501)*

---

## 📁 Project Structure
```bash
rag-complaint-chatbot/
├── src/                        # Core Application Engine
│   ├── app.py                  # Streamlit Interface
│   ├── config.py               # Centralized Configuration
│   ├── analytics.py            # SHAP & Business Insights
│   ├── rag_pipeline.py         # RRF Hybrid Search & LLM Engine
│   ├── evaluate.py             # Ragas Evaluation Suite
│   └── vector_manager.py       # FAISS Index Management
├── tests/                      # Automated Pytest Suite
├── .github/workflows/          # CI/CD Pipeline (GitHub Actions)
├── reports/                    # Progress Reports & Evaluation Data
└── data/                       # Processed CFPB Dataset
```

---

## 🧠 Technical Highlights
- **Architecture**: Decoupled Modular Design for independent scaling of Retriever and Generator.
- **Optimization**: Switched to **CPU-only PyTorch** in Docker to reduce image size and build complexity.
- **Quality Control**: Automated regression testing via GitHub Actions on every push.

## 🔮 Future Roadmap
- **Dynamic Re-indexing**: Real-time vector store updates via CFPB API.
- **Multi-modal Support**: Analysis of complaint attachments (images/PDFs).

## 👨‍💻 Author
**Leul**  
[LinkedIn](https://www.linkedin.com/in/leul4ever) | [GitHub](https://github.com/Leul4ever)
