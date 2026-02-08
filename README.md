# 🤖 Discord RAG Bot - AI Bootcamp Knowledge Assistant

A production-ready Discord bot that lets students upload course materials and ask questions using Retrieval-Augmented Generation (RAG). Get accurate answers from your own documents with source citations!

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Discord.py](https://img.shields.io/badge/discord.py-2.3.2-blue.svg)](https://discordpy.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 Project Overview

### Purpose
Help AI Bootcamp students **stop searching through PDFs manually** and **avoid ChatGPT hallucinations** by providing:
- Accurate answers directly from course materials
- Source citations for every answer
- Multi-knowledge base organization
- Real-time document processing in Discord

### Main Users
1. **Primary:** AI Bootcamp students/interns learning RAG systems
2. **Secondary:** Instructors managing course materials
3. **Future:** Any team needing document-based Q&A

### Key Features

| Feature | Description | Status |
|---------|-------------|--------|
| 📤 **File Upload** | Upload PDF, DOCX, TXT, MD via Discord | ✅ Complete |
| 📚 **Multi-KB System** | Create unlimited named knowledge bases | ✅ Complete |
| 💬 **Smart Q&A** | Ask questions, get contextual answers | ✅ Complete |
| 📝 **Source Citations** | Every answer shows source documents | ✅ Complete |
| 📊 **Progress Tracking** | Real-time upload and processing status | ✅ Complete |
| 🗑️ **KB Management** | List, view, and delete knowledge bases | ✅ Complete |
| 🎯 **100% Local** | No API costs, no credit cards needed | ✅ Complete |

---

## 🏗️ Architecture

### Tech Stack (All Free & Local!)

| Component | Technology | Why? |
|-----------|-----------|------|
| **Embeddings** | SentenceTransformers (all-MiniLM-L6-v2) | Free, 384-dim vectors, runs locally |
| **Vector DB** | ChromaDB | Persistent storage, fast similarity search |
| **LLM** | Ollama (llama3.2:3b) | Free, local, good quality |
| **Bot** | Discord.py | Modern slash commands, rich embeds |
| **File Processing** | pypdf, python-docx | Standard Python libraries |

### Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    USER UPLOADS FILE                         │
│                         (Discord)                            │
└───────────────────────┬─────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│              FILE PROCESSING PIPELINE                        │
│                                                              │
│  1. CONVERT  →  PDF/DOCX/TXT → text                         │
│  2. CHUNK    →  RecursiveTextSplitter (500 chars)          │
│  3. EMBED    →  SentenceTransformers (384-dim vectors)     │
│  4. STORE    →  ChromaDB (persistent vector DB)            │
└───────────────────────┬─────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│                 KNOWLEDGE BASE CREATED                       │
│              (Ready for questions!)                          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                  USER ASKS QUESTION                          │
│                         (Discord)                            │
└───────────────────────┬─────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│                  RAG QUERY PIPELINE                          │
│                                                              │
│  1. EMBED QUERY  →  Convert question to vector              │
│  2. SEARCH       →  Find top-5 similar chunks (cosine)     │
│  3. AUGMENT      →  Build prompt with context               │
│  4. GENERATE     →  Ollama LLM produces answer              │
└───────────────────────┬─────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│            ANSWER WITH SOURCE CITATIONS                      │
│                    (Back to user)                            │
└─────────────────────────────────────────────────────────────┘
```

### Project Structure

```
discord-rag-bot/
├── src/discord_rag_bot/
│   ├── bot.py                    # 🤖 Main Discord bot entry point
│   │
│   ├── core/                     # 🧠 Core RAG logic
│   │   ├── rag_engine.py         # RAG orchestrator
│   │   └── knowledge_base.py     # KB management
│   │
│   ├── processing/               # 📄 Document processing
│   │   ├── converters.py         # PDF/DOCX/TXT → text
│   │   ├── chunkers.py           # Smart chunking
│   │   └── file_processor.py     # Processing pipeline
│   │
│   ├── embeddings/               # 🔢 Vector embeddings
│   │   └── embedding_service.py  # SentenceTransformers
│   │
│   ├── storage/                  # 💾 Data persistence
│   │   └── vector_store.py       # ChromaDB manager
│   │
│   ├── retrieval/                # 🔍 Vector search
│   │   └── retriever.py          # Similarity search
│   │
│   ├── generation/               # 💬 Answer generation
│   │   └── generator.py          # Ollama LLM integration
│   │
│   ├── commands/                 # 🎮 Discord slash commands
│   │   ├── upload.py             # Upload files
│   │   ├── ask.py                # Ask questions
│   │   ├── list_kb.py            # List KBs
│   │   └── delete_kb.py          # Delete KB
│   │
│   └── utils/                    # 🛠️ Utilities
│       └── config.py             # Configuration
│
├── data/                         # 📁 Runtime data
│   ├── chromadb/                 # Vector database
│   ├── knowledge_bases/          # KB metadata (JSON)
│   └── uploads/                  # Temp file storage
│
├── .env                          # 🔐 Environment variables
├── pyproject.toml                # 📦 Dependencies
└── README.md                     # 📖 This file
```

---

## 🚀 Installation & Setup

### Prerequisites

1. **Python 3.12+**
   ```bash
   python3 --version  # Should be 3.12 or higher
   ```

2. **uv Package Manager** (Fast Python installer)
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   source ~/.zshrc  # or ~/.bashrc
   ```

3. **Ollama** (Local LLM - Required!)
   ```bash
   # macOS
   brew install ollama
   
   # Start Ollama (keep this running in a separate terminal)
   ollama serve
   
   # Download model (3.2GB, one-time download)
   ollama pull llama3.2:3b
   ```

### Project Setup

```bash
# 1. Navigate to project
cd discord-rag-bot

# 2. Install dependencies
uv sync

# 3. Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows
```

### Discord Bot Configuration

1. **Create Discord Application**
   - Go to https://discord.com/developers/applications
   - Click "New Application"
   - Name it (e.g., "AI Bootcamp RAG Bot")

2. **Create Bot**
   - Go to "Bot" tab
   - Click "Add Bot"
   - Under "Privileged Gateway Intents", enable:
     - ✅ MESSAGE CONTENT INTENT (Required!)
   - Click "Reset Token" → Copy the token

3. **Create `.env` File**
   ```bash
   # In project root
   echo "DISCORD_BOT_TOKEN=your_token_here" > .env
   ```

4. **Invite Bot to Server**
   - Go to "OAuth2" → "URL Generator"
   - Select scopes: `bot`, `applications.commands`
   - Select permissions: 
     - Send Messages
     - Read Message History
     - Embed Links
     - Attach Files
   - Copy URL → Open in browser → Select your server

### Running the Bot

```bash
# Make sure Ollama is running first!
# Terminal 1: ollama serve

# Terminal 2: Run bot
python -m discord_rag_bot.bot

# You should see:
# ✅ Bot is ready! Logged in as YourBot
# 📊 Connected to 1 server(s)
```

---

## 🎮 Discord Commands

### `/upload` - Create Knowledge Base

Upload files to create a searchable knowledge base.

**Usage:**
```
/upload name:AI-Bootcamp file1:[attach PDF] file2:[attach DOCX] description:Course materials
```

**Parameters:**
- `name` (required): Knowledge base name
- `file1` (required): First file (PDF, DOCX, TXT, or MD)
- `file2-5` (optional): Additional files
- `description` (optional): Description of the KB

**What happens:**
1. ⏳ Bot validates files (type, size)
2. 📄 Converts each file to text
3. ✂️ Chunks text into 500-character pieces
4. 🔢 Generates embeddings (384-dim vectors)
5. 💾 Stores in ChromaDB
6. ✅ KB ready for questions!

**Example Output:**
```
✅ Knowledge Base Created!
AI-Bootcamp is ready to use

📊 Statistics
✅ Status: success
📄 Files: 3 processed, 0 failed
📦 Chunks: 45 total
🕐 Created: 2024-02-08 14:30

📁 Processed Files
• syllabus.pdf: 12 chunks
• project_guide.docx: 18 chunks
• faq.txt: 15 chunks

💡 Next Steps
Use /ask kb_name:AI-Bootcamp question:<your question> to start asking!
```

---

### `/ask` - Ask Questions

Query your knowledge base and get AI-powered answers with sources.

**Usage:**
```
/ask kb_name:AI-Bootcamp question:What is the deadline for Phase 2?
```

**Parameters:**
- `kb_name` (required): Which knowledge base to query
- `question` (required): Your question

**What happens:**
1. 🔢 Converts question to embedding
2. 🔍 Searches for top-5 most similar chunks
3. 📝 Builds prompt with retrieved context
4. 🤖 Ollama generates contextual answer
5. 📚 Shows sources used

**Example Output:**
```
💬 Answer
Phase 2 should be completed by the end of Week 3. The deadline allows you 
to start development even without attending Office Hours. Focus on implementing 
the core RAG logic including data ingestion, retrieval, and generation.

📚 Knowledge Base: AI-Bootcamp
📊 Sources: 5 chunks retrieved

📄 Top Source: project_guide.pdf
```
Phase 2: Development
Can start development even if not attend Office hours...
```
```

---

### `/list-kb` - List Knowledge Bases

See all your knowledge bases.

**Usage:**
```
/list-kb
```

**Example Output:**
```
📚 Your Knowledge Bases (2)
You have 2 knowledge base(s)

AI-Bootcamp
✅ Status: success
📊 Chunks: 45
📄 Files: 3 processed, 0 failed
🕐 Created: 2024-02-08 14:30
📝 Course materials

Python-Tutorials
✅ Status: success
📊 Chunks: 67
📄 Files: 5 processed, 0 failed
🕐 Created: 2024-02-07 10:15
📝 Python learning resources
```

---

### `/delete-kb` - Delete Knowledge Base

Permanently delete a knowledge base.

**Usage:**
```
/delete-kb kb_name:AI-Bootcamp
```

**Example Output:**
```
✅ Knowledge Base Deleted
AI-Bootcamp has been permanently deleted

📊 Statistics
• 45 chunks removed
• 3 files deleted
```

---

### `/help` - Show Help

Display all available commands.

**Usage:**
```
/help
```

---

## ⚙️ Configuration

Edit `.env` to customize:

```bash
# Discord
DISCORD_BOT_TOKEN=your_token_here

# Ollama (optional - defaults shown)
OLLAMA_MODEL=llama3.2:3b
OLLAMA_BASE_URL=http://localhost:11434

# Embeddings (optional)
EMBEDDING_MODEL=all-MiniLM-L6-v2

# RAG Parameters (optional)
CHUNK_SIZE=500           # Characters per chunk
CHUNK_OVERLAP=50         # Overlap between chunks
TOP_K_RETRIEVAL=5        # Chunks to retrieve per query

# File Limits (optional)
MAX_FILE_SIZE_MB=10      # Max file size
```

---

## 🧪 Testing Your Setup

### Test 1: Bot Connection
```bash
python -m discord_rag_bot.bot

# Expected:
# ✅ Bot is ready! Logged in as YourBot
# 📊 Connected to 1 server(s)
```

### Test 2: Upload Test File
1. In Discord: `/upload name:Test file1:[attach sample.pdf]`
2. Wait for processing (shows progress)
3. Should see: ✅ Knowledge Base Created!

### Test 3: Ask Question
```
/ask kb_name:Test question:What is this document about?
```
Should get answer with source citation.

### Test 4: List KBs
```
/list-kb
```
Should show "Test" knowledge base.

---

## 🐛 Troubleshooting

### "Ollama connection error"
**Problem:** Bot can't connect to Ollama

**Solution:**
```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Verify model
ollama list
# Should show: llama3.2:3b

# If model missing:
ollama pull llama3.2:3b
```

---

### "Discord bot not responding to commands"
**Problem:** Slash commands don't appear

**Solutions:**
1. Check MESSAGE CONTENT INTENT is enabled
2. Verify bot has correct permissions
3. Wait up to 1 hour for commands to sync
4. Try kicking and re-inviting bot

---

### "Import errors"
**Problem:** ModuleNotFoundError

**Solution:**
```bash
# Reinstall dependencies
uv sync --reinstall

# Activate venv
source .venv/bin/activate
```

---

### "File upload fails"
**Problem:** Upload command returns error

**Check:**
1. File size < 10MB
2. File type is PDF, DOCX, TXT, or MD
3. Ollama is running
4. ChromaDB directory has write permissions

---

## 📊 Performance & Limitations

### Current Capabilities
- ✅ Handles PDFs up to 10MB
- ✅ Processes 5 files simultaneously
- ✅ 500 char chunks (adjustable)
- ✅ Top-5 retrieval (adjustable)
- ✅ ~2-10 second response time

### Known Limitations
- ⚠️ Tables in PDFs may not extract perfectly
- ⚠️ Images are not processed
- ⚠️ Very long documents (>100 pages) may be slow
- ⚠️ No conversation memory (each question is independent)

### Future Improvements
- [ ] Conversation memory (chat history)
- [ ] Hybrid search (keyword + vector)
- [ ] Re-ranking for better results
- [ ] Support for more file types (PPTX, HTML)
- [ ] Batch question answering
- [ ] Export/import knowledge bases

---

## 🎓 Data Scientist Assignment Completion

### Phase 1: Preparation ✅

**Architecture Design:**
- ✅ RAG system architecture documented (see Architecture section)
- ✅ Data flow diagrams created
- ✅ Component selection justified

**Technology Choices:**
| Component | Choice | Rationale |
|-----------|--------|-----------|
| Embeddings | SentenceTransformers | Free, local, good quality, 384-dim vectors |
| Vector DB | ChromaDB | Easy setup, persistent, fast similarity search |
| LLM | Ollama (llama3.2:3b) | Free, local, no API costs, good quality |
| Chunking | RecursiveCharacterTextSplitter | Semantic-aware, preserves context |

### Phase 2: Development ✅

**Data Ingestion Pipeline:**
- ✅ File conversion (PDF/DOCX/TXT → text)
- ✅ Smart chunking (500 chars, 50 overlap)
- ✅ Embedding generation (SentenceTransformers)
- ✅ Vector storage (ChromaDB persistent)

**Retrieval Logic:**
- ✅ Query embedding generation
- ✅ Cosine similarity search
- ✅ Top-K retrieval (configurable)
- ✅ Metadata filtering

**Augmentation & Generation:**
- ✅ Context-aware prompt engineering
- ✅ LLM integration (Ollama)
- ✅ Source citation tracking
- ✅ Answer generation with grounding

**Bonus Features:**
- ✅ Multi-user support
- ✅ Multiple knowledge bases per user
- ✅ Progress tracking
- ✅ Error handling
- ✅ Evaluation metrics (retrieval scores)

---

## 📚 Additional Resources

### Documentation
- [Discord.py Docs](https://discordpy.readthedocs.io/)
- [Ollama Docs](https://ollama.ai/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [SentenceTransformers](https://www.sbert.net/)

### Tutorials
- [RAG Systems Explained](https://github.com/mongodb-developer/genai-devday-notebooks)
- [Discord Bot Development](https://realpython.com/how-to-make-a-discord-bot-python/)

---

## 🤝 Contributing

This is an educational project. Improvements welcome:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 🙏 Acknowledgments

- **AI Bootcamp** instructors and mentors
- **MongoDB** RAG Workshop materials
- **Anthropic Claude** for development assistance
- **Open Source** communities (SentenceTransformers, ChromaDB, Ollama, Discord.py)

---

**Built for the AI Bootcamp Data Scientist track**

*Making RAG accessible, understandable, and completely free!*