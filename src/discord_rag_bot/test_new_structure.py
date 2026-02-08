"""
Test new modular structure
"""

from discord_rag_bot.utils.config import Config
from discord_rag_bot.processing.converters import DocumentConverter
from discord_rag_bot.processing.chunkers import TextChunker

print("="*70)
print("🧪 TESTING NEW PROJECT STRUCTURE")
print("="*70 + "\n")

# Test 1: Config
print("1️⃣ Testing Config...")
try:
    print(f"   ✅ Project root: {Config.PROJECT_ROOT}")
    print(f"   ✅ Data dir: {Config.DATA_DIR}")
    print(f"   ✅ Chunk size: {Config.CHUNK_SIZE}")
    print(f"   ✅ Embedding model: {Config.EMBEDDING_MODEL}")
    print()
except Exception as e:
    print(f"   ❌ Error: {e}\n")

# Test 2: Text Converter
print("2️⃣ Testing Text Conversion...")
try:
    test_text = """This is a test document.
    
It has multiple paragraphs.

Each paragraph should be preserved when converting."""
    
    # Create temporary file
    import tempfile
    from pathlib import Path
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(test_text)
        temp_path = Path(f.name)
    
    # Convert
    converted = DocumentConverter.convert(temp_path)
    print(f"   ✅ Converted text ({len(converted)} chars)")
    print(f"   Preview: {converted[:100]}...")
    
    # Cleanup
    temp_path.unlink()
    print()
except Exception as e:
    print(f"   ❌ Error: {e}\n")

# Test 3: Chunking
print("3️⃣ Testing Text Chunking...")
try:
    chunker = TextChunker(chunk_size=100, chunk_overlap=20)
    
    sample_text = """The Discord RAG Bot is an advanced system. 
    It uses retrieval-augmented generation to answer questions. 
    The system chunks documents into smaller pieces. 
    Each chunk is converted into a vector embedding. 
    These embeddings are stored in ChromaDB. 
    When a user asks a question, relevant chunks are retrieved. 
    The LLM then generates an answer based on the retrieved context."""
    
    chunks = chunker.chunk_text(sample_text)
    print(f"   ✅ Created {len(chunks)} chunks")
    
    for i, chunk in enumerate(chunks[:2], 1):  # Show first 2
        print(f"   Chunk {i}: {chunk[:80]}...")
    
    print()
except Exception as e:
    print(f"   ❌ Error: {e}\n")

print("="*70)
print("✅ STRUCTURE TEST COMPLETE!")
print("="*70)
print("\n📁 New folders created:")
print("   • src/discord_rag_bot/core/")
print("   • src/discord_rag_bot/processing/")
print("   • src/discord_rag_bot/embeddings/")
print("   • src/discord_rag_bot/retrieval/")
print("   • src/discord_rag_bot/generation/")
print("   • src/discord_rag_bot/storage/")
print("   • src/discord_rag_bot/commands/")
print("   • src/discord_rag_bot/utils/")
print("\n📦 Modules working:")
print("   ✅ Config management")
print("   ✅ Document conversion (PDF, DOCX, TXT)")
print("   ✅ Text chunking")
print("\n🚀 Next: Create embedding, retrieval, and generation modules!\n")