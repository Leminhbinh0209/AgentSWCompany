"""
Lesson 06: Understanding LLMs
==============================

This lesson introduces the LLM interface and implementations,
including MockLLM and OpenAILLM.

Run this lesson:
    python lesson_06.py
"""
import sys
import os
import asyncio

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.llm import MockLLM, OpenAILLM, BaseLLM


async def main():
    print("=" * 60)
    print("Lesson 06: Understanding LLMs")
    print("=" * 60)
    print()
    
    # 1. Using MockLLM
    print("1. Using MockLLM (No API Key Required)")
    print("-" * 60)
    mock_llm = MockLLM()
    
    prompt = "Write a PRD for a calculator app"
    response = await mock_llm.aask(prompt)
    print(f"Prompt: {prompt}")
    print(f"Response preview: {response[:150]}...")
    print()
    
    # 2. MockLLM with system messages
    print("2. MockLLM with System Messages")
    print("-" * 60)
    system_msg = "You are a Product Manager. Write PRDs."
    prompt = "Create a PRD for a todo app"
    response = await mock_llm.aask(prompt, system_msgs=[system_msg])
    print(f"System: {system_msg}")
    print(f"Prompt: {prompt}")
    print(f"Response preview: {response[:150]}...")
    print()
    
    # 3. Different prompt types
    print("3. Different Prompt Types")
    print("-" * 60)
    prompts = [
        ("Write a PRD", "prd"),
        ("Design a system", "design"),
        ("Write code", "code"),
    ]
    
    for prompt, prompt_type in prompts:
        response = await mock_llm.aask(prompt)
        print(f"{prompt_type.upper()}: {response[:80]}...")
    print()
    
    # 4. OpenAILLM (if available)
    print("4. OpenAILLM (Requires API Key)")
    print("-" * 60)
    try:
        # Try to create OpenAILLM (will fail without API key)
        # In real usage, you would do:
        # openai_llm = OpenAILLM(api_key="your-api-key-here")
        # response = await openai_llm.aask("Hello")
        print("OpenAILLM requires:")
        print("  1. Install: pip install openai")
        print("  2. API key from OpenAI")
        print("  3. Usage: OpenAILLM(api_key='your-key')")
        print("  (Skipping actual call - requires API key)")
    except Exception as e:
        print(f"OpenAILLM not available: {e}")
    print()
    
    # 5. LLM interface
    print("5. LLM Interface")
    print("-" * 60)
    print("BaseLLM provides:")
    print("  - aask(prompt, system_msgs): Async ask method")
    print("  - All LLMs implement this interface")
    print("  - Easy to swap implementations")
    print()
    
    # 6. Using LLM in actions
    print("6. Using LLM in Actions")
    print("-" * 60)
    from framework.action import Action
    from framework.schema import ActionOutput
    from typing import List
    
    class LLMAction(Action):
        async def run(self, messages=None, **kwargs):
            prompt = "Generate a response"
            response = await self._ask_llm(prompt, "You are helpful")
            return ActionOutput(content=response)
    
    action = LLMAction(name="LLMAction", llm=mock_llm)
    result = await action.run()
    print(f"Action using LLM: {result.content[:100]}...")
    print()
    
    print("=" * 60)
    print("Lesson 06 Complete!")
    print("=" * 60)
    print()
    print("Key Takeaways:")
    print("- LLMs provide AI capabilities to actions")
    print("- MockLLM is for testing without API keys")
    print("- OpenAILLM connects to OpenAI API")
    print("- All LLMs implement the same interface")


if __name__ == "__main__":
    asyncio.run(main())

