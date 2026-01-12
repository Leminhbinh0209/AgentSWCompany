# Lesson 22: QA Engineer

## Learning Targets

By the end of this lesson, you will be able to:
- Understand the QAEngineer role
- Generate tests automatically
- Report bugs and issues

## Overview

QAEngineer ensures code quality through automated testing and bug reporting.

## Key Concepts

### QAEngineer Role

The `QAEngineer` role provides:
- Test generation
- Test execution
- Bug reporting

## Guidance

### 1. Using QAEngineer

```python
from framework.roles.qa_engineer import QAEngineer

qa = QAEngineer(llm=llm)
test_code = await qa.generate_tests(code)
```

## Exercises

### Exercise 1: Test Generator
Use QAEngineer to generate tests

### Exercise 2: Bug Reporter
Report bugs from test results

## Practice Tasks

1. **Test Creator**: Generate tests for various code
2. **Test Runner**: Execute tests and collect results
3. **Bug Tracker**: Track and report bugs

## Next Steps

- Move to Lesson 23 to learn about Technical Writer
- Try generating different test types
- Experiment with bug reporting

## Additional Resources

- Check `framework/roles/qa_engineer.py` for full implementation

