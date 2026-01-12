"""Project Repository for managing complete software projects"""
from pathlib import Path
from typing import Optional, Dict, List
from framework.repository.file_repository import FileRepository


class ProjectRepo:
    """Repository for managing a complete software project"""
    
    # Standard directory names
    DOCS_DIR = "docs"
    SRC_DIR = "src"
    TESTS_DIR = "tests"
    RESOURCES_DIR = "resources"
    CONFIG_DIR = "config"
    
    def __init__(self, root: str | Path):
        """
        Initialize Project Repository
        
        Args:
            root: Root directory path for the project
        """
        if isinstance(root, str):
            self.root = Path(root).resolve()
        else:
            self.root = Path(root).resolve()
        
        self.root.mkdir(parents=True, exist_ok=True)
        
        # Initialize sub-repositories
        self.docs = FileRepository(self.root, self.DOCS_DIR)
        self.srcs = FileRepository(self.root, self.SRC_DIR)
        self.tests = FileRepository(self.root, self.TESTS_DIR)
        self.resources = FileRepository(self.root, self.RESOURCES_DIR)
        self.config = FileRepository(self.root, self.CONFIG_DIR)
    
    @property
    def workdir(self) -> Path:
        """Get the working directory"""
        return self.root
    
    def create_file(self, filepath: str, content: str, repo: Optional[str] = None) -> Dict[str, any]:
        """
        Create a file in the project
        
        Args:
            filepath: Path to the file (relative to repo or root)
            content: Content to write
            repo: Which repository to use (docs, srcs, tests, resources, config)
                  If None, filepath is relative to root
                  
        Returns:
            Dict with status
        """
        if repo:
            repo_obj = getattr(self, repo, None)
            if repo_obj:
                return repo_obj.create_file(filepath, content)
            else:
                return {
                    "status": "error",
                    "message": f"Unknown repository: {repo}"
                }
        else:
            # Create in root
            file_path = self.root / filepath
            file_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                file_path.write_text(content, encoding='utf-8')
                return {
                    "status": "success",
                    "message": f"File created: {file_path}",
                    "path": str(file_path.relative_to(self.root))
                }
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"Failed to create file: {str(e)}"
                }
    
    def read_file(self, filepath: str, repo: Optional[str] = None) -> str:
        """
        Read a file from the project
        
        Args:
            filepath: Path to the file
            repo: Which repository to use (optional)
            
        Returns:
            File content
        """
        if repo:
            repo_obj = getattr(self, repo, None)
            if repo_obj:
                return repo_obj.read_file(filepath)
            else:
                raise ValueError(f"Unknown repository: {repo}")
        else:
            file_path = self.root / filepath
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            return file_path.read_text(encoding='utf-8')
    
    def get_structure(self) -> Dict[str, any]:
        """
        Get the complete project structure
        
        Returns:
            Dict representing the project structure
        """
        structure = {
            "root": str(self.root),
            "directories": {
                "docs": self.docs.get_structure(),
                "src": self.srcs.get_structure(),
                "tests": self.tests.get_structure(),
                "resources": self.resources.get_structure(),
                "config": self.config.get_structure()
            },
            "root_files": []
        }
        
        # Get root-level files
        for item in self.root.iterdir():
            if item.is_file():
                structure["root_files"].append(item.name)
        
        structure["root_files"].sort()
        
        return structure
    
    def list_all_files(self) -> List[str]:
        """List all files in the project"""
        all_files = []
        
        for repo_name in ["docs", "srcs", "tests", "resources", "config"]:
            repo = getattr(self, repo_name)
            files = repo.list_files(recursive=True)
            all_files.extend(files)
        
        # Add root files
        for item in self.root.iterdir():
            if item.is_file():
                all_files.append(item.name)
        
        return sorted(set(all_files))
    
    def create_readme(self, content: str) -> Dict[str, any]:
        """Create a README.md file in the root"""
        return self.create_file("README.md", content)
    
    def create_requirements(self, packages: List[str]) -> Dict[str, any]:
        """Create a requirements.txt file"""
        content = "\n".join(packages) + "\n"
        return self.create_file("requirements.txt", content)
    
    def create_gitignore(self, patterns: List[str]) -> Dict[str, any]:
        """Create a .gitignore file"""
        content = "\n".join(patterns) + "\n"
        return self.create_file(".gitignore", content)
    
    def initialize_python_package(self, package_name: str) -> Dict[str, any]:
        """
        Initialize a Python package structure
        
        Args:
            package_name: Name of the package
            
        Returns:
            Dict with initialization results
        """
        results = []
        
        # Create __init__.py in src
        results.append(self.srcs.create_file("__init__.py", f'"""Package: {package_name}"""\n'))
        
        # Create package directory structure
        package_dir = package_name.replace("-", "_")
        results.append(self.srcs.create_file(f"{package_dir}/__init__.py", f'"""Module: {package_dir}"""\n'))
        
        return {
            "status": "success",
            "package_name": package_name,
            "results": results
        }
    
    def create_test_structure(self) -> Dict[str, any]:
        """Create basic test structure"""
        results = []
        
        # Create __init__.py in tests
        results.append(self.tests.create_file("__init__.py", ""))
        
        # Create conftest.py for pytest
        conftest_content = """import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))
"""
        results.append(self.tests.create_file("conftest.py", conftest_content))
        
        return {
            "status": "success",
            "results": results
        }
    
    def get_project_summary(self) -> Dict[str, any]:
        """Get a summary of the project"""
        structure = self.get_structure()
        
        summary = {
            "root": str(self.root),
            "total_files": len(self.list_all_files()),
            "directories": {
                "docs": len(self.docs.all_files),
                "src": len(self.srcs.all_files),
                "tests": len(self.tests.all_files),
                "resources": len(self.resources.all_files),
                "config": len(self.config.all_files)
            },
            "root_files": len(structure["root_files"])
        }
        
        return summary
    
    def __str__(self) -> str:
        """String representation of the project"""
        summary = self.get_project_summary()
        return f"""ProjectRepo({self.root})
  Docs: {summary['directories']['docs']} files
  Source: {summary['directories']['src']} files
  Tests: {summary['directories']['tests']} files
  Resources: {summary['directories']['resources']} files
  Config: {summary['directories']['config']} files
  Root: {summary['root_files']} files
  Total: {summary['total_files']} files"""

