"""Write PRD action"""
from framework.action import Action
from framework.schema import Message, ActionOutput
from typing import List


class WritePRD(Action):
    """Action to write a Product Requirement Document"""
    
    def __init__(self, llm=None):
        super().__init__(name="WritePRD", llm=llm)
    
    async def run(self, messages: List[Message] = None, **kwargs) -> ActionOutput:
        # Extract requirement from messages
        requirement = ""
        if messages:
            requirement = messages[-1].content
        
        system_prompt = """You are a Product Manager. Write a comprehensive PRD 
        (Product Requirement Document) based on the user requirement."""
        
        prompt = f"""Based on the following requirement, write a detailed PRD:

Requirement: {requirement}

Include:
1. Product Overview
2. User Stories
3. Functional Requirements
4. Non-functional Requirements
5. Success Metrics
"""
        
        prd_content = await self._ask_llm(prompt, system_prompt)
        
        return ActionOutput(
            content=prd_content,
            instruct_content={"type": "PRD", "content": prd_content}
        )

