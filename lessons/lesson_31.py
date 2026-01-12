"""
Lesson 31: Environment.run() and Automatic Workflow
====================================================

This lesson demonstrates the Environment.run() method for automatic workflow
execution without manual role iteration.

Run this lesson:
    python lesson_31.py
"""
import sys
import os
import asyncio

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.environment import Environment
from framework.context import Context
from framework.roles.product_manager import ProductManager
from framework.roles.architect import Architect
from framework.roles.engineer import Engineer
from framework.schema import Message
from framework.llm import get_llm


async def main():
    print("=" * 80)
    print("Lesson 31: Environment.run() and Automatic Workflow")
    print("=" * 80)
    print()
    
    print("Environment.run() automatically processes all roles in each round.")
    print("No manual iteration needed - the environment handles everything!")
    print()
    
    # 1. Creating Environment with Context
    print("1. Creating Environment with Context")
    print("-" * 80)
    ctx = Context()
    env = Environment(context=ctx)
    
    llm = get_llm(
        local_model_path="EMPTY",
        vllm_base_url="http://localhost:8000/v1",
        vllm_model="codellama/CodeLlama-7b-Instruct-hf"
    )
    
    # Add roles
    env.add_roles([
        ProductManager(llm=llm),
        Architect(llm=llm),
        Engineer(llm=llm),
    ])
    
    print(f"✓ Environment created with {len(env.roles)} roles")
    print()
    
    # 2. Publishing Initial Message
    print("2. Publishing Initial Message")
    print("-" * 80)
    initial_msg = Message(
        content="Create a simple calculator application",
        role="User",
        cause_by="UserRequirement"
    )
    env.publish_message(initial_msg, send_to="ProductManager")
    print(f"✓ Message published to ProductManager")
    print(f"  - Total messages: {len(env.message_history)}")
    print()
    
    # 3. Manual vs Automatic Processing
    print("3. Manual vs Automatic Processing")
    print("-" * 80)
    print("OLD WAY (Manual):")
    print("  for role in roles:")
    print("      if role.working_memory:")
    print("          message = await role.react()")
    print()
    print("NEW WAY (Automatic):")
    print("  await env.run()  # Handles everything!")
    print()
    
    # 4. Running Environment Automatically
    print("4. Running Environment Automatically")
    print("-" * 80)
    print("Running one round automatically...")
    await env.run()
    print(f"✓ Round completed automatically")
    print(f"  - Messages after round: {len(env.message_history)}")
    print(f"  - Environment idle: {env.is_idle}")
    print()
    
    # 5. Multiple Rounds
    print("5. Running Multiple Rounds")
    print("-" * 80)
    for round_num in range(3):
        if env.is_idle:
            print(f"  Round {round_num + 1}: Environment is idle, stopping")
            break
        
        print(f"  Round {round_num + 1}: Running...")
        await env.run()
        print(f"    - Messages: {len(env.message_history)}")
        print(f"    - Idle: {env.is_idle}")
    print()
    
    # 6. Idle Detection
    print("6. Idle Detection")
    print("-" * 80)
    print(f"✓ Environment idle status: {env.is_idle}")
    if env.is_idle:
        print("  - All roles have no messages to process")
        print("  - Workflow can stop")
    else:
        print("  - Some roles still have messages")
        print("  - Continue running")
    print()
    
    # 7. Message History
    print("7. Message History")
    print("-" * 80)
    print(f"✓ Total messages: {len(env.history)}")
    print("Recent messages:")
    for i, msg in enumerate(env.history[-5:], 1):
        print(f"  {i}. [{msg.role}] via {msg.cause_by}")
    print()
    
    print("=" * 80)
    print("Lesson 31 Complete!")
    print("=" * 80)
    print()
    print("Key Takeaways:")
    print("- Environment.run() processes all roles automatically")
    print("- No manual iteration needed")
    print("- is_idle property detects when workflow can stop")
    print("- Automatic message routing handles communication")
    print("- This is the foundation for fully automated workflows")


if __name__ == "__main__":
    asyncio.run(main())

