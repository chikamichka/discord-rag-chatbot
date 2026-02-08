from typing import List, Dict, Any, Callable, Optional
from pathlib import Path
from discord_rag_bot.processing.converters import DocumentConverter
from discord_rag_bot.processing.chunkers import TextChunker
from discord_rag_bot.core.knowledge_base import KnowledgeBase
import asyncio


class FileProcessingResult:
    """Result of processing a single file"""
    
    def __init__(self, filename: str):
        self.filename = filename
        self.success = False
        self.chunks = 0
        self.error = None
        self.file_size = 0
        self.processing_time = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'filename': self.filename,
            'success': self.success,
            'chunks': self.chunks,
            'error': self.error,
            'file_size': self.file_size,
            'processing_time_seconds': round(self.processing_time, 2)
        }


class FileProcessor:
    """Process files with progress tracking"""
    
    def __init__(self, chunker: TextChunker):
        """
        Initialize processor
        
        Args:
            chunker: Text chunker instance
        """
        self.chunker = chunker
    
    async def process_file(
        self,
        file_path: Path,
        metadata: Dict[str, Any] = None,
        progress_callback: Optional[Callable[[str, float], None]] = None
    ) -> FileProcessingResult:
        """
        Process a single file
        
        Args:
            file_path: Path to file
            metadata: Additional metadata to attach
            progress_callback: Callback for progress updates (message, percentage)
            
        Returns:
            Processing result
        """
        import time
        
        result = FileProcessingResult(file_path.name)
        result.file_size = file_path.stat().st_size
        start_time = time.time()
        
        try:
            # Update progress: Starting
            if progress_callback:
                await progress_callback(f"📄 Converting {file_path.name}...", 0)
            
            # Convert to text
            text = await asyncio.to_thread(DocumentConverter.convert, file_path)
            
            if not text or not text.strip():
                raise ValueError("No text extracted from file")
            
            # Update progress: Chunking
            if progress_callback:
                await progress_callback(f"✂️ Chunking {file_path.name}...", 50)
            
            # Chunk text
            file_metadata = metadata or {}
            file_metadata.update({
                'filename': file_path.name,
                'file_type': file_path.suffix,
                'file_size': result.file_size
            })
            
            chunks = self.chunker.chunk_with_metadata(text, file_metadata)
            
            # Update progress: Complete
            if progress_callback:
                await progress_callback(f"✅ {file_path.name} processed!", 100)
            
            result.success = True
            result.chunks = len(chunks)
            result.processing_time = time.time() - start_time
            
            return result, chunks
        
        except Exception as e:
            result.success = False
            result.error = str(e)
            result.processing_time = time.time() - start_time
            
            if progress_callback:
                await progress_callback(f"❌ {file_path.name} failed: {str(e)}", 100)
            
            return result, []
    
    async def process_files(
        self,
        file_paths: List[Path],
        kb: KnowledgeBase,
        metadata: Dict[str, Any] = None,
        progress_callback: Optional[Callable[[str, int, int], None]] = None
    ) -> List[Dict[str, Any]]:
        """
        Process multiple files
        
        Args:
            file_paths: List of file paths
            kb: Knowledge base to update
            metadata: Base metadata for all files
            progress_callback: Callback(current_file, total_files, percentage)
            
        Returns:
            List of all chunks from all files
        """
        all_chunks = []
        
        for i, file_path in enumerate(file_paths, 1):
            # Progress callback
            if progress_callback:
                await progress_callback(file_path.name, i, len(file_paths))
            
            # Process file
            result, chunks = await self.process_file(file_path, metadata)
            
            # Update KB
            if result.success:
                kb.add_file(result.to_dict())
                all_chunks.extend(chunks)
            else:
                kb.add_error(result.filename, result.error)
        
        return all_chunks