import faiss
import json
from typing import List
from pathlib import Path
from src.utils.logger import Logger
from sentence_transformers import SentenceTransformer
import numpy as np


class VectorStore:

    def __init__(
        self,
        index_path="./data/vectorstore/faiss.index",
        docstore_path="./data/vectorstore/docstore.json",
        embedding_model="sentence-transformers/all-MiniLM-L6-v2"
    ):

        self.index_path = Path(index_path)
        self.docstore_path = Path(docstore_path)
        self.embedding_model = embedding_model

        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        self.docstore_path.parent.mkdir(parents=True, exist_ok=True)

        self.logger = Logger("VECTORSTORE", "./logs/vectorstore.log").get_logger()
        self.logger.info("Initializing VectorStore...")

        self.logger.info(f"Loading embedding model: {embedding_model}")
        self.embedder = SentenceTransformer(embedding_model)

        self.index = None
        self.docstore = []

        self._load_store()


    def _load_store(self):
        if self.index_path.exists() and self.docstore_path.exists():
            self.logger.info("Loading FAISS index and docstore...")

            self.index = faiss.read_index(str(self.index_path))

            with open(self.docstore_path, "r", encoding="utf-8") as f:
                self.docstore = json.load(f)

        else:
            self.logger.info("Creating new FAISS index and docstore...")
            self.index = faiss.IndexFlatL2(384)  # 384 dims for MiniLM
            self.docstore = []


    def add_documents(self, docs: List[str]):
        self.logger.info(f"Adding {len(docs)} documents to vectorstore...")

        embeddings = self.embedder.encode(docs, convert_to_numpy=True)

        self.index.add(embeddings)
        self.docstore.extend(docs)

        self._save_store()


    def _save_store(self):
        faiss.write_index(self.index, str(self.index_path))

        with open(self.docstore_path, "w", encoding="utf-8") as f:
            json.dump(self.docstore, f, indent=4, ensure_ascii=False)

        self.logger.info("Vectorstore saved.")


    def search(self, query: str, top_k: int = 5) -> List[str]:
        self.logger.info(f"Searching for: {query}")

        query_embedding = self.embedder.encode([query], convert_to_numpy=True)

        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for idx in indices[0]:
            if idx < len(self.docstore):
                results.append(self.docstore[idx])

        self.logger.info(f"Found {len(results)} matching chunks")
        return results
