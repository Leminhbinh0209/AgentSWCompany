# Lesson 12: Search Engine Tool

## Learning Targets

By the end of this lesson, you will be able to:
- Use the SearchEngine tool to search the web
- Get search results
- Summarize search results
- Integrate search into workflows

## Overview

The SearchEngine tool allows agents to search the web and retrieve information.

## Key Concepts

### SearchEngine Tool

The `SearchEngine` class provides:
- **search(query, num_results)**: Search the web
- **search_and_summarize(query, max_results)**: Search and summarize

## Guidance

### 1. Basic Search

```python
from framework.tools.search_engine import SearchEngine

search_engine = SearchEngine()
results = await search_engine.search("Python", num_results=10)
```

### 2. Search and Summarize

```python
summary = await search_engine.search_and_summarize("topic", max_results=5)
```

## Exercises

### Exercise 1: Research Tool
Create a research tool that:
- Searches multiple queries
- Combines results
- Generates reports

### Exercise 2: Information Gatherer
Create a gatherer that:
- Searches for specific information
- Validates sources
- Extracts key facts

## Practice Tasks

1. **Query Optimizer**: Optimize search queries
2. **Result Analyzer**: Analyze search results
3. **Search Aggregator**: Aggregate multiple searches

## Next Steps

- Move to Lesson 13 to learn about Project Repository
- Try different search queries
- Experiment with result processing

## Additional Resources

- Check `framework/tools/search_engine.py` for full implementation

