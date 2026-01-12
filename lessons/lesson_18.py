"""
Lesson 18: Project Manager
===========================

This lesson demonstrates the ProjectManager role for task management.

Run this lesson:
    python lesson_18.py
"""
import sys
import os
import asyncio

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.roles.project_manager import ProjectManager
from framework.llm import get_llm


async def main():
    print("=" * 60)
    print("Lesson 18: Project Manager")
    print("=" * 60)
    print()
    
    llm = get_llm(
        local_model_path="EMPTY", #"./HF_MODELS/Meta-Llama-3-8B-Instruct-GGUF/Meta-Llama-3-8B-Instruct.Q3_K_M.gguf",
        vllm_base_url="http://localhost:8000/v1",
        vllm_model="codellama/CodeLlama-7b-Instruct-hf"
    )
    pm = ProjectManager(llm=llm)
    
    print("1. Project Manager Role")
    print("-" * 60)
    print(f"Name: {pm.name}")
    print(f"Profile: {pm.profile}")
    print(f"Goal: {pm.goal}")
    print(f"Actions: {[a.name for a in pm.actions]}")
    print()
    
    print("=" * 60)
    print("Lesson 18 Complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

