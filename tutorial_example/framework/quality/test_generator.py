"""Test Generator for creating and running tests"""
import re
import ast
from typing import Dict, List, Optional, Any
from pathlib import Path
from framework.tools.terminal import Terminal
from framework.llm import BaseLLM


class TestGenerator:
    """Generator for creating and running tests"""
    
    def __init__(self, workspace_path: str = ".", llm: Optional[BaseLLM] = None):
        """
        Initialize Test Generator
        
        Args:
            workspace_path: Workspace directory
            llm: Optional LLM for generating test code
        """
        self.workspace_path = Path(workspace_path).resolve()
        self.llm = llm
        self.terminal = Terminal(workspace_path=str(self.workspace_path))
    
    async def generate_tests(self, code: str, test_type: str = "unit", 
                           module_name: str = "module") -> str:
        """
        Generate test code for given code
        
        Args:
            code: Source code to test
            test_type: Type of tests (unit, integration, etc.)
            module_name: Name of the module being tested
            
        Returns:
            Generated test code
        """
        if self.llm:
            return await self._generate_with_llm(code, test_type, module_name)
        else:
            return self._generate_basic_tests(code, module_name)
    
    def _generate_basic_tests(self, code: str, module_name: str) -> str:
        """Generate basic test structure without LLM"""
        test_code = f"""import unittest
import sys
from pathlib import Path

# Add source to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

try:
    from {module_name} import *
except ImportError:
    # If import fails, adjust the import path
    pass

class Test{module_name.capitalize()}(unittest.TestCase):
    \"\"\"Tests for {module_name} module\"\"\"
"""
        
        # Try to extract functions from code
        try:
            tree = ast.parse(code)
            functions = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
                    functions.append(node.name)
            
            # Generate basic tests for each function
            for func_name in functions[:5]:  # Limit to 5 functions
                test_code += f"""
    def test_{func_name}(self):
        \"\"\"Test {func_name} function\"\"\"
        # TODO: Add test cases for {func_name}
        # Example:
        # result = {func_name}(arg1, arg2)
        # self.assertIsNotNone(result)
        pass
"""
        except SyntaxError:
            # If code has syntax errors, add a placeholder test
            test_code += """
    def test_placeholder(self):
        \"\"\"Placeholder test\"\"\"
        self.assertTrue(True)
"""
        
        test_code += """
if __name__ == '__main__':
    unittest.main()
"""
        return test_code
    
    async def _generate_with_llm(self, code: str, test_type: str, module_name: str) -> str:
        """Generate tests using LLM"""
        prompt = f"""Generate comprehensive {test_type} tests for the following Python code.

Module name: {module_name}

Code to test:
```python
{code}
```

Requirements:
1. Use unittest framework
2. Include test cases for all functions
3. Test edge cases and error conditions
4. Include proper setup and teardown if needed
5. Add docstrings to test methods

Generate complete, runnable test code:"""

        try:
            response = await self.llm.aask(prompt)
            # Extract code block if present
            code_match = re.search(r'```python\n(.*?)\n```', response, re.DOTALL)
            if code_match:
                return code_match.group(1)
            return response
        except Exception:
            return self._generate_basic_tests(code, module_name)
    
    async def run_tests(self, test_file: str) -> Dict[str, Any]:
        """
        Run test file
        
        Args:
            test_file: Path to test file
            
        Returns:
            Dict with test results
        """
        test_path = Path(test_file)
        if not test_path.is_absolute():
            test_path = self.workspace_path / test_file
        
        if not test_path.exists():
            return {
                "status": "error",
                "message": f"Test file not found: {test_path}",
                "passed": 0,
                "failed": 0,
                "errors": 0
            }
        
        # Try pytest first, then unittest
        result = await self.terminal.run_tests(str(test_path))
        
        # Parse results
        output = result.get("stdout", "")
        errors = result.get("stderr", "")
        
        # Extract test statistics
        passed = len(re.findall(r'PASSED|ok', output))
        failed = len(re.findall(r'FAILED|FAIL', output))
        errors_count = len(re.findall(r'ERROR', output))
        
        return {
            "status": "success" if result["returncode"] == 0 else "failure",
            "returncode": result["returncode"],
            "passed": passed,
            "failed": failed,
            "errors": errors_count,
            "stdout": output,
            "stderr": errors
        }
    
    async def get_coverage(self, code_path: str, test_path: str) -> Dict[str, Any]:
        """
        Get test coverage (basic estimation)
        
        Args:
            code_path: Path to source code
            test_path: Path to test file
            
        Returns:
            Dict with coverage information
        """
        coverage = {
            "status": "success",
            "coverage_estimate": 0,
            "functions_tested": 0,
            "functions_total": 0,
            "details": {}
        }
        
        try:
            # Read source code
            code_file = Path(code_path)
            if not code_file.is_absolute():
                code_file = self.workspace_path / code_path
            
            if code_file.exists():
                source_code = code_file.read_text()
                source_tree = ast.parse(source_code)
                source_functions = []
                for node in ast.walk(source_tree):
                    if isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
                        source_functions.append(node.name)
                
                coverage["functions_total"] = len(source_functions)
                
                # Read test code
                test_file = Path(test_path)
                if not test_file.is_absolute():
                    test_file = self.workspace_path / test_path
                
                if test_file.exists():
                    test_code = test_file.read_text()
                    test_tree = ast.parse(test_code)
                    test_functions = []
                    for node in ast.walk(test_tree):
                        if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                            # Extract function name from test name
                            func_name = node.name.replace('test_', '')
                            test_functions.append(func_name)
                    
                    # Match test functions to source functions
                    tested = []
                    for func in source_functions:
                        # Check if there's a test for this function
                        if any(func in test_func or test_func.endswith(func) for test_func in test_functions):
                            tested.append(func)
                    
                    coverage["functions_tested"] = len(tested)
                    if source_functions:
                        coverage["coverage_estimate"] = len(tested) / len(source_functions) * 100
                    
                    coverage["details"] = {
                        "source_functions": source_functions,
                        "test_functions": test_functions,
                        "tested_functions": tested
                    }
        
        except Exception as e:
            coverage["status"] = "error"
            coverage["error"] = str(e)
        
        return coverage
    
    async def fix_failing_tests(self, code: str, test_results: Dict[str, Any]) -> str:
        """
        Suggest fixes for failing tests
        
        Args:
            code: Source code
            test_results: Test execution results
            
        Returns:
            Suggested fixes
        """
        if not self.llm:
            return "LLM not available for fixing tests"
        
        error_output = test_results.get("stderr", "")
        stdout = test_results.get("stdout", "")
        
        prompt = f"""The following tests are failing. Analyze the errors and suggest fixes for the source code.

Source code:
```python
{code}
```

Test output:
{stdout}

Errors:
{error_output}

Provide specific fixes for the source code to make the tests pass."""

        try:
            response = await self.llm.aask(prompt)
            return response
        except Exception:
            return "Unable to generate fixes"
    
    def extract_functions(self, code: str) -> List[Dict[str, Any]]:
        """
        Extract function information from code
        
        Args:
            code: Source code
            
        Returns:
            List of function information
        """
        functions = []
        
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_info = {
                        "name": node.name,
                        "line": node.lineno,
                        "args": [arg.arg for arg in node.args.args],
                        "docstring": ast.get_docstring(node) or ""
                    }
                    functions.append(func_info)
        except SyntaxError:
            pass
        
        return functions
    
    async def generate_test_cases(self, function_code: str, function_name: str) -> List[Dict[str, str]]:
        """
        Generate test cases for a specific function
        
        Args:
            function_code: Function code
            function_name: Function name
            
        Returns:
            List of test case dictionaries
        """
        test_cases = []
        
        # Basic test case structure
        test_cases.append({
            "name": f"test_{function_name}_basic",
            "code": f"# Basic test for {function_name}\n        result = {function_name}()\n        self.assertIsNotNone(result)"
        })
        
        # If LLM available, generate more comprehensive tests
        if self.llm:
            prompt = f"""Generate 3-5 test cases for this function:

```python
{function_code}
```

For each test case, provide:
1. Test name (test_{function_name}_...)
2. Test code (unittest.TestCase method body)

Format as:
Test 1: test_name
Code:
test code here
"""
            try:
                response = await self.llm.aask(prompt)
                # Parse response (simplified)
                # In production, use more sophisticated parsing
            except Exception:
                pass
        
        return test_cases

