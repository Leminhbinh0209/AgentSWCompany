"""Example: Simple Software Company using the multi-agent framework"""
import asyncio
from framework.team import Team
from framework.roles.product_manager import ProductManager
from framework.roles.architect import Architect
from framework.roles.engineer import Engineer
from framework.llm import MockLLM, OpenAILLM


async def main():
    print("="*60)
    print("Multi-Agent Software Company Demo")
    print("="*60)
    
    # Initialize LLM
    # Use MockLLM for testing without API key
    # For real usage, use: llm = OpenAILLM(api_key="your-key-here")
    llm = MockLLM()
    
    print("\nInitializing team...")
    
    # Create team
    team = Team()
    
    # Hire roles
    team.hire([
        ProductManager(llm=llm),
        Architect(llm=llm),
        Engineer(llm=llm),
    ])
    
    # Set budget
    team.invest(10.0)
    
    print("Team ready!")
    print(f"Roles: {[r.name for r in team.environment.get_all_roles()]}")
    
    # Run with an idea
    idea = "Create a simple calculator application that can add, subtract, multiply, and divide numbers"
    
    print(f"\nStarting project with idea: {idea}")
    print("\n" + "="*60)
    
    result = await team.run(idea, n_round=5)
    
    print("\n" + "="*60)
    print("Project Complete!")
    print("="*60)
    
    # Show final results
    if "code" in result:
        print("\nGenerated Code:")
        print("-" * 60)
        print(result["code"])
        print("-" * 60)
    
    print(f"\nTotal messages exchanged: {len(team.environment.message_history)}")
    print(f"Rounds executed: {team.current_round + 1}")


if __name__ == "__main__":
    asyncio.run(main())

