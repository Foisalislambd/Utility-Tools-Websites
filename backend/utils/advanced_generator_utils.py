"""Advanced generator utility functions"""
import random
import string
import secrets
from typing import Dict, Any, List
from datetime import datetime, timedelta
import json

def credit_card_generator(card_type: str = "visa") -> Dict[str, Any]:
    """Generate fake credit card numbers for testing (NOT REAL)"""
    
    # Card type prefixes and lengths
    card_types = {
        "visa": {"prefixes": ["4"], "length": 16},
        "mastercard": {"prefixes": ["51", "52", "53", "54", "55"], "length": 16},
        "amex": {"prefixes": ["34", "37"], "length": 15},
        "discover": {"prefixes": ["6011"], "length": 16}
    }
    
    if card_type not in card_types:
        card_type = "visa"
    
    card_info = card_types[card_type]
    prefix = random.choice(card_info["prefixes"])
    length = card_info["length"]
    
    # Generate the rest of the number
    remaining_length = length - len(prefix) - 1  # -1 for check digit
    number = prefix + ''.join([str(random.randint(0, 9)) for _ in range(remaining_length)])
    
    # Calculate Luhn check digit
    def luhn_check_digit(number):
        digits = [int(d) for d in number]
        for i in range(len(digits) - 1, -1, -2):
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9
        return str((10 - sum(digits) % 10) % 10)
    
    check_digit = luhn_check_digit(number)
    full_number = number + check_digit
    
    # Format with spaces
    formatted = ' '.join([full_number[i:i+4] for i in range(0, len(full_number), 4)])
    
    # Generate expiry date (future date)
    exp_month = random.randint(1, 12)
    exp_year = random.randint(2025, 2030)
    
    # Generate CVV
    cvv_length = 4 if card_type == "amex" else 3
    cvv = ''.join([str(random.randint(0, 9)) for _ in range(cvv_length)])
    
    return {
        "number": full_number,
        "formatted": formatted,
        "type": card_type.title(),
        "expiry_month": f"{exp_month:02d}",
        "expiry_year": str(exp_year),
        "cvv": cvv,
        "disclaimer": "FOR TESTING PURPOSES ONLY - NOT A REAL CREDIT CARD"
    }

def name_generator(gender: str = "random", origin: str = "english") -> Dict[str, str]:
    """Generate random names"""
    
    names_db = {
        "english": {
            "male_first": ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Christopher"],
            "female_first": ["Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen"],
            "last": ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
        },
        "spanish": {
            "male_first": ["José", "Luis", "Carlos", "Juan", "Antonio", "Pedro", "Francisco", "Alejandro", "Diego", "Miguel"],
            "female_first": ["María", "Ana", "Carmen", "Isabel", "Pilar", "Rosa", "Teresa", "Laura", "Patricia", "Cristina"],
            "last": ["García", "Rodríguez", "González", "Fernández", "López", "Martínez", "Sánchez", "Pérez", "Gómez", "Martín"]
        }
    }
    
    if origin not in names_db:
        origin = "english"
    
    if gender == "random":
        gender = random.choice(["male", "female"])
    
    first_names = names_db[origin][f"{gender}_first"]
    last_names = names_db[origin]["last"]
    
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    
    return {
        "first_name": first_name,
        "last_name": last_name,
        "full_name": f"{first_name} {last_name}",
        "gender": gender,
        "origin": origin
    }

def email_generator(domain: str = None, username: str = None) -> Dict[str, str]:
    """Generate random email addresses"""
    
    domains = [
        "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "example.com",
        "test.com", "demo.com", "sample.org", "placeholder.net", "fake.io"
    ]
    
    if not domain:
        domain = random.choice(domains)
    
    if not username:
        # Generate username
        adjectives = ["cool", "smart", "happy", "lucky", "super", "mega", "ultra", "pro"]
        nouns = ["user", "person", "player", "coder", "ninja", "master", "expert", "guru"]
        
        username = random.choice(adjectives) + random.choice(nouns) + str(random.randint(100, 9999))
    
    email = f"{username}@{domain}"
    
    return {
        "email": email,
        "username": username,
        "domain": domain
    }

def username_generator(style: str = "random") -> Dict[str, Any]:
    """Generate usernames in different styles"""
    
    styles = {
        "adjective_noun": {
            "adjectives": ["cool", "smart", "happy", "lucky", "super", "mega", "ultra", "pro", "epic", "awesome"],
            "nouns": ["user", "person", "player", "coder", "ninja", "master", "expert", "guru", "wizard", "hero"]
        },
        "animal": {
            "adjectives": ["swift", "clever", "mighty", "brave", "silent", "golden", "silver", "fierce"],
            "animals": ["tiger", "eagle", "wolf", "lion", "fox", "bear", "shark", "falcon", "panther", "dragon"]
        },
        "tech": {
            "prefixes": ["cyber", "digital", "quantum", "neural", "binary", "crypto", "matrix", "pixel"],
            "suffixes": ["dev", "code", "tech", "byte", "bit", "net", "sys", "core", "hub", "lab"]
        }
    }
    
    if style not in styles:
        style = random.choice(list(styles.keys()))
    
    if style in ["adjective_noun", "animal"]:
        adj = random.choice(styles[style]["adjectives" if style == "adjective_noun" else "adjectives"])
        noun = random.choice(styles[style]["nouns" if style == "adjective_noun" else "animals"])
        username = f"{adj}{noun}{random.randint(10, 999)}"
    else:  # tech
        prefix = random.choice(styles[style]["prefixes"])
        suffix = random.choice(styles[style]["suffixes"])
        username = f"{prefix}{suffix}{random.randint(10, 999)}"
    
    # Generate variations
    variations = [
        username,
        username.lower(),
        username.upper(),
        f"{username}_{random.randint(10, 99)}",
        f"_{username}_",
        f"{username}.{random.randint(10, 99)}"
    ]
    
    return {
        "username": username,
        "style": style,
        "variations": variations
    }

