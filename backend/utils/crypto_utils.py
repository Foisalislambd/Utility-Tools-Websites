"""Cryptography utility functions"""
import hashlib
import base64
import json
from typing import Dict, Any
from jose import jwt, JWTError

def create_hash(text: str, algorithm: str = "md5") -> Dict[str, Any]:
    """Create hash of text"""
    try:
        algorithms = {
            "md5": hashlib.md5,
            "sha1": hashlib.sha1,
            "sha224": hashlib.sha224,
            "sha256": hashlib.sha256,
            "sha384": hashlib.sha384,
            "sha512": hashlib.sha512
        }
        
        if algorithm not in algorithms:
            return {"result": "Unsupported algorithm", "success": False}
        
        hash_obj = algorithms[algorithm]()
        hash_obj.update(text.encode())
        result = hash_obj.hexdigest()
        
        return {
            "hash": result,
            "algorithm": algorithm.upper(),
            "input_length": len(text),
            "hash_length": len(result),
            "success": True
        }
    except Exception as e:
        return {"result": str(e), "success": False}

def decode_jwt(token: str) -> Dict[str, Any]:
    """Decode JWT token without verification"""
    try:
        # Decode header
        header = jwt.get_unverified_header(token)
        
        # Decode payload
        payload = jwt.get_unverified_claims(token)
        
        return {
            "header": header,
            "payload": payload,
            "success": True,
            "algorithm": header.get("alg", "Unknown"),
            "type": header.get("typ", "Unknown")
        }
    except JWTError as e:
        return {"result": f"Invalid JWT: {str(e)}", "success": False}
    except Exception as e:
        return {"result": str(e), "success": False}

def encrypt_decrypt_text(text: str, key: str, operation: str, algorithm: str = "aes") -> Dict[str, Any]:
    """Encrypt or decrypt text (simple implementation)"""
    try:
        from cryptography.fernet import Fernet
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        import os
        
        # Generate key from password
        salt = b'salt_1234567890'  # In production, use random salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key_bytes = base64.urlsafe_b64encode(kdf.derive(key.encode()))
        f = Fernet(key_bytes)
        
        if operation == "encrypt":
            encrypted = f.encrypt(text.encode())
            result = base64.b64encode(encrypted).decode()
        else:  # decrypt
            try:
                encrypted_data = base64.b64decode(text)
                decrypted = f.decrypt(encrypted_data)
                result = decrypted.decode()
            except Exception:
                return {"result": "Invalid encrypted text or wrong key", "success": False}
        
        return {
            "result": result,
            "operation": operation,
            "algorithm": algorithm.upper(),
            "success": True
        }
    except Exception as e:
        return {"result": str(e), "success": False}

def generate_rsa_keys() -> Dict[str, Any]:
    """Generate RSA key pair"""
    try:
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
        
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        # Get public key
        public_key = private_key.public_key()
        
        # Serialize private key
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()
        
        # Serialize public key
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()
        
        return {
            "private_key": private_pem,
            "public_key": public_pem,
            "key_size": 2048,
            "success": True
        }
    except Exception as e:
        return {"result": str(e), "success": False}

def analyze_certificate(cert_text: str) -> Dict[str, Any]:
    """Analyze SSL certificate"""
    try:
        from cryptography import x509
        from cryptography.hazmat.primitives import serialization
        
        # Try to load certificate
        try:
            cert = x509.load_pem_x509_certificate(cert_text.encode())
        except:
            cert = x509.load_der_x509_certificate(base64.b64decode(cert_text))
        
        # Extract information
        subject = cert.subject.rfc4514_string()
        issuer = cert.issuer.rfc4514_string()
        not_before = cert.not_valid_before
        not_after = cert.not_valid_after
        serial_number = str(cert.serial_number)
        
        # Get public key info
        public_key = cert.public_key()
        key_size = public_key.key_size if hasattr(public_key, 'key_size') else None
        
        return {
            "subject": subject,
            "issuer": issuer,
            "valid_from": not_before.isoformat(),
            "valid_until": not_after.isoformat(),
            "serial_number": serial_number,
            "key_size": key_size,
            "algorithm": cert.signature_algorithm_oid._name,
            "success": True
        }
    except Exception as e:
        return {"result": str(e), "success": False}

def calculate_checksum(text: str, algorithm: str = "crc32") -> Dict[str, Any]:
    """Calculate various checksums"""
    try:
        import zlib
        
        if algorithm == "crc32":
            result = hex(zlib.crc32(text.encode()) & 0xffffffff)
        elif algorithm == "adler32":
            result = hex(zlib.adler32(text.encode()) & 0xffffffff)
        else:
            # Use hashlib for other algorithms
            hash_obj = getattr(hashlib, algorithm)()
            hash_obj.update(text.encode())
            result = hash_obj.hexdigest()
        
        return {
            "checksum": result,
            "algorithm": algorithm.upper(),
            "input_length": len(text),
            "success": True
        }
    except Exception as e:
        return {"result": str(e), "success": False}