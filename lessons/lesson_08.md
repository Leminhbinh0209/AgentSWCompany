# Lesson 08: Complete Software Company Workflow

## Learning Targets

By the end of this lesson, you will be able to:
- Understand the complete workflow from idea to code
- Create and run a complete team workflow
- Analyze workflow results and statistics
- Understand message flow between roles

## Overview

This lesson brings together all the concepts from previous lessons to create a complete software development workflow. You'll see how roles collaborate to transform an idea into working code.

## Key Concepts

### Complete Workflow

1. **User Requirement** → ProductManager
2. **PRD** → Architect
3. **Design** → Engineer
4. **Code** → Final Output

### Workflow Components

- **Team**: Orchestrates the workflow
- **Roles**: Perform specific tasks
- **Actions**: Execute tasks
- **Messages**: Enable communication

## Guidance

### 1. Setting Up the Workflow

```python
from framework.team import Team
from framework.roles.product_manager import ProductManager
from framework.roles.architect import Architect
from framework.roles.engineer import Engineer

team = Team()
team.hire([
    ProductManager(llm=llm),
    Architect(llm=llm),
    Engineer(llm=llm),
])
```

### 2. Running the Workflow

```python
idea = "Create a calculator application"
result = await team.run(idea, n_round=10)
```

### 3. Analyzing Results

```python
if "code" in result:
    print(result["code"])
if "prd" in result:
    print(result["prd"])
if "design" in result:
    print(result["design"])
```

### 4. Message Statistics

```python
# Count messages by role
role_counts = {}
for msg in team.environment.message_history:
    role_counts[msg.role] = role_counts.get(msg.role, 0) + 1
```

## Exercises

### Exercise 1: Custom Workflow
Create a workflow with:
- Custom roles
- Additional steps
- Different routing logic

**Solution Template:**
```python
team = Team()
# Add custom roles
# Run workflow
# Analyze results
```

### Exercise 2: Workflow Analyzer
Create an analyzer that:
- Tracks workflow progress
- Identifies bottlenecks
- Suggests optimizations

### Exercise 3: Workflow Optimizer
Optimize the workflow to:
- Reduce rounds needed
- Improve output quality
- Handle errors gracefully

**Challenge:** Can you implement parallel processing for independent tasks?

## Practice Tasks

1. **Workflow Tester**: Test workflows with different ideas
2. **Workflow Monitor**: Monitor workflow execution in real-time
3. **Workflow Reporter**: Generate detailed workflow reports

## Next Steps

After completing this lesson:
- Move to Lesson 09 to learn about Tools (Editor, Terminal)
- Try creating workflows with different role combinations
- Experiment with workflow customization

## Common Pitfalls

- **Round Limits**: Workflows stop after max_rounds
- **Message Routing**: Ensure proper message routing
- **Error Handling**: Handle errors in workflow

## Additional Resources

- Check `tutorial_example/simple_software_company.py` for a complete example
- Review previous lessons for component details

