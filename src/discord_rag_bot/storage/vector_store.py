"""
Vector store management with ChromaDB
"""

from typing import List, Dict, Any
from pathlib import Path
import chromadb
from discord_rag_bot.embeddings import EmbeddingService
from discord_rag_bot.utils.config import Config


class VectorStore:
    """Manage vector storage with ChromaDB"""
    
    def __init__(self):
        """Initialize vector store"""
        self.client = chromadb.PersistentClient(path=str(Config.CHROMADB_DIR))
        print(f"💾 Vector store initialized at: {Config.CHROMADB_DIR}")
    
    def create_collection(self, collection_name: str, metadata: Dict[str, Any] = None) -> chromadb.Collection:
        """
        Create a new collection
        
        Args:
            collection_name: Name for the collection
            metadata: Optional metadata
            
        Returns:
            ChromaDB collection
        """
        # Delete if exists
        try:
            self.client.delete_collection(collection_name)
        except:
            pass
        
        # Ensure metadata is not empty (ChromaDB requirement)
        if not metadata:
            metadata = {"description": f"Knowledge base: {collection_name}"}
        
        collection = self.client.create_collection(
            name=collection_name,
            metadata=metadata
        )
        
        return collection
    
    def get_collection(self, collection_name: str) -> chromadb.Collection:
        """
        Get existing collection
        
        Args:
            collection_name: Name of collection
            
        Returns:
            ChromaDB collection
            
        Raises:
            ValueError: If collection doesn't exist
        """
        try:
            return self.client.get_collection(collection_name)
        except Exception as e:
            raise ValueError(f"Collection '{collection_name}' not found: {e}")
    
    def add_chunks(
        self,
        collection_name: str,
        chunks: List[Dict[str, Any]],
        embedding_service: EmbeddingService
    ) -> int:
        """
        Add chunks to a collection
        
        Args:
            collection_name: Name of collection
            chunks: List of chunks with 'content' and 'metadata'
            embedding_service: Service to generate embeddings
            
        Returns:
            Number of chunks added
        """
        collection = self.get_collection(collection_name)
        
        # Extract content
        texts = [chunk['content'] for chunk in chunks]
        metadatas = [chunk['metadata'] for chunk in chunks]
        
        # Generate embeddings
        print(f"🔢 Generating embeddings for {len(texts)} chunks...")
        embeddings = embedding_service.embed_batch(texts, show_progress=True)
        
        # Generate IDs (use existing count to avoid ID conflicts)
        existing_count = collection.count()
        ids = [f"chunk_{existing_count + i}" for i in range(len(texts))]
        
        # Add to collection
        collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        return len(texts)
    
    def list_collections(self) -> List[str]:
        """List all collection names"""
        collections = self.client.list_collections()
        return [col.name for col in collections]
    
    def delete_collection(self, collection_name: str):
        """Delete a collection"""
        self.client.delete_collection(collection_name)
    
    def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        """Get statistics for a collection"""
        try:
            collection = self.get_collection(collection_name)
            return {
                'name': collection_name,
                'count': collection.count(),
                'metadata': collection.metadata
            }
        except ValueError:
            return None