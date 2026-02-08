from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
from enum import Enum
import json


class ProcessingStatus(Enum):
    """Status of knowledge base processing"""
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"  # Some files succeeded, some failed


class KnowledgeBase:
    """Represents a user's knowledge base"""
    
    def __init__(
        self,
        kb_id: str,
        name: str,
        owner_id: str,
        owner_name: str,
        description: str = ""
    ):
        """
        Initialize knowledge base
        
        Args:
            kb_id: Unique identifier
            name: Knowledge base name
            owner_id: Discord user ID
            owner_name: Discord username
            description: Optional description
        """
        self.kb_id = kb_id
        self.name = name
        self.owner_id = owner_id
        self.owner_name = owner_name
        self.description = description
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        # Processing status
        self.status = ProcessingStatus.PENDING
        self.total_files = 0
        self.processed_files = 0
        self.failed_files = 0
        self.total_chunks = 0
        
        # File details
        self.files = []  # List of processed file info
        self.errors = []  # Processing errors
    
    def add_file(self, file_info: Dict[str, Any]):
        """Add processed file information"""
        self.files.append(file_info)
        self.processed_files += 1
        self.total_chunks += file_info.get('chunks', 0)
        self.updated_at = datetime.now()
    
    def add_error(self, filename: str, error: str):
        """Record a file processing error"""
        self.errors.append({
            'filename': filename,
            'error': error,
            'timestamp': datetime.now().isoformat()
        })
        self.failed_files += 1
        self.updated_at = datetime.now()
    
    def update_status(self):
        """Update overall processing status"""
        if self.processed_files == 0 and self.failed_files == 0:
            self.status = ProcessingStatus.PENDING
        elif self.processed_files + self.failed_files < self.total_files:
            self.status = ProcessingStatus.PROCESSING
        elif self.failed_files == self.total_files:
            self.status = ProcessingStatus.FAILED
        elif self.failed_files > 0:
            self.status = ProcessingStatus.PARTIAL
        else:
            self.status = ProcessingStatus.SUCCESS
    
    def get_progress_percentage(self) -> int:
        """Get processing progress as percentage"""
        if self.total_files == 0:
            return 0
        return int(((self.processed_files + self.failed_files) / self.total_files) * 100)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            'kb_id': self.kb_id,
            'name': self.name,
            'owner_id': self.owner_id,
            'owner_name': self.owner_name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'status': self.status.value,
            'total_files': self.total_files,
            'processed_files': self.processed_files,
            'failed_files': self.failed_files,
            'total_chunks': self.total_chunks,
            'files': self.files,
            'errors': self.errors
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KnowledgeBase':
        """Create from dictionary"""
        kb = cls(
            kb_id=data['kb_id'],
            name=data['name'],
            owner_id=data['owner_id'],
            owner_name=data['owner_name'],
            description=data.get('description', '')
        )
        
        kb.created_at = datetime.fromisoformat(data['created_at'])
        kb.updated_at = datetime.fromisoformat(data['updated_at'])
        kb.status = ProcessingStatus(data['status'])
        kb.total_files = data['total_files']
        kb.processed_files = data['processed_files']
        kb.failed_files = data['failed_files']
        kb.total_chunks = data['total_chunks']
        kb.files = data.get('files', [])
        kb.errors = data.get('errors', [])
        
        return kb


class KnowledgeBaseManager:
    """Manage all knowledge bases"""
    
    def __init__(self, storage_path: Path):
        """
        Initialize manager
        
        Args:
            storage_path: Path to store KB metadata
        """
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.kb_file = self.storage_path / "knowledge_bases.json"
        
        # Load existing KBs
        self.knowledge_bases: Dict[str, KnowledgeBase] = {}
        self._load()
    
    def create_kb(
        self,
        name: str,
        owner_id: str,
        owner_name: str,
        description: str = "",
        file_count: int = 0
    ) -> KnowledgeBase:
        """
        Create a new knowledge base
        
        Args:
            name: KB name
            owner_id: Discord user ID
            owner_name: Discord username
            description: Optional description
            file_count: Number of files to process
            
        Returns:
            Created knowledge base
        """
        # Generate unique ID
        kb_id = f"{owner_id}_{name.lower().replace(' ', '_')}_{int(datetime.now().timestamp())}"
        
        kb = KnowledgeBase(
            kb_id=kb_id,
            name=name,
            owner_id=owner_id,
            owner_name=owner_name,
            description=description
        )
        
        kb.total_files = file_count
        kb.update_status()
        
        self.knowledge_bases[kb_id] = kb
        self._save()
        
        return kb
    
    def get_kb(self, kb_id: str) -> Optional[KnowledgeBase]:
        """Get knowledge base by ID"""
        return self.knowledge_bases.get(kb_id)
    
    def get_user_kbs(self, owner_id: str) -> List[KnowledgeBase]:
        """Get all KBs for a user"""
        return [kb for kb in self.knowledge_bases.values() if kb.owner_id == owner_id]
    
    def find_kb_by_name(self, owner_id: str, name: str) -> Optional[KnowledgeBase]:
        """Find KB by owner and name"""
        for kb in self.knowledge_bases.values():
            if kb.owner_id == owner_id and kb.name.lower() == name.lower():
                return kb
        return None
    
    def update_kb(self, kb: KnowledgeBase):
        """Update and save KB"""
        kb.update_status()
        self.knowledge_bases[kb.kb_id] = kb
        self._save()
    
    def delete_kb(self, kb_id: str) -> bool:
        """Delete a knowledge base"""
        if kb_id in self.knowledge_bases:
            del self.knowledge_bases[kb_id]
            self._save()
            return True
        return False
    
    def _save(self):
        """Save KBs to disk"""
        data = {
            kb_id: kb.to_dict()
            for kb_id, kb in self.knowledge_bases.items()
        }
        
        with open(self.kb_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load(self):
        """Load KBs from disk"""
        if not self.kb_file.exists():
            return
        
        try:
            with open(self.kb_file, 'r') as f:
                data = json.load(f)
            
            self.knowledge_bases = {
                kb_id: KnowledgeBase.from_dict(kb_data)
                for kb_id, kb_data in data.items()
            }
        except Exception as e:
            print(f"⚠️ Error loading knowledge bases: {e}")