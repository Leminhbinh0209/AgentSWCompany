"""
Lesson 17: Planning
===================

This lesson demonstrates the Planner for task planning and management.

Run this lesson:
    python lesson_17.py
"""
import sys
import os
import asyncio

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.planning.planner import Planner
from framework.planning.task import Task, TaskStatus
from framework.planning.plan import Plan
from framework.llm import MockLLM


async def main():
    print("=" * 60)
    print("Lesson 17: Planning")
    print("=" * 60)
    print()
    
    planner = Planner(llm=MockLLM())
    
    # Create a plan
    print("1. Creating a Plan")
    print("-" * 60)
    goal = "Create a calculator application"
    plan = await planner.create_plan(goal)
    print(f"Plan created with {len(plan.tasks)} tasks")
    for i, task in enumerate(plan.tasks[:3], 1):
        print(f"  {i}. {task.description[:50]}...")
    print()
    
    print("=" * 60)
    print("Lesson 17 Complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

