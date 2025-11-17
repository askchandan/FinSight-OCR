# FinSight-OCR

![Python](https://img.shields.io/badge/-Python-blue?logo=python&logoColor=white) ![License](https://img.shields.io/badge/license-GPL-green)

## 📝 Description

FinSight-OCR is your intelligent assistant for understanding your bank statements. This Python-based tool leverages advanced OCR technology to extract transaction data from your statements. More than just data extraction, FinSight-OCR uses LLMs to analyze your spending patterns, providing insightful summaries and answering your financial queries in a conversational manner. Test its capabilities and gain control of your financial data today.

## ✨ Features

- 🧪 Testing


## 🛠️ Tech Stack

- 🐍 Python


## 📦 Key Dependencies

```
requests: latest
kaggle: latest
python-dotenv: latest
ollama: latest
chromadb: latest
langchain-huggingface: latest
faiss-cpu: latest
sentence-transformers: latest
```

## 📁 Project Structure

```
.
├── LICENSE
├── configs
│   ├── model_config.yaml
│   └── vectorstore.yaml
├── requirements.txt
├── run.py
├── sentece-transformers
│   └── all-MiniLM-L6-v2
│       ├── 1_Pooling
│       │   └── config.json
│       ├── config.json
│       ├── config_sentence_transformers.json
│       ├── model.safetensors
│       ├── modules.json
│       ├── sentence_bert_config.json
│       ├── special_tokens_map.json
│       ├── tokenizer.json
│       ├── tokenizer_config.json
│       └── vocab.txt
├── src
│   ├── __init__.py
│   ├── ingestion
│   │   ├── __init__.py
│   │   ├── loaders
│   │   │   ├── __init__.py
│   │   │   └── image_loader.py
│   │   └── preprocess
│   │       ├── __init__.py
│   │       └── ocr.py
│   ├── llm
│   │   ├── __init__.py
│   │   ├── model.py
│   │   └── prompt_template.py
│   ├── pipeline
│   │   ├── __init__.py
│   │   └── rag_pipeline.py
│   ├── retriever
│   │   ├── __init__.py
│   │   └── retriever.py
│   ├── utils
│   │   ├── __init__.py
│   │   └── logger.py
│   └── vectorstore
│       ├── __init__.py
│       ├── ingest.py
│       └── store.py
└── tests
    ├── __init__.py
    ├── test_ocr.py
    └── test_rag.py
```

## 🛠️ Development Setup

### Python Setup
1. Install Python (v3.8+ recommended)
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`


## 👥 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/askchandan/FinSight-OCR.git`
3. **Create** a new branch: `git checkout -b feature/your-feature`
4. **Commit** your changes: `git commit -am 'Add some feature'`
5. **Push** to your branch: `git push origin feature/your-feature`
6. **Open** a pull request

Please ensure your code follows the project's style guidelines and includes tests where applicable.

## 📜 License

This project is licensed under the GPL License.

---
*This README was generated with ❤️ by ReadmeBuddy*
