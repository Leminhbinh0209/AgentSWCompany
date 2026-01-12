"""
Lesson 02: Understanding Actions
==================================

This lesson introduces the Action class, which represents tasks that
agents can perform.

Run this lesson:
    python lesson_02.py
"""
import sys
import os
import asyncio

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.action import Action
from framework.schema import Message, ActionOutput
from framework.llm import get_llm
from typing import List


# Example action implementation
class GreetAction(Action):
    """A simple greeting action"""
    
    async def run(self, messages: List[Message] = None, **kwargs) -> ActionOutput:
        name = kwargs.get("name", "World")
        greeting = f"Hello, {name}!"
        
        return ActionOutput(
            content=greeting,
            instruct_content={"greeting": greeting, "name": name}
        )


class CalculateAction(Action):
    """A simple calculation action"""
    
    async def run(self, messages: List[Message] = None, **kwargs) -> ActionOutput:
        a = kwargs.get("a", 0)
        b = kwargs.get("b", 0)
        operation = kwargs.get("operation", "add")
        
        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        elif operation == "divide":
            result = a / b if b != 0 else "Error: Division by zero"
        else:
            result = "Unknown operation"
        
        return ActionOutput(
            content=f"Result: {result}",
            instruct_content={"result": result, "operation": operation}
        )


async def main():
    print("=" * 60)
    print("Lesson 02: Understanding Actions")
    print("=" * 60)
    print()
    
    # 1. Create a simple action
    print("1. Creating a Simple Action")
    print("-" * 60)
    greet_action = GreetAction(name="GreetAction")
    result = await greet_action.run(name="Alice")
    print(f"Action Name: {greet_action.name}")
    print(f"Output: {result.content}")
    print(f"Structured Output: {result.instruct_content}")
    print()
    
    # 2. Action with parameters
    print("2. Action with Parameters")
    print("-" * 60)
    calc_action = CalculateAction(name="CalculateAction")
    result = await calc_action.run(a=10, b=5, operation="add")
    print(f"Calculation: 10 + 5 = {result.instruct_content['result']}")
    print()
    
    # 3. Multiple operations
    print("3. Multiple Operations")
    print("-" * 60)
    operations = [
        ("add", 10, 5),
        ("subtract", 10, 5),
        ("multiply", 10, 5),
        ("divide", 10, 5),
    ]
    
    for op, a, b in operations:
        result = await calc_action.run(a=a, b=b, operation=op)
        print(f"{a} {op} {b} = {result.instruct_content['result']}")
    print()
    
    # 4. Action with messages context
    print("4. Action with Message Context")
    print("-" * 60)
    messages = [
        Message(content="Calculate 15 + 25", role="User")
    ]
    result = await calc_action.run(messages=messages, a=15, b=25, operation="add")
    print(f"With context: {result.content}")
    print()
    
    # 5. Converting ActionOutput to Message
    print("5. Converting ActionOutput to Message")
    print("-" * 60)
    output = await greet_action.run(name="Bob")
    message = output.to_message(role="Greeter", cause_by="GreetAction")
    print(f"Message: {message}")
    print(f"Role: {message.role}")
    print(f"Caused by: {message.cause_by}")
    print()
    
    print("=" * 60)
    print("Lesson 02 Complete!")
    print("=" * 60)
    print()
    print("Key Takeaways:")
    print("- Actions are tasks that agents can perform")
    print("- Actions return ActionOutput with content and structured data")
    print("- Actions can use message context and keyword arguments")
    print("- ActionOutput can be converted to Messages")


if __name__ == "__main__":
    asyncio.run(main())

