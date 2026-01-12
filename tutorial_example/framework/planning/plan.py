"""Plan class for managing tasks"""
from typing import Dict, List, Optional
from datetime import datetime
from framework.planning.task import Task, TaskStatus


class Plan:
    """Plan containing multiple tasks with dependencies"""
    
    def __init__(self, goal: str = "", plan_id: str = ""):
        """
        Initialize a plan
        
        Args:
            goal: Goal of the plan
            plan_id: Unique identifier for the plan
        """
        self.goal = goal
        self.plan_id = plan_id or f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.tasks: Dict[str, Task] = {}
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def add_task(self, task: Task) -> bool:
        """
        Add a task to the plan
        
        Args:
            task: Task to add
            
        Returns:
            True if added successfully
        """
        if task.id in self.tasks:
            return False  # Task already exists
        
        self.tasks[task.id] = task
        self.updated_at = datetime.now()
        return True
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID"""
        return self.tasks.get(task_id)
    
    def remove_task(self, task_id: str) -> bool:
        """Remove a task from the plan"""
        if task_id not in self.tasks:
            return False
        
        # Remove this task from other tasks' dependencies
        for task in self.tasks.values():
            if task_id in task.dependencies:
                task.dependencies.remove(task_id)
        
        del self.tasks[task_id]
        self.updated_at = datetime.now()
        return True
    
    def get_next_tasks(self) -> List[Task]:
        """
        Get tasks that can be started (no incomplete dependencies)
        
        Returns:
            List of tasks ready to start
        """
        completed_ids = [
            task_id for task_id, task in self.tasks.items()
            if task.status == TaskStatus.COMPLETED
        ]
        
        next_tasks = []
        for task in self.tasks.values():
            if task.status == TaskStatus.PENDING and task.can_start(completed_ids):
                next_tasks.append(task)
        
        # Sort by priority (higher first)
        next_tasks.sort(key=lambda t: t.priority, reverse=True)
        return next_tasks
    
    def get_blocked_tasks(self) -> List[Task]:
        """Get tasks that are blocked"""
        blocked = []
        for task in self.tasks.values():
            if task.is_blocked(self.tasks):
                blocked.append(task)
        return blocked
    
    def get_progress(self) -> Dict[str, any]:
        """
        Get plan progress statistics
        
        Returns:
            Dict with progress metrics
        """
        total = len(self.tasks)
        if total == 0:
            return {
                "total": 0,
                "completed": 0,
                "in_progress": 0,
                "pending": 0,
                "blocked": 0,
                "completion_percentage": 0
            }
        
        completed = sum(1 for t in self.tasks.values() if t.status == TaskStatus.COMPLETED)
        in_progress = sum(1 for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS)
        pending = sum(1 for t in self.tasks.values() if t.status == TaskStatus.PENDING)
        blocked = sum(1 for t in self.tasks.values() if t.status == TaskStatus.BLOCKED)
        
        return {
            "total": total,
            "completed": completed,
            "in_progress": in_progress,
            "pending": pending,
            "blocked": blocked,
            "completion_percentage": (completed / total * 100) if total > 0 else 0
        }
    
    def mark_complete(self, task_id: str) -> bool:
        """
        Mark a task as completed
        
        Args:
            task_id: ID of task to complete
            
        Returns:
            True if successful
        """
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        task.complete()
        self.updated_at = datetime.now()
        return True
    
    def start_task(self, task_id: str) -> bool:
        """Start a task"""
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        if task.status == TaskStatus.PENDING:
            task.start()
            self.updated_at = datetime.now()
            return True
        return False
    
    def get_task_order(self) -> List[List[str]]:
        """
        Get tasks in execution order (considering dependencies)
        Uses topological sort
        
        Returns:
            List of task ID lists, each list can be executed in parallel
        """
        # Build dependency graph
        in_degree = {task_id: len(task.dependencies) for task_id, task in self.tasks.items()}
        graph = {task_id: [] for task_id in self.tasks.keys()}
        
        for task in self.tasks.values():
            for dep_id in task.dependencies:
                if dep_id in graph:
                    graph[dep_id].append(task.id)
        
        # Topological sort
        result = []
        queue = [task_id for task_id, degree in in_degree.items() if degree == 0]
        
        while queue:
            level = []
            next_queue = []
            
            for task_id in queue:
                level.append(task_id)
                for dependent_id in graph[task_id]:
                    in_degree[dependent_id] -= 1
                    if in_degree[dependent_id] == 0:
                        next_queue.append(dependent_id)
            
            if level:
                result.append(level)
            queue = next_queue
        
        return result
    
    def to_dict(self) -> Dict[str, any]:
        """Convert plan to dictionary"""
        return {
            "plan_id": self.plan_id,
            "goal": self.goal,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "tasks": {task_id: task.to_dict() for task_id, task in self.tasks.items()}
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> 'Plan':
        """Create plan from dictionary"""
        plan = cls(
            goal=data.get("goal", ""),
            plan_id=data.get("plan_id", "")
        )
        
        if data.get("created_at"):
            plan.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("updated_at"):
            plan.updated_at = datetime.fromisoformat(data["updated_at"])
        
        for task_id, task_data in data.get("tasks", {}).items():
            task = Task.from_dict(task_data)
            plan.add_task(task)
        
        return plan
    
    def __str__(self) -> str:
        """String representation"""
        progress = self.get_progress()
        return f"""Plan: {self.goal}
  ID: {self.plan_id}
  Progress: {progress['completed']}/{progress['total']} ({progress['completion_percentage']:.1f}%)
  Status: {progress['completed']} completed, {progress['in_progress']} in progress, {progress['pending']} pending, {progress['blocked']} blocked"""

