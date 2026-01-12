"""Write Code action"""
from framework.action import Action
from framework.schema import Message, ActionOutput
from typing import List


class WriteCode(Action):
    """Action to write code based on design"""
    
    def __init__(self, llm=None):
        super().__init__(name="WriteCode", llm=llm)
    
    async def run(self, messages: List[Message] = None, **kwargs) -> ActionOutput:
        # Extract design/requirements from messages
        design = ""
        if messages:
            design = messages[-1].content
        
        system_prompt = """You are a Senior Software Engineer. Write clean, 
        well-documented code based on the design specification."""
        
        prompt = f"""Based on the following design, write the implementation code:

Design: {design}

Requirements:
1. Write complete, runnable code
2. Include proper error handling
3. Add comments and docstrings
4. Follow best practices
"""
        
        code = await self._ask_llm(prompt, system_prompt)
        
        return ActionOutput(
            content=code,
            instruct_content={"type": "code", "content": code}
        )

