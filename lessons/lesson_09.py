"""
Lesson 09: File Editor Tool
============================

This lesson demonstrates the Editor tool for file operations.

Run this lesson:
    python lesson_09.py
"""
import sys
import os
import asyncio
import tempfile
import shutil

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.tools.editor import Editor


async def main():
    print("=" * 60)
    print("Lesson 09: File Editor Tool")
    print("=" * 60)
    print()
    
    # Create temporary workspace
    workspace = tempfile.mkdtemp(prefix="editor_lesson_")
    print(f"Workspace: {workspace}")
    print()
    
    try:
        editor = Editor(workspace_path=workspace)
        
        # 1. Create a file
        print("1. Creating a File")
        print("-" * 60)
        content = """def hello():
    print("Hello, World!")

if __name__ == "__main__":
    hello()
"""
        result = await editor.create_file("hello.py", content)
        print(f"Status: {result['status']}")
        print(f"File: {result['path']}")
        print(f"Size: {result['size']} bytes")
        print()
        
        # 2. Read a file
        print("2. Reading a File")
        print("-" * 60)
        read_content = await editor.read("hello.py")
        print(f"Content preview: {read_content[:100]}...")
        print()
        
        # 3. Edit a file by replace
        print("3. Editing a File (Replace)")
        print("-" * 60)
        edit_result = await editor.edit_file_by_replace("hello.py", "Hello, World!", "Hello, Python!")
        print(f"Status: {edit_result['status']}")
        if edit_result['status'] == 'success':
            print(f"Changes: {edit_result.get('changes', {})}")
        print()
        
        # 4. Write file
        print("4. Writing File")
        print("-" * 60)
        new_content = """def hello(name="World"):
    print(f"Hello, {name}!")

if __name__ == "__main__":
    hello("Python")
"""
        write_result = await editor.write("hello.py", new_content)
        print(f"Status: {write_result['status']}")
        print()
        
        # 5. Find files
        print("5. Finding Files")
        print("-" * 60)
        files = await editor.find_file("*.py")
        print(f"Found {len(files)} Python files")
        for file in files:
            print(f"  {file}")
        print()
        
        print("=" * 60)
        print("Lesson 09 Complete!")
        print("=" * 60)
        
    finally:
        shutil.rmtree(workspace)
        print(f"\nCleaned up workspace: {workspace}")


if __name__ == "__main__":
    asyncio.run(main())

