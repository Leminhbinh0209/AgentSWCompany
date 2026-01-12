"""
Lesson 23: Technical Writer
===========================

This lesson demonstrates the TechnicalWriter role for documentation.

Run this lesson:
    python lesson_23.py
"""
import sys
import os
import asyncio

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.roles.technical_writer import TechnicalWriter
from framework.llm import get_llm


async def main():
    print("=" * 60)
    print("Lesson 23: Technical Writer")
    print("=" * 60)
    print()
    
    llm = get_llm(
        local_model_path="EMPTY", #"./HF_MODELS/Meta-Llama-3-8B-Instruct-GGUF/Meta-Llama-3-8B-Instruct.Q3_K_M.gguf",
        vllm_base_url="http://localhost:8000/v1",
        vllm_model="codellama/CodeLlama-7b-Instruct-hf"
    )
    writer = TechnicalWriter(llm=llm)
    
    print("1. Technical Writer Role")
    print("-" * 60)
    print(f"Name: {writer.name}")
    print(f"Profile: {writer.profile}")
    print(f"Goal: {writer.goal}")
    print(f"Actions: {[a.name for a in writer.actions]}")
    print()
    
    doc = await writer.write_documentation("A calculator application", doc_type="project")
    print(f"Generated documentation ({len(doc)} chars)")
    print()
    
    print("=" * 60)
    print("Lesson 23 Complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

