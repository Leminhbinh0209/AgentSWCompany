"""Action for writing tests"""
from typing import List
from framework.action import Action
from framework.schema import Message, ActionOutput


class WriteTest(Action):
    """Action to write test cases for code"""
    
    def __init__(self, llm=None):
        super().__init__(name="WriteTest", llm=llm)
    
    async def run(self, messages: List[Message] = None, **kwargs) -> ActionOutput:
        """Generate test code"""
        code = ""
        if messages:
            code = messages[-1].content
        
        system_prompt = """You are a QA Engineer. Write comprehensive test cases using unittest framework 
        for the given code. Include edge cases and error conditions."""
        
        prompt = f"""Write comprehensive unit tests for the following code:

```python
{code}
```

Requirements:
1. Use unittest framework
2. Test all functions
3. Include edge cases
4. Test error conditions
5. Add proper docstrings
"""
        
        test_code = await self._ask_llm(prompt, system_prompt)
        
        return ActionOutput(
            content=test_code,
            instruct_content={"type": "test", "code": test_code}
        )


class RunTest(Action):
    """Action to run tests"""
    
    def __init__(self, llm=None):
        super().__init__(name="RunTest", llm=llm)
    
    async def run(self, messages: List[Message] = None, **kwargs) -> ActionOutput:
        """Run test file"""
        test_file = kwargs.get("test_file", "tests/test_main.py")
        
        from framework.tools.terminal import Terminal
        workspace = kwargs.get("workspace", self.context.get("workspace", "."))
        terminal = Terminal(workspace_path=workspace)
        
        result = await terminal.run_tests(test_file)
        
        # Parse test results
        output = f"Test Results:\n"
        output += f"Status: {result.get('status', 'unknown')}\n"
        output += f"Return Code: {result.get('returncode', -1)}\n"
        if result.get('stdout'):
            output += f"\nOutput:\n{result['stdout']}"
        if result.get('stderr'):
            output += f"\nErrors:\n{result['stderr']}"
        
        return ActionOutput(
            content=output,
            instruct_content={"type": "test_results", "results": result}
        )


class ReportBugs(Action):
    """Action to report bugs found during testing"""
    
    def __init__(self, llm=None):
        super().__init__(name="ReportBugs", llm=llm)
    
    async def run(self, messages: List[Message] = None, **kwargs) -> ActionOutput:
        """Generate bug report"""
        test_results = ""
        if messages:
            test_results = messages[-1].content
        
        system_prompt = """You are a QA Engineer. Analyze test results and create a bug report 
        with severity, steps to reproduce, and expected vs actual behavior."""
        
        prompt = f"""Based on the following test results, create a bug report:

{test_results}

Include:
1. Bug description
2. Severity (Critical, High, Medium, Low)
3. Steps to reproduce
4. Expected behavior
5. Actual behavior
6. Suggested fix
"""
        
        bug_report = await self._ask_llm(prompt, system_prompt)
        
        return ActionOutput(
            content=bug_report,
            instruct_content={"type": "bug_report", "content": bug_report}
        )

