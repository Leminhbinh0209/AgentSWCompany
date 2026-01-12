"""Task class for representing individual tasks"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    """Task status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


@dataclass
class Task:
    """Represents a single task in a plan"""
    
    id: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    dependencies: List[str] = field(default_factory=list)
    assigned_to: Optional[str] = None
    priority: int = 5  # 1-10, higher is more important
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def can_start(self, completed_tasks: List[str]) -> bool:
        """
        Check if task can start (all dependencies completed)
        
        Args:
            completed_tasks: List of completed task IDs
            
        Returns:
            True if all dependencies are completed
        """
        if not self.dependencies:
            return True
        return all(dep_id in completed_tasks for dep_id in self.dependencies)
    
    def is_blocked(self, all_tasks: Dict[str, 'Task']) -> bool:
        """
        Check if task is blocked by incomplete dependencies
        
        Args:
            all_tasks: Dictionary of all tasks by ID
            
        Returns:
            True if blocked by dependencies
        """
        if not self.dependencies:
            return False
        
        for dep_id in self.dependencies:
            if dep_id not in all_tasks:
                return True  # Dependency doesn't exist
            dep_task = all_tasks[dep_id]
            if dep_task.status != TaskStatus.COMPLETED:
                return True  # Dependency not completed
        
        return False
    
    def start(self):
        """Mark task as in progress"""
        if self.status == TaskStatus.PENDING:
            self.status = TaskStatus.IN_PROGRESS
            self.started_at = datetime.now()
    
    def complete(self):
        """Mark task as completed"""
        if self.status == TaskStatus.IN_PROGRESS:
            self.status = TaskStatus.COMPLETED
            self.completed_at = datetime.now()
    
    def block(self):
        """Mark task as blocked"""
        self.status = TaskStatus.BLOCKED
    
    def unblock(self):
        """Unblock task (set to pending)"""
        if self.status == TaskStatus.BLOCKED:
            self.status = TaskStatus.PENDING
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary"""
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status.value,
            "dependencies": self.dependencies,
            "assigned_to": self.assigned_to,
            "priority": self.priority,
            "estimated_hours": self.estimated_hours,
            "actual_hours": self.actual_hours,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create task from dictionary"""
        task = cls(
            id=data["id"],
            description=data["description"],
            status=TaskStatus(data.get("status", "pending")),
            dependencies=data.get("dependencies", []),
            assigned_to=data.get("assigned_to"),
            priority=data.get("priority", 5),
            estimated_hours=data.get("estimated_hours"),
            actual_hours=data.get("actual_hours"),
            metadata=data.get("metadata", {})
        )
        
        if data.get("created_at"):
            task.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("started_at"):
            task.started_at = datetime.fromisoformat(data["started_at"])
        if data.get("completed_at"):
            task.completed_at = datetime.fromisoformat(data["completed_at"])
        
        return task
    
    def __str__(self) -> str:
        """String representation"""
        status_icon = {
            TaskStatus.PENDING: "⏳",
            TaskStatus.IN_PROGRESS: "🔄",
            TaskStatus.COMPLETED: "✅",
            TaskStatus.BLOCKED: "🚫",
            TaskStatus.CANCELLED: "❌"
        }
        icon = status_icon.get(self.status, "❓")
        deps = f" (depends on: {', '.join(self.dependencies)})" if self.dependencies else ""
        return f"{icon} [{self.id}] {self.description}{deps}"

