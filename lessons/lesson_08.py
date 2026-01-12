"""
Lesson 08: Complete Software Company Workflow
==============================================

This lesson demonstrates the complete workflow from idea to code
using the multi-agent framework.

Run this lesson:
    python lesson_08.py
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
    print("Lesson 08: Complete Software Company Workflow")
    print("=" * 60)
    print()
    
    # 1. Initialize team
    print("1. Initializing Team")
    print("-" * 60)
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
    
    team.invest(100.0)
    print(f"Team created with {len(team.environment.get_all_roles())} roles")
    print(f"Investment: ${team.investment}")
    print()
    
    # 2. Define project idea
    print("2. Project Idea")
    print("-" * 60)
    idea = "Create a simple todo list application that allows users to add, remove, and mark tasks as complete"
    print(f"Idea: {idea}")
    print()
    
    # 3. Run the workflow
    print("3. Running Workflow")
    print("-" * 60)
    print("Workflow steps:")
    print("  1. User → ProductManager: Requirement")
    print("  2. ProductManager → Architect: PRD")
    print("  3. Architect → Engineer: Design")
    print("  4. Engineer → Final: Code")
    print()
    
    result = await team.run(idea, n_round=5)
    print()
    
    # 4. Display results
    print("4. Results")
    print("-" * 60)
    if "prd" in result:
        print("✓ PRD Generated")
        print(f"  Preview: {result['prd'][:150]}...")
        print()
    
    if "design" in result:
        print("✓ Design Generated")
        print(f"  Preview: {result['design'][:150]}...")
        print()
    
    if "code" in result:
        print("✓ Code Generated")
        print(f"  Preview: {result['code'][:150]}...")
        print()
    
    # 5. Message statistics
    print("5. Message Statistics")
    print("-" * 60)
    print(f"Total messages: {len(team.environment.message_history)}")
    print(f"Rounds executed: {team.current_round + 1}")
    
    # Count messages by role
    role_counts = {}
    for msg in team.environment.message_history:
        role_counts[msg.role] = role_counts.get(msg.role, 0) + 1
    
    print("\nMessages by role:")
    for role, count in role_counts.items():
        print(f"  {role}: {count}")
    print()
    
    # 6. Workflow summary
    print("6. Workflow Summary")
    print("-" * 60)
    print("Complete workflow executed:")
    print("  ✓ Requirement received")
    print("  ✓ PRD created")
    print("  ✓ Design created")
    print("  ✓ Code generated")
    print()
    
    print("=" * 60)
    print("Lesson 08 Complete!")
    print("=" * 60)
    print()
    print("Key Takeaways:")
    print("- Teams orchestrate the complete workflow")
    print("- Roles work together to transform idea to code")
    print("- Messages flow between roles automatically")
    print("- The framework handles the entire process")


if __name__ == "__main__":
    asyncio.run(main())

