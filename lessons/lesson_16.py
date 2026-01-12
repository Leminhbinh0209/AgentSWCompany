"""
Lesson 16: Testing
==================

This lesson demonstrates the TestGenerator for creating and running tests.

Run this lesson:
    python lesson_16.py
"""
import sys
import os
import asyncio
import tempfile
import shutil

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.quality.test_generator import TestGenerator
from framework.llm import get_llm


async def main():
    print("=" * 60)
    print("Lesson 16: Testing")
    print("=" * 60)
    print()
    
    workspace = "myproject_lesson_16"
    os.makedirs(workspace, exist_ok=True)
    print(f"Workspace: {workspace}")
    
    
    code = """def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
"""
        
    generator = TestGenerator(workspace_path=workspace, llm=get_llm())
    
    # Generate tests
    print("1. Generating Tests")
    print("-" * 60)
    test_code = await generator.generate_tests(code, test_type="unit", module_name="calculator")
    print(f"Generated test code ({len(test_code)} chars)")
    print(test_code)
    print()
    
    print("=" * 60)
    print("Lesson 16 Complete!")
    print("=" * 60)
        
    print(f"Please manually clear the workspace folder when done:")
    print(f"  {workspace}")
    print()


if __name__ == "__main__":
    asyncio.run(main())

