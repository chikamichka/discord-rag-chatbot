from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from discord_rag_bot.utils.config import Config


class TextChunker:
    """Smart text chunking with various strategies"""
    
    def __init__(
        self,
        chunk_size: int = None,
        chunk_overlap: int = None
    ):
        """
        Initialize chunker
        
        Args:
            chunk_size: Size of chunks (default from config)
            chunk_overlap: Overlap between chunks (default from config)
        """
        self.chunk_size = chunk_size or Config.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or Config.CHUNK_OVERLAP
        
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Chunk text into smaller pieces
        
        Args:
            text: Input text
            
        Returns:
            List of text chunks
        """
        if not text or not text.strip():
            return []
        
        chunks = self.splitter.split_text(text)
        
        # Filter out very small chunks
        chunks = [chunk for chunk in chunks if len(chunk.strip()) > 20]
        
        return chunks
    
    def chunk_with_metadata(self, text: str, metadata: dict = None) -> List[dict]:
        """
        Chunk text and attach metadata to each chunk
        
        Args:
            text: Input text
            metadata: Metadata to attach to each chunk
            
        Returns:
            List of dicts with 'content' and 'metadata' keys
        """
        chunks = self.chunk_text(text)
        metadata = metadata or {}
        
        result = []
        for i, chunk in enumerate(chunks):
            chunk_data = {
                'content': chunk,
                'metadata': {
                    **metadata,
                    'chunk_index': i,
                    'total_chunks': len(chunks)
                }
            }
            result.append(chunk_data)
        
        return result