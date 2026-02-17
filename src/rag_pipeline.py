import logging
import torch
from typing import List, Dict, Any, Tuple, Optional
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from src.config import rag_cfg
from src.retriever import ComplaintRetriever

logger = logging.getLogger(__name__)

class RAGPipeline:
    """Orchestrates the Retrieval-Augmented Generation process for complaint analysis."""

    def __init__(self, model_id: str = rag_cfg.model_id):
        """
        Initialize the RAG pipeline.
        
        Args:
            model_id: The Hugging Face model ID to use for generation.
        """
        try:
            logger.info("Initializing RAG Pipeline...")
            
            # 1. Initialize Retriever
            self.retriever = ComplaintRetriever()
            
            # 2. Initialize Generator
            logger.info(f"Loading model and tokenizer: {model_id}...")
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
            
            # Using CPU for stability
            self.model.to("cpu")
            
            logger.info("RAG Pipeline initialized successfully (Direct Model Usage).")
        except Exception as e:
            logger.error(f"Failed to initialize RAG Pipeline: {e}")
            raise

    def answer(self, question: str) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Full RAG pipeline: retrieval -> prompting -> generation
        """
        try:
            # 1. Retrieve context
            results = self.retriever.retrieve(question)
            
            if not results:
                return "I don't have enough information to answer that question.", []
            
            # Extract content for the model and metadata for the UI
            context = "\n".join([r['content'] for r in results])
            sources = [r['metadata'] for r in results]
            
            # 2. Format prompt
            # T5/FLAN-T5 works best with clear instructions
            formatted_prompt = f"Answer the following consumer complaint question using the provided context. If the answer is not in the context, say you don't know.\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:"
            
            # 3. Generate response directly using the model
            logger.info(f"Generating response for question: {question[:50]}...")
            
            inputs = self.tokenizer(formatted_prompt, return_tensors="pt", truncation=True, max_length=1024).to("cpu")
            
            outputs = self.model.generate(
                inputs["input_ids"],
                max_length=512,
                do_sample=True,
                temperature=0.7,
                top_p=0.9
            )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            return response.strip(), sources
        except Exception as e:
            logger.error(f"Error generating answer for '{question}': {e}")
            return "An error occurred while processing your request.", []
