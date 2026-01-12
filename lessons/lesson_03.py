"""
Lesson 03: Understanding Roles
================================

This lesson introduces the Role class, which represents agents
in the multi-agent system.

Run this lesson:
    python lesson_03.py
"""
import sys
import os
import asyncio

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.role import Role
from framework.action import Action
from framework.schema import Message, ActionOutput
from framework.llm import MockLLM
from typing import List


# Example action for the role
class EchoAction(Action):
    """Echo action that repeats input"""
    
    async def run(self, messages: List[Message] = None, **kwargs) -> ActionOutput:
        if messages:
            content = messages[-1].content
        else:
            content = kwargs.get("text", "Hello")
        
        return ActionOutput(
            content=f"Echo: {content}",
            instruct_content={"echoed": content}
        )


async def main():
    print("=" * 60)
    print("Lesson 03: Understanding Roles")
    print("=" * 60)
    print()
    
    # 1. Create a simple role
    print("1. Creating a Simple Role")
    print("-" * 60)
    llm = MockLLM()
    role = Role(
        name="EchoAgent",
        profile="Echo Agent",
        goal="Echo messages back",
        actions=[EchoAction(llm=llm)],
        llm=llm
    )
    print(f"Role Name: {role.name}")
    print(f"Profile: {role.profile}")
    print(f"Goal: {role.goal}")
    print(f"Actions: {[a.name for a in role.actions]}")
    print()
    
    # 2. Role observes messages
    print("2. Role Observes Messages")
    print("-" * 60)
    msg1 = Message(content="Hello, EchoAgent!", role="User")
    role.observe(msg1)
    print(f"Message observed: {msg1.content}")
    print(f"Memory size: {len(role.memory)}")
    print(f"Working memory size: {len(role.working_memory)}")
    print()
    
    # 3. Role thinks about what to do
    print("3. Role Thinks")
    print("-" * 60)
    action = role.think()
    if action:
        print(f"Role decided to execute: {action.name}")
    else:
        print("No action to execute")
    print()
    
    # 4. Role acts
    print("4. Role Acts")
    print("-" * 60)
    response = await role.act()
    if response:
        print(f"Response: {response.content}")
        print(f"From: {response.role}")
        print(f"Caused by: {response.cause_by}")
    print()
    
    # 5. Role reacts (observe -> think -> act)
    print("5. Role Reacts (Complete Cycle)")
    print("-" * 60)
    msg2 = Message(content="Can you echo this?", role="User")
    role.observe(msg2)
    response = await role.react()
    if response:
        print(f"Response: {response.content}")
    print()
    
    # 6. Role with context
    print("6. Role with Shared Context")
    print("-" * 60)
    context = {"project_name": "MyProject", "version": "1.0"}
    role.set_context(context)
    print(f"Context set: {context}")
    print()
    
    print("=" * 60)
    print("Lesson 03 Complete!")
    print("=" * 60)
    print()
    print("Key Takeaways:")
    print("- Roles are agents with goals and actions")
    print("- Roles observe messages and decide what to do")
    print("- Roles can think, act, and react")
    print("- Roles maintain memory of past messages")


if __name__ == "__main__":
    asyncio.run(main())

