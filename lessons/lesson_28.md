# Lesson 28: Context System

## Learning Targets

By the end of this lesson, you will be able to:
- Understand the Context system and its purpose
- Use AttrDict for project data management
- Manage project paths automatically
- Integrate cost management with Context
- Serialize and deserialize Context

## Overview

The Context system is the foundation for managing project state, configuration, and costs. It provides a centralized way to store and access project information throughout the workflow.

## Key Concepts

### Context Class

The `Context` class contains:
- **kwargs**: AttrDict for storing project data (project_path, etc.)
- **config**: Configuration object
- **cost_manager**: Cost tracking and budget management

### AttrDict

A dictionary-like object that allows attribute-style access:
```python
ctx.kwargs.project_name  # Instead of ctx.kwargs['project_name']
ctx.kwargs.set("key", "value")
ctx.kwargs.get("key", default)
```

## Guidance

### 1. Creating Context

```python
from framework.context import Context

ctx = Context()
```

### 2. Storing Project Data

```python
# Using set/get methods
ctx.kwargs.set("project_name", "MyProject")
name = ctx.kwargs.get("project_name")

# Attribute-style access
ctx.kwargs.project_name = "MyProject"
name = ctx.kwargs.project_name
```

### 3. Project Path Management

```python
# Set and create project path
ctx.set_project_path("my_project")

# Get project path
path = ctx.get_project_path()
```

### 4. Cost Management Integration

```python
# Set budget
ctx.cost_manager.max_budget = 10.0

# Track costs
ctx.cost_manager.add_cost(0.5, role="ProductManager", action="WritePRD")

# Check remaining
remaining = ctx.cost_manager.get_remaining_budget()
```

### 5. Serialization

```python
# Save context
serialized = ctx.serialize()

# Load context
new_ctx = Context()
new_ctx.deserialize(serialized)
```

## Exercises

### Exercise 1: Project State Manager
Create a function that:
- Creates a Context
- Stores project metadata
- Tracks costs
- Returns a summary

### Exercise 2: Context Persistence
Create a system that:
- Saves Context to file
- Loads Context from file
- Preserves all state

## Practice Tasks

1. **Context Creator**: Create contexts for different projects
2. **State Manager**: Manage project state with Context
3. **Cost Tracker**: Track costs across multiple actions

## Next Steps

- Move to Lesson 29 to learn about Cost Management
- Try integrating Context with Team
- Experiment with serialization

## Additional Resources

- Check `framework/context.py` for full implementation
- Review `framework/config.py` for configuration

