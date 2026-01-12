"""Experience retriever for learning from past projects"""
from typing import List, Dict, Optional, Any
from framework.memory.memory import Memory
import difflib


class ExperienceRetriever:
    """Retriever for storing and retrieving experiences"""
    
    def __init__(self, memory: Optional[Memory] = None, storage_path: str = "memory"):
        """
        Initialize Experience Retriever
        
        Args:
            memory: Optional Memory instance
            storage_path: Storage path for memory
        """
        self.memory = memory or Memory(storage_path=storage_path)
    
    async def store_experience(self, task: str, solution: str, result: Dict[str, Any], 
                              task_type: Optional[str] = None) -> str:
        """
        Store an experience
        
        Args:
            task: Task description
            solution: Solution/approach used
            result: Result dictionary (success, performance, etc.)
            task_type: Optional task type
            
        Returns:
            Key of stored experience
        """
        import hashlib
        key = f"exp_{hashlib.md5(task.encode()).hexdigest()[:8]}"
        
        metadata = {
            "type": "experience",
            "task": task,
            "task_type": task_type or "general",
            "result": result,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        }
        
        await self.memory.store(key, solution, metadata)
        return key
    
    async def retrieve(self, query: str, task_type: Optional[str] = None, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve similar experiences
        
        Args:
            query: Query string
            task_type: Optional task type filter
            limit: Maximum number of results
            
        Returns:
            List of similar experiences
        """
        # Get all experiences
        experiences = await self.memory.get_experience(task_type)
        
        if not experiences:
            return []
        
        # Calculate similarity
        query_lower = query.lower()
        scored_experiences = []
        
        for exp in experiences:
            task = exp.get("task", "").lower()
            solution = str(exp.get("solution", "")).lower()
            
            # Calculate similarity
            task_similarity = difflib.SequenceMatcher(None, query_lower, task).ratio()
            solution_similarity = difflib.SequenceMatcher(None, query_lower, solution[:len(query_lower) * 2]).ratio()
            
            # Combined similarity (weighted)
            similarity = (task_similarity * 0.7) + (solution_similarity * 0.3)
            
            scored_experiences.append({
                **exp,
                "similarity": similarity
            })
        
        # Sort by similarity
        scored_experiences.sort(key=lambda x: x.get("similarity", 0), reverse=True)
        return scored_experiences[:limit]
    
    async def get_best_practices(self, task_type: str) -> List[Dict[str, Any]]:
        """
        Get best practices for a task type
        
        Args:
            task_type: Task type
            
        Returns:
            List of best practices
        """
        experiences = await self.memory.get_experience(task_type)
        
        # Filter for successful experiences
        successful = [
            exp for exp in experiences
            if exp.get("result", {}).get("success", False)
        ]
        
        # Sort by result quality (if available)
        if successful:
            successful.sort(
                key=lambda x: x.get("result", {}).get("score", 0),
                reverse=True
            )
        
        return successful[:5]  # Top 5
    
    async def learn_from_experience(self, task: str, solution: str, 
                                   success: bool, performance: Optional[Dict[str, Any]] = None) -> str:
        """
        Learn from an experience and store it
        
        Args:
            task: Task description
            solution: Solution used
            success: Whether it was successful
            performance: Optional performance metrics
            
        Returns:
            Key of stored experience
        """
        result = {
            "success": success,
            "performance": performance or {},
            "score": 100 if success else 0
        }
        
        return await self.store_experience(task, solution, result)

