"""
Lesson 21: Complete Workflow
============================

This lesson demonstrates the complete end-to-end workflow.

Run this lesson:
    python lesson_21.py
"""
import sys
import os
import asyncio

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.team import Team
from framework.roles.product_manager import ProductManager
from framework.roles.architect import Architect
from framework.roles.engineer import Engineer
from framework.llm import get_llm


async def main():
    print("=" * 60)
    print("Lesson 21: Complete Workflow")
    print("=" * 60)
    print()
    
    llm = get_llm(
        local_model_path="EMPTY", #"./HF_MODELS/Meta-Llama-3-8B-Instruct-GGUF/Meta-Llama-3-8B-Instruct.Q3_K_M.gguf",
        vllm_base_url="http://localhost:8000/v1",
        vllm_model="codellama/CodeLlama-7b-Instruct-hf"
    )
    team = Team()
    
    team.hire([
        ProductManager(llm=llm),
        Architect(llm=llm),
        Engineer(llm=llm),
    ])
    
    idea = "Create a simple todo list application"
    print(f"Idea: {idea}")
    print()
    
    result = await team.run(idea, n_round=5)
    
    print("\nResults:")
    if "code" in result:
        print("✓ Code generated")
    if "prd" in result:
        print("✓ PRD created")
    if "design" in result:
        print("✓ Design created")
    
    print("\n" + "=" * 60)
    print("Lesson 21 Complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

