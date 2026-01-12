"""Base Action class"""
from abc import ABC, abstractmethod
from typing import List, Optional
from framework.schema import Message, ActionOutput


class Action(ABC):
    """Base class for all actions"""
    
    def __init__(self, name: str = None, llm=None):
        self.name = name or self.__class__.__name__
        self.llm = llm
        self.context = {}  # Shared context
    
    def set_llm(self, llm):
        """Set the LLM for this action"""
        self.llm = llm
    
    def set_context(self, context: dict):
        """Set shared context"""
        self.context = context
    
    @abstractmethod
    async def run(self, messages: List[Message] = None, **kwargs) -> ActionOutput:
        """
        Execute the action
        
        Args:
            messages: Previous messages for context
            **kwargs: Additional parameters
            
        Returns:
            ActionOutput: The result of the action
        """
        pass
    
    async def _ask_llm(self, prompt: str, system_prompt: str = None) -> str:
        """Helper method to call LLM"""
        if not self.llm:
            raise ValueError("LLM not set for action")
        
        if system_prompt:
            return await self.llm.aask(prompt, system_msgs=[system_prompt])
        return await self.llm.aask(prompt)

