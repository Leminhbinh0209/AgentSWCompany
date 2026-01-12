# Lesson 33: Configuration System

## Learning Targets

By the end of this lesson, you will be able to:
- Use Config for centralized configuration
- Create LLMConfig for LLM settings
- Load configuration from YAML files
- Use config with Context
- Configure per-role settings

## Overview

The Configuration system provides centralized management of all framework settings. It supports YAML files and programmatic configuration.

## Key Concepts

### Config Class

The `Config` class contains:
- **llm**: LLMConfig for LLM settings
- **workspace**: Default workspace directory
- **repair_llm_output**: Whether to repair LLM output

### LLMConfig

LLM-specific configuration:
- **api_type**: API type (vllm, openai, etc.)
- **base_url**: Base URL for API
- **api_key**: API key
- **model**: Model name
- **local_model_path**: Path to local model

## Guidance

### 1. Default Configuration

```python
from framework.config import Config

config = Config.default()
```

### 2. Custom LLM Configuration

```python
from framework.config import LLMConfig

llm_config = LLMConfig(
    api_type="vllm",
    base_url="http://localhost:8000/v1",
    model="codellama/CodeLlama-7b-Instruct-hf"
)
config.llm = llm_config
```

### 3. Loading from YAML

```python
config = Config.from_yaml("~/.metagpt/config2.yaml")
```

### 4. Using with Context

```python
from framework.context import Context

ctx = Context(config=config)
```

### 5. Configuration Dictionary

```python
config_dict = config.to_dict()
# Convert to dictionary for serialization
```

## Exercises

### Exercise 1: Config Manager
Create a system that:
- Loads config from YAML
- Validates configuration
- Provides default fallbacks

### Exercise 2: Multi-Config System
Create a system that:
- Manages multiple configs
- Switches between configs
- Validates config changes

## Practice Tasks

1. **Config Loader**: Load and validate configs
2. **Config Manager**: Manage multiple configurations
3. **Config Validator**: Validate configuration settings

## Next Steps

- Move to Lesson 34 to learn about generate_repo()
- Try creating custom configurations
- Experiment with YAML configs

## Additional Resources

- Check `framework/config.py` for full implementation
- Review YAML configuration examples

