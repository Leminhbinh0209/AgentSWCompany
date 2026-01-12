# Lesson 19: Memory

## Learning Targets

By the end of this lesson, you will be able to:
- Use Memory for persistent storage
- Store and retrieve information
- Search memory contents

## Overview

Memory provides persistent key-value storage for agents to remember information across sessions.

## Key Concepts

### Memory System

The `Memory` class provides:
- **store()**: Store key-value pairs
- **retrieve()**: Retrieve values by key
- **search()**: Search memory by pattern

## Guidance

### 1. Using Memory

```python
from framework.memory.memory import Memory

memory = Memory(storage_path=".")
await memory.store("key", "value")
value = await memory.retrieve("key")
```

## Exercises

### Exercise 1: Memory Manager
Store and retrieve various types of data

### Exercise 2: Memory Search
Search memory for specific information

## Practice Tasks

1. **Data Store**: Store project information
2. **Memory Search**: Search stored data
3. **Memory Manager**: Manage memory efficiently

## Next Steps

- Move to Lesson 20 to learn about Advanced Actions
- Try storing complex data structures
- Experiment with memory search

## Additional Resources

- Check `framework/memory/memory.py` for full implementation

