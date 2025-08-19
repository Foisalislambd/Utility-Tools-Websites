"""Text utility functions"""
import re
import difflib
from typing import Dict, Any

def count_words(text: str) -> Dict[str, Any]:
    """Count words, characters, lines, and paragraphs in text"""
    if not text:
        return {"words": 0, "characters": 0, "characters_no_spaces": 0, "lines": 0, "paragraphs": 0}
    
    words = len(re.findall(r'\b\w+\b', text))
    characters = len(text)
    characters_no_spaces = len(text.replace(' ', '').replace('\t', '').replace('\n', ''))
    lines = len(text.split('\n'))
    paragraphs = len([p for p in text.split('\n\n') if p.strip()])
    
    return {
        "words": words,
        "characters": characters,
        "characters_no_spaces": characters_no_spaces,
        "lines": lines,
        "paragraphs": paragraphs,
        "reading_time": round(words / 200, 1)  # Average reading speed
    }

def convert_case(text: str, case_type: str) -> Dict[str, str]:
    """Convert text case"""
    conversions = {
        "upper": text.upper(),
        "lower": text.lower(),
        "title": text.title(),
        "sentence": text.capitalize(),
        "camel": ''.join(word.capitalize() for word in re.findall(r'\b\w+\b', text)),
        "snake": '_'.join(re.findall(r'\b\w+\b', text.lower())),
        "kebab": '-'.join(re.findall(r'\b\w+\b', text.lower())),
        "pascal": ''.join(word.capitalize() for word in re.findall(r'\b\w+\b', text))
    }
    
    if case_type == "all":
        return conversions
    
    return {"result": conversions.get(case_type, text)}

def compare_text(text1: str, text2: str) -> Dict[str, Any]:
    """Compare two texts and show differences"""
    diff = list(difflib.unified_diff(
        text1.splitlines(keepends=True),
        text2.splitlines(keepends=True),
        fromfile='Text 1',
        tofile='Text 2'
    ))
    
    similarity = difflib.SequenceMatcher(None, text1, text2).ratio()
    
    return {
        "similarity": round(similarity * 100, 2),
        "diff": ''.join(diff),
        "changes": len(diff) - 2 if len(diff) > 2 else 0
    }

def format_text(text: str, operation: str) -> Dict[str, str]:
    """Format text with various operations"""
    operations = {
        "trim": text.strip(),
        "remove_extra_spaces": re.sub(r'\s+', ' ', text),
        "remove_line_breaks": text.replace('\n', ' ').replace('\r', ''),
        "add_line_numbers": '\n'.join(f"{i+1}. {line}" for i, line in enumerate(text.split('\n'))),
        "reverse": text[::-1],
        "sort_lines": '\n'.join(sorted(text.split('\n'))),
        "remove_duplicates": '\n'.join(dict.fromkeys(text.split('\n'))),
        "extract_emails": '\n'.join(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)),
        "extract_urls": '\n'.join(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text))
    }
    
    return {"result": operations.get(operation, text)}

def encode_decode_text(text: str, operation: str, encoding: str = "utf-8") -> Dict[str, str]:
    """Encode or decode text"""
    try:
        if operation == "encode":
            if encoding == "base64":
                import base64
                result = base64.b64encode(text.encode()).decode()
            elif encoding == "url":
                import urllib.parse
                result = urllib.parse.quote(text)
            elif encoding == "html":
                import html
                result = html.escape(text)
            else:
                result = text.encode(encoding).hex()
        else:  # decode
            if encoding == "base64":
                import base64
                result = base64.b64decode(text).decode()
            elif encoding == "url":
                import urllib.parse
                result = urllib.parse.unquote(text)
            elif encoding == "html":
                import html
                result = html.unescape(text)
            else:
                result = bytes.fromhex(text).decode(encoding)
        
        return {"result": result, "success": True}
    except Exception as e:
        return {"result": str(e), "success": False}