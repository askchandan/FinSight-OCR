import json
from pathlib import Path
from src.vectorstore.store import VectorStore
from src.utils.logger import Logger


class JSONIngestor:

    def __init__(self, input_dir="./data/output"):
        self.input_dir = Path(input_dir)
        self.logger = Logger("JSON_INGESTOR", "./logs/ingest.log").get_logger()

    def load_json_files(self):
        json_files = list(self.input_dir.glob("*.json"))

        if not json_files:
            self.logger.warning("No JSON files found.")
            return []

        documents = []

        for file in json_files:
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Convert JSON to a flattened text chunk
                text_chunk = self.json_to_text(data)

                documents.append(text_chunk)

                self.logger.info(f"Loaded: {file.name}")

            except Exception as e:
                self.logger.error(f"Failed to read {file}: {e}")

        return documents

    def json_to_text(self, data: dict) -> str:
        """
        Convert parsed bank statements into clean text.
        This text will be embedded and stored in FAISS.
        """

        lines = []

        for key, value in data.items():
            lines.append(f"{key.replace('_', ' ')}: {value}")

        return "\n".join(lines)
