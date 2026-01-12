"""
Lesson 24: DevOps Engineer
==========================

This lesson demonstrates the DevOpsEngineer role for deployment.

Run this lesson:
    python lesson_24.py
"""
import sys
import os
import asyncio

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.roles.devops_engineer import DevOpsEngineer
from framework.llm import MockLLM


async def main():
    print("=" * 60)
    print("Lesson 24: DevOps Engineer")
    print("=" * 60)
    print()
    
    llm = MockLLM()
    devops = DevOpsEngineer(llm=llm)
    
    print("1. DevOps Engineer Role")
    print("-" * 60)
    print(f"Name: {devops.name}")
    print(f"Profile: {devops.profile}")
    print(f"Goal: {devops.goal}")
    print(f"Actions: {[a.name for a in devops.actions]}")
    print()
    
    project_info = "Flask REST API, Python 3.9, port 5000"
    dockerfile = await devops.create_dockerfile(project_info)
    print(f"Generated Dockerfile ({len(dockerfile)} chars)")
    print()
    
    print("=" * 60)
    print("Lesson 24 Complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

