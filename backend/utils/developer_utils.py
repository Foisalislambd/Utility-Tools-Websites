"""Developer utility functions"""
import re
import json
import random
from typing import Dict, Any, List

def code_formatter(code: str, language: str = "javascript") -> Dict[str, Any]:
    """Format code with basic indentation"""
    if not code:
        return {"result": ""}
    
    # Basic formatting for different languages
    if language.lower() in ["javascript", "js"]:
        return format_javascript(code)
    elif language.lower() in ["python", "py"]:
        return format_python(code)
    elif language.lower() in ["css"]:
        return format_css(code)
    elif language.lower() in ["html"]:
        return format_html(code)
    else:
        return {"result": code, "message": "Language not supported for formatting"}

def format_javascript(code: str) -> Dict[str, str]:
    """Basic JavaScript formatting"""
    formatted = code
    
    # Add line breaks after semicolons and braces
    formatted = re.sub(r';(?!\s*\n)', ';\n', formatted)
    formatted = re.sub(r'\{(?!\s*\n)', ' {\n', formatted)
    formatted = re.sub(r'\}(?!\s*\n)', '\n}\n', formatted)
    
    # Basic indentation
    lines = formatted.split('\n')
    indented_lines = []
    indent_level = 0
    
    for line in lines:
        stripped = line.strip()
        if stripped:
            if stripped.endswith('{'):
                indented_lines.append('  ' * indent_level + stripped)
                indent_level += 1
            elif stripped.startswith('}'):
                indent_level = max(0, indent_level - 1)
                indented_lines.append('  ' * indent_level + stripped)
            else:
                indented_lines.append('  ' * indent_level + stripped)
        else:
            indented_lines.append('')
    
    return {"result": '\n'.join(indented_lines)}

def format_python(code: str) -> Dict[str, str]:
    """Basic Python formatting"""
    lines = code.split('\n')
    formatted_lines = []
    indent_level = 0
    
    for line in lines:
        stripped = line.strip()
        if stripped:
            if stripped.endswith(':'):
                formatted_lines.append('    ' * indent_level + stripped)
                indent_level += 1
            elif stripped in ['else:', 'elif', 'except:', 'finally:']:
                indent_level = max(0, indent_level - 1)
                formatted_lines.append('    ' * indent_level + stripped)
                indent_level += 1
            else:
                formatted_lines.append('    ' * indent_level + stripped)
        else:
            formatted_lines.append('')
    
    return {"result": '\n'.join(formatted_lines)}

def format_css(code: str) -> Dict[str, str]:
    """Basic CSS formatting"""
    formatted = code
    
    # Add line breaks and indentation
    formatted = re.sub(r'\{', ' {\n', formatted)
    formatted = re.sub(r';', ';\n', formatted)
    formatted = re.sub(r'\}', '\n}\n', formatted)
    
    lines = formatted.split('\n')
    indented_lines = []
    
    for line in lines:
        stripped = line.strip()
        if stripped:
            if stripped.endswith('{'):
                indented_lines.append(stripped)
            elif stripped == '}':
                indented_lines.append(stripped)
            else:
                indented_lines.append('  ' + stripped)
        else:
            indented_lines.append('')
    
    return {"result": '\n'.join(indented_lines)}

def format_html(code: str) -> Dict[str, str]:
    """Basic HTML formatting"""
    # Simple HTML formatting
    formatted = code
    
    # Add line breaks after tags
    formatted = re.sub(r'><', '>\n<', formatted)
    
    lines = formatted.split('\n')
    indented_lines = []
    indent_level = 0
    
    for line in lines:
        stripped = line.strip()
        if stripped:
            if re.match(r'<\/\w+>', stripped):  # Closing tag
                indent_level = max(0, indent_level - 1)
                indented_lines.append('  ' * indent_level + stripped)
            elif re.match(r'<\w+[^>]*>', stripped) and not stripped.endswith('/>'):  # Opening tag
                indented_lines.append('  ' * indent_level + stripped)
                if not re.match(r'<(br|hr|img|input|meta|link)', stripped, re.IGNORECASE):
                    indent_level += 1
            else:
                indented_lines.append('  ' * indent_level + stripped)
        else:
            indented_lines.append('')
    
    return {"result": '\n'.join(indented_lines)}

