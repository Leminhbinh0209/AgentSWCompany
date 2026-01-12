"""Schema definitions for messages and data structures"""
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
import asyncio


@dataclass
class Message:
    """Message between roles"""
    content: str
    role: str
    cause_by: Optional[str] = None
    send_to: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)


class MessageQueue:
    """Asynchronous message buffer"""
    
    def __init__(self):
        self.queue = asyncio.Queue()
        self.history: list[Message] = []
    
    async def put(self, message: Message):
        """Add message to queue"""
        await self.queue.put(message)
        self.history.append(message)
    
    async def get(self) -> Optional[Message]:
        """Get message from queue (non-blocking)"""
        try:
            return self.queue.get_nowait()
        except asyncio.QueueEmpty:
            return None
    
    def empty(self) -> bool:
        """Check if queue is empty"""
        return self.queue.empty()
    
    def size(self) -> int:
        """Get queue size"""
        return self.queue.qsize()


@dataclass
class ActionOutput:
    """Output from an action"""
    content: str
    instruct_content: Optional[Dict[str, Any]] = None
    
    def to_message(self, role: str, cause_by: Optional[str] = None) -> Message:
        """Convert to Message"""
        return Message(
            content=self.content,
            role=role,
            cause_by=cause_by or "Action"
        )
