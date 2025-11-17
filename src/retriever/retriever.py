from src.vectorstore.store import VectorStore
from src.utils.logger import Logger


class Retriever:

    def __init__(self, vectorstore, top_k=5):
        self.top_k = top_k
        self.logger = Logger("RETRIEVER", "./logs/retriever.log").get_logger()

        # Use existing vectorstore (no new load!)
        self.vectorstore = vectorstore

        self.logger.info("Retriever initialized.")


    def retrieve(self, query: str):

        self.logger.info(f"Retrieving context for query: {query}")

        results = self.vectorstore.search(query, top_k=self.top_k)

        if not results:
            self.logger.warning("No relevant documents retrieved.")

        return results
