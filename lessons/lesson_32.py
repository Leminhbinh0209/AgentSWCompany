"""
Lesson 32: Serialization and State Management
==============================================

This lesson demonstrates how to save and load team state using serialization,
enabling project recovery and state persistence.

Run this lesson:
    python lesson_32.py
"""
import sys
import os
import asyncio
from pathlib import Path

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.team import Team
from framework.context import Context
from framework.roles.product_manager import ProductManager
from framework.roles.architect import Architect
from framework.roles.engineer import Engineer
from framework.llm import get_llm


async def main():
    print("=" * 80)
    print("Lesson 32: Serialization and State Management")
    print("=" * 80)
    print()
    
    print("Serialization allows you to save team state and recover it later.")
    print("This enables project recovery, state persistence, and workflow resumption.")
    print()
    
    # 1. Creating Team with State
    print("1. Creating Team with State")
    print("-" * 80)
    ctx = Context()
    ctx.set_project_path("lesson_32_project")
    ctx.kwargs.set("project_name", "TestProject")
    ctx.kwargs.set("version", "1.0.0")
    
    llm = get_llm(
        local_model_path="EMPTY",
        vllm_base_url="http://localhost:8000/v1",
        vllm_model="codellama/CodeLlama-7b-Instruct-hf"
    )
    
    team = Team(context=ctx)
    team.hire([
        ProductManager(llm=llm),
        Architect(llm=llm),
        Engineer(llm=llm),
    ])
    team.invest(10.0)
    team.idea = "Create a simple application"
    
    # Add some costs
    team.context.cost_manager.add_cost(0.5, role="ProductManager", action="WritePRD")
    
    print(f"✓ Team created")
    print(f"  - Idea: {team.idea}")
    print(f"  - Investment: ${team.investment:.2f}")
    print(f"  - Roles: {len(team.environment.roles)}")
    print(f"  - Project path: {ctx.get_project_path()}")
    print()
    
    # 2. Serializing Team
    print("2. Serializing Team State")
    print("-" * 80)
    storage_path = Path("./storage/lesson_32_team")
    team.serialize(storage_path)
    
    print(f"✓ Team serialized to: {storage_path}")
    print(f"  - Team file: {storage_path / 'team.json'}")
    print(f"  - File exists: {(storage_path / 'team.json').exists()}")
    print()
    
    # 3. Deserializing Team
    print("3. Deserializing Team State")
    print("-" * 80)
    new_ctx = Context()
    recovered_team = Team.deserialize(storage_path, context=new_ctx)
    
    print(f"✓ Team recovered from storage")
    print(f"  - Idea: {recovered_team.idea}")
    print(f"  - Investment: ${recovered_team.investment:.2f}")
    print(f"  - Roles: {len(recovered_team.environment.roles)}")
    print(f"  - Current round: {recovered_team.current_round}")
    print()
    
    # 4. Verifying State Recovery
    print("4. Verifying State Recovery")
    print("-" * 80)
    print("✓ Context state:")
    print(f"  - Project name: {recovered_team.context.kwargs.get('project_name')}")
    print(f"  - Version: {recovered_team.context.kwargs.get('version')}")
    print(f"  - Project path: {recovered_team.context.get_project_path()}")
    print()
    print("✓ Cost state:")
    print(f"  - Total cost: ${recovered_team.cost_manager.total_cost:.2f}")
    print(f"  - Budget: ${recovered_team.cost_manager.max_budget:.2f}")
    print(f"  - Transactions: {len(recovered_team.cost_manager.cost_history)}")
    print()
    
    # 5. Continuing Workflow
    print("5. Continuing Workflow from Saved State")
    print("-" * 80)
    print("You can continue the workflow from where it left off:")
    print("  - Recover team from storage")
    print("  - Continue running rounds")
    print("  - All state is preserved")
    print()
    
    # 6. Use Cases
    print("6. Use Cases for Serialization")
    print("-" * 80)
    print("✓ Project recovery after interruption")
    print("✓ State persistence across sessions")
    print("✓ Workflow resumption")
    print("✓ Team state backup")
    print("✓ Long-running project management")
    print()
    
    print("=" * 80)
    print("Lesson 32 Complete!")
    print("=" * 80)
    print()
    print("Key Takeaways:")
    print("- Serialization saves complete team state")
    print("- Deserialization recovers all state")
    print("- Context, costs, and team info are preserved")
    print("- Enables project recovery and resumption")
    print("- Essential for long-running projects")
    print()
    print(f"Please manually clear the storage folder when done:")
    print(f"  {os.path.abspath(storage_path)}")


if __name__ == "__main__":
    asyncio.run(main())

