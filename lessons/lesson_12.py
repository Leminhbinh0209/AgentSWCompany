"""
Lesson 12: Search Engine Tool
==============================

This lesson demonstrates the SearchEngine tool for web search.

Run this lesson:
    python lesson_12.py
"""
import sys
import os
import asyncio

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.tools.search_engine import SearchEngine


async def main():
    print("=" * 60)
    print("Lesson 12: Search Engine Tool")
    print("Install duckduckgo_search for best results: pip install ddgs")
    print("=" * 60)
    print()
    
    search_engine = SearchEngine(preferred_provider="ddg")  # Use DuckDuckGo library
    
    # 1. Search the web
    print("1. Searching the Web")
    print("-" * 60)
    query = "Current US President's name"
    results = await search_engine.search(query, num_results=5)
    print(f"Query: {query}")
    print(f"Found {len(results)} results")
    for i, result in enumerate(results[:3], 1):
        print(f"\n{i}. {result.get('title', 'N/A')}")
        print(f"   URL: {result.get('url', 'N/A')[:60]}...")
        print(f"   {result.get('snippet', 'N/A')[:80]}...")
    print()
    
    # 2. Search and summarize
    print("2. Search and Summarize")
    print("-" * 60)
    summary = await search_engine.search_and_summarize("CEO of Google", max_results=3)
    print(f"Summary: {summary[:300]}...")
    print()
    
    print("=" * 60)
    print("Lesson 12 Complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

