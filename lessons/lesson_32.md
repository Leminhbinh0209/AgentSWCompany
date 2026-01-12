# Lesson 32: Serialization and State Management

## Learning Targets

By the end of this lesson, you will be able to:
- Serialize team state to disk
- Deserialize and recover team state
- Understand what state is preserved
- Use serialization for project recovery
- Manage long-running projects

## Overview

Serialization allows you to save the complete state of a team and recover it later. This is essential for project recovery, state persistence, and resuming interrupted workflows.

## Key Concepts

### Serialization

Saves team state to disk:
```python
team.serialize(Path("./storage/team"))
```

### Deserialization

Loads team state from disk:
```python
team = Team.deserialize(Path("./storage/team"), context=ctx)
```

### Preserved State

Serialization preserves:
- Team idea and investment
- All roles and their state
- Context (project path, kwargs)
- Cost manager state
- Message history
- Current round

## Guidance

### 1. Serializing Team

```python
from pathlib import Path

storage_path = Path("./storage/team")
team.serialize(storage_path)
```

### 2. Deserializing Team

```python
from framework.context import Context

ctx = Context()
team = Team.deserialize(storage_path, context=ctx)
```

### 3. Project Recovery

```python
# Save state periodically
if round_num % 5 == 0:
    team.serialize(Path("./storage/team"))

# Recover after interruption
team = Team.deserialize(Path("./storage/team"), context=ctx)
await team.run(idea=team.idea, n_round=remaining_rounds)
```

### 4. State Verification

```python
# Verify recovered state
assert team.idea == original_idea
assert team.investment == original_investment
assert len(team.environment.roles) == original_role_count
```

## Exercises

### Exercise 1: State Saver
Create a system that:
- Saves team state periodically
- Recovers from saved state
- Verifies state integrity

### Exercise 2: Project Recovery
Build a recovery system that:
- Detects interrupted projects
- Recovers team state
- Resumes workflow

## Practice Tasks

1. **State Manager**: Save and load team state
2. **Recovery System**: Implement project recovery
3. **State Validator**: Verify serialized state

## Next Steps

- Move to Lesson 33 to learn about Configuration System
- Try implementing periodic state saving
- Experiment with project recovery

## Additional Resources

- Check `framework/team.py` for serialize/deserialize methods
- Review `framework/context.py` for context serialization

