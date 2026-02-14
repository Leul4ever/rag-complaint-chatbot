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
            
            # Create a pipeline for text2text generation
            # Note: Explicitly setting device to 'cpu' for stability as requested
            self.gen_pipeline = pipeline(
                "text2text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device="cpu",
                max_length=512,
                do_sample=True,
                temperature=0.7
            )
            
            logger.info("RAG Pipeline initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize RAG Pipeline: {e}")
            raise

    def answer(self, question: str) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Answer a user question using the RAG pipeline.
        
        Args:
            question: The user's query string.
            
        Returns:
            A tuple containing the generated answer string and a list of source metadata.
        """
        try:
            # 1. Retrieve context
            hits = self.retriever.retrieve(question, k=rag_cfg.top_k)
            
            if not hits:
                return "I don't have enough information to answer that question.", []
            
            # 2. Format context
            context_text = "\n\n".join([f"Source {i+1}:\n{hit['content']}" for i, hit in enumerate(hits)])
            sources = [hit['metadata'] for hit in hits]
            
            # 3. Format prompt using the template from config
            formatted_prompt = rag_cfg.prompt_template.format(context=context_text, question=question)
            
            # 4. Generate response
            logger.info(f"Generating response for question: {question[:50]}...")
            output = self.gen_pipeline(formatted_prompt)
            response: str = output[0]['generated_text']
            
            return response.strip(), sources
        except Exception as e:
            logger.error(f"Error generating answer for '{question}': {e}")
            return "An error occurred while processing your request.", []
