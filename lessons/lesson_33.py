"""
Lesson 33: Configuration System
=================================

This lesson demonstrates the Configuration system for centralized
configuration management.

Run this lesson:
    python lesson_33.py
"""
import sys
import os
import asyncio
from pathlib import Path

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.config import Config, LLMConfig


async def main():
    print("=" * 80)
    print("Lesson 33: Configuration System")
    print("=" * 80)
    print()
    
    print("The Configuration system provides centralized configuration management.")
    print("It supports YAML files and programmatic configuration.")
    print()
    
    # 1. Default Configuration
    print("1. Default Configuration")
    print("-" * 80)
    config = Config.default()
    
    print(f"✓ Default config created")
    print(f"  - LLM API type: {config.llm.api_type}")
    print(f"  - LLM model: {config.llm.model}")
    print(f"  - LLM base URL: {config.llm.base_url}")
    print(f"  - Workspace: {config.workspace}")
    print()
    
    # 2. Custom LLM Configuration
    print("2. Custom LLM Configuration")
    print("-" * 80)
    custom_llm_config = LLMConfig(
        api_type="vllm",
        base_url="http://localhost:8000/v1",
        model="codellama/CodeLlama-7b-Instruct-hf",
        local_model_path="EMPTY"
    )
    
    config.llm = custom_llm_config
    print(f"✓ Custom LLM config set")
    print(f"  - Model: {config.llm.model}")
    print(f"  - Base URL: {config.llm.base_url}")
    print()
    
    # 3. Configuration Dictionary
    print("3. Configuration Dictionary")
    print("-" * 80)
    config_dict = config.to_dict()
    print(f"✓ Config converted to dictionary:")
    print(f"  - Keys: {list(config_dict.keys())}")
    print(f"  - LLM keys: {list(config_dict['llm'].keys())}")
    print()
    
    # 4. YAML Configuration (Example)
    print("4. YAML Configuration Support")
    print("-" * 80)
    print("Config supports loading from YAML files:")
    print("""
# Example config2.yaml
llm:
  api_type: "vllm"
  base_url: "http://localhost:8000/v1"
  model: "codellama/CodeLlama-7b-Instruct-hf"
  local_model_path: "EMPTY"
workspace: "workspace"
""")
    print("Load with: Config.from_yaml('~/.metagpt/config2.yaml')")
    print()
    
    # 5. Using Config with Context
    print("5. Using Config with Context")
    print("-" * 80)
    from framework.context import Context
    
    ctx = Context(config=config)
    print(f"✓ Context created with config")
    print(f"  - Config model: {ctx.config.llm.model}")
    print(f"  - Config workspace: {ctx.config.workspace}")
    print()
    
    # 6. Per-Role Configuration
    print("6. Per-Role Configuration (Advanced)")
    print("-" * 80)
    print("You can create different configs for different roles:")
    print("""
pm_config = LLMConfig(model="gpt-4", ...)
architect_config = LLMConfig(model="gpt-3.5-turbo", ...)
engineer_config = LLMConfig(model="codellama", ...)
""")
    print()
    
    # 7. Configuration Benefits
    print("7. Configuration Benefits")
    print("-" * 80)
    print("✓ Centralized configuration management")
    print("✓ YAML file support for easy editing")
    print("✓ Per-role configuration support")
    print("✓ Default values for quick setup")
    print("✓ Type-safe configuration objects")
    print()
    
    print("=" * 80)
    print("Lesson 33 Complete!")
    print("=" * 80)
    print()
    print("Key Takeaways:")
    print("- Config provides centralized configuration")
    print("- Supports YAML files for easy management")
    print("- LLMConfig manages LLM settings")
    print("- Can be used with Context")
    print("- Enables per-role configuration")


if __name__ == "__main__":
    asyncio.run(main())

