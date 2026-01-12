# Lesson 06: Understanding LLMs

## Learning Targets

By the end of this lesson, you will be able to:
- Understand the LLM interface
- Use MockLLM for testing
- Use OpenAILLM for production
- Use VLLM for localhost inference
- Use LocalLLM for llama.cpp inference
- Integrate LLMs with actions

## Overview

LLMs (Large Language Models) provide AI capabilities to the framework. The framework supports multiple LLM implementations through a common interface.

## Key Concepts

### BaseLLM Interface

All LLMs implement:
- **aask(prompt, system_msgs)**: Async method to ask the LLM

### LLM Implementations

- **MockLLM**: For testing without API keys
- **OpenAILLM**: Connects to OpenAI API
- **VLLM**: Connects to vLLM server on localhost
- **LocalLLM**: Uses llama.cpp for local GGUF model inference
- **Custom LLMs**: You can implement your own

## Guidance

### 1. Using MockLLM

```python
from framework.llm import MockLLM

llm = MockLLM()
response = await llm.aask("Hello")
```

### 2. Using OpenAILLM

```python
from framework.llm import OpenAILLM

llm = OpenAILLM(api_key="your-api-key")
response = await llm.aask("Hello")
```

### 3. Using VLLM (vLLM Server)

```python
from framework.llm import VLLM

# Connect to vLLM server running on localhost:8000
llm = VLLM(base_url="http://localhost:8000/v1", model="your-model-name")
response = await llm.aask("Hello")
```

**Requirements:**
- vLLM server running on localhost (default: `http://localhost:8000/v1`)
- Server must support OpenAI-compatible API
- Install: `pip install aiohttp` (for async HTTP requests)

### 4. Using LocalLLM (llama.cpp)

```python
from framework.llm import LocalLLM

# Load a GGUF model file
llm = LocalLLM(
    model_path="/path/to/model.gguf",
    temperature=0.2,
    max_tokens=512,
    n_ctx=2048
)
response = await llm.aask("Hello")
```

**Requirements:**
- GGUF model file
- Install: `pip install llama-cpp-python`

### 5. Using System Messages

```python
system_msg = "You are a helpful assistant"
response = await llm.aask("Hello", system_msgs=[system_msg])
```

### 6. Using LLM in Actions

```python
class MyAction(Action):
    async def run(self, messages=None, **kwargs):
        response = await self._ask_llm("Prompt", "System message")
        return ActionOutput(content=response)
```

## Exercises

### Exercise 1: Custom LLM
Create a custom LLM that:
- Echoes the prompt back
- Adds a prefix to responses
- Implements the BaseLLM interface

**Solution Template:**
```python
class EchoLLM(BaseLLM):
    async def aask(self, prompt: str, system_msgs=None):
        # Your code here
        pass
```

### Exercise 2: LLM Wrapper
Create an LLM wrapper that:
- Logs all prompts and responses
- Caches responses
- Tracks usage statistics

### Exercise 3: Multi-LLM Action
Create an action that:
- Uses multiple LLMs
- Compares responses
- Returns the best one

**Challenge:** Can you implement a voting system for multiple LLMs?

## Practice Tasks

1. **LLM Tester**: Test different prompts with MockLLM
2. **LLM Analyzer**: Analyze response patterns
3. **LLM Optimizer**: Optimize prompts for better responses

## Next Steps

After completing this lesson:
- Move to Lesson 07 to learn about Actions in detail
- Try implementing custom LLMs
- Experiment with different prompts

## Common Pitfalls

- **Async Required**: LLM methods are async, use await
- **API Keys**: OpenAILLM requires valid API key
- **vLLM Server**: VLLM requires a running vLLM server on localhost
- **Model Files**: LocalLLM requires a valid GGUF model file path
- **System Messages**: Use system messages for role definition

## Additional Resources

- Check `framework/llm.py` for LLM implementations
- See OpenAI API documentation for OpenAILLM usage
- See vLLM documentation for server setup
- See llama.cpp documentation for LocalLLM usage

