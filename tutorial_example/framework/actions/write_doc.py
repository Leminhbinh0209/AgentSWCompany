"""Actions for writing documentation"""
from typing import List
from framework.action import Action
from framework.schema import Message, ActionOutput


class WriteDoc(Action):
    """Action to write general documentation"""
    
    def __init__(self, llm=None):
        super().__init__(name="WriteDoc", llm=llm)
    
    async def run(self, messages: List[Message] = None, **kwargs) -> ActionOutput:
        """Generate documentation"""
        content = ""
        doc_type = kwargs.get("doc_type", "general")
        
        if messages:
            content = messages[-1].content
        
        system_prompt = f"""You are a Technical Writer. Write comprehensive {doc_type} documentation 
        that is clear, well-structured, and easy to understand."""
        
        prompt = f"""Write {doc_type} documentation for:

{content}

Make it clear, well-structured, and comprehensive.
"""
        
        doc_content = await self._ask_llm(prompt, system_prompt)
        
        return ActionOutput(
            content=doc_content,
            instruct_content={"type": "documentation", "doc_type": doc_type}
        )


class WriteAPI(Action):
    """Action to write API documentation"""
    
    def __init__(self, llm=None):
        super().__init__(name="WriteAPI", llm=llm)
    
    async def run(self, messages: List[Message] = None, **kwargs) -> ActionOutput:
        """Generate API documentation"""
        code = ""
        if messages:
            code = messages[-1].content
        
        system_prompt = """You are a Technical Writer specializing in API documentation. 
        Write clear API documentation with endpoints, parameters, responses, and examples."""
        
        prompt = f"""Write API documentation for the following code:

```python
{code}
```

Include:
1. API Overview
2. Endpoints/Functions
3. Parameters
4. Return values
5. Examples
6. Error codes
"""
        
        api_doc = await self._ask_llm(prompt, system_prompt)
        
        return ActionOutput(
            content=api_doc,
            instruct_content={"type": "api_documentation"}
        )


class WriteTutorial(Action):
    """Action to write tutorials"""
    
    def __init__(self, llm=None):
        super().__init__(name="WriteTutorial", llm=llm)
    
    async def run(self, messages: List[Message] = None, **kwargs) -> ActionOutput:
        """Generate tutorial"""
        topic = ""
        if messages:
            topic = messages[-1].content
        
        system_prompt = """You are a Technical Writer. Write step-by-step tutorials that are 
        beginner-friendly, well-structured, and include examples."""
        
        prompt = f"""Write a comprehensive tutorial on:

{topic}

Include:
1. Introduction
2. Prerequisites
3. Step-by-step instructions
4. Code examples
5. Common issues and solutions
6. Next steps
"""
        
        tutorial = await self._ask_llm(prompt, system_prompt)
        
        return ActionOutput(
            content=tutorial,
            instruct_content={"type": "tutorial"}
        )

