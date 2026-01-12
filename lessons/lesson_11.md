# Lesson 11: Web Browser Tool

## Learning Targets

By the end of this lesson, you will be able to:
- Use the Browser tool to navigate websites
- Extract content from web pages
- Extract links from pages
- Work with web content

## Overview

The Browser tool allows agents to navigate the web, extract content, and interact with web pages.

## Key Concepts

### Browser Tool

The `Browser` class provides:
- **goto(url)**: Navigate to a URL
- **extract_links()**: Extract all links from current page
- **extract_text()**: Extract text content

## Guidance

### 1. Navigating

```python
from framework.tools.browser import Browser

browser = Browser()
result = await browser.goto("https://example.com")
```

### 2. Extracting Content

```python
links = await browser.extract_links()
text = await browser.extract_text()
```

## Exercises

### Exercise 1: Web Scraper
Create a scraper that:
- Visits multiple pages
- Extracts specific information
- Saves data

### Exercise 2: Link Crawler
Create a crawler that:
- Follows links
- Extracts content
- Builds a site map

## Practice Tasks

1. **Page Analyzer**: Analyze web page structure
2. **Content Extractor**: Extract specific content types
3. **Link Validator**: Validate links on a page

## Next Steps

- Move to Lesson 12 to learn about Search Engine
- Try scraping different websites
- Experiment with content extraction

## Additional Resources

- Check `framework/tools/browser.py` for full implementation

