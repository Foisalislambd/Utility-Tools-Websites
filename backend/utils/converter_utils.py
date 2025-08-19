"""Converter utility functions"""
import json
import base64
import urllib.parse
import xml.etree.ElementTree as ET
import markdown
from typing import Dict, Any

def base64_convert(text: str, action: str) -> Dict[str, Any]:
    """Convert to/from base64"""
    try:
        if action == "encode":
            result = base64.b64encode(text.encode()).decode()
        else:  # decode
            result = base64.b64decode(text).decode()
        return {"result": result, "success": True}
    except Exception as e:
        return {"result": str(e), "success": False}

def url_convert(text: str, action: str) -> Dict[str, Any]:
    """URL encode/decode"""
    try:
        if action == "encode":
            result = urllib.parse.quote(text)
        else:  # decode
            result = urllib.parse.unquote(text)
        return {"result": result, "success": True}
    except Exception as e:
        return {"result": str(e), "success": False}

def format_json(text: str) -> Dict[str, Any]:
    """Format and validate JSON"""
    try:
        parsed = json.loads(text)
        formatted = json.dumps(parsed, indent=2, sort_keys=True)
        return {
            "result": formatted,
            "success": True,
            "valid": True,
            "size": len(text),
            "formatted_size": len(formatted)
        }
    except json.JSONDecodeError as e:
        return {
            "result": str(e),
            "success": False,
            "valid": False
        }

def csv_to_json(csv_text: str) -> Dict[str, Any]:
    """Convert CSV to JSON"""
    try:
        import csv
        import io
        
        reader = csv.DictReader(io.StringIO(csv_text))
        result = [row for row in reader]
        return {
            "result": json.dumps(result, indent=2),
            "success": True,
            "rows": len(result)
        }
    except Exception as e:
        return {"result": str(e), "success": False}

def xml_to_json(xml_text: str) -> Dict[str, Any]:
    """Convert XML to JSON"""
    try:
        def xml_to_dict(element):
            result = {}
            for child in element:
                if len(child) == 0:
                    result[child.tag] = child.text
                else:
                    result[child.tag] = xml_to_dict(child)
            return result
        
        root = ET.fromstring(xml_text)
        result = {root.tag: xml_to_dict(root)}
        return {
            "result": json.dumps(result, indent=2),
            "success": True
        }
    except Exception as e:
        return {"result": str(e), "success": False}

def markdown_to_html(md_text: str) -> Dict[str, Any]:
    """Convert Markdown to HTML"""
    try:
        html = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])
        return {
            "result": html,
            "success": True,
            "word_count": len(md_text.split())
        }
    except Exception as e:
        return {"result": str(e), "success": False}

def convert_units(value: float, from_unit: str, to_unit: str, unit_type: str) -> Dict[str, Any]:
    """Convert between different units"""
    try:
        # Length conversions (to meters)
        length_units = {
            "mm": 0.001, "cm": 0.01, "m": 1, "km": 1000,
            "in": 0.0254, "ft": 0.3048, "yd": 0.9144, "mi": 1609.34
        }
        
        # Weight conversions (to grams)
        weight_units = {
            "mg": 0.001, "g": 1, "kg": 1000, "t": 1000000,
            "oz": 28.3495, "lb": 453.592, "st": 6350.29
        }
        
        # Temperature conversions
        def convert_temperature(value, from_unit, to_unit):
            if from_unit == to_unit:
                return value
            
            # Convert to Celsius first
            if from_unit == "f":
                celsius = (value - 32) * 5/9
            elif from_unit == "k":
                celsius = value - 273.15
            else:  # celsius
                celsius = value
            
            # Convert from Celsius to target
            if to_unit == "f":
                return celsius * 9/5 + 32
            elif to_unit == "k":
                return celsius + 273.15
            else:  # celsius
                return celsius
        
        if unit_type == "length":
            result = value * length_units[from_unit] / length_units[to_unit]
        elif unit_type == "weight":
            result = value * weight_units[from_unit] / weight_units[to_unit]
        elif unit_type == "temperature":
            result = convert_temperature(value, from_unit, to_unit)
        else:
            raise ValueError("Unsupported unit type")
        
        return {
            "result": round(result, 6),
            "success": True,
            "conversion": f"{value} {from_unit} = {round(result, 6)} {to_unit}"
        }
    except Exception as e:
        return {"result": str(e), "success": False}

def convert_color(color: str, from_format: str, to_format: str) -> Dict[str, Any]:
    """Convert between color formats"""
    try:
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        def rgb_to_hex(r, g, b):
            return f"#{r:02x}{g:02x}{b:02x}"
        
        def rgb_to_hsl(r, g, b):
            r, g, b = r/255.0, g/255.0, b/255.0
            max_val = max(r, g, b)
            min_val = min(r, g, b)
            diff = max_val - min_val
            
            # Lightness
            l = (max_val + min_val) / 2
            
            if diff == 0:
                h = s = 0
            else:
                # Saturation
                s = diff / (2 - max_val - min_val) if l > 0.5 else diff / (max_val + min_val)
                
                # Hue
                if max_val == r:
                    h = (60 * ((g - b) / diff) + 360) % 360
                elif max_val == g:
                    h = (60 * ((b - r) / diff) + 120) % 360
                else:
                    h = (60 * ((r - g) / diff) + 240) % 360
            
            return (round(h), round(s * 100), round(l * 100))
        
        # Parse input color
        if from_format == "hex":
            r, g, b = hex_to_rgb(color)
        elif from_format == "rgb":
            r, g, b = map(int, color.replace('rgb(', '').replace(')', '').split(','))
        
        # Convert to target format
        if to_format == "hex":
            result = rgb_to_hex(r, g, b)
        elif to_format == "rgb":
            result = f"rgb({r}, {g}, {b})"
        elif to_format == "hsl":
            h, s, l = rgb_to_hsl(r, g, b)
            result = f"hsl({h}, {s}%, {l}%)"
        
        return {"result": result, "success": True}
    except Exception as e:
        return {"result": str(e), "success": False}

def convert_timestamp(timestamp: str, from_format: str, to_format: str) -> Dict[str, Any]:
    """Convert between timestamp formats"""
    try:
        from datetime import datetime
        import time
        
        if from_format == "unix":
            dt = datetime.fromtimestamp(float(timestamp))
        elif from_format == "iso":
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        else:
            dt = datetime.strptime(timestamp, from_format)
        
        if to_format == "unix":
            result = str(int(dt.timestamp()))
        elif to_format == "iso":
            result = dt.isoformat()
        else:
            result = dt.strftime(to_format)
        
        return {
            "result": result,
            "success": True,
            "readable": dt.strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        return {"result": str(e), "success": False}