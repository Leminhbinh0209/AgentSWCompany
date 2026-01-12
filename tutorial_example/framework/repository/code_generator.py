"""Code Generator for creating project files from designs"""
from typing import Dict, List, Optional, Any
from framework.repository.project_repo import ProjectRepo
from framework.tools.editor import Editor
from framework.tools.terminal import Terminal


class CodeGenerator:
    """Generator for creating code files from design specifications"""
    
    def __init__(self, repo: ProjectRepo, llm=None):
        """
        Initialize Code Generator
        
        Args:
            repo: Project repository
            llm: LLM for code generation (optional)
        """
        self.repo = repo
        self.llm = llm
        self.editor = Editor(workspace_path=str(repo.workdir))
        self.terminal = Terminal(workspace_path=str(repo.workdir))
    
    async def generate_project(self, design: str, project_name: str = "project") -> Dict[str, any]:
        """
        Generate a complete project from design
        
        Args:
            design: Design specification
            project_name: Name of the project
            
        Returns:
            Dict with generation results
        """
        results = {
            "status": "success",
            "files_created": [],
            "errors": []
        }
        
        # Create README
        readme = f"# {project_name}\n\n{design}\n"
        result = self.repo.create_readme(readme)
        if result["status"] == "success":
            results["files_created"].append("README.md")
        
        # Create basic structure
        self.repo.initialize_python_package(project_name)
        self.repo.create_test_structure()
        
        return results
    
    async def generate_file(self, filepath: str, code: str, repo: str = "srcs") -> Dict[str, any]:
        """
        Generate a single code file
        
        Args:
            filepath: Path to the file
            code: Code content
            repo: Repository to use (srcs, tests, etc.)
            
        Returns:
            Dict with generation result
        """
        result = self.repo.create_file(filepath, code, repo=repo)
        
        # Check syntax if it's a Python file
        if filepath.endswith('.py'):
            syntax_check = await self.terminal.check_syntax(
                str(self.repo.workdir / repo / filepath)
            )
            result["syntax_valid"] = syntax_check.get("valid", False)
            if not syntax_check.get("valid", False):
                result["syntax_error"] = syntax_check.get("message", "")
        
        return result
    
    async def generate_module(self, module_name: str, functions: List[str], 
                             docstring: str = "") -> Dict[str, any]:
        """
        Generate a Python module with functions
        
        Args:
            module_name: Name of the module
            functions: List of function definitions
            docstring: Module docstring
            
        Returns:
            Dict with generation results
        """
        code = f'"""{docstring or f"Module: {module_name}"}"""\n\n'
        code += "\n\n".join(functions)
        code += "\n"
        
        filepath = f"{module_name}.py"
        return await self.generate_file(filepath, code, repo="srcs")
    
    async def create_package_structure(self, structure: Dict[str, Any]) -> Dict[str, any]:
        """
        Create a package structure from a dictionary
        
        Args:
            structure: Dict defining the structure
                {
                    "package_name": "mypackage",
                    "modules": [
                        {"name": "module1", "functions": [...]},
                        ...
                    ],
                    "subpackages": {...}
                }
        
        Returns:
            Dict with creation results
        """
        results = {
            "status": "success",
            "files_created": [],
            "errors": []
        }
        
        package_name = structure.get("package_name", "package")
        
        # Create package __init__.py
        init_content = f'"""Package: {package_name}"""\n'
        result = self.repo.srcs.create_file(f"{package_name}/__init__.py", init_content)
        if result["status"] == "success":
            results["files_created"].append(f"{package_name}/__init__.py")
        
        # Create modules
        for module in structure.get("modules", []):
            module_name = module.get("name", "module")
            functions = module.get("functions", [])
            docstring = module.get("docstring", "")
            
            code = f'"""{docstring}"""\n\n'
            code += "\n\n".join(functions)
            code += "\n"
            
            filepath = f"{package_name}/{module_name}.py"
            result = self.repo.srcs.create_file(filepath, code)
            if result["status"] == "success":
                results["files_created"].append(filepath)
            else:
                results["errors"].append(f"Failed to create {filepath}: {result.get('message', '')}")
        
        return results
    
    async def generate_from_template(self, template: str, context: Dict[str, str]) -> str:
        """
        Generate code from a template
        
        Args:
            template: Template string with placeholders
            context: Context dict for template substitution
            
        Returns:
            Generated code
        """
        code = template
        for key, value in context.items():
            code = code.replace(f"{{{key}}}", str(value))
        return code
    
    async def generate_tests(self, module_name: str, test_cases: List[Dict[str, str]]) -> Dict[str, any]:
        """
        Generate test file for a module
        
        Args:
            module_name: Name of the module to test
            test_cases: List of test case dicts
                [{"name": "test_function", "code": "..."}, ...]
        
        Returns:
            Dict with generation result
        """
        test_code = f"""import unittest
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from {module_name} import *

class Test{module_name.capitalize()}(unittest.TestCase):
"""
        
        for test_case in test_cases:
            test_name = test_case.get("name", "test_function")
            test_body = test_case.get("code", "pass")
            test_code += f"""
    def {test_name}(self):
{self._indent(test_body, 8)}
"""
        
        test_code += """
if __name__ == '__main__':
    unittest.main()
"""
        
        filepath = f"test_{module_name}.py"
        return await self.generate_file(filepath, test_code, repo="tests")
    
    def _indent(self, text: str, spaces: int) -> str:
        """Indent text by specified number of spaces"""
        indent = " " * spaces
        return "\n".join(indent + line for line in text.split("\n"))
    
    async def generate_documentation(self, module_name: str, description: str) -> Dict[str, any]:
        """
        Generate documentation for a module
        
        Args:
            module_name: Name of the module
            description: Module description
            
        Returns:
            Dict with generation result
        """
        doc_content = f"""# {module_name}

{description}

## Functions

(Add function documentation here)

## Usage

```python
from {module_name} import *

# Add usage examples here
```
"""
        filepath = f"{module_name}.md"
        return self.repo.docs.create_file(filepath, doc_content)

