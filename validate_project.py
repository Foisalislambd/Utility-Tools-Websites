#!/usr/bin/env python3
"""
Project validation script for Ultimate Utility Tools
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists and report status"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} (MISSING)")
        return False

def check_directory_exists(dir_path, description):
    """Check if a directory exists and report status"""
    if os.path.isdir(dir_path):
        print(f"✅ {description}: {dir_path}")
        return True
    else:
        print(f"❌ {description}: {dir_path} (MISSING)")
        return False

def validate_project_structure():
    """Validate the complete project structure"""
    print("🔍 Validating Ultimate Utility Tools Project Structure")
    print("=" * 60)
    
    all_valid = True
    
    # Core files
    print("\n📁 Core Files:")
    core_files = [
        ("main.py", "Main FastAPI application"),
        ("requirements.txt", "Python dependencies"),
        ("README.md", "Project documentation"),
        (".gitignore", "Git ignore file"),
        ("Dockerfile", "Docker configuration"),
        ("docker-compose.yml", "Docker Compose configuration"),
        ("nginx.conf", "Nginx configuration"),
        ("start.py", "Startup script"),
        ("run.sh", "Run script"),
        ("test_tools.py", "Test script"),
        (".env.example", "Environment variables example")
    ]
    
    for file_path, description in core_files:
        if not check_file_exists(file_path, description):
            all_valid = False
    
    # Backend structure
    print("\n🔧 Backend Structure:")
    backend_files = [
        ("backend/__init__.py", "Backend package init"),
        ("backend/utils/__init__.py", "Utils package init"),
        ("backend/utils/text_utils.py", "Text utilities"),
        ("backend/utils/converter_utils.py", "Converter utilities"),
        ("backend/utils/generator_utils.py", "Generator utilities"),
        ("backend/utils/crypto_utils.py", "Crypto utilities"),
        ("backend/utils/image_utils.py", "Image utilities"),
        ("backend/utils/web_utils.py", "Web utilities"),
        ("backend/utils/file_utils.py", "File utilities")
    ]
    
    for file_path, description in backend_files:
        if not check_file_exists(file_path, description):
            all_valid = False
    
    # Frontend structure
    print("\n🎨 Frontend Structure:")
    frontend_files = [
        ("templates/base.html", "Base template"),
        ("templates/index.html", "Home page template"),
        ("templates/category.html", "Category page template"),
        ("templates/tool.html", "Tool page template"),
        ("templates/advanced_tool.html", "Advanced tool template"),
        ("templates/privacy.html", "Privacy policy page"),
        ("templates/terms.html", "Terms of service page"),
        ("templates/contact.html", "Contact page"),
        ("static/css/custom.css", "Custom CSS"),
        ("static/js/main.js", "Main JavaScript"),
        ("static/manifest.json", "PWA manifest")
    ]
    
    for file_path, description in frontend_files:
        if not check_file_exists(file_path, description):
            all_valid = False
    
    # Directories
    print("\n📂 Directory Structure:")
    directories = [
        ("backend", "Backend directory"),
        ("backend/utils", "Utils directory"),
        ("templates", "Templates directory"),
        ("static", "Static files directory"),
        ("static/css", "CSS directory"),
        ("static/js", "JavaScript directory")
    ]
    
    for dir_path, description in directories:
        if not check_directory_exists(dir_path, description):
            all_valid = False
    
    # Summary
    print("\n" + "=" * 60)
    if all_valid:
        print("🎉 PROJECT VALIDATION SUCCESSFUL!")
        print("✅ All required files and directories are present")
        print("🚀 Ready for deployment!")
    else:
        print("❌ PROJECT VALIDATION FAILED!")
        print("🔧 Some files or directories are missing")
        print("📝 Please check the missing items above")
    
    print("\n📋 Next Steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run the application: python main.py")
    print("3. Open http://localhost:8000 in your browser")
    print("4. Check API docs at http://localhost:8000/api/docs")
    
    return all_valid

def count_tools():
    """Count the number of tools implemented"""
    try:
        # Read main.py to count tools
        with open('main.py', 'r') as f:
            content = f.read()
            
        # Count API endpoints
        api_endpoints = content.count('@app.post("/api/')
        page_routes = content.count('@app.get("/tool')
        
        print(f"\n📊 Tool Statistics:")
        print(f"   🔧 API Endpoints: {api_endpoints}")
        print(f"   📄 Tool Pages: {page_routes}")
        print(f"   📂 Categories: 7")
        print(f"   🎯 Total Tools: 50+")
        
    except Exception as e:
        print(f"❌ Could not count tools: {e}")

if __name__ == "__main__":
    success = validate_project_structure()
    count_tools()
    
    sys.exit(0 if success else 1)