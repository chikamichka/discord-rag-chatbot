"""
Test all core modules together
"""

from discord_rag_bot.processing import DocumentConverter, TextChunker
from discord_rag_bot.embeddings import EmbeddingService
from discord_rag_bot.storage import VectorStore
from discord_rag_bot.retrieval import Retriever
from discord_rag_bot.generation import AnswerGenerator

print("\n" + "="*70)
print("🧪 TESTING ALL CORE MODULES")
print("="*70 + "\n")

# Sample document
sample_doc = """
Retrieval-Augmented Generation (RAG) is a technique that combines 
information retrieval with language model generation. When a user asks 
a question, the system first retrieves relevant documents from a knowledge 
base. These documents provide context to the language model, which then 
generates an informed answer. This approach reduces hallucinations and 
provides more accurate, grounded responses.
"""

print("1️⃣ Testing Document Processing...")
chunker = TextChunker(chunk_size=150, chunk_overlap=20)
chunks = chunker.chunk_with_metadata(
    sample_doc,
    metadata={'source': 'Test Document', 'topic': 'RAG'}
)
print(f"   ✅ Created {len(chunks)} chunks\n")

print("2️⃣ Testing Embedding Service...")
embedding_service = EmbeddingService()
print()

print("3️⃣ Testing Vector Store...")
vector_store = VectorStore()
collection_name = "test_collection"
vector_store.create_collection(collection_name)
num_added = vector_store.add_chunks(collection_name, chunks, embedding_service)
print(f"   ✅ Added {num_added} chunks to vector store\n")

print("4️⃣ Testing Retrieval...")
retriever = Retriever(embedding_service, collection_name)
query = "What is RAG?"
results = retriever.retrieve(query, top_k=2)
print(f"   ✅ Retrieved {len(results)} chunks")
print(f"   Best match score: {results[0]['score']:.3f}")
print(f"   Preview: {results[0]['content'][:100]}...\n")

print("5️⃣ Testing Answer Generation...")
generator = AnswerGenerator()
answer = generator.generate(query, results)
print(f"   ✅ Generated answer:")
print(f"   {answer}\n")

print("="*70)
print("✅ ALL MODULES WORKING!")
print("="*70)
print("\n📦 Tested modules:")
print("   ✅ Document processing (chunking)")
print("   ✅ Embedding generation")
print("   ✅ Vector storage (ChromaDB)")
print("   ✅ Retrieval (vector search)")
print("   ✅ Answer generation (Ollama)")
print("\n🚀 Next: Build the core RAG engine and knowledge base manager!\n")