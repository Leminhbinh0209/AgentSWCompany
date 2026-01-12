# Lesson 05: Understanding Teams

## Learning Targets

By the end of this lesson, you will be able to:
- Understand the `Team` class and its purpose
- Create teams with multiple roles
- Run teams with ideas
- Understand team workflow and rounds

## Overview

Teams orchestrate multiple roles to work together on a project. They manage the workflow from initial idea through PRD, design, and code generation.

## Key Concepts

### Team Class

The `Team` class contains:
- **environment**: Environment managing roles
- **idea**: The initial project idea
- **investment**: Budget for the project
- **max_rounds**: Maximum number of rounds
- **current_round**: Current round number

### Team Methods

- **hire(roles)**: Add roles to the team
- **invest(amount)**: Set project budget
- **run(idea, n_round)**: Run the team workflow

## Guidance

### 1. Creating a Team

```python
from framework.team import Team

team = Team()
```

### 2. Hiring Roles

```python
from framework.roles.product_manager import ProductManager
from framework.roles.architect import Architect
from framework.roles.engineer import Engineer

team.hire([
    ProductManager(llm=llm),
    Architect(llm=llm),
    Engineer(llm=llm),
])
```

### 3. Running a Team

```python
idea = "Create a calculator application"
result = await team.run(idea, n_round=10)
```

### 4. Accessing Results

```python
if "code" in result:
    print(result["code"])
if "prd" in result:
    print(result["prd"])
if "design" in result:
    print(result["design"])
```

## Exercises

### Exercise 1: Custom Team
Create a team with custom roles:
- Add a QA role
- Add a Documentation role
- Run the team and see how they interact

**Solution Template:**
```python
team = Team()
# Add custom roles
# Run with idea
# Check results
```

### Exercise 2: Team Workflow
Modify the team workflow to:
- Add more rounds
- Track progress per round
- Stop early if complete

### Exercise 3: Team Budget
Implement budget tracking:
- Each action costs money
- Track spending per role
- Stop if budget exceeded

**Challenge:** Can you implement a bidding system for actions?

## Practice Tasks

1. **Team Monitor**: Create a monitor that tracks team progress
2. **Team Optimizer**: Optimize team workflow for efficiency
3. **Team Analyzer**: Analyze team performance and bottlenecks

## Next Steps

After completing this lesson:
- Move to Lesson 06 to learn about LLMs
- Try creating teams with different role combinations
- Experiment with team workflows

## Common Pitfalls

- **Async Required**: Team.run() is async, use await
- **Round Limits**: Teams stop after max_rounds or when complete
- **Role Order**: Roles process in specific order (ProductManager -> Architect -> Engineer)

## Additional Resources

- Check `framework/team.py` for the full Team class
- See `tutorial_example/simple_software_company.py` for a complete example

