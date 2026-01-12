"""
Lesson 14: Code Generation
===========================

This lesson demonstrates the CodeGenerator for generating code files.

Run this lesson:
    python lesson_14.py
"""
import sys
import os
import asyncio
import tempfile
import shutil

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.repository.project_repo import ProjectRepo
from framework.repository.code_generator import CodeGenerator
from framework.llm import MockLLM


async def main():
    print("=" * 60)
    print("Lesson 14: Code Generation")
    print("=" * 60)
    print()
    
    workspace = tempfile.mkdtemp(prefix="code_gen_lesson_")
    print(f"Workspace: {workspace}")
    print()
    
    try:
        repo = ProjectRepo(workspace)
        llm = MockLLM()
        generator = CodeGenerator(repo, llm=llm)
        
        # 1. Generate project
        print("1. Generating Project")
        print("-" * 60)
        design = "A simple calculator application"
        result = await generator.generate_project(design, "calculator")
        print(f"Status: {result['status']}")
        print(f"Files created: {result['files_created']}")
        print()
        
        # 2. Generate code file
        print("2. Generating Code File")
        print("-" * 60)
        code = """def add(a, b):
    return a + b

def subtract(a, b):
    return a - b
"""
        result = await generator.generate_file("calculator.py", code, repo="srcs")
        print(f"Status: {result.get('status', 'success')}")
        print()
        
        print("=" * 60)
        print("Lesson 14 Complete!")
        print("=" * 60)
        
    finally:
        shutil.rmtree(workspace)
        print(f"\nCleaned up workspace: {workspace}")


if __name__ == "__main__":
    asyncio.run(main())

