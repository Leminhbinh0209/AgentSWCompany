"""Conditional Action for conditional execution"""
from typing import List, Optional, Callable, Any
from framework.action import Action
from framework.schema import Message, ActionOutput


class ConditionalAction(Action):
    """Action that executes conditionally based on messages or context"""
    
    def __init__(self, name: str = "ConditionalAction", llm=None,
                 condition_func: Optional[Callable] = None,
                 if_true_action: Optional[Action] = None,
                 if_false_action: Optional[Action] = None):
        """
        Initialize Conditional Action
        
        Args:
            name: Action name
            llm: Optional LLM
            condition_func: Function to check condition
            if_true_action: Action to execute if condition is true
            if_false_action: Action to execute if condition is false
        """
        super().__init__(name=name, llm=llm)
        self.condition_func = condition_func
        self.if_true_action = if_true_action
        self.if_false_action = if_false_action
    
    async def _check_condition(self, messages: Optional[List[Message]] = None, **kwargs) -> bool:
        """
        Check the condition
        
        Args:
            messages: Optional messages
            **kwargs: Additional parameters
            
        Returns:
            True if condition is met
        """
        if self.condition_func:
            return self.condition_func(messages, **kwargs)
        
        # Default: check if messages exist
        if messages:
            return len(messages) > 0
        
        # Check context
        if self.context:
            return len(self.context) > 0
        
        return False
    
    async def _execute_if_true(self, messages: Optional[List[Message]] = None, **kwargs) -> ActionOutput:
        """
        Execute action if condition is true
        
        Args:
            messages: Optional messages
            **kwargs: Additional parameters
            
        Returns:
            ActionOutput from true action
        """
        if self.if_true_action:
            return await self.if_true_action.run(messages=messages, **kwargs)
        
        return ActionOutput(
            content="Condition is true, but no action specified",
            instruct_content={"condition": True}
        )
    
    async def _execute_if_false(self, messages: Optional[List[Message]] = None, **kwargs) -> ActionOutput:
        """
        Execute action if condition is false
        
        Args:
            messages: Optional messages
            **kwargs: Additional parameters
            
        Returns:
            ActionOutput from false action
        """
        if self.if_false_action:
            return await self.if_false_action.run(messages=messages, **kwargs)
        
        return ActionOutput(
            content="Condition is false, but no action specified",
            instruct_content={"condition": False}
        )
    
    async def run(self, messages: Optional[List[Message]] = None, **kwargs) -> ActionOutput:
        """
        Execute the conditional action
        
        Args:
            messages: Optional messages
            **kwargs: Additional parameters
            
        Returns:
            ActionOutput from executed action
        """
        condition = await self._check_condition(messages, **kwargs)
        
        if condition:
            return await self._execute_if_true(messages, **kwargs)
        else:
            return await self._execute_if_false(messages, **kwargs)


class RetryAction(Action):
    """Action that retries on failure"""
    
    def __init__(self, action: Action, max_retries: int = 3, name: str = None, llm=None):
        """
        Initialize Retry Action
        
        Args:
            action: Action to retry
            max_retries: Maximum number of retries
            name: Optional action name
            llm: Optional LLM
        """
        super().__init__(name=name or f"Retry_{action.name}", llm=llm)
        self.action = action
        self.max_retries = max_retries
    
    async def run(self, messages: Optional[List[Message]] = None, **kwargs) -> ActionOutput:
        """
        Execute action with retries
        
        Args:
            messages: Optional messages
            **kwargs: Additional parameters
            
        Returns:
            ActionOutput from action
        """
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                result = await self.action.run(messages=messages, **kwargs)
                return result
            except Exception as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    # Wait before retry (exponential backoff)
                    import asyncio
                    await asyncio.sleep(2 ** attempt)
                else:
                    # Last attempt failed
                    return ActionOutput(
                        content=f"Action failed after {self.max_retries} attempts: {str(e)}",
                        instruct_content={"error": str(e), "attempts": self.max_retries}
                    )
        
        return ActionOutput(
            content=f"Action failed: {str(last_error)}",
            instruct_content={"error": str(last_error)}
        )

