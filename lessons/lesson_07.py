"""
Lesson 07: Core Actions - WritePRD, WriteDesign, WriteCode
===========================================================

This lesson demonstrates the core actions: WritePRD, WriteDesign, and WriteCode.

Run this lesson:
    python lesson_07.py
"""
import sys
import os
import asyncio

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.actions.write_prd import WritePRD
from framework.actions.write_design import WriteDesign
from framework.actions.write_code import WriteCode
from framework.schema import Message
from framework.llm import MockLLM


async def main():
    print("=" * 60)
    print("Lesson 07: Core Actions")
    print("=" * 60)
    print()
    
    llm = MockLLM()
    
    # 1. WritePRD Action
    print("1. WritePRD Action")
    print("-" * 60)
    write_prd = WritePRD(llm=llm)
    requirement = "Create a simple calculator application"
    messages = [Message(content=requirement, role="User", cause_by="UserRequirement")]
    
    prd_result = await write_prd.run(messages=messages)
    print(f"Requirement: {requirement}")
    print(f"PRD Preview: {prd_result.content[:200]}...")
    print()
    
    # 2. WriteDesign Action
    print("2. WriteDesign Action")
    print("-" * 60)
    write_design = WriteDesign(llm=llm)
    prd_message = Message(content=prd_result.content, role="ProductManager", cause_by="WritePRD")
    
    design_result = await write_design.run(messages=[prd_message])
    print(f"Design Preview: {design_result.content[:200]}...")
    print()
    
    # 3. WriteCode Action
    print("3. WriteCode Action")
    print("-" * 60)
    write_code = WriteCode(llm=llm)
    design_message = Message(content=design_result.content, role="Architect", cause_by="WriteDesign")
    
    code_result = await write_code.run(messages=[design_message])
    print(f"Code Preview: {code_result.content[:200]}...")
    print()
    
    # 4. Complete Workflow
    print("4. Complete Workflow")
    print("-" * 60)
    print("Workflow:")
    print("  User Requirement → WritePRD → PRD")
    print("  PRD → WriteDesign → Design")
    print("  Design → WriteCode → Code")
    print()
    
    # 5. Action Output Structure
    print("5. Action Output Structure")
    print("-" * 60)
    print(f"PRD Output Type: {prd_result.instruct_content.get('type')}")
    print(f"Design Output Type: {design_result.instruct_content.get('type')}")
    print(f"Code Output Type: {code_result.instruct_content.get('type')}")
    print()
    
    # 6. Converting to Messages
    print("6. Converting ActionOutput to Messages")
    print("-" * 60)
    prd_message = prd_result.to_message(role="ProductManager", cause_by="WritePRD")
    design_message = design_result.to_message(role="Architect", cause_by="WriteDesign")
    code_message = code_result.to_message(role="Engineer", cause_by="WriteCode")
    
    print(f"PRD Message: [{prd_message.role}] {prd_message.content[:50]}...")
    print(f"Design Message: [{design_message.role}] {design_message.content[:50]}...")
    print(f"Code Message: [{code_message.role}] {code_message.content[:50]}...")
    print()
    
    print("=" * 60)
    print("Lesson 07 Complete!")
    print("=" * 60)
    print()
    print("Key Takeaways:")
    print("- WritePRD creates Product Requirement Documents")
    print("- WriteDesign creates system designs from PRDs")
    print("- WriteCode generates code from designs")
    print("- Actions form a workflow chain")


if __name__ == "__main__":
    asyncio.run(main())

