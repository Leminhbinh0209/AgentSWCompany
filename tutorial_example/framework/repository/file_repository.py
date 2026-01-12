"""File Repository for organizing project files"""
from pathlib import Path
from typing import List, Dict, Optional
import os


class FileRepository:
    """Repository for managing files in a specific directory"""
    
    def __init__(self, base_path: Path, relative_path: str = "."):
        """
        Initialize FileRepository
        
        Args:
            base_path: Base directory path
            relative_path: Relative path from base (e.g., "docs", "src")
        """
        self.base_path = Path(base_path).resolve()
        self.relative_path = Path(relative_path)
        self.repo_path = self.base_path / self.relative_path
        self.repo_path.mkdir(parents=True, exist_ok=True)
    
    def create_file(self, filename: str, content: str) -> Dict[str, any]:
        """
        Create a file in the repository
        
        Args:
            filename: Name of the file
            content: Content to write
            
        Returns:
            Dict with status and file path
        """
        file_path = self.repo_path / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            file_path.write_text(content, encoding='utf-8')
            return {
                "status": "success",
                "message": f"File created: {file_path}",
                "path": str(file_path.relative_to(self.base_path)),
                "absolute_path": str(file_path)
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to create file: {str(e)}",
                "path": str(file_path.relative_to(self.base_path))
            }
    
    def read_file(self, filename: str) -> str:
        """
        Read a file from the repository
        
        Args:
            filename: Name of the file
            
        Returns:
            File content
        """
        file_path = self.repo_path / filename
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        return file_path.read_text(encoding='utf-8')
    
    def file_exists(self, filename: str) -> bool:
        """Check if a file exists"""
        file_path = self.repo_path / filename
        return file_path.exists()
    
    def list_files(self, pattern: str = "*", recursive: bool = True) -> List[str]:
        """
        List files in the repository
        
        Args:
            pattern: File pattern (e.g., "*.py")
            recursive: Whether to search recursively
            
        Returns:
            List of file paths (relative to base)
        """
        files = []
        
        if recursive:
            for file_path in self.repo_path.rglob(pattern):
                if file_path.is_file():
                    files.append(str(file_path.relative_to(self.base_path)))
        else:
            for file_path in self.repo_path.glob(pattern):
                if file_path.is_file():
                    files.append(str(file_path.relative_to(self.base_path)))
        
        return sorted(files)
    
    @property
    def all_files(self) -> List[str]:
        """Get all files in the repository"""
        return self.list_files()
    
    def get_structure(self) -> Dict[str, any]:
        """
        Get the directory structure
        
        Returns:
            Dict representing the directory structure
        """
        structure = {
            "path": str(self.repo_path.relative_to(self.base_path)),
            "files": [],
            "directories": []
        }
        
        for item in self.repo_path.iterdir():
            if item.is_file():
                structure["files"].append(item.name)
            elif item.is_dir():
                structure["directories"].append(item.name)
        
        structure["files"].sort()
        structure["directories"].sort()
        
        return structure
    
    def delete_file(self, filename: str) -> Dict[str, any]:
        """
        Delete a file from the repository
        
        Args:
            filename: Name of the file to delete
            
        Returns:
            Dict with status
        """
        file_path = self.repo_path / filename
        
        if not file_path.exists():
            return {
                "status": "error",
                "message": f"File not found: {file_path}"
            }
        
        try:
            file_path.unlink()
            return {
                "status": "success",
                "message": f"File deleted: {file_path}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to delete file: {str(e)}"
            }
    
    def get_file_info(self, filename: str) -> Dict[str, any]:
        """
        Get information about a file
        
        Args:
            filename: Name of the file
            
        Returns:
            Dict with file information
        """
        file_path = self.repo_path / filename
        
        if not file_path.exists():
            return {
                "exists": False,
                "path": str(file_path.relative_to(self.base_path))
            }
        
        stat = file_path.stat()
        return {
            "exists": True,
            "path": str(file_path.relative_to(self.base_path)),
            "absolute_path": str(file_path),
            "size": stat.st_size,
            "modified": stat.st_mtime,
            "is_file": file_path.is_file(),
            "is_dir": file_path.is_dir()
        }

