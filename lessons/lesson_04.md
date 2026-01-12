# Lesson 04: Understanding Environment

## Learning Targets

By the end of this lesson, you will be able to:
- Understand the `Environment` class and its purpose
- Add roles to the environment
- Publish messages (broadcast and targeted)
- Use environment context and message history

## Overview

The Environment is the central hub that manages all roles and routes messages between them. It maintains message history and provides shared context for all roles.

## Key Concepts

### Environment Class

The `Environment` class contains:
- **roles**: Dictionary of roles by name
- **message_history**: List of all messages
- **context**: Shared context dictionary

### Environment Methods

- **add_role(role)**: Add a role to the environment
- **add_roles(roles)**: Add multiple roles
- **publish_message(message, send_to)**: Publish a message (broadcast or targeted)
- **get_role(name)**: Get a role by name
- **get_all_roles()**: Get all roles

## Guidance

### 1. Creating Environment

```python
from framework.environment import Environment

env = Environment()
```

### 2. Adding Roles

```python
env.add_role(role1)
env.add_role(role2)

# Or add multiple at once
env.add_roles([role1, role2])
```

### 3. Publishing Messages

```python
# Broadcast to all roles
message = Message(content="Hello", role="User")
env.publish_message(message)

# Send to specific role
env.publish_message(message, send_to="Agent1")
```

### 4. Using Context

```python
env.context["key"] = "value"
# All roles can access this context
```

## Exercises

### Exercise 1: Multi-Agent Communication
Create an environment with 3 roles:
- Role A sends a message to Role B
- Role B processes and sends to Role C
- Role C responds back

**Solution Template:**
```python
env = Environment()
# Add roles
# Publish messages
# Track message flow
```

### Exercise 2: Message Routing
Create a message router that:
- Routes messages based on content keywords
- Routes messages based on sender
- Maintains routing history

### Exercise 3: Context Sharing
Create an environment where:
- Roles share project information via context
- Roles can read and update context
- Context changes are logged

**Challenge:** Can you implement a context versioning system?

## Practice Tasks

1. **Message Filter**: Filter messages in history by role or content
2. **Role Manager**: Create a manager that adds/removes roles dynamically
3. **Message Analyzer**: Analyze message patterns in history

## Next Steps

After completing this lesson:
- Move to Lesson 05 to learn about Teams
- Try implementing custom message routing
- Experiment with environment context

## Common Pitfalls

- **Broadcast vs Targeted**: Remember to specify send_to for targeted messages
- **Context Updates**: Context changes affect all roles immediately
- **Message History**: History grows indefinitely (consider cleanup)

## Additional Resources

- Check `framework/environment.py` for the full Environment class
- See how environment is used in `framework/team.py`

