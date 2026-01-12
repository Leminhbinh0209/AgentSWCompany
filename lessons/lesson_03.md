# Lesson 03: Understanding Roles

## Learning Targets

By the end of this lesson, you will be able to:
- Understand the `Role` class and its purpose
- Create roles with actions
- Understand how roles observe, think, and act
- Use role memory and context

## Overview

Roles represent agents in the multi-agent system. Each role has a goal, a set of actions it can perform, and memory to track conversations. Roles observe messages, think about what to do, and act accordingly.

## Key Concepts

### Role Class

The `Role` class contains:
- **name**: Unique identifier for the role
- **profile**: Description of the role
- **goal**: What the role aims to achieve
- **actions**: List of actions the role can perform
- **llm**: Optional LLM for AI-powered actions
- **memory**: Recent messages (deque, max 100)
- **working_memory**: Current task context

### Role Methods

- **observe(message)**: Store a message in memory
- **think()**: Decide which action to take
- **act(action)**: Execute an action
- **react()**: Complete cycle: observe -> think -> act

## Guidance

### 1. Creating a Role

```python
from framework.role import Role
from framework.actions.my_action import MyAction

role = Role(
    name="MyRole",
    profile="Description",
    goal="Achieve something",
    actions=[MyAction(llm=llm)],
    llm=llm
)
```

### 2. Role Observes Messages

```python
message = Message(content="Hello", role="User")
role.observe(message)
```

### 3. Role Reacts

```python
# Complete cycle: observe -> think -> act
response = await role.react()
```

### 4. Role with Context

```python
context = {"key": "value"}
role.set_context(context)
```

## Exercises

### Exercise 1: Create a Custom Role
Create a role called `CalculatorRole` that:
- Has a goal to perform calculations
- Has an action to add two numbers
- Can observe calculation requests
- Responds with results

**Solution Template:**
```python
class AddAction(Action):
    async def run(self, messages: List[Message] = None, **kwargs) -> ActionOutput:
        # Your code here
        pass

role = Role(
    name="CalculatorRole",
    profile="Calculator",
    goal="Perform calculations",
    actions=[AddAction(llm=llm)],
    llm=llm
)
```

### Exercise 2: Role Memory
Create a role that:
- Remembers the last 5 messages
- Can recall previous conversations
- Uses memory to provide context-aware responses

### Exercise 3: Multi-Action Role
Create a role with multiple actions:
- One action for greeting
- One action for saying goodbye
- Role decides which action to use based on message content

**Challenge:** Can you make the role learn from past interactions?

## Practice Tasks

1. **Role Logger**: Create a role that logs all its actions
2. **Role Validator**: Create a role that validates input before acting
3. **Role Chain**: Create multiple roles that work together

## Next Steps

After completing this lesson:
- Move to Lesson 04 to learn about the Environment
- Try creating roles with multiple actions
- Experiment with role memory and context

## Common Pitfalls

- **Forgetting async**: Role methods like `act()` and `react()` are async
- **Empty actions**: Roles need at least one action to do something
- **Memory overflow**: Memory is limited (max 100 messages)

## Additional Resources

- Check `framework/role.py` for the full Role class
- See `framework/roles/product_manager.py` for a real-world role example

