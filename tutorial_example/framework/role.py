"""Role/Agent implementation"""
from typing import List, Optional
from framework.action import Action
from framework.actions.write_prd import WritePRD
from framework.actions.write_design import WriteDesign
from framework.actions.write_code import WriteCode
from framework.schema import Message, ActionOutput
from collections import deque


class Role:
    """Base role/agent class"""
    
    def __init__(
        self,
        name: str,
        profile: str,
        goal: str,
        actions: List[Action] = None,
        llm=None
    ):
        self.name = name
        self.profile = profile
        self.goal = goal
        self.actions = actions or []
        self.llm = llm
        
        # Memory and state
        self.memory: deque = deque(maxlen=100)  # Recent messages
        self.working_memory: List[Message] = []  # Current task context
        
        # Initialize actions with LLM
        for action in self.actions:
            if self.llm:
                action.set_llm(self.llm)
    
    def set_llm(self, llm):
        """Set LLM for role and its actions"""
        self.llm = llm
        for action in self.actions:
            action.set_llm(llm)
    
    def set_context(self, context: dict):
        """Set shared context for role and actions"""
        self._context = context
        for action in self.actions:
            action.set_context(context)
    
    def set_environment(self, environment):
        """Set environment reference (for TeamLeader coordination)"""
        self._environment = environment
    
    def add_action(self, action: Action):
        """Add an action to this role"""
        if self.llm:
            action.set_llm(self.llm)
        self.actions.append(action)
    
    def observe(self, message: Message):
        """Observe and store a message"""
        self.memory.append(message)
        # Only add to working memory if it's relevant to this role
        if self._is_relevant(message):
            self.working_memory.append(message)
    
    def _is_relevant(self, message: Message) -> bool:
        """Check if message is relevant to this role"""
        # If message is specifically sent to this role, it's relevant
        if message.send_to == self.name:
            return True
        
        # If message is broadcast (send_to is None), check if we should process it
        if message.send_to is None:
            # ProductManager processes user requirements
            if self.name == "ProductManager" and message.cause_by == "UserRequirement":
                return True
            # Architect processes PRDs
            if self.name == "Architect" and message.cause_by == "WritePRD":
                return True
            # Engineer processes designs
            if self.name == "Engineer" and message.cause_by == "WriteDesign":
                return True
        
        return False
    
    def think(self) -> Optional[Action]:
        """
        Decide which action to take next
        
        Returns:
            Action to execute, or None if no action needed
        """
        if not self.actions:
            return None
        
        if not self.working_memory:
            return None
        
        # Get the most recent relevant message
        # Filter to only messages that are actually for this role
        relevant_messages = [msg for msg in self.working_memory if self._is_relevant(msg)]
        if not relevant_messages:
            return None
        
        last_msg = relevant_messages[-1]
        msg_content = last_msg.content.lower()
        msg_cause = last_msg.cause_by or ""
        
        # Route based on message cause_by (more reliable than content)
        if msg_cause == "UserRequirement" or "requirement" in msg_content or "idea" in msg_content:
            # Look for WritePRD action
            for action in self.actions:
                if isinstance(action, WritePRD):
                    return action
        
        if msg_cause == "WritePRD" or "prd" in msg_content or "product requirement" in msg_content:
            # Look for WriteDesign action
            for action in self.actions:
                if isinstance(action, WriteDesign):
                    return action
        
        if msg_cause == "WriteDesign" or "design" in msg_content or "architecture" in msg_content:
            # Look for WriteCode action
            for action in self.actions:
                if isinstance(action, WriteCode):
                    return action
        
        # Default: execute first available action
        return self.actions[0] if self.actions else None
    
    async def act(self, action: Optional[Action] = None) -> Optional[Message]:
        """
        Execute an action
        
        Args:
            action: Action to execute (if None, will think first)
            
        Returns:
            Message with action result, or None
        """
        if action is None:
            action = self.think()
        
        if action is None:
            return None
        
        # Prepare context from memory - only use relevant messages
        relevant_messages = [msg for msg in self.working_memory if self._is_relevant(msg)]
        if not relevant_messages:
            return None
        
        # Use the most recent relevant message
        context_messages = [relevant_messages[-1]]
        
        # Execute action
        try:
            output = await action.run(messages=context_messages)
            
            # Convert to message
            message = output.to_message(
                role=self.name,
                cause_by=action.name
            )
            
            # Store in memory
            self.memory.append(message)
            
            # Clear working memory after action
            self.working_memory.clear()
            
            return message
            
        except Exception as e:
            error_msg = Message(
                content=f"Error in {action.name}: {str(e)}",
                role=self.name,
                cause_by=action.name
            )
            return error_msg
    
    async def react(self) -> Optional[Message]:
        """
        React to observed messages: observe -> think -> act
        
        Returns:
            Message from action, or None
        """
        # If we have messages to process, act on them
        if self.working_memory:
            return await self.act()
        return None