def code_minifier(code: str, language: str = "javascript") -> Dict[str, Any]:
    """Minify code by removing whitespace and comments"""
    if not code:
        return {"result": ""}
    
    original_size = len(code)
    
    if language.lower() in ["javascript", "js"]:
        minified = minify_javascript(code)
    elif language.lower() in ["css"]:
        minified = minify_css(code)
    else:
        # Generic minification
        minified = re.sub(r'\s+', ' ', code).strip()
    
    return {
        "result": minified,
        "original_size": original_size,
        "minified_size": len(minified),
        "compression_ratio": f"{((original_size - len(minified)) / original_size * 100):.1f}%"
    }

def minify_javascript(code: str) -> str:
    """Minify JavaScript code"""
    # Remove comments
    code = re.sub(r'//.*?\n', '\n', code)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    
    # Remove extra whitespace
    code = re.sub(r'\s+', ' ', code)
    code = re.sub(r'\s*([{}();,])\s*', r'\1', code)
    
    return code.strip()

def minify_css(code: str) -> str:
    """Minify CSS code"""
    # Remove comments
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    
    # Remove extra whitespace
    code = re.sub(r'\s+', ' ', code)
    code = re.sub(r'\s*([{}:;,])\s*', r'\1', code)
    
    return code.strip()

