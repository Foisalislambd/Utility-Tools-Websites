"""Generator utility functions"""
import random
import string
import uuid
import qrcode
import io
import base64
from typing import Dict, Any

def generate_password(length: int = 12, include_symbols: bool = True) -> Dict[str, Any]:
    """Generate a secure password"""
    characters = string.ascii_letters + string.digits
    if include_symbols:
        characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    password = ''.join(random.choice(characters) for _ in range(length))
    
    # Calculate strength
    strength_score = 0
    if any(c.islower() for c in password):
        strength_score += 1
    if any(c.isupper() for c in password):
        strength_score += 1
    if any(c.isdigit() for c in password):
        strength_score += 1
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        strength_score += 1
    if length >= 12:
        strength_score += 1
    
    strength_levels = ["Very Weak", "Weak", "Fair", "Good", "Strong"]
    strength = strength_levels[min(strength_score - 1, 4)] if strength_score > 0 else "Very Weak"
    
    return {
        "password": password,
        "length": length,
        "strength": strength,
        "score": strength_score
    }

def generate_uuid(version: int = 4) -> Dict[str, str]:
    """Generate UUID"""
    if version == 1:
        result = str(uuid.uuid1())
    elif version == 4:
        result = str(uuid.uuid4())
    else:
        result = str(uuid.uuid4())  # Default to v4
    
    return {
        "uuid": result,
        "version": version,
        "uppercase": result.upper(),
        "no_hyphens": result.replace('-', '')
    }

def generate_qr_code(text: str) -> Dict[str, Any]:
    """Generate QR code"""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        
        return {
            "qr_code": f"data:image/png;base64,{img_str}",
            "text": text,
            "success": True
        }
    except Exception as e:
        return {"result": str(e), "success": False}

def generate_lorem_ipsum(paragraphs: int = 3, words_per_paragraph: int = 50) -> Dict[str, str]:
    """Generate Lorem Ipsum text"""
    lorem_words = [
        "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit",
        "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore",
        "magna", "aliqua", "enim", "ad", "minim", "veniam", "quis", "nostrud",
        "exercitation", "ullamco", "laboris", "nisi", "aliquip", "ex", "ea", "commodo",
        "consequat", "duis", "aute", "irure", "in", "reprehenderit", "voluptate",
        "velit", "esse", "cillum", "fugiat", "nulla", "pariatur", "excepteur", "sint",
        "occaecat", "cupidatat", "non", "proident", "sunt", "culpa", "qui", "officia",
        "deserunt", "mollit", "anim", "id", "est", "laborum"
    ]
    
    result_paragraphs = []
    for _ in range(paragraphs):
        paragraph_words = []
        for _ in range(words_per_paragraph):
            paragraph_words.append(random.choice(lorem_words))
        
        paragraph = ' '.join(paragraph_words)
        paragraph = paragraph[0].upper() + paragraph[1:] + '.'
        result_paragraphs.append(paragraph)
    
    return {
        "result": '\n\n'.join(result_paragraphs),
        "paragraphs": paragraphs,
        "words_per_paragraph": words_per_paragraph,
        "total_words": paragraphs * words_per_paragraph
    }

def generate_fake_data(data_type: str, count: int = 1) -> Dict[str, Any]:
    """Generate fake data"""
    import random
    from datetime import datetime, timedelta
    
    first_names = ["John", "Jane", "Mike", "Sarah", "David", "Emily", "Chris", "Lisa", "Tom", "Anna"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "example.com"]
    
    def generate_email():
        first = random.choice(first_names).lower()
        last = random.choice(last_names).lower()
        domain = random.choice(domains)
        return f"{first}.{last}@{domain}"
    
    def generate_phone():
        return f"+1-{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
    
    def generate_address():
        street_num = random.randint(1, 9999)
        streets = ["Main St", "Oak Ave", "Pine Rd", "Elm Dr", "Cedar Ln"]
        cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
        return f"{street_num} {random.choice(streets)}, {random.choice(cities)}"
    
    def generate_date():
        start = datetime.now() - timedelta(days=365*5)
        end = datetime.now()
        random_date = start + timedelta(days=random.randint(0, (end-start).days))
        return random_date.strftime("%Y-%m-%d")
    
    generators = {
        "name": lambda: f"{random.choice(first_names)} {random.choice(last_names)}",
        "email": generate_email,
        "phone": generate_phone,
        "address": generate_address,
        "date": generate_date,
        "number": lambda: random.randint(1, 1000),
        "text": lambda: ' '.join(random.choices(["lorem", "ipsum", "dolor", "sit", "amet"], k=5))
    }
    
    try:
        results = []
        for _ in range(count):
            results.append(generators[data_type]())
        
        return {
            "results": results,
            "count": count,
            "type": data_type,
            "success": True
        }
    except Exception as e:
        return {"result": str(e), "success": False}

def generate_hash(text: str, algorithm: str = "md5") -> Dict[str, Any]:
    """Generate hash of text"""
    import hashlib
    
    try:
        algorithms = {
            "md5": hashlib.md5,
            "sha1": hashlib.sha1,
            "sha256": hashlib.sha256,
            "sha512": hashlib.sha512
        }
        
        if algorithm not in algorithms:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
        
        hash_obj = algorithms[algorithm]()
        hash_obj.update(text.encode())
        result = hash_obj.hexdigest()
        
        return {
            "hash": result,
            "algorithm": algorithm,
            "input_length": len(text),
            "success": True
        }
    except Exception as e:
        return {"result": str(e), "success": False}

def generate_random_number(min_val: int = 1, max_val: int = 100, count: int = 1) -> Dict[str, Any]:
    """Generate random numbers"""
    try:
        numbers = [random.randint(min_val, max_val) for _ in range(count)]
        return {
            "numbers": numbers,
            "min": min_val,
            "max": max_val,
            "count": count,
            "sum": sum(numbers),
            "average": round(sum(numbers) / len(numbers), 2)
        }
    except Exception as e:
        return {"result": str(e), "success": False}

def generate_color_palette(count: int = 5) -> Dict[str, Any]:
    """Generate random color palette"""
    try:
        colors = []
        for _ in range(count):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            rgb_color = f"rgb({r}, {g}, {b})"
            colors.append({
                "hex": hex_color,
                "rgb": rgb_color,
                "r": r, "g": g, "b": b
            })
        
        return {
            "colors": colors,
            "count": count,
            "success": True
        }
    except Exception as e:
        return {"result": str(e), "success": False}