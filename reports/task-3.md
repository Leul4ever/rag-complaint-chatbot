# Task 3 Report: RAG Core Logic and Evaluation

## 1. RAG Pipeline Implementation

The RAG (Retrieval-Augmented Generation) pipeline for the Intelligent Complaint Analysis system was implemented with a focus on modularity, robustness, and local execution efficiency.

### System Components
1.  **Retriever (`src/retriever.py`)**:
    - Loads the pre-built FAISS index from `vector_store/`.
    - Utilizes `VectorManager` to embed user queries using the `all-MiniLM-L6-v2` model.
    - Performs a similarity search to fetch the top **k=5** most relevant chunks.
2.  **Generator (`src/rag_pipeline.py`)**:
    - Integrates a generative LLM (**MBZUAI/LaMini-Flan-T5-248M**) selected for its high quality-to-size ratio and CPU compatibility.
    - Implemented a direct `transformers` pipeline to ensure stability across environments.
3.  **Prompt Engineering**:
    - A specialized prompt template was designed to enforce groundedness:
    ```
    You are a financial analyst assistant for CrediTrust... 
    Use the following retrieved complaint excerpts... 
    If the context doesn't contain the answer, state that you don't have enough information.
    ```

---

## 2. Qualitative Evaluation Results

The system was evaluated against 8 representative questions. The following table summarizes the performance based on the specific criteria requested.

| Question | Generated Answer | Retrieved Sources (show 1-2) | Quality Score (1-5) | Comments/Analysis |
|----------|------------------|-----------------------------|---------------------|-------------------|
| Common complaints about unauthorized credit card charges? | Complaints include lost/stolen card, fraud cases, and specific charges. | ID: 3647591, ID: 3788614 | 5 | Accurate and grounded in specific examples found in the context. |
| Issues with savings account interest rates? | Consumers are misled by interest rates that are often misleading. | ID: 3130047, ID: 2778366 | 4 | Correctly identified the sentiment of being "misled" by rates. |
| Main reasons for debt collection complaints? | Main reasons are not specified in the provided context. | ID: 2373120, ID: 9249146 | 4 | "Safe" response. The model correctly identified that the context lacked specific "reasons" beyond general collection issues. |
| Problems with money transfers and virtual currency? | Connection not specific; focused on Venmo/MoneyGram. | ID: 3686114, ID: 7439825 | 3 | The model was overly cautious but retrieval was highly relevant to the apps mentioned. |
| Complaints about personal loan fees? | Lack of transparency, inaccurate reporting, and predatorial loans. | ID: 8005089, ID: 8416836 | 5 | High quality extraction of specific grievance keywords. |
| Identity theft complaints described? | Described as fraudulent, inaccurate, and false information on accounts. | ID: 12736502, ID: 7062068 | 5 | Very precise summary of the descriptive language used by victims. |
| Recurring problems with credit card rewards? | Program not as advertised; requires new charges or forfeiture of dollars. | ID: 3454618, ID: 5883376 | 5 | Excellent detail level regarding the "catch-22" mechanics of rewards. |
| Issues with bank account service fees? | Unreliable customer service, lack of transparency, difficulty canceling fees. | ID: 10604200, ID: 6476450 | 4 | Accurately captured the frustration with support and fee policies. |

---

## 3. Analysis & Key Takeaways

### What Worked Well
- **Context Grounding**: The model followed instructions well, frequently refusing to answer if the context was too thin, which is ideal for compliance-heavy environments. 
- **Domain Accuracy**: The retrieval system (FAISS + MiniLM) proved highly effective at finding specific financial grievances.
- **Inference Speed**: Local execution on CPU was fast enough for non-interactive analysis.

### Areas for Improvement
- **Model Reasoning**: A larger model might provide more descriptive summaries for complex/broad queries.
- **Prompt Sensitivity**: The model's "refusal" threshold is quite high. Tuning temperature could improve descriptive depth.

## 4. Conclusion
Task 3 is successfully completed. We have a working RAG core logic that retrieves relevant complaints and generates grounded, cited answers. This core logic serves as the backend for the Task 4 UI.
