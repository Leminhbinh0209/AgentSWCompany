"""
Lesson 11: Web Browser Tool
============================

This lesson demonstrates the Browser tool for web navigation.

Run this lesson:
    python lesson_11.py
"""
import sys
import os
import asyncio

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.tools.browser import Browser


async def main():
    print("=" * 60)
    print("Lesson 11: Web Browser Tool")
    print("=" * 60)
    print()
    
    browser = Browser()
    
    # 1. Navigate to a URL
    print("1. Navigating to a URL")
    print("-" * 60)
    result = await browser.goto("example.com")
    print(f"Status: {result['status']}")
    print(f"URL: {result['url']}")
    print(f"Title: {result.get('title', 'N/A')}")
    print()
    
    # 2. Extract links
    print("2. Extracting Links")
    print("-" * 60)
    links = await browser.extract_links()
    print(f"Found {len(links)} links")
    for link in links[:5]:
        print(f"  {link.get('text', '')[:]}: {link.get('url', '')[:]}")
    print()
    
    # 3. Extract text
    print("3. Extracting Text")
    print("-" * 60)
    text = await browser.extract_text()
    print(f"Text preview: {text[:]}...")
    print()
    
    print("=" * 60)
    print("Lesson 11 Complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

