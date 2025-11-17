from src.retriever.retriever import Retriever
from src.llm.model import LLMModel
from src.llm.prompt_template import FIN_DOMAIN_PROMPT
from src.utils.logger import Logger


class RAGPipeline:

    def __init__(self, retriever, model_name="qwen3:0.6b", top_k=5):
        self.logger = Logger("RAG_PIPELINE", "./logs/rag_pipeline.log").get_logger()

        self.retriever = retriever
        self.llm = LLMModel(model_name)
        self.top_k = top_k


    def query(self, user_query: str):

        self.logger.info(f"User Query: {user_query}")
        context_chunks = self.retriever.retrieve(user_query)

        if not context_chunks:
            self.logger.warning("No context found! Returning fallback response.")
            return "No relevant information found in your knowledge base."

        
        context_text = "\n".join(context_chunks)
        rag_prompt = FIN_DOMAIN_PROMPT.format(
            context=context_text,
            query=user_query
        )

        self.logger.debug(f"RAG Prompt Sent to LLM:\n{rag_prompt[:500]}...")

        answer = self.llm.generate(prompt=rag_prompt)
        self.logger.info("RAG Response generated.")
        
        return answer