def api_key_generator(length: int = 32, format_type: str = "hex") -> Dict[str, str]:
    """Generate API keys in different formats"""
    
    if format_type == "hex":
        key = secrets.token_hex(length // 2)
    elif format_type == "base64":
        key = secrets.token_urlsafe(length)
    elif format_type == "uuid":
        import uuid
        key = str(uuid.uuid4())
    else:  # alphanumeric
        key = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))
    
    return {
        "api_key": key,
        "format": format_type,
        "length": len(key),
        "entropy_bits": len(key) * 4 if format_type == "hex" else len(key) * 6
    }

def random_ip(version: int = 4) -> Dict[str, str]:
    """Generate random IP addresses"""
    
    if version == 4:
        # IPv4
        octets = [str(random.randint(1, 254)) for _ in range(4)]
        ip = ".".join(octets)
        return {
            "ip": ip,
            "version": "IPv4",
            "type": "public" if not ip.startswith(("10.", "192.168.", "172.")) else "private"
        }
    else:
        # IPv6
        groups = [f"{random.randint(0, 65535):04x}" for _ in range(8)]
        ip = ":".join(groups)
        return {
            "ip": ip,
            "version": "IPv6",
            "compressed": ip  # Could implement compression logic
        }

def random_mac() -> Dict[str, str]:
    """Generate random MAC address"""
    
    # Generate 6 random bytes
    mac_bytes = [random.randint(0, 255) for _ in range(6)]
    
    # Format in different styles
    colon_format = ":".join(f"{b:02x}" for b in mac_bytes)
    dash_format = "-".join(f"{b:02x}" for b in mac_bytes)
    dot_format = ".".join(f"{mac_bytes[i]:02x}{mac_bytes[i+1]:02x}" for i in range(0, 6, 2))
    
    return {
        "mac": colon_format,
        "colon_format": colon_format,
        "dash_format": dash_format,
        "dot_format": dot_format,
        "vendor": "Unknown (Random)"
    }

def random_user_agent() -> Dict[str, str]:
    """Generate random user agent strings"""
    
    browsers = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ]
    
    user_agent = random.choice(browsers)
    
    # Parse user agent
    if "Chrome" in user_agent:
        browser = "Chrome"
    elif "Firefox" in user_agent:
        browser = "Firefox"
    elif "Safari" in user_agent and "Chrome" not in user_agent:
        browser = "Safari"
    else:
        browser = "Unknown"
    
    if "Windows" in user_agent:
        os = "Windows"
    elif "Macintosh" in user_agent:
        os = "macOS"
    elif "Linux" in user_agent:
        os = "Linux"
    else:
        os = "Unknown"
    
    return {
        "user_agent": user_agent,
        "browser": browser,
        "operating_system": os
    }

def placeholder_image(width: int = 300, height: int = 200, format: str = "png") -> Dict[str, str]:
    """Generate placeholder image URL"""
    
    services = [
        f"https://via.placeholder.com/{width}x{height}.{format}",
        f"https://picsum.photos/{width}/{height}",
        f"https://dummyimage.com/{width}x{height}/{random.choice(['ff0000', '00ff00', '0000ff', 'ffff00', 'ff00ff', '00ffff'])}/ffffff.{format}"
    ]
    
    url = random.choice(services)
    
    return {
        "url": url,
        "width": width,
        "height": height,
        "format": format,
        "aspect_ratio": f"{width}:{height}"
    }

def gradient_generator(colors: int = 2) -> Dict[str, Any]:
    """Generate CSS gradient"""
    
    # Generate random colors
    color_list = []
    for _ in range(colors):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color_list.append(f"#{r:02x}{g:02x}{b:02x}")
    
    # Generate gradient direction
    directions = ["to right", "to left", "to bottom", "to top", "45deg", "90deg", "135deg", "180deg"]
    direction = random.choice(directions)
    
    # Create CSS gradient
    gradient = f"linear-gradient({direction}, {', '.join(color_list)})"
    
    return {
        "css": gradient,
        "colors": color_list,
        "direction": direction,
        "color_count": len(color_list)
    }

def random_quote() -> Dict[str, str]:
    """Generate random inspirational quotes"""
    
    quotes = [
        {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
        {"text": "Innovation distinguishes between a leader and a follower.", "author": "Steve Jobs"},
        {"text": "Life is what happens to you while you're busy making other plans.", "author": "John Lennon"},
        {"text": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt"},
        {"text": "It is during our darkest moments that we must focus to see the light.", "author": "Aristotle"},
        {"text": "Success is not final, failure is not fatal: it is the courage to continue that counts.", "author": "Winston Churchill"},
        {"text": "The way to get started is to quit talking and begin doing.", "author": "Walt Disney"},
        {"text": "Don't let yesterday take up too much of today.", "author": "Will Rogers"},
        {"text": "You learn more from failure than from success.", "author": "Unknown"},
        {"text": "It's not whether you get knocked down, it's whether you get up.", "author": "Vince Lombardi"}
    ]
    
    quote = random.choice(quotes)
    
    return {
        "quote": quote["text"],
        "author": quote["author"],
        "length": len(quote["text"]),
        "word_count": len(quote["text"].split())
    }