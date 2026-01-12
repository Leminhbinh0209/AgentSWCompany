# Lesson 29: Cost Management

## Learning Targets

By the end of this lesson, you will be able to:
- Use CostManager to track API costs
- Enforce budget limits
- View cost history and summaries
- Handle budget exceptions
- Reset cost tracking

## Overview

Cost Management is essential for controlling API expenses. The CostManager tracks all costs, enforces budgets, and provides detailed cost history.

## Key Concepts

### CostManager

The `CostManager` class provides:
- **add_cost()**: Record a cost transaction
- **get_remaining_budget()**: Calculate remaining budget
- **get_summary()**: Get cost summary
- **reset()**: Clear all costs

### CostRecord

Each cost transaction is recorded as a `CostRecord` with:
- **timestamp**: When the cost occurred
- **role**: Which role incurred the cost
- **action**: Which action caused the cost
- **cost**: Cost amount
- **description**: Optional description

### Budget Enforcement

When budget is exceeded, `NoMoneyException` is raised:
```python
if total_cost >= max_budget:
    raise NoMoneyException(total_cost, "Insufficient funds")
```

## Guidance

### 1. Creating Cost Manager

```python
from framework.utils.cost_manager import CostManager

cost_mgr = CostManager(max_budget=10.0)
```

### 2. Adding Costs

```python
cost_mgr.add_cost(
    cost=0.5,
    role="ProductManager",
    action="WritePRD",
    description="PRD generation"
)
```

### 3. Checking Budget

```python
remaining = cost_mgr.get_remaining_budget()
if remaining < 1.0:
    print("Warning: Low budget!")
```

### 4. Handling Budget Exceptions

```python
from framework.utils.exceptions import NoMoneyException

try:
    cost_mgr.add_cost(15.0, role="Engineer", action="WriteCode")
except NoMoneyException as e:
    print(f"Budget exceeded: ${e.total_cost:.2f}")
```

### 5. Cost Summary

```python
summary = cost_mgr.get_summary()
# Returns: {
#     "total_cost": 1.2,
#     "max_budget": 10.0,
#     "remaining": 8.8,
#     "transactions": 3
# }
```

## Exercises

### Exercise 1: Budget Tracker
Create a function that:
- Tracks costs for multiple roles
- Warns when budget is low
- Provides detailed reports

### Exercise 2: Cost Analyzer
Create a system that:
- Analyzes costs by role
- Identifies expensive actions
- Suggests optimizations

## Practice Tasks

1. **Cost Tracker**: Track costs across a project
2. **Budget Manager**: Manage multiple budgets
3. **Cost Reporter**: Generate cost reports

## Next Steps

- Move to Lesson 30 to learn about TeamLeader Role
- Integrate cost management with Team
- Experiment with budget limits

## Additional Resources

- Check `framework/utils/cost_manager.py` for full implementation
- Review `framework/utils/exceptions.py` for exceptions

