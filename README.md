# 🤖 Discord RAG Bot - AI Bootcamp Project

A production-ready Discord bot using Retrieval-Augmented Generation (RAG) to answer questions about the AI Bootcamp documentation.

## 🎯 Project Overview

**Role:** Data Scientist  
**Tech Stack:** 100% Local & Free (No Credit Cards!)

- **Vector DB:** ChromaDB (local, in-memory)
- **Embeddings:** SentenceTransformers (all-MiniLM-L6-v2)
- **LLM:** Ollama (llama3.2:3b - runs locally)
- **Bot Framework:** Discord.py
- **Package Manager:** uv (fast Python package installer)

## 📁 Project Structure

```
discord-rag-bot/
├── src/
│   └── discord_rag_bot/
│       ├── __init__.py
│       ├── bot.py                    # 🤖 Discord bot entry point
│       │
│       ├── core/                     # 🧠 Core RAG logic
│       │   ├── __init__.py
│       │   ├── rag_engine.py         # Main RAG orchestrator
│       │   └── knowledge_base.py     # KB management (user KBs)
│       │
│       ├── processing/               # 📄 Document processing
│       │   ├── __init__.py
│       │   ├── converters.py         # PDF/DOCX/TXT → text
│       │   ├── chunkers.py           # Smart text chunking
│       │   └── validators.py         # File validation
│       │
│       ├── embeddings/               # 🔢 Vector embeddings
│       │   ├── __init__.py
│       │   └── embedding_service.py  # Embedding generation
│       │
│       ├── retrieval/                # 🔍 Search & retrieval
│       │   ├── __init__.py
│       │   └── retriever.py          # Vector search logic
│       │
│       ├── generation/               # 💬 Answer generation
│       │   ├── __init__.py
│       │   └── generator.py          # LLM integration (Ollama)
│       │
│       ├── storage/                  # 💾 Data persistence
│       │   ├── __init__.py
│       │   ├── vector_store.py       # ChromaDB manager
│       │   └── memory_store.py       # MongoDB for chat history
│       │
│       ├── commands/                 # 🎮 Discord commands
│       │   ├── __init__.py
│       │   ├── upload.py             # Upload files command
│       │   ├── ask.py                # Ask questions command
│       │   ├── list_kb.py            # List knowledge bases
│       │   └── delete_kb.py          # Delete knowledge base
│       │
│       └── utils/                    # 🛠️ Utilities
│           ├── __init__.py
│           ├── helpers.py            # Helper functions
│           └── config.py             # Configuration
│
├── data/                             # 📁 Data storage
│   ├── uploads/                      # Temporary file uploads
│   ├── chromadb/                     # Vector DB persistence
│   └── logs/                         # Application logs
│
├── tests/                            # 🧪 Tests
│   └── ...
│
├── .env                              # 🔐 Environment variables
├── pyproject.toml                    # 📦 Dependencies
└── README.md                         # 📖 Documentation
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.12+** installed
2. **uv** package manager:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Ollama** (local LLM):
   ```bash
   # macOS
   brew install ollama
   
   # Start Ollama service
   ollama serve
   
   # In another terminal, pull the model (3.2GB download)
   ollama pull llama3.2:3b
   ```

### Installation

```bash
# 1. Clone/enter project directory
cd discord-rag-bot

# 2. Install dependencies
uv sync

# 3. Activate virtual environment
source .venv/bin/activate  # macOS/Linux
```
