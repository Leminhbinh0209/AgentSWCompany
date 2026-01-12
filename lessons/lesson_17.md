# Lesson 17: Planning

## Learning Targets

By the end of this lesson, you will be able to:
- Use Planner to create plans from goals
- Understand task management
- Work with plans and tasks

## Overview

Planner creates structured plans from goals, breaking them down into manageable tasks.

## Key Concepts

### Planner

The `Planner` class provides:
- **create_plan()**: Create plan from goal
- Task breakdown
- Dependency management

## Guidance

### 1. Creating Plans

```python
from framework.planning.planner import Planner

planner = Planner(llm=llm)
plan = await planner.create_plan("Goal description")
```

## Exercises

### Exercise 1: Plan Creator
Create plans for different goals

### Exercise 2: Task Manager
Manage tasks and dependencies

## Practice Tasks

1. **Plan Generator**: Generate plans for various projects
2. **Task Tracker**: Track task progress
3. **Dependency Analyzer**: Analyze task dependencies

## Next Steps

- Move to Lesson 18 to learn about Project Manager
- Try creating complex plans
- Experiment with task management

## Additional Resources

- Check `framework/planning/planner.py` for full implementation

