# Lesson 34: generate_repo() - Complete Software Company

## Learning Targets

By the end of this lesson, you will be able to:
- Use generate_repo() for fully automated project generation
- Understand how all components work together
- Build CLI tools using generate_repo()
- Compare manual vs automated approaches
- Create complete software companies

## Overview

generate_repo() is the main entry point that combines all components into a single function. It's similar to MetaGPT's `metagpt "Create a 2048 game"` command.

## Key Concepts

### generate_repo() Function

The main function that:
- Creates Context and Team automatically
- Hires all necessary roles (including TeamLeader)
- Sets up cost management
- Runs workflow automatically
- Manages project paths
- Returns project path

### Integration

generate_repo() integrates:
- Context system
- Cost management
- TeamLeader coordination
- Environment.run() automatic workflow
- Project path management
- Serialization support

## Guidance

### 1. Simple Usage

```python
from framework.software_company import generate_repo

project_path = generate_repo("Create a calculator app")
```

### 2. With Options

```python
project_path = generate_repo(
    idea="Create a game",
    investment=15.0,
    n_round=10,
    project_name="my_game"
)
```

### 3. Async Version

```python
from framework.software_company import generate_repo_async

project_path = await generate_repo_async("Create a todo app")
```

### 4. Recovery

```python
# Recover from saved state
project_path = generate_repo(
    idea="",  # Will use idea from saved state
    recover_path="./storage/team"
)
```

## Exercises

### Exercise 1: Project Generator
Create a function that:
- Uses generate_repo() for multiple projects
- Tracks all project paths
- Generates a summary

### Exercise 2: CLI Tool
Build a CLI tool that:
- Takes idea as argument
- Uses generate_repo()
- Outputs project path

## Practice Tasks

1. **Project Creator**: Generate multiple projects
2. **CLI Builder**: Build command-line tools
3. **Batch Generator**: Generate projects in batch

## Next Steps

- Try building your own CLI tool
- Experiment with different project types
- Integrate with other systems

## Additional Resources

- Check `framework/software_company.py` for full implementation
- Review MetaGPT's software_company.py for reference
- See lesson_27.py for CLI tool example

## Congratulations! 🎉

You've completed all 34 lessons and learned:
- Messages and communication
- Roles and actions
- Teams and workflows
- Planning and memory
- Advanced actions
- All new features (Context, Cost Management, TeamLeader, etc.)
- Complete automation with generate_repo()

You can now build fully automated software companies!

