"""Project Manager role"""
from typing import List
from framework.role import Role
from framework.planning.write_tasks import WriteTasks


class ProjectManager(Role):
    """Project Manager role for task breakdown and project coordination"""
    
    def __init__(self, llm=None):
        super().__init__(
            name="ProjectManager",
            profile="Project Manager",
            goal="Break down tasks according to PRD/technical design, generate a task list, and analyze task dependencies",
            actions=[WriteTasks(llm=llm)],
            llm=llm
        )
    
    async def create_task_list(self, prd: str, design: str) -> List:
        """
        Create task list from PRD and design
        
        Args:
            prd: Product Requirement Document
            design: System design
            
        Returns:
            List of tasks
        """
        # Use WriteTasks action
        write_tasks_action = next((a for a in self.actions if isinstance(a, WriteTasks)), None)
        if write_tasks_action:
            from framework.schema import Message
            messages = [
                Message(content=prd, role="ProductManager", cause_by="WritePRD"),
                Message(content=design, role="Architect", cause_by="WriteDesign")
            ]
            result = await write_tasks_action.run(messages=messages)
            return result.instruct_content.get("tasks", [])
        return []
    
    async def track_progress(self) -> dict:
        """
        Track project progress
        
        Returns:
            Dict with progress information
        """
        # Get plan from context if available
        if hasattr(self, 'context') and "plans" in self.context:
            plans = self.context.get("plans", {})
            if plans:
                # Get the latest plan
                from framework.planning.plan import Plan
                latest_plan_id = list(plans.keys())[-1]
                plan_data = plans[latest_plan_id]
                plan = Plan.from_dict(plan_data)
                return plan.get_progress()
        
        return {
            "total": 0,
            "completed": 0,
            "in_progress": 0,
            "pending": 0,
            "blocked": 0,
            "completion_percentage": 0
        }

