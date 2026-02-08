from typing import List, Dict, Any, Optional
from pathlib import Path
from discord_rag_bot.embeddings import EmbeddingService
from discord_rag_bot.storage import VectorStore
from discord_rag_bot.retrieval import Retriever
from discord_rag_bot.generation import AnswerGenerator
from discord_rag_bot.processing import TextChunker
from discord_rag_bot.processing.file_processor import FileProcessor
from discord_rag_bot.core.knowledge_base import KnowledgeBaseManager, KnowledgeBase, ProcessingStatus
from discord_rag_bot.utils.config import Config


class RAGEngine:
    """Main RAG system orchestrator"""
    
    def __init__(self):
        """Initialize RAG engine"""
        print("🚀 Initializing RAG Engine...")
        
        # Core components
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()
        self.answer_generator = AnswerGenerator()
        self.chunker = TextChunker()
        self.file_processor = FileProcessor(self.chunker)
        
        # Knowledge base manager
        kb_storage = Config.DATA_DIR / "knowledge_bases"
        self.kb_manager = KnowledgeBaseManager(kb_storage)
        
        print("✅ RAG Engine ready!\n")
    
    async def create_knowledge_base(
        self,
        name: str,
        owner_id: str,
        owner_name: str,
        file_paths: List[Path],
        description: str = "",
        progress_callback = None
    ) -> KnowledgeBase:
        """
        Create a new knowledge base from files
        
        Args:
            name: KB name
            owner_id: Discord user ID
            owner_name: Discord username
            file_paths: List of files to process
            description: Optional description
            progress_callback: Callback for progress updates
            
        Returns:
            Created knowledge base
        """
        # Create KB record
        kb = self.kb_manager.create_kb(
            name=name,
            owner_id=owner_id,
            owner_name=owner_name,
            description=description,
            file_count=len(file_paths)
        )
        
        try:
            # Create vector collection
            collection_metadata = {
                'kb_id': kb.kb_id,
                'name': name,
                'owner_id': owner_id,
                'description': description
            }
            self.vector_store.create_collection(kb.kb_id, collection_metadata)
            
            # Process files
            chunks = await self.file_processor.process_files(
                file_paths=file_paths,
                kb=kb,
                metadata={'kb_id': kb.kb_id, 'kb_name': name},
                progress_callback=progress_callback
            )
            
            # Add chunks to vector store
            if chunks:
                self.vector_store.add_chunks(kb.kb_id, chunks, self.embedding_service)
            
            # Update KB status
            self.kb_manager.update_kb(kb)
            
            return kb
        
        except Exception as e:
            kb.add_error("system", f"Failed to create KB: {str(e)}")
            kb.status = ProcessingStatus.FAILED
            self.kb_manager.update_kb(kb)
            raise
    
    def query_knowledge_base(
        self,
        kb_id: str,
        query: str,
        top_k: int = None
    ) -> Dict[str, Any]:
        """
        Query a knowledge base
        
        Args:
            kb_id: Knowledge base ID
            query: User question
            top_k: Number of chunks to retrieve
            
        Returns:
            Dictionary with answer and metadata
        """
        # Get KB
        kb = self.kb_manager.get_kb(kb_id)
        if not kb:
            raise ValueError(f"Knowledge base '{kb_id}' not found")
        
        if kb.status != ProcessingStatus.SUCCESS:
            raise ValueError(f"Knowledge base is {kb.status.value}, cannot query")
        
        # Retrieve
        retriever = Retriever(self.embedding_service, kb_id)
        chunks = retriever.retrieve(query, top_k)
        
        # Generate answer
        answer = self.answer_generator.generate(query, chunks)
        
        return {
            'kb_id': kb_id,
            'kb_name': kb.name,
            'query': query,
            'answer': answer,
            'chunks': chunks,
            'num_chunks_retrieved': len(chunks)
        }
    
    def get_user_knowledge_bases(self, owner_id: str) -> List[KnowledgeBase]:
        """Get all KBs for a user"""
        return self.kb_manager.get_user_kbs(owner_id)
    
    def delete_knowledge_base(self, kb_id: str) -> bool:
        """Delete a knowledge base"""
        # Delete from vector store
        try:
            self.vector_store.delete_collection(kb_id)
        except:
            pass
        
        # Delete from manager
        return self.kb_manager.delete_kb(kb_id)