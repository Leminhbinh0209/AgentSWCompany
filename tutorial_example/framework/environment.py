"""Environment for managing roles and message routing"""
from typing import List, Dict, Optional
from framework.role import Role
from framework.schema import Message


class Environment:
    """Environment for managing roles and message routing"""
    
    def __init__(self):
        self.roles: Dict[str, Role] = {}
        self.message_history: List[Message] = []
        self.context: dict = {}  # Shared context
    
    def add_role(self, role: Role):
        """Add a role to the environment"""
        self.roles[role.name] = role
        role.set_context(self.context)
    
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

