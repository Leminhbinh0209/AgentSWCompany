"""
Lesson 10: Terminal Tool
=========================

This lesson demonstrates the Terminal tool for command execution.

Run this lesson:
    python lesson_10.py
"""
import sys
import os
import asyncio
import tempfile
import shutil

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.tools.terminal import Terminal


async def main():
    print("=" * 60)
    print("Lesson 10: Terminal Tool")
    print("=" * 60)
    print()
    
    workspace = tempfile.mkdtemp(prefix="terminal_lesson_")
    print(f"Workspace: {workspace}")
    print()
    
    try:
        terminal = Terminal(workspace_path=workspace)
        
        # 1. Run a command
        print("1. Running a Command")
        print("-" * 60)
        result = await terminal.run_command("echo 'Hello, Terminal!'")
        print(f"Status: {result['status']}")
        print(f"Output: {result['stdout']}")
        print()
        
        # 2. Run Python code
        print("2. Running Python Code")
        print("-" * 60)
        python_code = """
print("Hello from Python!")
result = 2 + 3
print(f"2 + 3 = {result}")
"""
        result = await terminal.run_python(python_code)
        print(f"Status: {result['status']}")
        print(f"Output: {result['stdout']}")
        print()
        
        # 3. Check syntax
        print("3. Checking Syntax")
        print("-" * 60)
        # Create a test file
        test_file = os.path.join(workspace, "test.py")
        with open(test_file, 'w') as f:
            f.write("def hello():\n    print('Hello')\n")
        
        result = await terminal.check_syntax("test.py")
        print(f"Valid: {result['valid']}")
        print(f"Message: {result['message']}")
        print()
        
        # 4. Get Python version
        print("4. Getting Python Version")
        print("-" * 60)
        version = await terminal.get_python_version()
        print(f"Python version: {version}")
        print()
        
        print("=" * 60)
        print("Lesson 10 Complete!")
        print("=" * 60)
        
    finally:
        shutil.rmtree(workspace)
        print(f"\nCleaned up workspace: {workspace}")


if __name__ == "__main__":
    asyncio.run(main())

