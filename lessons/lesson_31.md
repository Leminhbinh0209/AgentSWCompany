# Lesson 31: Environment.run() and Automatic Workflow

## Learning Targets

By the end of this lesson, you will be able to:
- Understand Environment.run() for automatic workflow
- Use is_idle property to detect completion
- Run workflows without manual iteration
- Understand automatic message routing
- Build fully automated systems

## Overview

Environment.run() is the key to fully automated workflows. Instead of manually iterating through roles, the environment automatically processes all roles that have messages to handle.

## Key Concepts

### Environment.run()

Automatically processes all roles in one round:
```python
await env.run()  # Processes all roles with messages
```

### is_idle Property

Detects when all roles are idle:
```python
if env.is_idle:
    # All roles have no messages, workflow can stop
```

### Automatic Routing

Messages are automatically routed based on cause_by:
- WritePRD → Architect
- WriteDesign → Engineer
- WriteCode → Final output

## Guidance

### 1. Running Environment

```python
from framework.environment import Environment

env = Environment(context=Context())
# ... add roles and publish messages ...

# Run one round automatically
await env.run()
```

### 2. Multiple Rounds

```python
for round_num in range(n_rounds):
    if env.is_idle:
        break
    await env.run()
```

### 3. Idle Detection

```python
# Check if environment is idle
if env.is_idle:
    print("Workflow complete!")
else:
    print("Still processing...")
```

### 4. Message History

```python
# Access message history
history = env.history  # or env.message_history
print(f"Total messages: {len(history)}")
```

## Exercises

### Exercise 1: Automatic Workflow
Create a workflow that:
- Runs automatically for multiple rounds
- Stops when idle
- Reports progress

### Exercise 2: Workflow Monitor
Create a monitor that:
- Tracks workflow progress
- Detects idle state
- Reports statistics

## Practice Tasks

1. **Workflow Runner**: Run workflows automatically
2. **Idle Detector**: Implement idle detection logic
3. **Progress Tracker**: Track workflow progress

## Next Steps

- Move to Lesson 32 to learn about Serialization
- Try building fully automated workflows
- Experiment with idle detection

## Additional Resources

- Check `framework/environment.py` for full implementation
- Review automatic routing logic

