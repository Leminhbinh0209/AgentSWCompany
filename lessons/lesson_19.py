"""
Lesson 19: Memory
=================

This lesson demonstrates the Memory system for persistent storage.

Run this lesson:
    python lesson_19.py
"""
import sys
import os
import asyncio

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.memory.memory import Memory


async def main():
    print("=" * 60)
    print("Lesson 19: Memory")
    print("=" * 60)
    print()
    
    workspace = "myproject_lesson_19"
    os.makedirs(workspace, exist_ok=True)
    print(f"Workspace: {workspace}")
    

    memory = Memory(storage_path=workspace)
    
    # Store and retrieve
    print("1. Storing and Retrieving")
    print("-" * 60)
    await memory.store("key1", "value1")
    value = await memory.retrieve("key1")
    print(f"Stored: key1 = value1")
    print(f"Retrieved: {value}")
    print()
    
    # Search
    print("2. Searching Memory")
    print("-" * 60)
    await memory.store("project_name", "MyProject")
    await memory.store("project_version", "1.0")
    results = await memory.search("project")
    print(f"Found {len(results)} results for 'project'")
    for result in results:
        print(f"  {result['key']}: {result['value']}")
    print()
    
    print("=" * 60)
    print("Lesson 19 Complete!")
    print("=" * 60)
    
    print(f"Please manually clear the workspace folder when done:")
    print(f"  {workspace}")
    print()

if __name__ == "__main__":
    asyncio.run(main())

