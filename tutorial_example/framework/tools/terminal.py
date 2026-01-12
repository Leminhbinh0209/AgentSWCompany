"""Terminal/Command Execution Tool"""
import asyncio
import subprocess
import sys
from pathlib import Path
from typing import Dict, Optional
import tempfile
import os


class Terminal:
    """Terminal tool for executing commands and running code"""
    
    def __init__(self, workspace_path: str = "."):
        """
        Initialize the Terminal
        
        Args:
            workspace_path: Base directory for command execution
        """
        self.workspace_path = Path(workspace_path).resolve()
        self.workspace_path.mkdir(parents=True, exist_ok=True)
    
    async def run_command(self, command: str, cwd: Optional[str] = None, timeout: int = 30) -> Dict[str, any]:
        """
        Execute a shell command
        
        Args:
            command: Command to execute
            cwd: Working directory (default: workspace_path)
            timeout: Timeout in seconds
            
        Returns:
            Dict with stdout, stderr, returncode
        """
        work_dir = Path(cwd).resolve() if cwd else self.workspace_path
        
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(work_dir)
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                return {
                    "status": "error",
                    "stdout": "",
                    "stderr": f"Command timed out after {timeout} seconds",
                    "returncode": -1
                }
            
            return {
                "status": "success" if process.returncode == 0 else "error",
                "stdout": stdout.decode('utf-8', errors='ignore'),
                "stderr": stderr.decode('utf-8', errors='ignore'),
                "returncode": process.returncode
            }
        except Exception as e:
            return {
                "status": "error",
                "stdout": "",
                "stderr": str(e),
                "returncode": -1
            }
    
    async def run_python(self, code: str, timeout: int = 30) -> Dict[str, any]:
        """
        Execute Python code
        
        Args:
            code: Python code to execute
            timeout: Timeout in seconds
            
        Returns:
            Dict with stdout, stderr, returncode
        """
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, dir=str(self.workspace_path)) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # Run the Python file
            result = await self.run_command(
                f"{sys.executable} {temp_file}",
                timeout=timeout
            )
            
            # Clean up
            try:
                os.unlink(temp_file)
            except Exception:
                pass
            
            return result
        except Exception as e:
            # Clean up on error
            try:
                os.unlink(temp_file)
            except Exception:
                pass
            return {
                "status": "error",
                "stdout": "",
                "stderr": str(e),
                "returncode": -1
            }
    
    async def install_package(self, package: str, use_pip: bool = True) -> Dict[str, any]:
        """
        Install a Python package
        
        Args:
            package: Package name to install
            use_pip: Whether to use pip (default: True)
            
        Returns:
            Dict with installation result
        """
        if use_pip:
            command = f"{sys.executable} -m pip install {package}"
        else:
            command = f"pip install {package}"
        
        return await self.run_command(command, timeout=120)
    
    async def run_tests(self, test_file: str, test_command: Optional[str] = None) -> Dict[str, any]:
        """
        Run tests using pytest or unittest
        
        Args:
            test_file: Test file path
            test_command: Custom test command (optional)
            
        Returns:
            Dict with test results
        """
        test_path = Path(test_file)
        
        if not test_path.is_absolute():
            test_path = self.workspace_path / test_file
        
        if not test_path.exists():
            return {
                "status": "error",
                "stdout": "",
                "stderr": f"Test file not found: {test_path}",
                "returncode": -1
            }
        
        # Try pytest first, then unittest
        if test_command:
            command = test_command
        else:
            # Check if pytest is available
            pytest_check = await self.run_command(f"{sys.executable} -m pytest --version", timeout=5)
            if pytest_check["returncode"] == 0:
                command = f"{sys.executable} -m pytest {test_path}"
            else:
                command = f"{sys.executable} -m unittest {test_path}"
        
        return await self.run_command(command, timeout=60)
    
    async def check_syntax(self, filename: str) -> Dict[str, any]:
        """
        Check Python syntax of a file
        
        Args:
            filename: Python file to check
            
        Returns:
            Dict with syntax check result
        """
        file_path = Path(filename)
        if not file_path.is_absolute():
            file_path = self.workspace_path / filename
        
        if not file_path.exists():
            return {
                "status": "error",
                "valid": False,
                "message": f"File not found: {file_path}"
            }
        
        command = f"{sys.executable} -m py_compile {file_path}"
        result = await self.run_command(command, timeout=10)
        
        return {
            "status": result["status"],
            "valid": result["returncode"] == 0,
            "message": result["stderr"] if result["stderr"] else "Syntax is valid",
            "stdout": result["stdout"]
        }
    
    async def get_python_version(self) -> str:
        """Get Python version"""
        result = await self.run_command(f"{sys.executable} --version", timeout=5)
        return result["stdout"].strip() if result["status"] == "success" else "Unknown"

