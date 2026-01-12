"""
Lesson 05: Understanding Teams
================================

This lesson introduces the Team class, which orchestrates multiple
roles to work together on a project.

Run this lesson:
    python lesson_05.py
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
    print("Lesson 05: Understanding Teams")
    print("=" * 60)
    print()
    
    # 1. Create a team
    print("1. Creating a Team")
    print("-" * 60)
    team = Team()
    print(f"Team created")
    print(f"Investment: ${team.investment}")
    print(f"Max rounds: {team.max_rounds}")
    print()
    
    # 2. Hire roles
    print("2. Hiring Roles")
    print("-" * 60)
    llm = get_llm(
        local_model_path="EMPTY", #"./HF_MODELS/Meta-Llama-3-8B-Instruct-GGUF/Meta-Llama-3-8B-Instruct.Q3_K_M.gguf",
        vllm_base_url="http://localhost:8000/v1",
        vllm_model="codellama/CodeLlama-7b-Instruct-hf"
    )
    team.hire([
        ProductManager(llm=llm),
        Architect(llm=llm),
        Engineer(llm=llm),
    ])
    roles = team.environment.get_all_roles()
    print(f"Hired {len(roles)} roles:")
    for role in roles:
        print(f"  - {role.name}: {role.profile}")
    print()
    
    # 3. Set investment
    print("3. Setting Investment")
    print("-" * 60)
    team.invest(100.0)
    print(f"Investment set to: ${team.investment}")
    print()
    
    # 4. Run team with an idea
    print("4. Running Team with an Idea")
    print("-" * 60)
    idea = "Create a simple greeting application"
    print(f"Idea: {idea}")
    print()
    
    result = await team.run(idea, n_round=5)
    print()
    
    # 5. Check results
    print("5. Checking Results")
    print("-" * 60)
    if "code" in result:
        print("✓ Code generated!")
        print(f"Code preview: {result['code'][:200]}...")
    if "prd" in result:
        print("✓ PRD created!")
    if "design" in result:
        print("✓ Design created!")
    print()
    
    # 6. Message history
    print("6. Message History")
    print("-" * 60)
    print(f"Total messages: {len(team.environment.message_history)}")
    print(f"Rounds executed: {team.current_round + 1}")
    print()
    
    print("=" * 60)
    print("Lesson 05 Complete!")
    print("=" * 60)
    print()
    print("Key Takeaways:")
    print("- Teams orchestrate multiple roles")
    print("- Teams manage the workflow from idea to code")
    print("- Teams track rounds and message history")
    print("- Teams provide context for all roles")


if __name__ == "__main__":
    asyncio.run(main())

