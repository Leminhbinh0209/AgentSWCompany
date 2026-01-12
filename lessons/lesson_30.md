# Lesson 30: TeamLeader Role

## Learning Targets

By the end of this lesson, you will be able to:
- Understand the TeamLeader role and its purpose
- Use TeamLeader to coordinate team workflow
- Publish messages to team members
- Get team information
- Integrate TeamLeader into teams

## Overview

TeamLeader is a special role that orchestrates the team workflow. It coordinates team members, provides team information, and can guide the overall project execution.

## Key Concepts

### TeamLeader Role

The `TeamLeader` class:
- **Orchestrates**: Coordinates team workflow
- **Informs**: Provides team information
- **Publishes**: Can send messages to team members
- **Coordinates**: Manages overall project execution

### Team Information

TeamLeader can access:
- List of all team members
- Role profiles and goals
- Team state and progress

## Guidance

### 1. Creating TeamLeader

```python
from framework.roles.team_leader import TeamLeader

team_leader = TeamLeader(llm=llm)
```

### 2. Adding to Team

```python
team = Team(context=Context())
team.hire([
    TeamLeader(llm=llm),
    ProductManager(llm=llm),
    Architect(llm=llm),
    Engineer(llm=llm),
])
```

### 3. Getting Team Information

```python
team_info = team_leader._get_team_info()
# Returns string with all team members and their info
```

### 4. Publishing Messages

```python
# Publish to specific role
team_leader.publish_team_message("Let's start!", send_to="ProductManager")

# Broadcast to all
team_leader.publish_team_message("Team update", send_to="")
```

### 5. Team Coordination

```python
# TeamLeader can react to coordinate
coordination_msg = await team_leader.react()
```

## Exercises

### Exercise 1: Team Coordinator
Create a TeamLeader that:
- Monitors team progress
- Publishes coordination messages
- Provides team status updates

### Exercise 2: Workflow Orchestrator
Enhance TeamLeader to:
- Analyze team state
- Make coordination decisions
- Guide workflow progression

## Practice Tasks

1. **Team Builder**: Create teams with TeamLeader
2. **Coordinator**: Use TeamLeader to coordinate workflows
3. **Team Monitor**: Monitor team state with TeamLeader

## Next Steps

- Move to Lesson 31 to learn about Environment.run()
- Try using TeamLeader in complex workflows
- Experiment with team coordination

## Additional Resources

- Check `framework/roles/team_leader.py` for full implementation
- Review team coordination patterns

