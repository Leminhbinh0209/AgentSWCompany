# Lesson 07: Core Actions - WritePRD, WriteDesign, WriteCode

## Learning Targets

By the end of this lesson, you will be able to:
- Understand the core actions: WritePRD, WriteDesign, WriteCode
- Use actions in sequence to create a workflow
- Convert ActionOutput to Messages
- Understand the action chain

## Overview

The core actions form the foundation of the software development workflow:
1. **WritePRD**: Creates Product Requirement Documents from user requirements
2. **WriteDesign**: Creates system designs from PRDs
3. **WriteCode**: Generates code from designs

## Key Concepts

### WritePRD Action

- Takes user requirements as input
- Generates comprehensive PRD
- Includes user stories, requirements, metrics

### WriteDesign Action

- Takes PRD as input
- Creates system architecture
- Includes components, APIs, technology stack

### WriteCode Action

- Takes design as input
- Generates implementation code
- Includes error handling, comments, best practices

## Guidance

### 1. Using WritePRD

```python
from framework.actions.write_prd import WritePRD

write_prd = WritePRD(llm=llm)
messages = [Message(content="Create a calculator", role="User")]
result = await write_prd.run(messages=messages)
```

### 2. Using WriteDesign

```python
from framework.actions.write_design import WriteDesign

write_design = WriteDesign(llm=llm)
prd_message = Message(content=prd_content, role="ProductManager")
result = await write_design.run(messages=[prd_message])
```

### 3. Using WriteCode

```python
from framework.actions.write_code import WriteCode

write_code = WriteCode(llm=llm)
design_message = Message(content=design_content, role="Architect")
result = await write_code.run(messages=[design_message])
```

### 4. Action Chain

```python
# Chain actions together
prd_result = await write_prd.run(messages=[requirement_msg])
design_result = await write_design.run(messages=[prd_result.to_message(...)])
code_result = await write_code.run(messages=[design_result.to_message(...)])
```

## Exercises

### Exercise 1: Custom PRD
Create a custom WritePRD that:
- Includes specific sections
- Validates requirements
- Formats output differently

**Solution Template:**
```python
class CustomWritePRD(WritePRD):
    async def run(self, messages=None, **kwargs):
        # Your custom logic
        pass
```

### Exercise 2: Design Validator
Create a validator that:
- Checks if design matches PRD
- Validates architecture decisions
- Suggests improvements

### Exercise 3: Code Generator
Enhance WriteCode to:
- Generate tests alongside code
- Include documentation
- Follow specific coding standards

**Challenge:** Can you create a feedback loop where code is reviewed and improved?

## Practice Tasks

1. **Action Tester**: Test each action with different inputs
2. **Workflow Builder**: Build custom workflows with actions
3. **Action Analyzer**: Analyze action outputs and quality

## Next Steps

After completing this lesson:
- Move to Lesson 08 to see the complete workflow
- Try creating custom actions
- Experiment with action chaining

## Common Pitfalls

- **Message Context**: Actions need proper message context
- **Action Order**: Actions must be executed in correct order
- **Output Format**: ActionOutput needs proper structure

## Additional Resources

- Check `framework/actions/write_prd.py` for WritePRD implementation
- Check `framework/actions/write_design.py` for WriteDesign implementation
- Check `framework/actions/write_code.py` for WriteCode implementation

