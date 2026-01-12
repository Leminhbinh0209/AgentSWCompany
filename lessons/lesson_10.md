# Lesson 10: Terminal Tool

## Learning Targets

By the end of this lesson, you will be able to:
- Use the Terminal tool to execute commands
- Run Python code through the terminal
- Check Python syntax
- Get system information

## Overview

The Terminal tool allows agents to execute shell commands and run Python code. It's essential for testing, building, and running code.

## Key Concepts

### Terminal Tool

The `Terminal` class provides:
- **run_command()**: Execute shell commands
- **run_python()**: Execute Python code
- **check_syntax()**: Validate Python syntax
- **get_python_version()**: Get Python version

## Guidance

### 1. Running Commands

```python
from framework.tools.terminal import Terminal

terminal = Terminal(workspace_path=".")
result = await terminal.run_command("ls -la")
```

### 2. Running Python Code

```python
code = "print('Hello')"
result = await terminal.run_python(code)
```

### 3. Checking Syntax

```python
result = await terminal.check_syntax("file.py")
if result['valid']:
    print("Syntax is valid")
```

## Exercises

### Exercise 1: Command Runner
Create a command runner that:
- Executes multiple commands
- Tracks success/failure
- Collects outputs

### Exercise 2: Code Executor
Create a code executor that:
- Runs Python code
- Captures output and errors
- Handles timeouts

### Exercise 3: Syntax Checker
Create a syntax checker that:
- Checks multiple files
- Reports all errors
- Suggests fixes

**Challenge:** Can you implement a code formatter?

## Practice Tasks

1. **Command Tester**: Test various shell commands
2. **Code Runner**: Run and test Python scripts
3. **System Info**: Gather system information

## Next Steps

After completing this lesson:
- Move to Lesson 11 to learn about the Browser tool
- Try executing complex commands
- Experiment with Python code execution

## Common Pitfalls

- **Async Required**: All methods are async
- **Timeout**: Commands may timeout
- **Error Handling**: Check status and stderr

## Additional Resources

- Check `framework/tools/terminal.py` for full implementation

