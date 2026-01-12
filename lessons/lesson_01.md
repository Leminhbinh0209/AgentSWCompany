# Lesson 01: Understanding Messages

## Learning Targets

By the end of this lesson, you will be able to:
- Understand the `Message` class and its purpose
- Create messages with different properties
- Understand message routing and context
- See how messages flow between agents

## Overview

Messages are the fundamental communication unit in a multi-agent system. Every interaction between agents happens through messages. Understanding messages is the first step to understanding how agents communicate.

## Key Concepts

### Message Class

The `Message` class contains:
- **content**: The actual message text
- **role**: Who sent the message (e.g., "User", "ProductManager")
- **cause_by**: Which action created this message (optional)
- **sent_from**: Explicit sender (optional)
- **send_to**: Explicit recipient (optional)
- **timestamp**: When the message was created (auto-generated)

## Guidance

### 1. Basic Message Creation

```python
from framework.schema import Message

# Simple message
msg = Message(
    content="Hello, world!",
    role="User"
)
```

### 2. Message with Context

```python
# Message with action context
msg = Message(
    content="Here is the PRD",
    role="ProductManager",
    cause_by="WritePRD"  # Tracks which action created this
)
```

### 3. Message Routing

```python
# Message with explicit routing
msg = Message(
    content="Please review this",
    role="Architect",
    sent_from="Architect",
    send_to="Engineer"
)
```

## Exercises

### Exercise 1: Create Basic Messages
Create three messages:
1. A user request message
2. A response from a ProductManager
3. A message from an Architect to an Engineer

**Solution Template:**
```python
# Your code here
```

### Exercise 2: Message Flow
Create a message flow that simulates:
1. User sends a requirement
2. ProductManager creates a PRD
3. Architect creates a design
4. Engineer writes code

**Hint:** Use a list to store messages in order.

### Exercise 3: Message Analysis
Write a function that:
- Takes a list of messages
- Returns the number of messages from each role
- Returns the most common action (cause_by)

**Challenge:** Can you find the longest message chain?

## Practice Tasks

1. **Message Logger**: Create a function that logs all messages with their timestamps
2. **Message Filter**: Create a function that filters messages by role or action
3. **Message Chain**: Create a function that finds all messages in a conversation chain

## Next Steps

After completing this lesson:
- Move to Lesson 02 to learn about Actions
- Try modifying messages to include more metadata
- Experiment with message routing between different roles

## Common Pitfalls

- **Forgetting timestamp**: Messages auto-generate timestamps, but you can set custom ones
- **Missing role**: Always specify the role that sent the message
- **Over-routing**: Not all messages need explicit sent_from/send_to

## Additional Resources

- Check `framework/schema.py` for the full Message class definition
- See how messages are used in `tutorial_example/simple_software_company.py`

