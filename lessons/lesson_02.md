# Lesson 02: Understanding Actions

## Learning Targets

By the end of this lesson, you will be able to:
- Understand the `Action` base class
- Create custom actions
- Use actions with parameters and context
- Convert ActionOutput to Messages

## Overview

Actions represent tasks that agents can perform. Every agent has a set of actions they can execute. Actions are the building blocks of agent behavior.

## Key Concepts

### Action Class

The `Action` base class provides:
- **name**: The action's name
- **llm**: Optional LLM for AI-powered actions
- **context**: Shared context dictionary
- **run()**: Abstract method that must be implemented

### ActionOutput

Actions return `ActionOutput` which contains:
- **content**: Human-readable output
- **instruct_content**: Structured data (optional)

## Guidance

### 1. Creating a Simple Action

```python
from framework.action import Action
from framework.schema import ActionOutput
from typing import List

class MyAction(Action):
    async def run(self, messages: List[Message] = None, **kwargs) -> ActionOutput:
        # Your logic here
        return ActionOutput(content="Result")
```

### 2. Action with Parameters

```python
class CalculateAction(Action):
    async def run(self, messages: List[Message] = None, **kwargs) -> ActionOutput:
        a = kwargs.get("a", 0)
        b = kwargs.get("b", 0)
        result = a + b
        return ActionOutput(
            content=f"Result: {result}",
            instruct_content={"result": result}
        )
```

### 3. Using Message Context

```python
async def run(self, messages: List[Message] = None, **kwargs) -> ActionOutput:
    if messages:
        last_message = messages[-1]
        # Use message content in your logic
        content = last_message.content
    return ActionOutput(content=content)
```

## Exercises

### Exercise 1: Create a Simple Action
Create an action called `ReverseStringAction` that:
- Takes a string parameter
- Returns the reversed string
- Includes both content and structured output

**Solution Template:**
```python
class ReverseStringAction(Action):
    async def run(self, messages: List[Message] = None, **kwargs) -> ActionOutput:
        # Your code here
        pass
```

### Exercise 2: Action with Multiple Parameters
Create a `FormatTextAction` that:
- Takes text, width, and alignment parameters
- Formats text according to the parameters
- Returns formatted text

### Exercise 3: Context-Aware Action
Create a `SummarizeAction` that:
- Takes messages as context
- Summarizes the conversation
- Returns a summary

**Challenge:** Can you make it use the LLM for better summaries?

## Practice Tasks

1. **Action Chain**: Create multiple actions and chain them together
2. **Action Validator**: Create an action that validates input parameters
3. **Action Logger**: Create an action that logs all other actions

## Next Steps

After completing this lesson:
- Move to Lesson 03 to learn about Roles
- Try creating more complex actions
- Experiment with action chaining

## Common Pitfalls

- **Forgetting async**: All action run methods must be async
- **Missing return type**: Always return ActionOutput
- **Not handling kwargs**: Use kwargs.get() with defaults for optional parameters

## Additional Resources

- Check `framework/action.py` for the base Action class
- See `framework/actions/write_prd.py` for a real-world action example

