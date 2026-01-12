"""Environment for managing roles and message routing"""
from typing import List, Dict, Optional
from pathlib import Path
from framework.role import Role
from framework.schema import Message, MessageQueue
from framework.context import Context


class Environment:
    """Environment for managing roles and message routing"""
    
    def __init__(self, context: Optional[Context] = None):
        """
        Initialize Environment
        
        Args:
            context: Optional context object
        """
        self.roles: Dict[str, Role] = {}
        self.message_history: List[Message] = []
        self.context = context or Context()
        self.msg_buffer = MessageQueue()  # Message buffer
        self._is_running = False
    
    def add_role(self, role: Role):
        """Add a role to the environment"""
        self.roles[role.name] = role
        # Set context if it's a dict (backward compatibility) or Context object
        if isinstance(self.context, dict):
            role.set_context(self.context)
        else:
            # For Context object, set the context's kwargs as dict
            role.set_context(self.context.kwargs.to_dict() if hasattr(self.context.kwargs, 'to_dict') else {})
        # Set environment reference (for TeamLeader)
        if hasattr(role, 'set_environment'):
            role.set_environment(self)
    
    def add_roles(self, roles: List[Role]):
        """Add multiple roles"""
        for role in roles:
            self.add_role(role)
    
    def publish_message(self, message: Message, send_to: Optional[str] = None):
        """
        Publish a message to the environment
        
        Args:
            message: Message to publish
            send_to: Specific role to send to (None = broadcast)
        """
        message.send_to = send_to
        self.message_history.append(message)
        
        if send_to:
            # Send to specific role
            if send_to in self.roles:
                self.roles[send_to].observe(message)
        else:
            # Broadcast to all roles
            for role in self.roles.values():
                role.observe(message)
    
    def get_role(self, name: str) -> Optional[Role]:
        """Get a role by name"""
        return self.roles.get(name)
    
    def get_all_roles(self) -> List[Role]:
        """Get all roles"""
        return list(self.roles.values())
    
    @property
    def history(self) -> List[Message]:
        """Get message history (MetaGPT compatibility)"""
        return self.message_history
    
    async def run(self):
        """
        Run one round of the environment.
        Processes all roles that have messages to handle.
        """
        if self.is_idle:
            return
        
        # Process all roles
        for role in self.roles.values():
            if role.working_memory:
                message = await role.react()
                if message:
                    # Route message automatically
                    self._auto_route_message(message)
    
    @property
    def is_idle(self) -> bool:
        """Check if all roles are idle (no messages to process)"""
        return all(not role.working_memory for role in self.roles.values())
    
    def _auto_route_message(self, message: Message):
        """Automatically route message to appropriate role"""
        # Routing logic based on cause_by
        routing_map = {
            "WritePRD": "Architect",
            "WriteDesign": "Engineer",
            "WriteCode": None,  # Final output
        }
        
        target_role = routing_map.get(message.cause_by)
        if target_role:
            self.publish_message(message, send_to=target_role)
        else:
            # Store final outputs in context
            if message.cause_by == "WriteCode":
                # Try to extract clean code from message content
                try:
                    from framework.utils.code_extractor import extract_code_blocks
                    clean_code = extract_code_blocks(message.content)
                    # Use extracted code if available, otherwise use original
                    code_content = clean_code if clean_code and len(clean_code) > 50 else message.content
                except ImportError:
                    # Fallback if code extractor not available
                    code_content = message.content
                
                if isinstance(self.context, dict):
                    self.context["code"] = code_content
                    self.context["code_raw"] = message.content  # Keep raw for reference
                    self.context["design"] = self._find_latest_message("WriteDesign")
                    self.context["prd"] = self._find_latest_message("WritePRD")
                else:
                    # Context object
                    self.context.kwargs.set("code", code_content)
                    self.context.kwargs.set("code_raw", message.content)  # Keep raw for reference
                    self.context.kwargs.set("design", self._find_latest_message("WriteDesign"))
                    self.context.kwargs.set("prd", self._find_latest_message("WritePRD"))
    
    def _find_latest_message(self, cause_by: str) -> str:
        """Find latest message with given cause_by"""
        for msg in reversed(self.message_history):
            if msg.cause_by == cause_by:
                return msg.content
        return ""
    
    def archive(self, auto_archive: bool = True):
        """
        Archive project after completion
        
        Args:
            auto_archive: Whether to automatically archive
        """
        if not auto_archive:
            return
        
        # Create archive summary
        archive_data = {
            "total_messages": len(self.message_history),
            "roles": [role.name for role in self.roles.values()],
            "final_state": {
                "has_code": "code" in (self.context if isinstance(self.context, dict) else self.context.kwargs.to_dict()),
                "has_design": "design" in (self.context if isinstance(self.context, dict) else self.context.kwargs.to_dict()),
                "has_prd": "prd" in (self.context if isinstance(self.context, dict) else self.context.kwargs.to_dict()),
            }
        }
        
        # Store in context
        if isinstance(self.context, dict):
            self.context["archive"] = archive_data
        else:
            self.context.kwargs.set("archive", archive_data)

