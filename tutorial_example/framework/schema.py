"""Core data models for the framework"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any
from enum import Enum


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass
class Message:
    """Message exchanged between roles"""
    content: str
    role: str  # Role name that sent this message
    cause_by: Optional[str] = None  # Action that caused this message
    sent_from: Optional[str] = None
    send_to: Optional[str] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def __str__(self):
        return f"[{self.role}] {self.content[:50]}..."


@dataclass
class ActionOutput:
    """Output from an action execution"""
    content: str
    instruct_content: Optional[Any] = None  # Structured output
    
    def to_message(self, role: str, cause_by: str) -> Message:
        """Convert action output to a message"""
        return Message(
            content=self.content,
            role=role,
            cause_by=cause_by
        )

