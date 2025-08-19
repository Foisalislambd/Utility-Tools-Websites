"""Advanced converter utility functions"""
import re
import json
import html
import yaml
from typing import Dict, Any
from datetime import datetime
import base64

def html_to_text(html_content: str) -> Dict[str, str]:
    """Convert HTML to plain text"""
    if not html_content:
        return {"result": ""}
    
    # Remove script and style elements
    text = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', html_content, flags=re.DOTALL)
    
    # Replace common HTML entities
    text = html.unescape(text)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return {
        "result": text,
        "original_length": len(html_content),
        "converted_length": len(text)
    }

def text_to_html(text: str, options: Dict[str, bool] = None) -> Dict[str, str]:
    """Convert plain text to HTML"""
    if not text:
        return {"result": ""}
    
    if not options:
        options = {
            "preserve_line_breaks": True,
            "convert_urls": True,
            "escape_html": True
        }
    
    result = text
    
    if options.get("escape_html", True):
        result = html.escape(result)
    
    if options.get("preserve_line_breaks", True):
        result = result.replace('\n', '<br>\n')
    
    if options.get("convert_urls", True):
        url_pattern = r'(https?://[^\s]+)'
        result = re.sub(url_pattern, r'<a href="\1" target="_blank">\1</a>', result)
    
    return {
        "result": result,
        "original_length": len(text),
        "converted_length": len(result)
    }

def yaml_converter(text: str, action: str = "to_json") -> Dict[str, Any]:
    """Convert between YAML and JSON"""
    try:
        if action == "to_json":
            # YAML to JSON
            data = yaml.safe_load(text)
            result = json.dumps(data, indent=2)
            return {"result": result, "success": True}
        else:
            # JSON to YAML
            data = json.loads(text)
            result = yaml.dump(data, default_flow_style=False, indent=2)
            return {"result": result, "success": True}
    except Exception as e:
        return {"result": str(e), "success": False}

def sql_formatter(sql: str) -> Dict[str, Any]:
    """Format SQL query (basic implementation)"""
    if not sql:
        return {"result": ""}
    
    # Basic SQL formatting
    keywords = [
        'SELECT', 'FROM', 'WHERE', 'JOIN', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN',
        'GROUP BY', 'ORDER BY', 'HAVING', 'INSERT', 'UPDATE', 'DELETE', 'CREATE',
        'ALTER', 'DROP', 'INDEX', 'TABLE', 'DATABASE', 'AND', 'OR', 'NOT', 'IN',
        'EXISTS', 'BETWEEN', 'LIKE', 'IS', 'NULL', 'DISTINCT', 'COUNT', 'SUM',
        'AVG', 'MIN', 'MAX', 'UNION', 'CASE', 'WHEN', 'THEN', 'ELSE', 'END'
    ]
    
    formatted = sql
    
    # Add line breaks before major keywords
    major_keywords = ['SELECT', 'FROM', 'WHERE', 'GROUP BY', 'ORDER BY', 'HAVING']
    for keyword in major_keywords:
        formatted = re.sub(f'\\b{keyword}\\b', f'\n{keyword}', formatted, flags=re.IGNORECASE)
    
    # Uppercase keywords
    for keyword in keywords:
        formatted = re.sub(f'\\b{keyword}\\b', keyword.upper(), formatted, flags=re.IGNORECASE)
    
    # Clean up whitespace
    formatted = re.sub(r'\n\s*\n', '\n', formatted)
    formatted = formatted.strip()
    
    return {
        "result": formatted,
        "original_length": len(sql),
        "formatted_length": len(formatted)
    }

def css_formatter(css: str) -> Dict[str, Any]:
    """Format CSS code"""
    if not css:
        return {"result": ""}
    
    # Basic CSS formatting
    formatted = css
    
    # Add line breaks after semicolons and braces
    formatted = re.sub(r';', ';\n    ', formatted)
    formatted = re.sub(r'\{', ' {\n    ', formatted)
    formatted = re.sub(r'\}', '\n}\n\n', formatted)
    
    # Clean up extra whitespace
    formatted = re.sub(r'\n\s*\n\s*\n', '\n\n', formatted)
    formatted = formatted.strip()
    
    return {
        "result": formatted,
        "original_length": len(css),
        "formatted_length": len(formatted)
    }

def js_formatter(js: str) -> Dict[str, Any]:
    """Format JavaScript code (basic implementation)"""
    if not js:
        return {"result": ""}
    
    # Basic JavaScript formatting
    formatted = js
    
    # Add line breaks after semicolons and braces
    formatted = re.sub(r';(?!\s*\n)', ';\n', formatted)
    formatted = re.sub(r'\{(?!\s*\n)', ' {\n', formatted)
    formatted = re.sub(r'\}(?!\s*\n)', '\n}\n', formatted)
    
    # Clean up whitespace
    formatted = re.sub(r'\n\s*\n\s*\n', '\n\n', formatted)
    formatted = formatted.strip()
    
    return {
        "result": formatted,
        "original_length": len(js),
        "formatted_length": len(formatted)
    }

