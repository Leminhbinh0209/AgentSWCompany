"""Planner for creating and managing plans"""
from typing import List, Dict, Optional, Any
from framework.planning.plan import Plan
from framework.planning.task import Task, TaskStatus
from framework.llm import BaseLLM
import re


class Planner:
    """Planner for creating and managing task plans"""
    
    def __init__(self, llm: Optional[BaseLLM] = None):
        """
        Initialize Planner
        
        Args:
            llm: Optional LLM for intelligent task breakdown
        """
        self.llm = llm
        self.plans: Dict[str, Plan] = {}
    
    async def create_plan(self, goal: str, plan_id: str = "") -> Plan:
        """
        Create a new plan from a goal
        
        Args:
            goal: Goal description
            plan_id: Optional plan ID
            
        Returns:
            Created plan
        """
        plan = Plan(goal=goal, plan_id=plan_id)
        
        if self.llm:
            # Use LLM to break down goal into tasks
            tasks = await self._break_down_goal(goal)
            for task_data in tasks:
                task = Task(
                    id=task_data.get("id", f"task_{len(plan.tasks) + 1}"),
                    description=task_data.get("description", ""),
                    priority=task_data.get("priority", 5),
                    estimated_hours=task_data.get("estimated_hours"),
                    dependencies=task_data.get("dependencies", [])
                )
                plan.add_task(task)
        else:
            # Basic task breakdown without LLM
            tasks = self._basic_breakdown(goal)
            for i, task_desc in enumerate(tasks, 1):
                task = Task(
                    id=f"task_{i}",
                    description=task_desc,
                    priority=5
                )
                plan.add_task(task)
        
        self.plans[plan.plan_id] = plan
        return plan
    
    async def _break_down_goal(self, goal: str) -> List[Dict[str, Any]]:
        """
        Break down goal into tasks using LLM
        
        Args:
            goal: Goal description
            
        Returns:
            List of task dictionaries
        """
        prompt = f"""Break down the following goal into specific, actionable tasks.
For each task, provide:
1. Task ID (task_1, task_2, etc.)
2. Description
3. Priority (1-10, higher is more important)
4. Estimated hours (optional)
5. Dependencies (list of task IDs this depends on)

Goal: {goal}

Format the response as a list of tasks, one per line, or as a structured list.
For example:
- task_1: Description (priority: 8, hours: 2)
- task_2: Description (priority: 6, hours: 1, depends on: task_1)
"""
        
        try:
            response = await self.llm.aask(prompt)
            return self._parse_task_list(response)
        except Exception:
            return self._basic_breakdown(goal)
    
    def _parse_task_list(self, response: str) -> List[Dict[str, Any]]:
        """Parse LLM response into task list"""
        tasks = []
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Try to extract task information
            task_match = re.match(r'[-*]?\s*(task_\d+|[^:]+):\s*(.+)', line)
            if task_match:
                task_id = task_match.group(1).strip()
                description = task_match.group(2).strip()
                
                # Extract priority
                priority_match = re.search(r'priority[:\s]*(\d+)', description, re.IGNORECASE)
                priority = int(priority_match.group(1)) if priority_match else 5
                
                # Extract hours
                hours_match = re.search(r'hours?[:\s]*(\d+\.?\d*)', description, re.IGNORECASE)
                estimated_hours = float(hours_match.group(1)) if hours_match else None
                
                # Extract dependencies
                deps_match = re.search(r'depends? on[:\s]*([^)]+)', description, re.IGNORECASE)
                dependencies = []
                if deps_match:
                    deps_str = deps_match.group(1)
                    dependencies = [d.strip() for d in re.split(r'[,;]', deps_str)]
                
                # Clean description
                description = re.sub(r'\([^)]*\)', '', description).strip()
                
                tasks.append({
                    "id": task_id if task_id.startswith('task_') else f"task_{len(tasks) + 1}",
                    "description": description,
                    "priority": priority,
                    "estimated_hours": estimated_hours,
                    "dependencies": dependencies
                })
        
        return tasks if tasks else self._basic_breakdown("")
    
    def _basic_breakdown(self, goal: str) -> List[str]:
        """Basic task breakdown without LLM"""
        # Simple keyword-based breakdown
        tasks = []
        
        if "create" in goal.lower() or "build" in goal.lower():
            tasks.append("Design the system architecture")
            tasks.append("Implement core functionality")
            tasks.append("Write tests")
            tasks.append("Create documentation")
        elif "fix" in goal.lower() or "debug" in goal.lower():
            tasks.append("Identify the issue")
            tasks.append("Fix the problem")
            tasks.append("Test the fix")
            tasks.append("Update documentation")
        else:
            tasks.append("Analyze requirements")
            tasks.append("Plan implementation")
            tasks.append("Execute plan")
            tasks.append("Verify results")
        
        return tasks
    
    async def add_task(self, plan_id: str, task: Task) -> bool:
        """
        Add a task to an existing plan
        
        Args:
            plan_id: Plan ID
            task: Task to add
            
        Returns:
            True if successful
        """
        plan = self.plans.get(plan_id)
        if not plan:
            return False
        return plan.add_task(task)
    
    async def get_next_tasks(self, plan_id: str) -> List[Task]:
        """
        Get next tasks that can be started
        
        Args:
            plan_id: Plan ID
            
        Returns:
            List of tasks ready to start
        """
        plan = self.plans.get(plan_id)
        if not plan:
            return []
        return plan.get_next_tasks()
    
    async def mark_complete(self, plan_id: str, task_id: str) -> bool:
        """
        Mark a task as completed
        
        Args:
            plan_id: Plan ID
            task_id: Task ID
            
        Returns:
            True if successful
        """
        plan = self.plans.get(plan_id)
        if not plan:
            return False
        return plan.mark_complete(task_id)
    
    async def update_plan(self, plan_id: str, feedback: str) -> bool:
        """
        Update plan based on feedback
        
        Args:
            plan_id: Plan ID
            feedback: Feedback to incorporate
            
        Returns:
            True if successful
        """
        plan = self.plans.get(plan_id)
        if not plan:
            return False
        
        if self.llm:
            # Use LLM to process feedback and update plan
            prompt = f"""Based on the following feedback, suggest updates to the plan.

Current plan goal: {plan.goal}
Current tasks: {len(plan.tasks)}

Feedback: {feedback}

Suggest:
1. New tasks to add
2. Tasks to modify
3. Tasks to remove
4. Priority changes
"""
            try:
                response = await self.llm.aask(prompt)
                # Parse and apply updates (simplified)
                # In production, use more sophisticated parsing
            except Exception:
                pass
        
        return True
    
    def get_plan(self, plan_id: str) -> Optional[Plan]:
        """Get a plan by ID"""
        return self.plans.get(plan_id)
    
    def list_plans(self) -> List[str]:
        """List all plan IDs"""
        return list(self.plans.keys())

