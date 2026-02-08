from typing import List, Dict, Any
import chromadb
from discord_rag_bot.embeddings import EmbeddingService
from discord_rag_bot.utils.config import Config


class Retriever:
    """Retrieve relevant chunks using vector search"""
    
    def __init__(self, embedding_service: EmbeddingService, collection_name: str):
        """
        Initialize retriever
        
        Args:
            embedding_service: Service for generating query embeddings
            collection_name: ChromaDB collection name
        """
        self.embedding_service = embedding_service
        self.collection_name = collection_name
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=str(Config.CHROMADB_DIR))
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": f"Knowledge base: {collection_name}"}
        )
    
    def retrieve(
        self,
        query: str,
        top_k: int = None,
        filter_metadata: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant chunks for a query
        
        Args:
            query: User question
            top_k: Number of results to return
            filter_metadata: Optional metadata filters
            
        Returns:
            List of retrieved chunks with metadata and scores
        """
        top_k = top_k or Config.TOP_K_RETRIEVAL
        
        # Generate query embedding
        query_embedding = self.embedding_service.embed_text(query)
        
        # Build query parameters
        query_params = {
            "query_embeddings": [query_embedding],
            "n_results": top_k
        }
        
        if filter_metadata:
            query_params["where"] = filter_metadata
        
        # Search
        results = self.collection.query(**query_params)
        
        # Format results
        retrieved = []
        for i in range(len(results['documents'][0])):
            chunk = {
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i],
                'score': 1 / (1 + results['distances'][0][i])  # Convert distance to similarity
            }
            retrieved.append(chunk)
        
        return retrieved
    
    def get_stats(self) -> Dict[str, Any]:
        """Get collection statistics"""
        return {
            'collection_name': self.collection_name,
            'total_chunks': self.collection.count(),
            'embedding_dimension': self.embedding_service.dimension
        }