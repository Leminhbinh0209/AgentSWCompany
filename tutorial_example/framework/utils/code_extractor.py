"""Utility functions for extracting code from LLM outputs"""
import re
from typing import List, Optional


def extract_code_blocks(content: str) -> str:
    """
    Extract code blocks from LLM output.
    
    Looks for code blocks in markdown format (```language ... ```)
    and returns the code content, removing explanatory text.
    
    Args:
        content: Full content that may contain code blocks
        
    Returns:
        Extracted code, or original content if no code blocks found
    """
    if not content:
        return ""
    
    # Pattern to match code blocks: ```language\ncode\n```
    code_block_pattern = r'```(?:\w+)?\n(.*?)```'
    matches = re.findall(code_block_pattern, content, re.DOTALL)
    
    if matches:
        # If multiple code blocks, join them with separators
        extracted_code = '\n\n'.join([match.strip() for match in matches])
        # Remove any trailing explanatory text
        extracted_code = _remove_explanatory_text(extracted_code)
        return extracted_code.strip()
    
    # If no code blocks found, try to find code-like content
    # Look for patterns like function definitions, class definitions, etc.
    lines = content.split('\n')
    code_lines = []
    in_code_section = False
    code_indicators = ['def ', 'class ', 'import ', 'function ', 'const ', 'let ', 'var ', 'export ', 'from ', 'require(']
    
    for i, line in enumerate(lines):
        # Detect start of code section
        if any(indicator in line for indicator in code_indicators):
            in_code_section = True
        
        if in_code_section:
            # Stop if we hit clear markdown/explanatory text
            stripped = line.strip().lower()
            
            # Stop conditions: explanatory text patterns
            stop_patterns = [
                r'^note:',
                r'^requirements?:',
                r'^the above code',
                r'^this is just',
                r'^above code is',
                r'^just an example',
                r'^may need to be',
                r'^should be',
                r'^follow best practices$',
                r'^include proper',
                r'^add comments',
            ]
            
            should_stop = False
            for pattern in stop_patterns:
                if re.match(pattern, stripped):
                    should_stop = True
                    break
            
            if should_stop:
                break
            
            # Also stop on numbered requirements list
            if re.match(r'^\d+\.\s+(write|include|add|follow)', stripped):
                break
            
            # Stop on markdown headers (but allow code comments)
            if (stripped.startswith('##') or 
                (stripped.startswith('#') and len(stripped) < 30 and 
                 'def' not in stripped and 'class' not in stripped and 'import' not in stripped)):
                # Check if next lines are code
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if not any(indicator in next_line for indicator in code_indicators):
                        break
            
            code_lines.append(line)
    
    if code_lines:
        result = '\n'.join(code_lines).strip()
        # Remove any trailing explanatory text
        result = _remove_explanatory_text(result)
        return result
    
    # Return original if no code detected, but still try to clean it
    return _remove_explanatory_text(content)


def _remove_explanatory_text(code: str) -> str:
    """
    Remove explanatory text from the end of code.
    
    Args:
        code: Code string that may have explanatory text
        
    Returns:
        Cleaned code
    """
    if not code:
        return ""
    
    lines = code.split('\n')
    clean_lines = []
    found_explanatory = False
    
    # Patterns that indicate explanatory text
    explanatory_patterns = [
        r'^note:',
        r'^requirements?:',
        r'^the above',
        r'^this is just',
        r'^just an example',
        r'^\d+\.\s+(write|include|add|follow)',
    ]
    
    for line in lines:
        stripped = line.strip().lower()
        
        # Check if this line starts explanatory text
        for pattern in explanatory_patterns:
            if re.match(pattern, stripped):
                found_explanatory = True
                break
        
        if found_explanatory:
            break
        
        clean_lines.append(line)
    
    return '\n'.join(clean_lines).strip()


def extract_code_by_language(content: str) -> dict:
    """
    Extract code blocks by language.
    
    Args:
        content: Full content that may contain code blocks
        
    Returns:
        Dictionary mapping language to code content
    """
    if not content:
        return {}
    
    # Pattern to match code blocks with language: ```language\ncode\n```
    code_block_pattern = r'```(\w+)?\n(.*?)```'
    matches = re.findall(code_block_pattern, content, re.DOTALL)
    
    result = {}
    for lang, code in matches:
        lang = lang or 'unknown'
        if lang not in result:
            result[lang] = []
        result[lang].append(code.strip())
    
    # Join multiple blocks of same language
    for lang in result:
        result[lang] = '\n\n'.join(result[lang])
    
    return result


def detect_code_language(code: str) -> Optional[str]:
    """
    Detect programming language from code content.
    
    Args:
        code: Code content
        
    Returns:
        Detected language or None
    """
    if not code:
        return None
    
    # Language detection patterns (check in order of specificity)
    # Check JavaScript/React first (most common in our use case)
    js_patterns = [
        r'import\s+.*from\s+[\'"]react',
        r'import\s+React',
        r'const\s+\w+\s*=\s*require\(',
        r'const\s+express\s*=',
        r'function\s+\w+\s*\([^)]*\)\s*\{',
        r'const\s+\w+\s*=\s*\([^)]*\)\s*=>',
    ]
    for pattern in js_patterns:
        if re.search(pattern, code, re.MULTILINE | re.IGNORECASE):
            return 'javascript'
    
    # Check other languages
    patterns = {
        'python': [r'^import\s+\w+$', r'^from\s+\w+\s+import', r'^def\s+\w+\s*\(', r'^class\s+\w+\s*[\(:]'],
        'typescript': [r'^import\s+.*from', r'const\s+\w+:\s*\w+', r'interface\s+\w+'],
        'java': [r'^package\s+\w+', r'^import\s+\w+;', r'^public\s+class\s+\w+'],
        'cpp': [r'^#include\s*<', r'^using\s+namespace', r'^class\s+\w+\s*\{'],
        'html': [r'^<!DOCTYPE\s+html', r'^<html', r'^<head>'],
        'css': [r'^\s*\w+\s*\{', r'^@\w+'],
    }
    
    for lang, lang_patterns in patterns.items():
        for pattern in lang_patterns:
            if re.search(pattern, code, re.MULTILINE | re.IGNORECASE):
                return lang
    
    return None

