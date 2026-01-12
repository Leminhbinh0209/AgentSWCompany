# Lesson 13: Project Repository

## Learning Targets

By the end of this lesson, you will be able to:
- Use ProjectRepo to manage project structure
- Create files in different repositories (docs, srcs, tests)
- Organize project files
- Understand project structure

## Overview

ProjectRepo provides a structured way to manage software projects with separate repositories for docs, source code, tests, and resources.

## Key Concepts

### ProjectRepo

The `ProjectRepo` class provides:
- **docs**: Documentation repository
- **srcs**: Source code repository
- **tests**: Test repository
- **resources**: Resources repository
- **config**: Configuration repository

## Guidance

### 1. Creating Project

```python
from framework.repository.project_repo import ProjectRepo

repo = ProjectRepo("my_project")
repo.initialize_python_package("mypackage")
```

### 2. Creating Files

```python
repo.docs.create_file("README.md", "# Project")
repo.srcs.create_file("main.py", "print('Hello')")
repo.tests.create_file("test_main.py", "import unittest")
```

## Exercises

### Exercise 1: Project Setup
Create a complete project with:
- README
- Source files
- Tests
- Documentation

### Exercise 2: Project Organizer
Organize files into proper repositories based on type

## Practice Tasks

1. **Project Creator**: Create projects with standard structure
2. **File Organizer**: Organize existing files into repositories
3. **Structure Validator**: Validate project structure

## Next Steps

- Move to Lesson 14 to learn about Code Generation
- Try creating different project types
- Experiment with project structure

## Additional Resources

- Check `framework/repository/project_repo.py` for full implementation

