from typing import List
from sentence_transformers import SentenceTransformer
from discord_rag_bot.utils.config import Config


class EmbeddingService:
    """Generate embeddings for text chunks"""
    
    def __init__(self, model_name: str = None):
        """
        Initialize embedding service
        
        Args:
            model_name: Name of sentence transformer model
        """
        self.model_name = model_name or Config.EMBEDDING_MODEL
        print(f"📊 Loading embedding model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)
        print(f"✅ Embedding model loaded (dimension: {self.model.get_sentence_embedding_dimension()})")
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector
        """
        embedding = self.model.encode(text, show_progress_bar=False)
        return embedding.tolist()
    
    def embed_batch(self, texts: List[str], show_progress: bool = True) -> List[List[float]]:
        """
        Generate embeddings for multiple texts
        
        Args:
            texts: List of input texts
            show_progress: Whether to show progress bar
            
        Returns:
            List of embedding vectors
        """
        embeddings = self.model.encode(texts, show_progress_bar=show_progress)
        return embeddings.tolist()
    
    @property
    def dimension(self) -> int:
        """Get embedding dimension"""
        return self.model.get_sentence_embedding_dimension()