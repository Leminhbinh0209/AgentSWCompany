"""Code Reviewer for automated code quality checks"""
import re
import ast
from typing import Dict, List, Optional, Any
from framework.llm import BaseLLM


class CodeReviewer:
    """Automated code reviewer for quality checks"""
    
    def __init__(self, llm: Optional[BaseLLM] = None):
        """
        Initialize Code Reviewer
        
        Args:
            llm: Optional LLM for advanced review suggestions
        """
        self.llm = llm
    
    async def review_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Perform comprehensive code review
        
        Args:
            code: Code to review
            language: Programming language (default: python)
            
        Returns:
            Dict with review results
        """
        review = {
            "status": "success",
            "language": language,
            "issues": [],
            "suggestions": [],
            "score": 100,
            "checks": {}
        }
        
        if language == "python":
            # Run all checks
            style_issues = await self.check_style(code)
            security_issues = await self.check_security(code)
            best_practices = self.check_best_practices(code)  # Not async
            complexity = self.check_complexity(code)
            
            review["checks"]["style"] = style_issues
            review["checks"]["security"] = security_issues
            review["checks"]["best_practices"] = best_practices
            review["checks"]["complexity"] = complexity
            
            # Collect all issues
            all_issues = style_issues + security_issues + best_practices
            review["issues"] = all_issues
            
            # Calculate score (deduct points for issues)
            score = 100
            for issue in all_issues:
                severity = issue.get("severity", "low")
                if severity == "high":
                    score -= 10
                elif severity == "medium":
                    score -= 5
                else:
                    score -= 1
            review["score"] = max(0, score)
            
            # Get suggestions
            if self.llm:
                suggestions = await self.suggest_improvements(code)
                review["suggestions"] = suggestions
        
        return review
    
    async def check_style(self, code: str) -> List[Dict[str, Any]]:
        """
        Check code style issues
        
        Args:
            code: Code to check
            
        Returns:
            List of style issues
        """
        issues = []
        
        # Check for long lines (PEP 8: max 79 characters)
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            if len(line) > 100:  # Allow some flexibility
                issues.append({
                    "type": "style",
                    "severity": "low",
                    "line": i,
                    "message": f"Line too long ({len(line)} characters, recommended: 79)",
                    "suggestion": "Break long lines into multiple lines"
                })
        
        # Check for trailing whitespace
        for i, line in enumerate(lines, 1):
            if line.rstrip() != line:
                issues.append({
                    "type": "style",
                    "severity": "low",
                    "line": i,
                    "message": "Trailing whitespace",
                    "suggestion": "Remove trailing whitespace"
                })
        
        # Check for mixed tabs and spaces
        has_tabs = any('\t' in line for line in lines)
        has_spaces = any(re.match(r'^ +', line) for line in lines if line.strip())
        if has_tabs and has_spaces:
            issues.append({
                "type": "style",
                "severity": "medium",
                "line": None,
                "message": "Mixed tabs and spaces",
                "suggestion": "Use only spaces (PEP 8 recommends 4 spaces per indentation level)"
            })
        
        # Check for missing docstrings in functions/classes
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if not ast.get_docstring(node):
                        issues.append({
                            "type": "style",
                            "severity": "low",
                            "line": node.lineno,
                            "message": f"Function '{node.name}' missing docstring",
                            "suggestion": "Add a docstring describing what the function does"
                        })
                elif isinstance(node, ast.ClassDef):
                    if not ast.get_docstring(node):
                        issues.append({
                            "type": "style",
                            "severity": "low",
                            "line": node.lineno,
                            "message": f"Class '{node.name}' missing docstring",
                            "suggestion": "Add a docstring describing the class"
                        })
        except SyntaxError:
            # If code has syntax errors, skip AST analysis
            pass
        
        return issues
    
    async def check_security(self, code: str) -> List[Dict[str, Any]]:
        """
        Check for security issues
        
        Args:
            code: Code to check
            
        Returns:
            List of security issues
        """
        issues = []
        lines = code.split('\n')
        
        # Check for dangerous functions
        dangerous_patterns = [
            (r'eval\s*\(', "high", "Use of eval() is dangerous and can lead to code injection"),
            (r'exec\s*\(', "high", "Use of exec() is dangerous and can lead to code injection"),
            (r'__import__\s*\(', "high", "Dynamic imports can be dangerous"),
            (r'pickle\.loads?\s*\(', "medium", "Pickle can execute arbitrary code"),
            (r'yaml\.load\s*\(', "medium", "yaml.load() can execute arbitrary code, use yaml.safe_load()"),
            (r'shell\s*=\s*True', "high", "shell=True in subprocess can be dangerous"),
            (r'password\s*=\s*["\'].*["\']', "high", "Hardcoded passwords are a security risk"),
        ]
        
        for i, line in enumerate(lines, 1):
            for pattern, severity, message in dangerous_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append({
                        "type": "security",
                        "severity": severity,
                        "line": i,
                        "message": message,
                        "code": line.strip(),
                        "suggestion": "Review and use safer alternatives"
                    })
        
        # Check for SQL injection patterns (basic)
        sql_patterns = [
            (r'\+.*["\'].*SELECT', "high", "Potential SQL injection - use parameterized queries"),
            (r'f["\'].*SELECT', "high", "Potential SQL injection in f-string - use parameterized queries"),
        ]
        
        for i, line in enumerate(lines, 1):
            for pattern, severity, message in sql_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append({
                        "type": "security",
                        "severity": severity,
                        "line": i,
                        "message": message,
                        "code": line.strip(),
                        "suggestion": "Use parameterized queries or ORM"
                    })
        
        return issues
    
    def check_best_practices(self, code: str) -> List[Dict[str, Any]]:
        """
        Check for best practices violations
        
        Args:
            code: Code to check
            
        Returns:
            List of best practice issues
        """
        issues = []
        lines = code.split('\n')
        
        # Check for bare except clauses
        for i, line in enumerate(lines, 1):
            if re.search(r'except\s*:', line):
                issues.append({
                    "type": "best_practice",
                    "severity": "medium",
                    "line": i,
                    "message": "Bare except clause catches all exceptions",
                    "suggestion": "Specify exception types: except ValueError: or except Exception:"
                })
        
        # Check for unused imports (basic check)
        try:
            tree = ast.parse(code)
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module.split('.')[0])
            
            # Simple check - if import is not used in code (very basic)
            code_lower = code.lower()
            for imp in imports:
                if imp.lower() not in code_lower.replace(f"import {imp.lower()}", ""):
                    # This is a very basic check, might have false positives
                    pass
        except SyntaxError:
            pass
        
        # Check for magic numbers
        magic_number_pattern = r'\b\d{3,}\b'
        for i, line in enumerate(lines, 1):
            if re.search(magic_number_pattern, line) and '#' not in line:
                # Check if it's not a common pattern
                if not re.search(r'(port|timeout|size|limit|max|min)\s*=\s*\d+', line, re.IGNORECASE):
                    issues.append({
                        "type": "best_practice",
                        "severity": "low",
                        "line": i,
                        "message": "Magic number detected - consider using a named constant",
                        "suggestion": "Define constants with meaningful names"
                    })
        
        return issues
    
    def check_complexity(self, code: str) -> Dict[str, Any]:
        """
        Check code complexity
        
        Args:
            code: Code to check
            
        Returns:
            Dict with complexity metrics
        """
        metrics = {
            "lines": len(code.split('\n')),
            "functions": 0,
            "classes": 0,
            "max_nesting": 0,
            "cyclomatic_complexity": 0
        }
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    metrics["functions"] += 1
                elif isinstance(node, ast.ClassDef):
                    metrics["classes"] += 1
            
            # Simple complexity check
            if metrics["lines"] > 500:
                metrics["complexity_warning"] = "File is very long, consider splitting into smaller modules"
            if metrics["functions"] > 20:
                metrics["complexity_warning"] = "Many functions in one file, consider splitting"
        
        except SyntaxError:
            pass
        
        return metrics
    
    async def suggest_improvements(self, code: str) -> List[str]:
        """
        Suggest code improvements using LLM
        
        Args:
            code: Code to review
            
        Returns:
            List of improvement suggestions
        """
        if not self.llm:
            return []
        
        prompt = f"""Review the following Python code and suggest improvements for:
