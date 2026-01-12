"""Action for writing task lists"""
from typing import List
from framework.action import Action
from framework.schema import Message, ActionOutput
from framework.planning.planner import Planner
from framework.planning.task import Task


class WriteTasks(Action):
    """Action to write a task list from PRD and design"""
    
    def __init__(self, llm=None):
        super().__init__(name="WriteTasks", llm=llm)
        self.planner = Planner(llm=llm)
    
    async def run(self, messages: List[Message] = None, **kwargs) -> ActionOutput:
        """
        Generate task list from PRD and design
        
        Args:
            messages: Previous messages (should contain PRD and design)
            **kwargs: Additional parameters
            
        Returns:
            ActionOutput with task list
        """
        # Extract PRD and design from messages
        prd = ""
        design = ""
        
        if messages:
            for msg in messages:
                if msg.cause_by == "WritePRD":
                    prd = msg.content
                elif msg.cause_by == "WriteDesign":
                    design = msg.content
        
        # Combine PRD and design for goal
        goal = f"Implement project based on PRD and design:\n\nPRD:\n{prd}\n\nDesign:\n{design}"
        
        # Create plan
        plan = await self.planner.create_plan(goal, plan_id=f"tasks_{len(self.planner.plans) + 1}")
        
        # Format task list
        task_list = f"# Task List\n\n"
        task_list += f"Goal: {plan.goal}\n\n"
        task_list += f"Total Tasks: {len(plan.tasks)}\n\n"
        
        # Get task execution order
        task_order = plan.get_task_order()
        
        task_list += "## Tasks by Priority Order\n\n"
        for level, task_ids in enumerate(task_order, 1):
            task_list += f"### Level {level} (can be done in parallel)\n\n"
            for task_id in task_ids:
                task = plan.get_task(task_id)
                if task:
                    task_list += f"- [{task.status.value}] {task.description}\n"
                    if task.dependencies:
                        task_list += f"  - Depends on: {', '.join(task.dependencies)}\n"
                    if task.estimated_hours:
                        task_list += f"  - Estimated: {task.estimated_hours} hours\n"
                    task_list += "\n"
        
        # Store plan in context
        if "plans" not in self.context:
            self.context["plans"] = {}
        self.context["plans"][plan.plan_id] = plan.to_dict()
        
        return ActionOutput(
            content=task_list,
            instruct_content={
                "type": "task_list",
                "plan_id": plan.plan_id,
                "tasks": [task.to_dict() for task in plan.tasks.values()],
                "task_count": len(plan.tasks)
            }
        )