def regex_builder(pattern_type: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
    """Build common regex patterns"""
    if not options:
        options = {}
    
    patterns = {
        "email": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        "phone": r'^\+?1?[-.\s]?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})$',
        "url": r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$',
        "ip": r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
        "credit_card": r'^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|3[0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})$',
        "password": r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
        "hex_color": r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
        "date": r'^\d{4}-\d{2}-\d{2}$',
        "time": r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$',
        "username": r'^[a-zA-Z0-9_]{3,20}$'
    }
    
    if pattern_type not in patterns:
        return {"error": f"Pattern type '{pattern_type}' not supported"}
    
    pattern = patterns[pattern_type]
    
    # Modify pattern based on options
    if options.get("case_insensitive"):
        flags = "i"
    else:
        flags = ""
    
    return {
        "pattern": pattern,
        "flags": flags,
        "description": f"Regular expression for {pattern_type}",
        "example_matches": get_example_matches(pattern_type)
    }

def get_example_matches(pattern_type: str) -> List[str]:
    """Get example matches for regex patterns"""
    examples = {
        "email": ["user@example.com", "test.email+tag@domain.co.uk"],
        "phone": ["+1-555-123-4567", "(555) 123-4567"],
        "url": ["https://www.example.com", "http://subdomain.example.org/path"],
        "ip": ["192.168.1.1", "10.0.0.1"],
        "credit_card": ["4111111111111111", "5555555555554444"],
        "password": ["Password123!", "MySecure@Pass1"],
        "hex_color": ["#FF0000", "#abc"],
        "date": ["2023-12-25", "2024-01-01"],
        "time": ["14:30", "09:15"],
        "username": ["user123", "cool_user"]
    }
    
    return examples.get(pattern_type, [])

def gitignore_generator(project_type: str) -> Dict[str, str]:
    """Generate .gitignore files for different project types"""
    
    gitignore_templates = {
        "python": """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
""",
        
        "node": """# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Directory for instrumented libs generated by jscoverage/JSCover
lib-cov

# Coverage directory used by tools like istanbul
coverage

# nyc test coverage
.nyc_output

# Grunt intermediate storage
.grunt

# Bower dependency directory
bower_components

# node-waf configuration
.lock-wscript

# Compiled binary addons
build/Release

# Dependency directories
node_modules/
jspm_packages/

# Optional npm cache directory
.npm

# Optional eslint cache
.eslintcache

# Optional REPL history
.node_repl_history

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# dotenv environment variables file
.env

# parcel-bundler cache
.cache
.parcel-cache

# next.js build output
.next

# nuxt.js build output
.nuxt

# vuepress build output
.vuepress/dist

# Serverless directories
.serverless

# IDE
.vscode/
.idea/

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
""",
        
        "java": """# Compiled class file
*.class

# Log file
*.log

# BlueJ files
*.ctxt

# Mobile Tools for Java (J2ME)
.mtj.tmp/

# Package Files
*.jar
*.war
*.nar
*.ear
*.zip
*.tar.gz
*.rar

# virtual machine crash logs
hs_err_pid*

# Maven
target/
pom.xml.tag
pom.xml.releaseBackup
pom.xml.versionsBackup
pom.xml.next
release.properties
dependency-reduced-pom.xml
buildNumber.properties
.mvn/timing.properties
.mvn/wrapper/maven-wrapper.jar

# Gradle
.gradle
build/
!gradle/wrapper/gradle-wrapper.jar
!**/src/main/**/build/
!**/src/test/**/build/

# IntelliJ IDEA
.idea/
*.iws
*.iml
*.ipr
out/
!**/src/main/**/out/
!**/src/test/**/out/

# Eclipse
.apt_generated
.classpath
.factorypath
.project
.settings
.springBeans
.sts4-cache
bin/
!**/src/main/**/bin/
!**/src/test/**/bin/

# NetBeans
/nbproject/private/
/nbbuild/
/dist/
/nbdist/
/.nb-gradle/

# VS Code
.vscode/

# Mac
.DS_Store

# Windows
Thumbs.db
ehthumbs.db
Desktop.ini
"""
    }
    
    if project_type not in gitignore_templates:
        return {"result": "# Project-specific .gitignore\n# Add your ignore patterns here", "project_type": project_type}
    
    return {
        "result": gitignore_templates[project_type].strip(),
        "project_type": project_type,
        "lines": len(gitignore_templates[project_type].strip().split('\n'))
    }

def license_generator(license_type: str, author: str = "Your Name", year: str = None) -> Dict[str, str]:
    """Generate software licenses"""
    
    if not year:
        year = str(datetime.now().year)
    
    licenses = {
        "mit": f"""MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.""",

        "apache": f"""Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/

Copyright {year} {author}

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.""",

        "gpl3": f"""GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) {year} {author}

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>."""
    }
    
    if license_type not in licenses:
        return {"result": "License type not supported", "license_type": license_type}
    
    return {
        "result": licenses[license_type],
        "license_type": license_type.upper(),
        "author": author,
        "year": year
    }

def variable_namer(description: str, naming_convention: str = "camelCase") -> Dict[str, Any]:
    """Generate variable names from description"""
    
    if not description:
        return {"error": "Description is required"}
    
    # Clean and split description
    words = re.findall(r'\b\w+\b', description.lower())
    
    if not words:
        return {"error": "No valid words found in description"}
    
    # Generate different naming conventions
    names = {}
    
    # camelCase
    names["camelCase"] = words[0] + ''.join(word.capitalize() for word in words[1:])
    
    # PascalCase
    names["PascalCase"] = ''.join(word.capitalize() for word in words)
    
    # snake_case
    names["snake_case"] = '_'.join(words)
    
    # kebab-case
    names["kebab-case"] = '-'.join(words)
    
    # CONSTANT_CASE
    names["CONSTANT_CASE"] = '_'.join(word.upper() for word in words)
    
    # Hungarian notation (simplified)
    if any(keyword in description.lower() for keyword in ['string', 'text', 'name']):
        prefix = "str"
    elif any(keyword in description.lower() for keyword in ['number', 'count', 'index']):
        prefix = "num"
    elif any(keyword in description.lower() for keyword in ['boolean', 'flag', 'is', 'has']):
        prefix = "bool"
    else:
        prefix = "var"
    
    names["hungarian"] = prefix + names["PascalCase"]
    
    return {
        "suggestions": names,
        "preferred": names.get(naming_convention, names["camelCase"]),
        "convention": naming_convention,
        "word_count": len(words)
    }