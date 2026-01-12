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
import tempfile
import shutil

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.memory.memory import Memory


async def main():
    print("=" * 60)
    print("Lesson 19: Memory")
    print("=" * 60)
    print()
    
    workspace = tempfile.mkdtemp(prefix="memory_lesson_")
    print(f"Workspace: {workspace}")
    print()
    
    try:
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
        for key, value in results.items():
            print(f"  {key}: {value}")
        print()
        
        print("=" * 60)
        print("Lesson 19 Complete!")
        print("=" * 60)
        
    finally:
        shutil.rmtree(workspace)
        print(f"\nCleaned up workspace: {workspace}")


if __name__ == "__main__":
    asyncio.run(main())

