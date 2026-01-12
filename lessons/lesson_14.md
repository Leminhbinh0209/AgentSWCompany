# Lesson 14: Code Generation

## Learning Targets

By the end of this lesson, you will be able to:
- Use CodeGenerator to generate projects
- Generate code files from designs
- Understand code generation workflow

## Overview

CodeGenerator uses LLMs to generate code files from design specifications.

## Key Concepts

### CodeGenerator

The `CodeGenerator` class provides:
- **generate_project()**: Generate complete project structure
- **generate_file()**: Generate individual code files

## Guidance

### 1. Generating Projects

```python
from framework.repository.code_generator import CodeGenerator

generator = CodeGenerator(repo, llm=llm)
result = await generator.generate_project(design, "project_name")
```

### 2. Generating Files

```python
result = await generator.generate_file("file.py", code, repo="srcs")
```

## Exercises

### Exercise 1: Project Generator
Generate a complete project with multiple files

### Exercise 2: Code Generator
Generate code from design specifications

## Practice Tasks

1. **Generator Tester**: Test code generation with different designs
2. **File Generator**: Generate multiple files for a project
3. **Template Generator**: Create code templates

## Next Steps

- Move to Lesson 15 to learn about Code Review
- Try generating different types of projects
- Experiment with code generation

## Additional Resources

- Check `framework/repository/code_generator.py` for full implementation

