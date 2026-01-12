"""
Lesson 01: Understanding Messages
===================================

This lesson introduces the Message class, the fundamental communication
unit in the multi-agent framework.

Run this lesson:
    python lesson_01.py
"""
import sys
import os
from datetime import datetime

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.schema import Message


def main():
    print("=" * 60)
    print("Lesson 01: Understanding Messages")
    print("=" * 60)
    print()
    
    # 1. Create a simple message
    print("1. Creating a Simple Message")
    print("-" * 60)
    msg1 = Message(
        content="Hello, I need a calculator application",
        role="User"
    )
    print(f"Message: {msg1}")
    print(f"Content: {msg1.content}")
    print(f"Role: {msg1.role}")
    print(f"Timestamp: {msg1.timestamp}")
    print()
    
    # 2. Create a message with cause_by
    print("2. Message with Action Context")
    print("-" * 60)
    msg2 = Message(
        content="Here is the PRD for the calculator",
        role="ProductManager",
        cause_by="WritePRD"
    )
    print(f"Message: {msg2}")
    print(f"Caused by: {msg2.cause_by}")
    print()
    
    # 3. Create a message with routing
    print("3. Message with Routing")
    print("-" * 60)
    msg3 = Message(
        content="Please review this design",
        role="Architect",
        cause_by="WriteDesign",
        sent_from="Architect",
        send_to="Engineer"
    )
    print(f"From: {msg3.sent_from}")
    print(f"To: {msg3.send_to}")
    print(f"Content: {msg3.content[:50]}...")
    print()
    
    # 4. Message flow example
    print("4. Message Flow Example")
    print("-" * 60)
    messages = [
        Message(content="Create a calculator", role="User"),
        Message(content="PRD created", role="ProductManager", cause_by="WritePRD"),
        Message(content="Design created", role="Architect", cause_by="WriteDesign"),
        Message(content="Code written", role="Engineer", cause_by="WriteCode"),
    ]
    
    for i, msg in enumerate(messages, 1):
        print(f"{i}. [{msg.role}] {msg.content}")
    print()
    
    print("=" * 60)
    print("Lesson 01 Complete!")
    print("=" * 60)
    print()
    print("Key Takeaways:")
    print("- Messages are the communication unit between agents")
    print("- Messages include content, role, and optional metadata")
    print("- cause_by tracks which action created the message")
    print("- Messages can be routed between specific roles")


if __name__ == "__main__":
    main()

