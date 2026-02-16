import os
import sys
import json
import logging
import pandas as pd
from datasets import Dataset

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from src.rag_pipeline import RAGPipeline
from src.config import paths

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_evaluation():
    """Run Ragas evaluation on the golden dataset."""
    try:
        # 1. Initialize RAG Pipeline
        rag = RAGPipeline()
        
        # 2. Define Golden Dataset (Questions & Ground Truths)
        # In a real scenario, we'd use ground truth answers too.
        eval_questions = [
            "What are common complaints about unauthorized credit card charges?",
            "What issues do consumers face with savings account interest rates?",
            "What are the main reasons for debt collection complaints mentioned?",
            "Describe problems related to money transfers and virtual currency.",
            "What do consumers complain about regarding personal loan fees?",
            "How are identity theft complaints described in the narratives?",
            "What are the recurring problems with credit card rewards programs?",
            "What issues do people have with bank account service fees?"
        ]
        
        results_data = []
        
        logger.info(f"Starting evaluation for {len(eval_questions)} questions...")
        
        for query in eval_questions:
            answer, sources = rag.answer(query)
            contexts = [s.get('original_text', '') for s in sources]
            
            results_data.append({
                "question": query,
                "answer": answer,
                "contexts": contexts,
                # For Ragas metrics that require ground_truth, we'd need them here.
                # Since we don't have them yet, we focus on Faithfulness and Relevancy.
                "ground_truth": "" 
            })
            
        # 3. Prepare dataset for Ragas
        df = pd.DataFrame(results_data)
        dataset = Dataset.from_pandas(df)
        
        # 4. Perform Evaluation
        # Note: Ragas typically requires an OpenAI API key or a custom LLM wrapper.
        # If no key is present, this may fail or need a local LLM setup.
        logger.info("Running Ragas evaluation metrics...")
        
        # We wrap this in a try-except to handle cases where Ragas requires an API key
        try:
            result = evaluate(
                dataset,
                metrics=[faithfulness, answer_relevancy]
            )
            
            summary = result.to_pandas()
            output_path = os.path.join(paths.reports_dir, "ragas_metrics.json")
            summary.to_json(output_path, orient="records", indent=4)
            logger.info(f"Evaluation complete. Results saved to {output_path}")
            
            print("\n--- Evaluation Summary ---")
            print(summary[['question', 'faithfulness', 'answer_relevancy']])
            
        except Exception as e:
            logger.warning(f"Ragas evaluation failed (likely due to missing LLM for scoring): {e}")
            logger.info("Falling back to saving raw generation results for manual review.")
            
            raw_output_path = os.path.join(paths.reports_dir, "eval_generation_raw.json")
            with open(raw_output_path, "w") as f:
                json.dump(results_data, f, indent=4)
            logger.info(f"Raw generation data saved to {raw_output_path}")

    except Exception as e:
        logger.error(f"Evaluation script failed: {e}")

if __name__ == "__main__":
    run_evaluation()
