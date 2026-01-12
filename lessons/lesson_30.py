"""
Lesson 30: TeamLeader Role
===========================

This lesson demonstrates the TeamLeader role for orchestrating team workflow
and coordinating team members.

Run this lesson:
    python lesson_30.py
"""
import sys
import os
import asyncio

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.team import Team
from framework.context import Context
from framework.roles.team_leader import TeamLeader
from framework.roles.product_manager import ProductManager
from framework.roles.architect import Architect
from framework.roles.engineer import Engineer
from framework.llm import get_llm


async def main():
    print("=" * 80)
    print("Lesson 30: TeamLeader Role")
    print("=" * 80)
    print()
    
    print("TeamLeader orchestrates the team workflow and coordinates team members.")
    print("It provides team information and can publish messages to the team.")
    print()
    
    # 1. Creating TeamLeader
    print("1. Creating TeamLeader")
    print("-" * 80)
    llm = get_llm(
        local_model_path="EMPTY",
        vllm_base_url="http://localhost:8000/v1",
        vllm_model="codellama/CodeLlama-7b-Instruct-hf"
    )
    
    team_leader = TeamLeader(llm=llm)
    print(f"✓ TeamLeader created")
    print(f"  - Name: {team_leader.name}")
    print(f"  - Profile: {team_leader.profile}")
    print(f"  - Goal: {team_leader.goal}")
    print()
    
    # 2. Team with TeamLeader
    print("2. Creating Team with TeamLeader")
    print("-" * 80)
    ctx = Context()
    team = Team(context=ctx)
    
    team.hire([
        team_leader,
        ProductManager(llm=llm),
        Architect(llm=llm),
        Engineer(llm=llm),
    ])
    
    # Set environment reference for TeamLeader
    team_leader.set_environment(team.environment)
    
    print(f"✓ Team created with {len(team.environment.roles)} roles")
    print(f"  - Roles: {[r.name for r in team.environment.get_all_roles()]}")
    print()
    
    # 3. Team Information
    print("3. Getting Team Information")
    print("-" * 80)
    team_info = team_leader._get_team_info()
    print(f"✓ Team information:")
    print(team_info)
    print()
    
    # 4. Publishing Team Messages
    print("4. Publishing Team Messages")
    print("-" * 80)
    team_leader.publish_team_message(
        "Let's start working on the project!",
        send_to="ProductManager"
    )
    print(f"✓ Message published to ProductManager")
    print(f"  - Total messages: {len(team.environment.message_history)}")
    print()
    
    # 5. Team Coordination
    print("5. Team Coordination")
    print("-" * 80)
    # TeamLeader can coordinate by reacting
    coordination_msg = await team_leader.react()
    if coordination_msg:
        print(f"✓ TeamLeader coordination:")
        print(f"  - Message: {coordination_msg.content}")
        print(f"  - Role: {coordination_msg.role}")
    print()
    
    # 6. TeamLeader in Workflow
    print("6. TeamLeader in Workflow")
    print("-" * 80)
    print("When TeamLeader is part of the team:")
    print("  - It can observe team state")
    print("  - It can coordinate team members")
    print("  - It can publish messages to guide workflow")
    print("  - It provides team information to other roles")
    print()
    
    print("=" * 80)
    print("Lesson 30 Complete!")
    print("=" * 80)
    print()
    print("Key Takeaways:")
    print("- TeamLeader orchestrates team workflow")
    print("- It can access team information")
    print("- It can publish messages to team members")
    print("- It coordinates the overall project execution")
    print("- It's essential for complex multi-agent workflows")


if __name__ == "__main__":
    asyncio.run(main())

