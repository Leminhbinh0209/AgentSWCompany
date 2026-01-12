"""
Lesson 15: Code Review
======================

This lesson demonstrates the CodeReviewer for automated code quality checks.

Run this lesson:
    python lesson_15.py
"""
import sys
import os
import asyncio

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.quality.code_reviewer import CodeReviewer
from framework.llm import get_llm


async def main():
    print("=" * 60)
    print("Lesson 15: Code Review")
    print("=" * 60)
    print()
    
    code = """def calculate(a, b):
    return a+b

def process_data(data):
    x = 0
    for i in data:
        x = x + i
    return x
"""
    
    reviewer = CodeReviewer(llm=get_llm())
    
    # Review code
    print("1. Reviewing Code")
    print("-" * 60)
    review = await reviewer.review_code(code)
    print(f"Score: {review['score']}/100")
    print(f"Issues found: {len(review['issues'])}")
    for issue in review['issues'][:3]:
        print(f"  - {issue.get('type', 'unknown')}: {issue.get('message', '')[:60]}")
    print()
    
    print("=" * 60)
    print("Lesson 15 Complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

