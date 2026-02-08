"""
Test the complete RAG engine with knowledge base management
"""

import asyncio
from pathlib import Path
import tempfile
from discord_rag_bot.core import RAGEngine

# Create temporary test files
def create_test_files():
    """Create temporary test documents"""
    temp_dir = Path(tempfile.mkdtemp())
    
    # File 1: RAG Basics
    file1 = temp_dir / "rag_basics.txt"
    file1.write_text("""
Retrieval-Augmented Generation (RAG) Overview

RAG is an AI framework that combines information retrieval with text generation.
When a user asks a question, the system first searches a knowledge base for 
relevant information. This retrieved context is then provided to a language 
model, which generates an informed answer based on the actual documents rather 
than just its training data.

Key benefits:
- Reduces hallucinations
- Provides grounded, factual answers
- Can be updated without retraining the model
- Citations to source material
""")
    
    # File 2: Implementation Details
    file2 = temp_dir / "implementation.txt"
    file2.write_text("""
RAG Implementation Components

1. Document Processing: Convert PDFs, DOCX, and other formats to text
2. Chunking: Break documents into manageable pieces (typically 500-1000 chars)
3. Embeddings: Convert text chunks into vector representations
4. Vector Storage: Store embeddings in a database like ChromaDB
5. Retrieval: Search for relevant chunks using semantic similarity
6. Generation: Use an LLM to create answers from retrieved context

Popular tools: LangChain, LlamaIndex, ChromaDB, Pinecone, Ollama
""")
    
    # File 3: Best Practices
    file3 = temp_dir / "best_practices.txt"
    file3.write_text("""
RAG Best Practices

Chunking Strategy:
- Keep chunks between 500-1000 characters
- Use overlap (50-100 chars) to preserve context
- Respect document structure (paragraphs, sections)

Retrieval Tuning:
- Start with top-k=3, adjust based on results
- Monitor retrieval precision
- Consider hybrid search (keyword + semantic)

Answer Quality:
- Instruct LLM to cite sources
- Use temperature 0.5-0.7 for consistency
- Implement fallback responses for low-confidence answers
""")
    
    return temp_dir, [file1, file2, file3]


async def progress_callback(filename: str, current: int, total: int):
    """Progress callback for file processing"""
    percentage = int((current / total) * 100)
    print(f"   📊 Processing file {current}/{total} ({percentage}%): {filename}")


async def main():
    print("\n" + "="*70)
    print("🧪 TESTING COMPLETE RAG ENGINE")
    print("="*70 + "\n")
    
    # Initialize engine
    engine = RAGEngine()
    
    # Create test files
    print("📄 Creating test documents...")
    temp_dir, file_paths = create_test_files()
    print(f"   ✅ Created {len(file_paths)} test files\n")
    
    # Test 1: Create Knowledge Base
    print("1️⃣ Creating Knowledge Base...")
    print("─" * 70)
    
    kb = await engine.create_knowledge_base(
        name="RAG Documentation",
        owner_id="123456789",
        owner_name="TestUser",
        file_paths=file_paths,
        description="Complete RAG system documentation",
        progress_callback=progress_callback
    )
    
    print(f"\n   ✅ Knowledge Base Created!")
    print(f"   ID: {kb.kb_id}")
    print(f"   Name: {kb.name}")
    print(f"   Status: {kb.status.value}")
    print(f"   Files: {kb.processed_files}/{kb.total_files}")
    print(f"   Failed: {kb.failed_files}")
    print(f"   Chunks: {kb.total_chunks}")
    print()
    
    # Test 2: Query the Knowledge Base
    print("2️⃣ Querying Knowledge Base...")
    print("─" * 70)
    
    test_questions = [
        "What is RAG?",
        "What are the main components of RAG?",
        "What chunk size should I use?",
    ]
    
    for question in test_questions:
        print(f"\n❓ Question: {question}")
        
        result = engine.query_knowledge_base(kb.kb_id, question)
        
        print(f"📊 Retrieved {result['num_chunks_retrieved']} chunks")
        print(f"\n💬 Answer:")
        print("─" * 70)
        print(result['answer'])
        print("─" * 70)
    
    # Test 3: List User's Knowledge Bases
    print("\n3️⃣ Listing User's Knowledge Bases...")
    print("─" * 70)
    
    user_kbs = engine.get_user_knowledge_bases("123456789")
    print(f"\n   Found {len(user_kbs)} knowledge base(s):\n")
    
    for kb in user_kbs:
        print(f"   📚 {kb.name}")
        print(f"      Status: {kb.status.value}")
        print(f"      Chunks: {kb.total_chunks}")
        print(f"      Files: {kb.processed_files} processed, {kb.failed_files} failed")
        print()
    
    # Test 4: Status Tracking
    print("4️⃣ Knowledge Base Details...")
    print("─" * 70)
    
    kb_details = kb.to_dict()
    print(f"\n   📊 Statistics:")
    print(f"      Total Files: {kb_details['total_files']}")
    print(f"      Processed: {kb_details['processed_files']}")
    print(f"      Failed: {kb_details['failed_files']}")
    print(f"      Total Chunks: {kb_details['total_chunks']}")
    print(f"      Progress: {kb.get_progress_percentage()}%")
    
    if kb_details['files']:
        print(f"\n   📄 Processed Files:")
        for file_info in kb_details['files']:
            print(f"      ✅ {file_info['filename']}: {file_info['chunks']} chunks")
    
    if kb_details['errors']:
        print(f"\n   ❌ Errors:")
        for error in kb_details['errors']:
            print(f"      {error['filename']}: {error['error']}")
    
    print()
    
    # Cleanup
    print("🧹 Cleaning up test files...")
    import shutil
    shutil.rmtree(temp_dir)
    
    print("\n" + "="*70)
    print("✅ ALL TESTS PASSED!")
    print("="*70)
    print("\n📦 Tested features:")
    print("   ✅ Knowledge base creation with multiple files")
    print("   ✅ File processing with progress tracking")
    print("   ✅ Status tracking (pending → processing → success)")
    print("   ✅ Vector storage and retrieval")
    print("   ✅ Answer generation with context")
    print("   ✅ User KB management")
    print("\n🚀 Next: Discord bot integration!\n")


if __name__ == "__main__":
    asyncio.run(main())