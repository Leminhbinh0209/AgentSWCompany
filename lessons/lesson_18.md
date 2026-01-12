# Lesson 18: Project Manager

## Learning Targets

By the end of this lesson, you will be able to:
- Understand the ProjectManager role
- Use ProjectManager for task management
- Integrate ProjectManager into workflows

## Overview

ProjectManager manages tasks, plans, and project execution.

## Key Concepts

### ProjectManager Role

The `ProjectManager` role:
- Creates task lists
- Manages project execution
- Tracks progress

## Guidance

### 1. Using ProjectManager

```python
from framework.roles.project_manager import ProjectManager

pm = ProjectManager(llm=llm)
```

## Exercises

### Exercise 1: Task Manager
Use ProjectManager to manage tasks

### Exercise 2: Project Tracker
Track project progress with ProjectManager

## Practice Tasks

1. **Task Creator**: Create tasks for projects
2. **Progress Tracker**: Track task progress
3. **Project Monitor**: Monitor project status

## Next Steps

- Move to Lesson 19 to learn about Memory
- Try managing different projects
- Experiment with task tracking

## Additional Resources

- Check `framework/roles/project_manager.py` for full implementation

