"""
run_all.py
Orchestrates the full pipeline:
1) OCR → JSON output
2) JSON → Documents (ingest)
3) Documents → VectorStore (FAISS)
4) Query → RAG pipeline
"""

import os
from pathlib import Path

from src.ingestion.preprocess.ocr import BankStatementOCR
from src.vectorstore.ingest import JSONIngestor
from src.vectorstore.store import VectorStore
from src.retriever.retriever import Retriever
from src.pipeline.rag_pipeline import RAGPipeline
from src.utils.logger import Logger


PROJECT_ROOT = Path(__file__).parent.resolve()
DATA_OUTPUT = PROJECT_ROOT / "data" / "output"

logger = Logger("RUN_ALL", "./logs/run_all.log").get_logger()
logger.info(f"Project root: {PROJECT_ROOT}")


# -------------------------------------------------
# STEP 1: Run OCR on images
# -------------------------------------------------
def step_1_process_images(input_dir="./data/extracted/images", output_dir="./data/output", model=None):
    """
    Run OCR ONLY if output JSON files do NOT already exist.
    Otherwise skip LLM OCR to save time and compute.
    """
    logger.info("STEP 1: Checking for existing JSON output files...")

    output_dir = Path(output_dir)
    json_files = list(output_dir.glob("*.json"))

    if json_files:
        logger.info(f"Skipped OCR: Found {len(json_files)} existing JSON files in {output_dir}")
        return []  # Return empty because OCR was skipped

    # No JSON files found → run OCR
    logger.info("No JSON files found. Running OCR with LLM...")
    parser = BankStatementOCR(input_dir=input_dir, output_dir=output_dir, model=model)
    results = parser.process_all_images()
    logger.info(f"OCR completed. Parsed {len(results)} files.")
    return results



# -------------------------------------------------
# STEP 2: Load JSON files → convert to text docs
# -------------------------------------------------
def step_2_ingest_json(output_dir="./data/output"):
    logger.info("STEP 2: Ingesting JSON files...")
    ingestor = JSONIngestor(input_dir=output_dir)
    docs = ingestor.load_json_files()
    logger.info(f"Ingested {len(docs)} documents.")
    return docs


# -------------------------------------------------
# STEP 3: Build VectorStore (FAISS)
# -------------------------------------------------
def step_3_build_vectorstore(docs, index_path="./data/vectorstore/faiss.index",
                             docstore_path="./data/vectorstore/docstore.json",
                             embedding_model="sentence-transformers/all-MiniLM-L6-v2"):

    logger.info("STEP 3: Building/Updating VectorStore...")

    # 🔥 Only ONE VectorStore instance is created here
    vectorstore = VectorStore(
        index_path=index_path,
        docstore_path=docstore_path,
        embedding_model=embedding_model
    )

    if docs:
        vectorstore.add_documents(docs)
        logger.info("Vectorstore updated.")
    else:
        logger.info("No documents found to add.")

    return vectorstore


# -------------------------------------------------
# STEP 4: Start RAG interactive Q&A
# -------------------------------------------------
def step_4_start_rag_interactive(vectorstore, model_name=None, top_k=5):

    logger.info("STEP 4: Initializing Retriever + RAG Pipeline...")

    # 🔥 Retriever uses existing VectorStore (no reload!)
    retriever = Retriever(vectorstore=vectorstore, top_k=top_k)

    # 🔥 RAGPipeline receives SAME retriever (no new VectorStore)
    rag = RAGPipeline(retriever=retriever, model_name=model_name, top_k=top_k)

    print("\nRAG console ready. Type 'exit' or 'quit' to stop.\n")

    while True:
        query = input("Question: ").strip()
        if query.lower() in ("exit", "quit"):
            print("Exiting RAG console...")
            break

        response = rag.query(query)
        print("\nANSWER:\n", response)
        print("-" * 40)


# -------------------------------------------------
# MAIN ORCHESTRATION
# -------------------------------------------------
def main():
    model_name = os.getenv("MODEL_NAME")

    if not model_name:
        logger.warning("MODEL_NAME not found in .env")
    else:
        logger.info(f"Using model: {model_name}")

    # 1) OCR: images → JSON
    step_1_process_images(model=model_name)

    # 2) JSON → text docs
    docs = step_2_ingest_json()

    # 3) Build vectorstore
    vectorstore = step_3_build_vectorstore(
        docs,
        embedding_model="sentence-transformers/all-MiniLM-L6-v2"
    )

    # 4) Start RAG console using the SAME vectorstore
    step_4_start_rag_interactive(
        vectorstore=vectorstore,
        model_name=model_name,
        top_k=5
    )


if __name__ == "__main__":
    main()
