"""Technical Writer role"""
from framework.role import Role
from framework.actions.write_doc import WriteDoc, WriteAPI, WriteTutorial


class TechnicalWriter(Role):
    """Technical Writer role for documentation"""
    
    def __init__(self, llm=None):
        super().__init__(
            name="TechnicalWriter",
            profile="Technical Writer",
            goal="Create comprehensive, clear, and well-structured documentation",
            actions=[WriteDoc(llm=llm), WriteAPI(llm=llm), WriteTutorial(llm=llm)],
            llm=llm
        )
    
    async def write_documentation(self, content: str, doc_type: str = "general") -> str:
        """
        Write general documentation
        
        Args:
            content: Content to document
            doc_type: Type of documentation
            
        Returns:
            Documentation content
        """
        from framework.schema import Message
        write_doc_action = next((a for a in self.actions if isinstance(a, WriteDoc)), None)
        if write_doc_action:
            messages = [Message(content=content, role="System", cause_by="DocumentationRequest")]
            result = await write_doc_action.run(messages=messages, doc_type=doc_type)
            return result.content
        return ""
    
    async def write_api_docs(self, code: str) -> str:
        """
        Write API documentation
        
        Args:
            code: Code to document
            
        Returns:
            API documentation
        """
        from framework.schema import Message
        write_api_action = next((a for a in self.actions if isinstance(a, WriteAPI)), None)
        if write_api_action:
            messages = [Message(content=code, role="Engineer", cause_by="WriteCode")]
            result = await write_api_action.run(messages=messages)
            return result.content
        return ""
    
    async def write_tutorial(self, topic: str) -> str:
        """
        Write tutorial
        
        Args:
            topic: Tutorial topic
            
        Returns:
            Tutorial content
        """
        from framework.schema import Message
        write_tutorial_action = next((a for a in self.actions if isinstance(a, WriteTutorial)), None)
        if write_tutorial_action:
            messages = [Message(content=topic, role="User", cause_by="TutorialRequest")]
            result = await write_tutorial_action.run(messages=messages)
            return result.content
        return ""

