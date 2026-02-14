import logging
import pandas as pd
from src.rag_pipeline import RAGPipeline

# Setup logging to be less verbose during eval
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

test_questions = [
    "What are common complaints about unauthorized credit card charges?",
    "What issues do consumers face with savings account interest rates?",
    "What are the main reasons for debt collection complaints mentioned?",
    "Describe problems related to money transfers and virtual currency.",
    "What do consumers complain about regarding personal loan fees?",
    "How are identity theft complaints described in the narratives?",
    "What are the recurring problems with credit card rewards programs?",
    ""
]

def run_evaluation():
    print("Initializing RAG Pipeline for Evaluation...")
    try:
        rag = RAGPipeline()
    except Exception as e:
        print(f"Error initializing RAG: {e}")
        return

    results = []
    print(f"\nRunning evaluation on {len(test_questions)} questions...\n")
    
    for i, q in enumerate(test_questions):
        print(f"[{i+1}/{len(test_questions)}] Processing: {q}")
        answer, sources = rag.answer(q)
        
        # Capture top 2 sources for the table
        source_details = []
        for s in sources[:2]:
            snippet = s['original_text'][:100].replace('\n', ' ') + "..."
            source_details.append(f"ID: {s['complaint_id']} | {snippet}")
        
        results.append({
            "Question": q,
            "Generated Answer": answer,
            "Retrieved Sources": "\n".join(source_details),
            "Quality Score (1-5)": "",  # To be filled manually
            "Comments/Analysis": ""      # To be filled manually
        })

    # Save to a JSON for clean reading
    import json
    with open("reports/eval_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
    
    print("\n" + "="*50)
    print("EVALUATION RESULTS SAVED TO reports/eval_results.json")
    print("="*50)

if __name__ == "__main__":
    run_evaluation()
