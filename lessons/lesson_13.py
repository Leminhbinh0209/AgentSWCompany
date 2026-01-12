"""
Lesson 13: Project Repository
==============================

This lesson demonstrates the ProjectRepo for managing project structure.

Run this lesson:
    python lesson_13.py
"""
import sys
import os
import asyncio
import tempfile
import shutil

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.repository.project_repo import ProjectRepo


async def main():
    print("=" * 60)
    print("Lesson 13: Project Repository")
    print("=" * 60)
    print()
    
    workspace = tempfile.mkdtemp(prefix="project_repo_lesson_")
    print(f"Workspace: {workspace}")
    print()
    
    try:
        repo = ProjectRepo(workspace)
        
        # 1. Create project structure
        print("1. Creating Project Structure")
        print("-" * 60)
        repo.initialize_python_package("myproject")
        print("✓ Python package initialized")
        print()
        
        # 2. Create files in different repos
        print("2. Creating Files in Repositories")
        print("-" * 60)
        repo.docs.create_file("README.md", "# My Project\n\nA sample project.")
        repo.srcs.create_file("main.py", "def main():\n    print('Hello')\n")
        repo.tests.create_file("test_main.py", "import unittest\n")
        print("✓ Files created in docs, srcs, and tests")
        print()
        
        # 3. Get project structure
        print("3. Project Structure")
        print("-" * 60)
        structure = repo.get_structure()
        print(f"Project structure:\n{structure}")
        print()
        
        # 4. List files
        print("4. Listing Files")
        print("-" * 60)
        docs_files = repo.docs.list_files()
        src_files = repo.srcs.list_files()
        print(f"Docs: {docs_files}")
        print(f"Source: {src_files}")
        print()
        
        print("=" * 60)
        print("Lesson 13 Complete!")
        print("=" * 60)
        
    finally:
        shutil.rmtree(workspace)
        print(f"\nCleaned up workspace: {workspace}")


if __name__ == "__main__":
    asyncio.run(main())

