# 🤖 Discord RAG Bot - AI Bootcamp Project

> **A production-ready Discord bot using Retrieval-Augmented Generation (RAG) to answer questions about course materials.**

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Discord.py](https://img.shields.io/badge/discord.py-2.3.2-blue.svg)](https://discordpy.readthedocs.io/)

---

## 🎯 Quick Overview

Upload PDFs, DOCX, TXT, or MD files to Discord → Ask questions → Get accurate answers with source citations!

**Tech Stack (100% Free & Local):**
- **Embeddings:** SentenceTransformers (all-MiniLM-L6-v2)
- **Vector DB:** ChromaDB (persistent)
- **LLM:** Ollama (llama3.2:3b)
- **Bot:** Discord.py

---

## 🚀 Quick Start

### 1. Install Ollama
```bash
brew install ollama
ollama serve  # Keep this running
ollama pull llama3.2:3b  # 3.2GB download
```

### 2. Setup Project
```bash
cd discord-rag-bot
uv sync
source .venv/bin/activate
```

### 3. Configure Discord Bot
```bash
# Create .env file
echo "DISCORD_BOT_TOKEN=your_token_here" > .env
```

Get token from: https://discord.com/developers/applications
- Create app → Bot → Enable MESSAGE CONTENT INTENT → Copy token

### 4. Run
```bash
python -m discord_rag_bot.bot
```

---

## 🎮 Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/upload` | Upload files to create KB | `/upload name:AI-Bootcamp file1:[PDF]` |
| `/ask` | Ask a question | `/ask kb_name:AI-Bootcamp question:What is RAG?` |
| `/list-kb` | List your KBs | `/list-kb` |
| `/delete-kb` | Delete a KB | `/delete-kb kb_name:AI-Bootcamp` |
| `/help` | Show help | `/help` |

---

## 📁 Project Structure

```
src/discord_rag_bot/
├── bot.py                    # Main entry point
├── core/                     # RAG engine & KB management
├── processing/               # File conversion & chunking
├── embeddings/               # SentenceTransformers
├── storage/                  # ChromaDB
├── retrieval/                # Vector search
├── generation/               # Ollama LLM
├── commands/                 # Discord commands
└── utils/                    # Config & helpers
```

---

## 🎓 Assignment Requirements

### Phase 1: Preparation ✅
- ✅ RAG architecture designed
- ✅ Researched embeddings (SentenceTransformers, OpenAI, Cohere)
- ✅ Researched vector stores (ChromaDB, FAISS, Pinecone)
- ✅ Selected local LLM (Ollama)

### Phase 2: Development ✅
- ✅ **Data Ingestion:** File conversion → chunking → embedding → storage
- ✅ **Retrieval:** Query embedding → vector search → top-K
- ✅ **Generation:** Context building → LLM prompting → grounded answers
- ✅ **Bonus:** Multi-user, multi-KB, progress tracking, evaluation

---

## 🐛 Troubleshooting

**Ollama not connecting:**
```bash
ollama serve  # Terminal 1
ollama list   # Terminal 2 - verify llama3.2:3b exists
```

**Discord commands not showing:**
- Enable MESSAGE CONTENT INTENT in Discord Developer Portal
- Wait up to 1 hour for command sync
- Try kicking/re-inviting bot

**Import errors:**
```bash
uv sync --reinstall
source .venv/bin/activate
```

---

## 📊 How It Works

```
Upload File
    ↓
Convert (PDF/DOCX/TXT → text)
    ↓  
Chunk (500 chars, 50 overlap)
    ↓
Embed (384-dim vectors)
    ↓
Store (ChromaDB)
    
Ask Question
    ↓
Embed Query
    ↓
Search (top-3 similar chunks)
    ↓
Generate (Ollama + context)
    ↓
Answer + Citations
```

---

## 💡 Key Features

- ✅ Multi-knowledge base per user
- ✅ Real-time progress tracking
- ✅ Source citations on every answer
- ✅ Error handling & validation
- ✅ 100% local (no API costs)
- ✅ Persistent storage

---

## 🎥 Demo

1. Upload files: `/upload name:Test file1:[PDF]`
2. Ask question: `/ask kb_name:Test question:What is this about?`
3. Get answer with sources!

---

## ⚙️ Configuration

Edit `.env`:
```bash
DISCORD_BOT_TOKEN=your_token
OLLAMA_MODEL=llama3.2:3b
EMBEDDING_MODEL=all-MiniLM-L6-v2
CHUNK_SIZE=500
CHUNK_OVERLAP=50
TOP_K_RETRIEVAL=3
MAX_FILE_SIZE_MB=10
```

---

## 🤝 Credits

- AI Bootcamp instructors
- MongoDB RAG Workshop
- Open source: SentenceTransformers, ChromaDB, Ollama, Discord.py

---

**Built for AI Bootcamp Data Scientist Track** 🚀