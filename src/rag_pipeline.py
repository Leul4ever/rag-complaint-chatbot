import logging
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from src.config import PROMPT_TEMPLATE, TOP_K
from src.retriever import ComplaintRetriever

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self, model_id="MBZUAI/LaMini-Flan-T5-248M"):
        """Initialize the RAG pipeline using direct transformers for stability."""
        try:
            logger.info("Initializing RAG Pipeline (Direct Inference)...")
            
            # 1. Initialize Retriever
            self.retriever = ComplaintRetriever()
            
            # 2. Initialize Generator
            logger.info(f"Loading model and tokenizer: {model_id}...")
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
            
            # Create a pipeline for text2text generation
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

    def answer(self, question):
        """Answer a user question using the RAG pipeline."""
        try:
            # 1. Retrieve context
            hits = self.retriever.retrieve(question, k=TOP_K)
            
            if not hits:
                return "I don't have enough information to answer that question.", []
            
            # 2. Format context
            context_text = "\n\n".join([f"Source {i+1}:\n{hit['content']}" for i, hit in enumerate(hits)])
            sources = [hit['metadata'] for hit in hits]
            
            # 3. Format prompt manually using the template from config
            formatted_prompt = PROMPT_TEMPLATE.format(context=context_text, question=question)
            
            # 4. Generate response
            logger.info("Generating response...")
            output = self.gen_pipeline(formatted_prompt)
            response = output[0]['generated_text']
            
            return response.strip(), sources
        except Exception as e:
            logger.error(f"Error generating answer for '{question}': {e}")
            return "An error occurred while processing your request.", []

if __name__ == "__main__":
    # Quick test
    logging.basicConfig(level=logging.INFO)
    rag = RAGPipeline()
    query = "What are the common complaints about credit card interest rates?"
    answer, sources = rag.answer(query)
    
    print(f"\nQUERY: {query}")
    print(f"\nANSWER:\n{answer}")
    print("\nSOURCES:")
    for s in sources[:2]:
        print(f"- Complaint ID: {s['complaint_id']} (Product: {s['product']})")
