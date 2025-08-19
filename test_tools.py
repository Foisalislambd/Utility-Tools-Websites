#!/usr/bin/env python3
"""
Test script for Ultimate Utility Tools
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"

def test_endpoint(endpoint, data=None, files=None, method="POST"):
    """Test an API endpoint"""
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}")
        else:
            response = requests.post(f"{BASE_URL}{endpoint}", data=data, files=files)
        
        return {
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "response": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def run_tests():
    """Run comprehensive tests"""
    print("🧪 Testing Ultimate Utility Tools API")
    print("=" * 50)
    
    # Test health check
    print("🏥 Testing health check...")
    result = test_endpoint("/health", method="GET")
    print(f"   {'✅' if result['success'] else '❌'} Health check: {result.get('response', result.get('error'))}")
    
    # Test text tools
    print("\n📝 Testing text tools...")
    
    # Word count
    result = test_endpoint("/api/text/word-count", {"text": "Hello world! This is a test."})
    print(f"   {'✅' if result['success'] else '❌'} Word count: {result.get('response', result.get('error'))}")
    
    # Case conversion
    result = test_endpoint("/api/text/case-convert", {"text": "Hello World", "case_type": "upper"})
    print(f"   {'✅' if result['success'] else '❌'} Case convert: {result.get('response', result.get('error'))}")
    
    # Test converters
    print("\n🔄 Testing converters...")
    
    # Base64
    result = test_endpoint("/api/convert/base64", {"text": "Hello World", "action": "encode"})
    print(f"   {'✅' if result['success'] else '❌'} Base64 encode: {result.get('response', result.get('error'))}")
    
    # JSON format
    result = test_endpoint("/api/convert/json", {"text": '{"name": "test", "value": 123}'})
    print(f"   {'✅' if result['success'] else '❌'} JSON format: {result.get('response', result.get('error'))}")
    
    # Test generators
    print("\n⚡ Testing generators...")
    
    # Password
    result = test_endpoint("/api/generate/password", {"length": "12", "include_symbols": "true"})
    print(f"   {'✅' if result['success'] else '❌'} Password generator: {result.get('response', result.get('error'))}")
    
    # UUID
    result = test_endpoint("/api/generate/uuid", {"version": "4"})
    print(f"   {'✅' if result['success'] else '❌'} UUID generator: {result.get('response', result.get('error'))}")
    
    # QR Code
    result = test_endpoint("/api/generate/qr", {"text": "https://example.com"})
    print(f"   {'✅' if result['success'] else '❌'} QR generator: {result.get('response', result.get('error'))}")
    
    # Test crypto tools
    print("\n🔒 Testing crypto tools...")
    
    # Hash
    result = test_endpoint("/api/crypto/hash", {"text": "Hello World", "algorithm": "md5"})
    print(f"   {'✅' if result['success'] else '❌'} Hash generator: {result.get('response', result.get('error'))}")
    
    # Test web pages
    print("\n🌐 Testing web pages...")
    
    pages = ["/", "/tools/text", "/tools/converters", "/tool/password_generator", "/privacy", "/terms", "/contact"]
    for page in pages:
        result = test_endpoint(page, method="GET")
        print(f"   {'✅' if result['success'] else '❌'} Page {page}: {'OK' if result['success'] else result.get('error')}")
    
    # Test SEO endpoints
    print("\n🔍 Testing SEO endpoints...")
    
    result = test_endpoint("/robots.txt", method="GET")
    print(f"   {'✅' if result['success'] else '❌'} Robots.txt: {'OK' if result['success'] else result.get('error')}")
    
    result = test_endpoint("/sitemap.xml", method="GET")
    print(f"   {'✅' if result['success'] else '❌'} Sitemap.xml: {'OK' if result['success'] else result.get('error')}")
    
    print("\n🎉 Testing completed!")

def wait_for_server():
    """Wait for server to be ready"""
    print("⏳ Waiting for server to start...")
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=2)
            if response.status_code == 200:
                print("✅ Server is ready!")
                return True
        except:
            pass
        
        time.sleep(1)
        print(f"   Attempt {attempt + 1}/{max_attempts}")
    
    print("❌ Server failed to start")
    return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--wait":
        if wait_for_server():
            run_tests()
    else:
        run_tests()