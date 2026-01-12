"""File Editor Tool for creating, reading, and editing files"""
import os
import re
from pathlib import Path
from typing import List, Dict, Optional
import difflib


class Editor:
    """File Editor tool for file operations"""
    
    def __init__(self, workspace_path: str = "."):
        """
        Initialize the Editor
        
        Args:
            workspace_path: Base directory for file operations
        """
        self.workspace_path = Path(workspace_path).resolve()
        self.workspace_path.mkdir(parents=True, exist_ok=True)
    
    def _get_path(self, filename: str) -> Path:
        """Get absolute path for a file"""
        if os.path.isabs(filename):
            return Path(filename)
        return self.workspace_path / filename
    
    async def create_file(self, filename: str, content: str) -> Dict[str, any]:
        """
        Create a new file with content
        
        Args:
            filename: Name/path of the file to create
            content: Content to write to the file
            
        Returns:
            Dict with status and file path
        """
        file_path = self._get_path(filename)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            file_path.write_text(content, encoding='utf-8')
            return {
                "status": "success",
                "message": f"File created: {file_path}",
                "path": str(file_path),
                "size": len(content)
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to create file: {str(e)}",
                "path": str(file_path)
            }
    
    async def read(self, filename: str) -> str:
        """
        Read content from a file
        
        Args:
            filename: Name/path of the file to read
            
        Returns:
            File content as string
        """
        file_path = self._get_path(filename)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        return file_path.read_text(encoding='utf-8')
    
    async def write(self, filename: str, content: str) -> Dict[str, any]:
        """
        Write content to a file (overwrites existing)
        
        Args:
            filename: Name/path of the file
            content: Content to write
            
        Returns:
            Dict with status
        """
        file_path = self._get_path(filename)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            file_path.write_text(content, encoding='utf-8')
            return {
                "status": "success",
                "message": f"File written: {file_path}",
                "path": str(file_path),
                "size": len(content)
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to write file: {str(e)}",
                "path": str(file_path)
            }
    
    async def edit_file_by_replace(self, filename: str, old_text: str, new_text: str) -> Dict[str, any]:
        """
        Replace text in a file
        
        Args:
            filename: Name/path of the file
            old_text: Text to replace
            new_text: Replacement text
            
        Returns:
            Dict with status and changes
        """
        file_path = self._get_path(filename)
        
        if not file_path.exists():
            return {
                "status": "error",
                "message": f"File not found: {file_path}"
            }
        
        try:
            content = await self.read(filename)
            
            if old_text not in content:
                return {
                    "status": "error",
                    "message": "Text to replace not found in file"
                }
            
            new_content = content.replace(old_text, new_text)
            result = await self.write(filename, new_content)
            
            return {
                "status": "success",
                "message": f"File edited: {file_path}",
                "path": str(file_path),
                "changes": {
                    "old_length": len(old_text),
                    "new_length": len(new_text),
                    "occurrences": content.count(old_text)
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to edit file: {str(e)}"
            }
    
    async def insert_content_at_line(self, filename: str, line_number: int, content: str) -> Dict[str, any]:
        """
        Insert content at a specific line number
        
        Args:
            filename: Name/path of the file
            line_number: Line number to insert at (1-indexed)
            content: Content to insert
            
        Returns:
            Dict with status
        """
        file_path = self._get_path(filename)
        
        if not file_path.exists():
            return {
                "status": "error",
                "message": f"File not found: {file_path}"
            }
        
        try:
            lines = (await self.read(filename)).splitlines(keepends=True)
            
            if line_number < 1 or line_number > len(lines) + 1:
                return {
                    "status": "error",
                    "message": f"Line number {line_number} out of range (1-{len(lines) + 1})"
                }
            
            # Insert at line_number (convert to 0-indexed)
            lines.insert(line_number - 1, content + '\n' if not content.endswith('\n') else content)
            new_content = ''.join(lines)
            
            result = await self.write(filename, new_content)
            return {
                "status": "success",
                "message": f"Content inserted at line {line_number}",
                "path": str(file_path),
                "line_number": line_number
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to insert content: {str(e)}"
            }
    
    async def find_file(self, pattern: str, directory: str = None) -> List[str]:
        """
        Find files matching a pattern
        
        Args:
            pattern: File name pattern (supports wildcards)
            directory: Directory to search in (default: workspace)
            
        Returns:
            List of matching file paths
        """
        search_dir = self._get_path(directory) if directory else self.workspace_path
        
        if not search_dir.exists():
            return []
        
        matches = []
        pattern_re = re.compile(pattern.replace('*', '.*'))
        
        for file_path in search_dir.rglob('*'):
            if file_path.is_file() and pattern_re.search(file_path.name):
                matches.append(str(file_path.relative_to(self.workspace_path)))
        
        return matches
    
    async def search_file(self, pattern: str, filename: str) -> List[Dict[str, any]]:
        """
        Search for text pattern in a file
        
        Args:
            pattern: Text pattern to search for (regex supported)
            filename: File to search in
            
        Returns:
            List of matches with line numbers and content
        """
        file_path = self._get_path(filename)
        
        if not file_path.exists():
            return []
        
        try:
            content = await self.read(filename)
            lines = content.splitlines()
            matches = []
            pattern_re = re.compile(pattern, re.IGNORECASE)
            
            for line_num, line in enumerate(lines, 1):
                if pattern_re.search(line):
                    matches.append({
                        "line": line_num,
                        "content": line.strip(),
                        "match": pattern_re.search(line).group()
                    })
            
            return matches
        except Exception as e:
            return []
    
    async def search_dir(self, pattern: str, directory: str = None) -> List[Dict[str, any]]:
        """
        Search for text pattern in all files in a directory
        
        Args:
            pattern: Text pattern to search for (regex supported)
            directory: Directory to search in (default: workspace)
            
        Returns:
            List of matches with file paths and line numbers
        """
        search_dir = self._get_path(directory) if directory else self.workspace_path
        
        if not search_dir.exists():
            return []
        
        matches = []
        pattern_re = re.compile(pattern, re.IGNORECASE)
        
        for file_path in search_dir.rglob('*'):
            if file_path.is_file():
                try:
                    content = file_path.read_text(encoding='utf-8')
                    lines = content.splitlines()
                    
                    for line_num, line in enumerate(lines, 1):
                        if pattern_re.search(line):
                            matches.append({
                                "file": str(file_path.relative_to(self.workspace_path)),
                                "line": line_num,
                                "content": line.strip()[:100]  # Limit content length
                            })
                except Exception:
                    # Skip files that can't be read as text
                    continue
        
        return matches
    
    async def similarity_search(self, query: str, directory: str = None, limit: int = 10) -> List[Dict[str, any]]:
        """
        Find files with similar content to the query
        
        Args:
            query: Query text to search for
            directory: Directory to search in (default: workspace)
            limit: Maximum number of results
            
        Returns:
            List of similar files with similarity scores
        """
        search_dir = self._get_path(directory) if directory else self.workspace_path
        
        if not search_dir.exists():
            return []
        
        results = []
        query_lower = query.lower()
        
        for file_path in search_dir.rglob('*'):
            if file_path.is_file():
                try:
                    content = file_path.read_text(encoding='utf-8')
                    content_lower = content.lower()
                    
                    # Simple similarity using ratio
                    similarity = difflib.SequenceMatcher(None, query_lower, content_lower[:1000]).ratio()
                    
                    if similarity > 0.1:  # Threshold
                        results.append({
                            "file": str(file_path.relative_to(self.workspace_path)),
                            "similarity": similarity,
                            "preview": content[:200]
                        })
                except Exception:
                    continue
        
        # Sort by similarity and return top results
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:limit]
    
    async def list_files(self, directory: str = None, recursive: bool = False) -> List[str]:
        """
        List files in a directory
        
        Args:
            directory: Directory to list (default: workspace)
            recursive: Whether to list recursively
            
        Returns:
            List of file paths
        """
        search_dir = self._get_path(directory) if directory else self.workspace_path
        
        if not search_dir.exists():
            return []
        
        files = []
        
        if recursive:
            for file_path in search_dir.rglob('*'):
                if file_path.is_file():
                    files.append(str(file_path.relative_to(self.workspace_path)))
        else:
            for file_path in search_dir.iterdir():
                if file_path.is_file():
                    files.append(str(file_path.relative_to(self.workspace_path)))
        
        return sorted(files)

