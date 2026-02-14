# Task 1: Project Selection & Gap Analysis

## Project Selection Justification
I have selected the **Intelligent Complaint Analysis (RAG Chatbot)** project for my capstone improvement. 

**Justification:**
Financial institutions process millions of customer complaints, and the ability to extract reliable, transparent, and actionable insights accurately is high-value. This project demonstrates advanced skills in **Generative AI (RAG)**, **Vector Databases**, and **Data Engineering**. While the current implementation is a functional prototype, it lacks the production-grade robustness—specifically in testing, CI/CD, and modular design—that the finance sector demands. Enhancing this project will showcase my ability to build reliable, maintainable, and low-risk AI solutions.

## Gap Analysis Checklist

| Category | Question | Status |
| :--- | :--- | :--- |
| **Code Quality** | Is the code modular and well-organized? | **Partial** |
| | Are there type hints on functions? | **Partial** |
| | Is there a clear project structure? | **Yes** |
| **Testing** | Are there unit tests for core functions? | **No** |
| | Do tests run automatically on push? | **No** |
| **Documentation** | Is the README comprehensive? | **Yes** |
| | Are there docstrings on functions? | **Partial** |
| **Reproducibility** | Can someone else run this project? | **Yes** |
| | Are dependencies in requirements.txt? | **Yes** |
| **Visualization** | Is there an interactive way to explore results? | **Yes** |
| **Business Impact** | Is the problem clearly articulated? | **Yes** |
| | Are success metrics defined? | **Partial** |

## Improvement Plan (Prioritized)

| Priority | Improvement | Description | Est. Time |
| :--- | :--- | :--- | :--- |
| 1 | **Code Refactoring** | Add comprehensive type hints, implement `dataclasses` for config, and increase modularity. | 4 Hours |
| 2 | **Automated Testing** | Write at least 5 unit/integration tests using `pytest` to ensure logic reliability. | 6 Hours |
| 3 | **CI/CD Pipeline** | Configure GitHub Actions for automated testing and linting on every push. | 3 Hours |
| 4 | **Model Explainability** | Integrate SHAP/LIME visualizations to explain why specific documents were retrieved. | 5 Hours |
| 5 | **Impact Dashboard** | Enhance the Streamlit UI with a "Business Insights" tab to track complaint trends. | 4 Hours |

**Total Estimated Time:** 22 Hours
