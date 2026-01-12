"""
Lesson 34: generate_repo() - Complete Software Company
=======================================================

This lesson demonstrates the generate_repo() function for fully automated
project generation, similar to MetaGPT's metagpt command.

Run this lesson:
    python lesson_34.py
"""
import sys
import os
import asyncio

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.software_company import generate_repo, generate_repo_async


async def main():
    print("=" * 80)
    print("Lesson 34: generate_repo() - Complete Software Company")
    print("=" * 80)
    print()
    
    print("generate_repo() is the main entry point for fully automated")
    print("project generation. It combines all components: Context, Team,")
    print("TeamLeader, Cost Management, and more!")
    print()
    
    # 1. Simple Usage (Like MetaGPT)
    print("1. Simple Usage (Like MetaGPT)")
    print("-" * 80)
    idea = "Create a simple todo list application"
    
    print(f"Idea: {idea}")
    print("\nGenerating project with generate_repo()...")
    print("(This is like: metagpt 'Create a todo list application')")
    print()
    
    try:
        project_path = generate_repo(
            idea=idea,
            investment=10.0,
            n_round=6,
            project_name="todo_app"
        )
        print(f"✓ Project generated!")
        print(f"  - Project path: {project_path}")
    except Exception as e:
        print(f"⚠ Note: {e}")
        print("  (This is expected if LLM server is not running)")
    print()
    
    # 2. Async Version
    print("2. Async Version")
    print("-" * 80)
    print("For async workflows, use generate_repo_async():")
    print()
    print("  project_path = await generate_repo_async(")
    print("      idea='Create a calculator',")
    print("      investment=10.0,")
    print("      n_round=8")
    print("  )")
    print()
    
    # 3. With All Options
    print("3. With All Options")
    print("-" * 80)
    print("generate_repo() supports many options:")
    print("""
project_path = generate_repo(
    idea="Create a game",
    investment=15.0,          # Budget
    n_round=10,              # Number of rounds
    project_name="my_game",  # Project name
    project_path="workspace/my_game",  # Custom path
    recover_path=None,       # Recover from saved state
    llm=custom_llm           # Custom LLM
)
""")
    print()
    
    # 4. What generate_repo() Does
    print("4. What generate_repo() Does Automatically")
    print("-" * 80)
    print("✓ Creates Context with configuration")
    print("✓ Creates Team with Context")
    print("✓ Hires TeamLeader, ProductManager, Architect, Engineer")
    print("✓ Sets investment and budget")
    print("✓ Runs workflow automatically")
    print("✓ Manages project path")
    print("✓ Returns project path")
    print()
    
    # 5. Comparison with Manual Approach
    print("5. Comparison: Manual vs generate_repo()")
    print("-" * 80)
    print("MANUAL APPROACH (many steps):")
    print("""
ctx = Context()
team = Team(context=ctx)
team.hire([TeamLeader(), ProductManager(), Architect(), Engineer()])
team.invest(10.0)
result = await team.run(idea="...", n_round=8)
""")
    print()
    print("generate_repo() APPROACH (one line):")
    print("""
project_path = generate_repo("Create a calculator")
""")
    print()
    
    # 6. Integration with All Features
    print("6. Integration with All Features")
    print("-" * 80)
    print("generate_repo() integrates:")
    print("  ✓ Context system for state management")
    print("  ✓ Cost management for budget tracking")
    print("  ✓ TeamLeader for coordination")
    print("  ✓ Environment.run() for automatic workflow")
    print("  ✓ Project path management")
    print("  ✓ Serialization support (via recover_path)")
    print()
    
    # 7. Building CLI Tools
    print("7. Building CLI Tools")
    print("-" * 80)
    print("generate_repo() is perfect for CLI tools:")
    print("""
# In your CLI tool:
def main():
    idea = sys.argv[1]
    project_path = generate_repo(idea)
    print(f"Project created at: {project_path}")

# Usage: python my_tool.py "Create a calculator"
""")
    print()
    
    print("=" * 80)
    print("Lesson 34 Complete!")
    print("=" * 80)
    print()
    print("Key Takeaways:")
    print("- generate_repo() is the main entry point")
    print("- It combines all components automatically")
    print("- One function call does everything")
    print("- Perfect for CLI tools and automation")
    print("- Similar to MetaGPT's metagpt command")
    print()
    print("🎉 Congratulations! You've learned all the components!")
    print("You can now build fully automated software companies!")


if __name__ == "__main__":
    asyncio.run(main())

