# Lesson 09: File Editor Tool

## Learning Targets

By the end of this lesson, you will be able to:
- Use the Editor tool to create, read, and edit files
- Search for content in files
- Find files by pattern
- Manage file operations in a workspace

## Overview

The Editor tool provides file operations for the multi-agent framework. It allows agents to create, read, edit, and search files in a workspace.

## Key Concepts

### Editor Tool

The `Editor` class provides:
- **create_file()**: Create new files with content
- **read()**: Read file contents
- **edit_file()**: Replace file content
- **search_in_file()**: Search for patterns in files
- **find_file()**: Find files by pattern

## Guidance

### 1. Creating Files

```python
from framework.tools.editor import Editor

editor = Editor(workspace_path=".")
result = await editor.create_file("hello.py", "print('Hello')")
```

### 2. Reading Files

```python
result = await editor.read("hello.py")
content = result['content']
```

### 3. Editing Files

```python
new_content = "print('Updated')"
result = await editor.edit_file("hello.py", new_content)
```

### 4. Searching in Files

```python
result = await editor.search_in_file("hello.py", "def")
matches = result['matches']
```

## Exercises

### Exercise 1: File Manager
Create a file manager that:
- Creates multiple files
- Reads all files
- Generates a summary

### Exercise 2: Code Analyzer
Create a code analyzer that:
- Searches for function definitions
- Finds imports
- Counts lines of code

### Exercise 3: File Organizer
Create a file organizer that:
- Groups files by extension
- Creates directory structure
- Moves files appropriately

**Challenge:** Can you implement file versioning?

## Practice Tasks

1. **File Creator**: Create a script that generates multiple files
2. **File Searcher**: Search across multiple files
3. **File Editor**: Batch edit multiple files

## Next Steps

After completing this lesson:
- Move to Lesson 10 to learn about the Terminal tool
- Try creating complex file structures
- Experiment with file operations

## Common Pitfalls

- **Workspace Path**: Always specify workspace path
- **File Paths**: Use relative paths within workspace
- **Async Operations**: All methods are async

## Additional Resources

- Check `framework/tools/editor.py` for full implementation

