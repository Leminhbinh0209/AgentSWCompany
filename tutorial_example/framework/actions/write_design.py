"""Write Design action"""
from framework.action import Action
from framework.schema import Message, ActionOutput
from typing import List


class WriteDesign(Action):
    """Action to write system design based on PRD"""
    
    def __init__(self, llm=None):
        super().__init__(name="WriteDesign", llm=llm)
    
    async def run(self, messages: List[Message] = None, **kwargs) -> ActionOutput:
        # Extract PRD from messages
        prd = ""
        if messages:
            prd = messages[-1].content
        
        system_prompt = """You are a System Architect. Create a detailed system design 
        based on the PRD."""
        
        prompt = f"""Based on the following PRD, create a system design:

PRD: {prd}

Include:
1. System Architecture
2. Component Design
3. API Design
4. Database Schema (if needed)
5. Technology Stack
"""
        
        design_content = await self._ask_llm(prompt, system_prompt)
        
        return ActionOutput(
            content=design_content,
            instruct_content={"type": "Design", "content": design_content}
        )