1. Code quality
2. Performance
3. Readability
4. Best practices

Code:
```python
{code}
```

Provide 3-5 specific, actionable suggestions."""

        try:
            response = await self.llm.aask(prompt)
            # Parse response into list of suggestions
            suggestions = [s.strip() for s in response.split('\n') if s.strip() and s.strip().startswith(('-', '•', '1.', '2.', '3.'))]
            return suggestions[:5]  # Limit to 5 suggestions
        except Exception:
            return []
    
    async def validate_tests(self, code: str, tests: str) -> Dict[str, Any]:
        """
        Validate that tests cover the code
        
        Args:
            code: Source code
            tests: Test code
            
        Returns:
            Dict with validation results
        """
        validation = {
            "status": "success",
            "test_functions": 0,
            "source_functions": 0,
            "coverage_estimate": 0,
            "issues": []
        }
        
        try:
            # Parse source code
            source_tree = ast.parse(code)
            source_functions = []
            for node in ast.walk(source_tree):
                if isinstance(node, ast.FunctionDef):
                    source_functions.append(node.name)
            
            # Parse test code
            test_tree = ast.parse(tests)
            test_functions = []
            for node in ast.walk(test_tree):
                if isinstance(node, ast.FunctionDef):
                    if node.name.startswith('test_'):
                        test_functions.append(node.name)
            
            validation["source_functions"] = len(source_functions)
            validation["test_functions"] = len(test_functions)
            
            # Estimate coverage (very basic)
            if source_functions:
                # Check if test functions match source functions
                tested_functions = []
                for test_func in test_functions:
                    # Extract function name from test name (e.g., test_add -> add)
                    func_name = test_func.replace('test_', '')
                    if func_name in source_functions:
                        tested_functions.append(func_name)
                
                validation["coverage_estimate"] = len(tested_functions) / len(source_functions) * 100
            else:
                validation["coverage_estimate"] = 0
            
            # Check for issues
            if validation["test_functions"] == 0:
                validation["issues"].append("No test functions found")
            if validation["coverage_estimate"] < 50:
                validation["issues"].append(f"Low test coverage estimate: {validation['coverage_estimate']:.1f}%")
        
        except SyntaxError as e:
            validation["status"] = "error"
            validation["issues"].append(f"Syntax error: {str(e)}")
        
        return validation

