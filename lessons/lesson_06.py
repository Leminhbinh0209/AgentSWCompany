"""
Lesson 06: Understanding LLMs
==============================

This lesson introduces the LLM interface and implementations,
including MockLLM, OpenAILLM, VLLM, and LocalLLM.

Run this lesson:
    python lesson_06.py
"""
import sys
import os
import asyncio

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.llm import MockLLM, OpenAILLM, VLLM, LocalLLM, BaseLLM, get_llm


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
    
    # 5. VLLM (vLLM Server on localhost)
    print("5. VLLM (Requires vLLM Server Running)")
    print("-" * 60)
    try:
        # Try to connect to vLLM server (will fail if server not running)
        # In real usage, you would do:
        # vllm = VLLM(base_url="http://localhost:8000/v1", model="your-model")
        # response = await vllm.aask("Hello")
        print("VLLM requires:")
        print("  1. Install: pip install aiohttp")
        print("  2. vLLM server running on localhost:8000")
        print("  3. Usage: VLLM(base_url='http://localhost:8000/v1', model='model-name')")
        print("  (Skipping actual call - requires running server)")
        # Try to create instance to check if dependencies are available
        vllm = VLLM(base_url="http://localhost:8000/v1", model="test-model")
        print("  ✓ VLLM class is available (but server may not be running)")
    except ImportError as e:
        print(f"  VLLM dependencies not available: {e}")
    except Exception as e:
        print(f"  VLLM available but server not running (expected): {e}")
    print()
    
    # 6. LocalLLM (llama.cpp)
    print("6. LocalLLM (Requires GGUF Model File)")
    print("-" * 60)
    try:
        # Try to create LocalLLM (will fail without model file)
        # In real usage, you would do:
        # local_llm = LocalLLM(model_path="/path/to/model.gguf")
        # response = await local_llm.aask("Hello")
        print("LocalLLM requires:")
        print("  1. Install: pip install llama-cpp-python")
        print("  2. GGUF model file")
        print("  3. Usage: LocalLLM(model_path='/path/to/model.gguf')")
        print("  (Skipping actual call - requires model file)")
        # Try to import to check if dependencies are available
        try:
            import llama_cpp
            print("  ✓ llama-cpp-python is installed")
        except ImportError:
            print("  ✗ llama-cpp-python not installed")
    except Exception as e:
        print(f"  LocalLLM not available: {e}")
    print()
    
    # 7. LLM interface
    print("7. LLM Interface")
    print("-" * 60)
    print("BaseLLM provides:")
    print("  - aask(prompt, system_msgs): Async ask method")
    print("  - All LLMs implement this interface")
    print("  - Easy to swap implementations")
    print("  - Four implementations available:")
    print("    1. MockLLM - for testing")
    print("    2. OpenAILLM - for OpenAI API")
    print("    3. VLLM - for vLLM server")
    print("    4. LocalLLM - for llama.cpp")
    print()
    
    # 8. Using get_llm() (Recommended)
    print("8. Using get_llm() (Recommended Approach)")
    print("-" * 60)
    print("get_llm() automatically selects the best available LLM:")
    print("  1. LocalLLM (if model file exists)")
    print("  2. VLLM (if server is running)")
    print("  3. MockLLM (fallback)")
    print()
    try:
        recommended_llm = get_llm(
        local_model_path="EMPTY", #"./HF_MODELS/Meta-Llama-3-8B-Instruct-GGUF/Meta-Llama-3-8B-Instruct.Q3_K_M.gguf",
        vllm_base_url="http://localhost:8000/v1",
        vllm_model="codellama/CodeLlama-7b-Instruct-hf"
    )
        llm_type = type(recommended_llm).__name__
        print(f"✓ Selected LLM: {llm_type}")
        test_response = await recommended_llm.aask("Hello")
        print(f"  Test response: {test_response[:80]}...")
    except Exception as e:
        print(f"  Error: {e}")
    print()
    
    # 9. Using LLM in actions
    print("9. Using LLM in Actions")
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
    print("- Use get_llm() for automatic LLM selection (recommended)")
    print("  Priority: LocalLLM → VLLM → MockLLM")
    print("- MockLLM is for testing without API keys")
    print("- OpenAILLM connects to OpenAI API")
    print("- VLLM connects to vLLM server on localhost")
    print("- LocalLLM uses llama.cpp for local GGUF models")
    print("- All LLMs implement the same interface")
    print("- Easy to swap between different LLM implementations")


if __name__ == "__main__":
    asyncio.run(main())

