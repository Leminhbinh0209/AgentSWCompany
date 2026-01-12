"""
Lesson 22: QA Engineer
======================

This lesson demonstrates the QAEngineer role for testing and quality assurance.

Run this lesson:
    python lesson_22.py
"""
import sys
import os
import asyncio

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.roles.qa_engineer import QAEngineer
from framework.llm import MockLLM


async def main():
    print("=" * 60)
    print("Lesson 22: QA Engineer")
    print("=" * 60)
    print()
    
    llm = MockLLM()
    qa = QAEngineer(llm=llm)
    
    print("1. QA Engineer Role")
    print("-" * 60)
    print(f"Name: {qa.name}")
    print(f"Profile: {qa.profile}")
    print(f"Goal: {qa.goal}")
    print(f"Actions: {[a.name for a in qa.actions]}")
    print()
    
    code = "def add(a, b): return a + b"
    test_code = await qa.generate_tests(code)
    print(f"Generated test code ({len(test_code)} chars)")
    print()
    
    print("=" * 60)
    print("Lesson 22 Complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

