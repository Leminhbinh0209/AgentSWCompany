"""
Lesson 04: Understanding Environment
====================================

This lesson introduces the Environment class, which manages roles
and message routing in the multi-agent system.

Run this lesson:
    python lesson_04.py
"""
import sys
import os
import asyncio

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.environment import Environment
from framework.role import Role
from framework.action import Action
from framework.schema import Message, ActionOutput
from framework.llm import MockLLM
from typing import List


# Simple action for demonstration
class GreetAction(Action):
    async def run(self, messages: List[Message] = None, **kwargs) -> ActionOutput:
        name = kwargs.get("name", "World")
        return ActionOutput(content=f"Hello, {name}!")


async def main():
    print("=" * 60)
    print("Lesson 04: Understanding Environment")
    print("=" * 60)
    print()
    
    # 1. Create environment
    print("1. Creating Environment")
    print("-" * 60)
    env = Environment()
    print(f"Environment created")
    print(f"Roles: {len(env.roles)}")
    print(f"Messages: {len(env.message_history)}")
    print()
    
    # 2. Add roles to environment
    print("2. Adding Roles to Environment")
    print("-" * 60)
    llm = MockLLM()
    
    role1 = Role(
        name="Agent1",
        profile="First Agent",
        goal="Greet people",
        actions=[GreetAction(llm=llm)],
        llm=llm
    )
    
    role2 = Role(
        name="Agent2",
        profile="Second Agent",
        goal="Greet people",
        actions=[GreetAction(llm=llm)],
        llm=llm
    )
    
    env.add_role(role1)
    env.add_role(role2)
    print(f"Added {len(env.roles)} roles")
    print(f"Role names: {list(env.roles.keys())}")
    print()
    
    # 3. Publish message (broadcast)
    print("3. Publishing Message (Broadcast)")
    print("-" * 60)
    msg = Message(
        content="Hello everyone!",
        role="User"
    )
    env.publish_message(msg)  # Broadcast to all
    print(f"Message published: {msg.content}")
    print(f"Total messages: {len(env.message_history)}")
    print(f"Agent1 memory: {len(role1.memory)}")
    print(f"Agent2 memory: {len(role2.memory)}")
    print()
    
    # 4. Publish message to specific role
    print("4. Publishing Message to Specific Role")
    print("-" * 60)
    msg2 = Message(
        content="Hello Agent1!",
        role="User"
    )
    env.publish_message(msg2, send_to="Agent1")
    print(f"Message sent to Agent1 only")
    print(f"Agent1 memory: {len(role1.memory)}")
    print(f"Agent2 memory: {len(role2.memory)}")
    print()
    
    # 5. Get roles
    print("5. Getting Roles")
    print("-" * 60)
    agent1 = env.get_role("Agent1")
    if agent1:
        print(f"Found: {agent1.name}")
    
    all_roles = env.get_all_roles()
    print(f"All roles: {[r.name for r in all_roles]}")
    print()
    
    # 6. Environment context
    print("6. Environment Context")
    print("-" * 60)
    env.context["project"] = "MyProject"
    env.context["version"] = "1.0"
    print(f"Context: {env.context}")
    print()
    
    # 7. Message history
    print("7. Message History")
    print("-" * 60)
    print(f"Total messages in history: {len(env.message_history)}")
    for i, msg in enumerate(env.message_history, 1):
        print(f"{i}. [{msg.role}]: {msg.content[:50]}...")
    print()
    
    print("=" * 60)
    print("Lesson 04 Complete!")
    print("=" * 60)
    print()
    print("Key Takeaways:")
    print("- Environment manages roles and message routing")
    print("- Messages can be broadcast or sent to specific roles")
    print("- Environment maintains message history")
    print("- Environment provides shared context for roles")


if __name__ == "__main__":
    asyncio.run(main())

