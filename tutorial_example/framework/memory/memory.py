"""Memory system for persistent storage"""
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import difflib


class Memory:
    """Long-term memory for storing and retrieving information"""
    
    def __init__(self, storage_path: str = "memory"):
        """
        Initialize Memory system
        
        Args:
            storage_path: Directory path for storing memory
        """
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.memory_file = self.storage_path / "memory.json"
        self._memory: Dict[str, Any] = {}
        self._load()
    
    def _load(self):
        """Load memory from disk"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    self._memory = json.load(f)
            except Exception:
                self._memory = {}
        else:
            self._memory = {}
    
    def _save(self):
        """Save memory to disk"""
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self._memory, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving memory: {e}")
    
    async def store(self, key: str, value: Any, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Store a value in memory
        
        Args:
            key: Key to store under
            value: Value to store
            metadata: Optional metadata
            
        Returns:
            True if successful
        """
        entry = {
            "value": value,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat(),
            "key": key
        }
        
        self._memory[key] = entry
        self._save()
        return True
    
    async def retrieve(self, key: str) -> Optional[Any]:
        """
        Retrieve a value from memory
        
        Args:
            key: Key to retrieve
            
        Returns:
            Stored value or None
        """
        entry = self._memory.get(key)
        if entry:
            return entry.get("value")
        return None
    
    async def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search memory by query string
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of matching entries
        """
        results = []
        query_lower = query.lower()
        
        for key, entry in self._memory.items():
            value = entry.get("value", "")
            metadata = entry.get("metadata", {})
            
            # Search in key, value, and metadata
            search_text = f"{key} {value} {json.dumps(metadata)}".lower()
            
            if query_lower in search_text:
                # Calculate similarity
                similarity = difflib.SequenceMatcher(None, query_lower, search_text[:len(query_lower) * 2]).ratio()
                
                results.append({
                    "key": key,
                    "value": value,
                    "metadata": metadata,
                    "timestamp": entry.get("timestamp"),
                    "similarity": similarity
                })
        
        # Sort by similarity
        results.sort(key=lambda x: x.get("similarity", 0), reverse=True)
        return results[:limit]
    
    async def get_experience(self, task_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get experiences by task type
        
        Args:
            task_type: Optional task type filter
            
        Returns:
            List of experiences
        """
        experiences = []
        
        for key, entry in self._memory.items():
            metadata = entry.get("metadata", {})
            entry_task_type = metadata.get("task_type")
            
            if task_type is None or entry_task_type == task_type:
                if metadata.get("type") == "experience":
                    experiences.append({
                        "key": key,
                        "task": metadata.get("task", ""),
                        "solution": entry.get("value", ""),
                        "result": metadata.get("result", {}),
                        "timestamp": entry.get("timestamp")
                    })
        
        # Sort by timestamp (newest first)
        experiences.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return experiences
    
    async def delete(self, key: str) -> bool:
        """Delete an entry from memory"""
        if key in self._memory:
            del self._memory[key]
            self._save()
            return True
        return False
    
    async def list_keys(self, pattern: Optional[str] = None) -> List[str]:
        """
        List all keys in memory
        
        Args:
            pattern: Optional pattern to filter keys
            
        Returns:
            List of keys
        """
        keys = list(self._memory.keys())
        
        if pattern:
            import re
            pattern_re = re.compile(pattern.replace('*', '.*'))
            keys = [k for k in keys if pattern_re.search(k)]
        
        return sorted(keys)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        return {
            "total_entries": len(self._memory),
            "storage_path": str(self.storage_path),
            "memory_file": str(self.memory_file),
            "file_size": self.memory_file.stat().st_size if self.memory_file.exists() else 0
        }
    
    def clear(self):
        """Clear all memory"""
        self._memory = {}
        self._save()

