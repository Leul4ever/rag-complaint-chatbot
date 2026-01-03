# Intelligent Complaint Analysis for Financial Services - RAG Chatbot

> [!NOTE]
> This project is currently in the **RAG Implementation** phase (Task 3).

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-In%20Development-yellow)]()
[![Task 2](https://img.shields.io/badge/Task%202-Complete-green)]()

## 📋 Project Overview

This project develops an intelligent **Retrieval-Augmented Generation (RAG) chatbot** for analyzing consumer complaints from the **Consumer Financial Protection Bureau (CFPB)** database. The chatbot enables users to query complaint data using natural language and receive contextually relevant responses powered by semantic search and large language models.

### Business Objective

Enable financial institutions and consumer advocates to:
- 🔍 Quickly search and retrieve relevant complaint information
- 📊 Understand complaint patterns and trends
- 💡 Generate insights from large-scale complaint data
- 🤖 Interact with complaint data through natural language queries

## 🎯 Key Features

- **Semantic Search**: Find relevant complaints using natural language queries
- **RAG Pipeline**: Combine retrieval with generative AI for comprehensive answers
- **Product-Specific Analysis**: Focus on Credit Cards, Personal Loans, Savings Accounts, and Money Transfers
- **Scalable Architecture**: Process millions of complaints efficiently
- **Clean Data Pipeline**: Automated preprocessing and text cleaning

## 📁 Project Structure

```
rag-complaint-chatbot/
│
├── data/                           # Data directory
│   ├── raw/                        # Raw CFPB complaint data
│   │   └── complaints.csv          # Original dataset (~6 GB)
│   └── processed/                  # Processed and cleaned data
│       └── complaints_processed.parquet  # Filtered & cleaned data (97 MB)
│
├── notebooks/                      # Jupyter notebooks for analysis
│   ├── Task_1_EDA_and_Preprocessing.ipynb  # ✅ EDA & preprocessing
│   └── README.md                   # Notebook documentation
│
├── reports/                        # Project reports and documentation
│   ├── task-1.md                   # Task 1 comprehensive report
│   └── figures/                    # EDA visualizations
│       ├── product_distribution.png
│       └── narrative_length_distribution.png
│
├── src/                            # Source code modules
│   └── __init__.py
│
├── tests/                          # Unit tests
│   └── __init__.py
│
├── vector_store/                   # Vector database storage
│
├── app.py                          # Main application entry point
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── .gitignore                      # Git ignore rules
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager
- 8GB+ RAM (for processing large datasets)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/rag-complaint-chatbot.git
cd rag-complaint-chatbot
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download the CFPB dataset**
- Download from: [CFPB Consumer Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/)
- Place `complaints.csv` in `data/raw/` directory

## 📊 Task 1: EDA and Data Preprocessing ✅

### Overview

Task 1 focused on understanding and preparing the CFPB complaint dataset for the RAG pipeline.

### Key Statistics

| Metric | Value |
|--------|-------|
| **Total Complaints** | 9,609,797 |
| **Complaints with Narratives** | 2,980,756 (31%) |
| **Complaints without Narratives** | 6,629,041 (69%) |
| **Average Narrative Length** | 176 words |
| **Median Narrative Length** | 114 words |
| **Data Compression** | 6 GB → 97 MB (98% reduction) |

### Data Processing Pipeline

1. **Data Loading**: Loaded 9.6M complaints from CSV
2. **Exploratory Analysis**:
   - Product distribution analysis
   - Narrative length statistics
   - Missing data assessment
3. **Filtering**:
   - Selected 4 product categories: Credit Card, Personal Loan, Savings Account, Money Transfers
   - Removed complaints without narratives
4. **Text Cleaning**:
   - Lowercased all text
   - Removed boilerplate phrases
   - Cleaned special characters
   - Normalized whitespace
5. **Data Storage**: Saved as Parquet format for efficient storage and retrieval

### Key Findings

- **69% of complaints lack detailed narratives**, requiring focus on the 31% with text
- **Narrative lengths vary significantly** (1 to 6,469 words), with most being concise
- **Product distribution is uneven**, with credit reporting dominating
- **Text cleaning reduced noise** while preserving semantic meaning

### Deliverables

- ✅ Jupyter Notebook: `notebooks/Task_1_EDA_and_Preprocessing.ipynb`
- ✅ Processed Data: `data/processed/complaints_processed.parquet`
- ✅ Comprehensive Report: `reports/task-1.md`
- ✅ Visualizations: `reports/figures/`

**📖 For detailed findings, see:** [`reports/task-1.md`](reports/task-1.md)

## 🛠️ Technology Stack

### Core Libraries

| Category | Technologies |
|----------|-------------|
| **Data Processing** | pandas, pyarrow |
| **Visualization** | matplotlib, seaborn |
| **Text Processing** | re (regex) |
| **Vector Store** | *(To be implemented in Task 2)* |
| **LLM Integration** | *(To be implemented in Task 3)* |
| **Web Framework** | *(To be implemented in Task 4)* |

### Dependencies

See [`requirements.txt`](requirements.txt) for the complete list of dependencies.

## 📈 Project Roadmap

### ✅ Task 1: EDA and Data Preprocessing (Complete)
- [x] Load and explore CFPB dataset
- [x] Analyze data quality and distributions
- [x] Filter and clean complaint narratives
- [x] Save processed data in Parquet format
- [x] Generate EDA visualizations
- [x] Document findings in comprehensive report

### ✅ Task 2: Vector Store Setup (Complete)
- [x] Generate embeddings for complaint narratives
- [x] Set up vector database (FAISS)
- [x] Index processed complaints
- [x] Implement similarity search
- [x] Document methodology in [Task 2 Report](reports/task-2.md)

### 📋 Task 3: RAG Pipeline Development (Planned)
- [ ] Design RAG architecture
- [ ] Integrate with LLM (OpenAI/Anthropic/Open-source)
- [ ] Implement query processing
- [ ] Build response generation
- [ ] Add context management

### 🌐 Task 4: Web Interface (Planned)
- [ ] Design user interface
- [ ] Build FastAPI/Flask backend
- [ ] Create frontend (Streamlit/Gradio)
- [ ] Implement chat interface
- [ ] Add query history

### 🧪 Task 5: Testing & Optimization (Planned)
- [ ] Unit tests
- [ ] Integration tests
- [ ] Performance optimization
- [ ] Response quality evaluation
- [ ] User acceptance testing

## 💻 Usage

### Running the EDA Notebook

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Launch Jupyter
jupyter notebook notebooks/Task_1_EDA_and_Preprocessing.ipynb
```

### Running the Application (Coming Soon)

```bash
python app.py
```

## 📝 Data Source

**Dataset**: CFPB Consumer Complaint Database  
**Source**: [Consumer Financial Protection Bureau](https://www.consumerfinance.gov/data-research/consumer-complaints/)  
**License**: Public Domain  
**Update Frequency**: Weekly

### Dataset Description

The Consumer Complaint Database is a collection of complaints about consumer financial products and services sent to companies for response. The database includes:
- Complaint narratives (when consumers opt to share)
- Product and issue information
- Company responses
- Geographic data
- Temporal data

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Your Name** - *Initial work*

## 🙏 Acknowledgments

- Consumer Financial Protection Bureau for providing the complaint database
- Open-source community for excellent tools and libraries
- [Add any other acknowledgments]

## 📧 Contact

For questions or feedback, please contact:
- Email: your.email@example.com
- GitHub: [@yourusername](https://github.com/yourusername)

---

**Last Updated**: January 3, 2026  
**Project Status**: Task 1 & 2 Complete ✅ | Task 3 Planned �
