# Lesson 24: DevOps Engineer

## Learning Targets

By the end of this lesson, you will be able to:
- Understand the DevOpsEngineer role
- Create Dockerfiles
- Setup CI/CD pipelines
- Create deployment scripts

## Overview

DevOpsEngineer automates deployment processes including containerization, CI/CD, and deployment scripts.

## Key Concepts

### DevOpsEngineer Role

The `DevOpsEngineer` role provides:
- Dockerfile creation
- CI/CD setup
- Deployment scripts

## Guidance

### 1. Using DevOpsEngineer

```python
from framework.roles.devops_engineer import DevOpsEngineer

devops = DevOpsEngineer(llm=llm)
dockerfile = await devops.create_dockerfile(project_info)
```

## Exercises

### Exercise 1: Container Creator
Create Dockerfiles for different projects

### Exercise 2: CI/CD Setup
Setup CI/CD pipelines

## Practice Tasks

1. **Docker Creator**: Create Dockerfiles
2. **CI/CD Builder**: Build CI/CD configurations
3. **Deploy Script Generator**: Generate deployment scripts

## Next Steps

- Review all lessons to master the framework
- Try combining all roles in a complete workflow
- Experiment with different project types

## Additional Resources

- Check `framework/roles/devops_engineer.py` for full implementation

