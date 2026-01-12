"""
Lesson 28: Context System
==========================

This lesson demonstrates the Context system for managing project state,
configuration, and costs.

Run this lesson:
    python lesson_28.py
"""
import sys
import os
import asyncio
from pathlib import Path

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.context import Context, AttrDict
from framework.config import Config


async def main():
    print("=" * 80)
    print("Lesson 28: Context System")
    print("=" * 80)
    print()
    
    print("The Context system manages project state, configuration, and costs.")
    print("It's the foundation for advanced features like cost tracking and")
    print("project path management.")
    print()
    
    # 1. Creating Context
    print("1. Creating Context")
    print("-" * 80)
    ctx = Context()
    print("✓ Context created")
    print(f"  - Cost manager initialized: {ctx.cost_manager is not None}")
    print(f"  - Config initialized: {ctx.config is not None}")
    print()
    
    # 2. Using AttrDict (kwargs)
    print("2. Using AttrDict for Project Data")
    print("-" * 80)
    # AttrDict allows attribute-style access
    ctx.kwargs.set("project_name", "MyProject")
    ctx.kwargs.set("version", "1.0.0")
    ctx.kwargs.set("author", "Developer")
    
    print(f"✓ Project data stored:")
    print(f"  - Project name: {ctx.kwargs.get('project_name')}")
    print(f"  - Version: {ctx.kwargs.get('version')}")
    print(f"  - Author: {ctx.kwargs.get('author')}")
    
    # Attribute-style access
    print(f"\n✓ Attribute-style access:")
    print(f"  - ctx.kwargs.project_name = {ctx.kwargs.project_name}")
    print()
    
    # 3. Project Path Management
    print("3. Project Path Management")
    print("-" * 80)
    project_path = "lesson_28_project"
    ctx.set_project_path(project_path)
    
    retrieved_path = ctx.get_project_path()
    print(f"✓ Project path set: {retrieved_path}")
    print(f"  - Directory created: {Path(project_path).exists()}")
    print()
    
    # 4. Cost Manager Integration
    print("4. Cost Manager Integration")
    print("-" * 80)
    ctx.cost_manager.max_budget = 10.0
    ctx.cost_manager.add_cost(0.5, role="ProductManager", action="WritePRD")
    ctx.cost_manager.add_cost(0.3, role="Architect", action="WriteDesign")
    
    print(f"✓ Costs tracked:")
    print(f"  - Total cost: ${ctx.cost_manager.total_cost:.2f}")
    print(f"  - Budget: ${ctx.cost_manager.max_budget:.2f}")
    print(f"  - Remaining: ${ctx.cost_manager.get_remaining_budget():.2f}")
    print(f"  - Transactions: {len(ctx.cost_manager.cost_history)}")
    print()
    
    # 5. Serialization
    print("5. Context Serialization")
    print("-" * 80)
    serialized = ctx.serialize()
    print(f"✓ Context serialized:")
    print(f"  - Keys: {list(serialized.keys())}")
    print(f"  - Project data: {list(serialized['kwargs'].keys())}")
    
    # Deserialize
    new_ctx = Context()
    new_ctx.deserialize(serialized)
    print(f"✓ Context deserialized:")
    print(f"  - Project name: {new_ctx.kwargs.get('project_name')}")
    print(f"  - Total cost: ${new_ctx.cost_manager.total_cost:.2f}")
    print()
    
    # 6. Integration with Config
    print("6. Integration with Configuration")
    print("-" * 80)
    config = Config.default()
    ctx_with_config = Context(config=config)
    
    print(f"✓ Context with config:")
    print(f"  - LLM model: {ctx_with_config.config.llm.model}")
    print(f"  - Workspace: {ctx_with_config.config.workspace}")
    print()
    
    print("=" * 80)
    print("Lesson 28 Complete!")
    print("=" * 80)
    print()
    print("Key Takeaways:")
    print("- Context manages project state, config, and costs")
    print("- AttrDict provides attribute-style access to data")
    print("- Project paths are automatically created")
    print("- Cost manager tracks all expenses")
    print("- Context can be serialized and recovered")
    print()
    print(f"Please manually clear the workspace folder when done:")
    print(f"  {os.path.abspath(project_path)}")


if __name__ == "__main__":
    asyncio.run(main())