def number_base_converter(number: str, from_base: int, to_base: int) -> Dict[str, Any]:
    """Convert numbers between different bases"""
    try:
        # Convert from source base to decimal
        decimal_value = int(number, from_base)
        
        # Convert from decimal to target base
        if to_base == 10:
            result = str(decimal_value)
        elif to_base == 2:
            result = bin(decimal_value)[2:]
        elif to_base == 8:
            result = oct(decimal_value)[2:]
        elif to_base == 16:
            result = hex(decimal_value)[2:].upper()
        else:
            # Custom base conversion
            if decimal_value == 0:
                result = "0"
            else:
                digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                result = ""
                while decimal_value > 0:
                    result = digits[decimal_value % to_base] + result
                    decimal_value //= to_base
        
        return {
            "result": result,
            "decimal_value": int(number, from_base),
            "from_base": from_base,
            "to_base": to_base,
            "success": True
        }
    
    except ValueError as e:
        return {"result": str(e), "success": False}

def roman_numeral_converter(value: str, action: str = "to_roman") -> Dict[str, Any]:
    """Convert between Roman numerals and integers"""
    try:
        if action == "to_roman":
            # Integer to Roman
            num = int(value)
            if num <= 0 or num > 3999:
                return {"result": "Number must be between 1 and 3999", "success": False}
            
            values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
            numerals = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
            
            result = ""
            for i, val in enumerate(values):
                count = num // val
                if count:
                    result += numerals[i] * count
                    num -= val * count
            
            return {"result": result, "decimal": int(value), "success": True}
        
        else:
            # Roman to Integer
            roman = value.upper()
            roman_values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
            
            result = 0
            prev_value = 0
            
            for char in reversed(roman):
                if char not in roman_values:
                    return {"result": f"Invalid Roman numeral character: {char}", "success": False}
                
                value = roman_values[char]
                if value < prev_value:
                    result -= value
                else:
                    result += value
                prev_value = value
            
            return {"result": str(result), "roman": value, "success": True}
    
    except ValueError as e:
        return {"result": str(e), "success": False}

def ascii_converter(text: str, action: str = "to_ascii") -> Dict[str, Any]:
    """Convert between text and ASCII codes"""
    try:
        if action == "to_ascii":
            # Text to ASCII codes
            ascii_codes = [str(ord(char)) for char in text]
            result = " ".join(ascii_codes)
            return {
                "result": result,
                "character_count": len(text),
                "success": True
            }
        else:
            # ASCII codes to text
            codes = text.split()
            characters = [chr(int(code)) for code in codes if code.isdigit()]
            result = "".join(characters)
            return {
                "result": result,
                "code_count": len(codes),
                "success": True
            }
    except Exception as e:
        return {"result": str(e), "success": False}

def unicode_converter(text: str, action: str = "to_unicode") -> Dict[str, Any]:
    """Convert between text and Unicode code points"""
    try:
        if action == "to_unicode":
            # Text to Unicode
            unicode_points = [f"U+{ord(char):04X}" for char in text]
            result = " ".join(unicode_points)
            return {
                "result": result,
                "character_count": len(text),
                "success": True
            }
        else:
            # Unicode to text
            # Handle both U+XXXX and plain hex formats
            codes = re.findall(r'(?:U\+)?([0-9A-Fa-f]+)', text)
            characters = [chr(int(code, 16)) for code in codes]
            result = "".join(characters)
            return {
                "result": result,
                "code_count": len(codes),
                "success": True
            }
    except Exception as e:
        return {"result": str(e), "success": False}

def morse_code_converter(text: str, action: str = "to_morse") -> Dict[str, Any]:
    """Convert between text and Morse code"""
    morse_code_dict = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
        '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
        '8': '---..', '9': '----.', ' ': '/'
    }
    
    try:
        if action == "to_morse":
            # Text to Morse code
            result = []
            for char in text.upper():
                if char in morse_code_dict:
                    result.append(morse_code_dict[char])
                elif char == ' ':
                    result.append('/')
            
            return {
                "result": " ".join(result),
                "character_count": len(text),
                "success": True
            }
        else:
            # Morse code to text
            reverse_dict = {v: k for k, v in morse_code_dict.items()}
            morse_chars = text.split()
            result = ""
            
            for morse_char in morse_chars:
                if morse_char in reverse_dict:
                    result += reverse_dict[morse_char]
                elif morse_char == '/':
                    result += ' '
            
            return {
                "result": result,
                "morse_count": len(morse_chars),
                "success": True
            }
    
    except Exception as e:
        return {"result": str(e), "success": False}

def binary_converter(text: str, action: str = "to_binary") -> Dict[str, Any]:
    """Convert between text and binary"""
    try:
        if action == "to_binary":
            # Text to binary
            binary_result = []
            for char in text:
                binary = format(ord(char), '08b')
                binary_result.append(binary)
            
            result = " ".join(binary_result)
            return {
                "result": result,
                "character_count": len(text),
                "success": True
            }
        else:
            # Binary to text
            binary_chars = text.split()
            result = ""
            
            for binary_char in binary_chars:
                if re.match(r'^[01]+$', binary_char):
                    decimal = int(binary_char, 2)
                    if 0 <= decimal <= 1114111:  # Valid Unicode range
                        result += chr(decimal)
            
            return {
                "result": result,
                "binary_count": len(binary_chars),
                "success": True
            }
    
    except Exception as e:
        return {"result": str(e), "success": False}