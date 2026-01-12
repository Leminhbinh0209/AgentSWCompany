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
        """
        Helper method to call LLM with cost tracking
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            
        Returns:
            LLM response
        """
        if not self.llm:
            raise ValueError("LLM not set for action")
        
        # Track cost if context has cost_manager
        cost_manager = None
        role_name = ""
        if isinstance(self.context, dict):
            # Try to get cost_manager from context
            # Context might be a dict or have a reference to Context object
            pass
        else:
            # Context might be a Context object
            if hasattr(self.context, 'cost_manager'):
                cost_manager = self.context.cost_manager
                role_name = getattr(self, '_role_name', '')
        
        # Call LLM
        if system_prompt:
            response = await self.llm.aask(prompt, system_msgs=[system_prompt])
        else:
            response = await self.llm.aask(prompt)
        
        # Track cost (estimate: ~0.001 per request for mock, adjust for real APIs)
        if cost_manager:
            estimated_cost = 0.001  # Placeholder - in real implementation, get from LLM response
            cost_manager.add_cost(
                estimated_cost,
                role=role_name,
                action=self.name,
                description=f"LLM call for {self.name}"
            )
        
        return response

