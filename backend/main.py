from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from typing import Optional, List
import json

# Import utility modules
from backend.utils import (
    text_utils, converter_utils, generator_utils, 
    crypto_utils, image_utils, web_utils, file_utils
)

app = FastAPI(
    title="Ultimate Utility Tools",
    description="A comprehensive collection of free utility tools for developers and everyday users",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Tool categories for SEO and navigation
TOOL_CATEGORIES = {
    "text": {
        "name": "Text Tools",
        "description": "Text manipulation, formatting, and analysis tools",
        "tools": [
            "word_count", "character_count", "text_case_converter", 
            "text_diff", "text_formatter", "remove_duplicates",
            "sort_lines", "reverse_text", "text_encoder_decoder"
        ]
    },
    "converters": {
        "name": "Converters",
        "description": "Convert between different formats and units",
        "tools": [
            "base64_converter", "url_encoder", "json_formatter",
            "csv_to_json", "xml_to_json", "markdown_to_html",
            "unit_converter", "color_converter", "timestamp_converter"
        ]
    },
    "generators": {
        "name": "Generators",
        "description": "Generate passwords, UUIDs, QR codes, and more",
        "tools": [
            "password_generator", "uuid_generator", "qr_generator",
            "lorem_ipsum", "fake_data", "hash_generator",
            "random_number", "color_palette", "barcode_generator"
        ]
    },
    "crypto": {
        "name": "Cryptography",
        "description": "Encryption, decryption, and hashing tools",
        "tools": [
            "md5_hash", "sha_hash", "encrypt_decrypt",
            "jwt_decoder", "certificate_info", "rsa_generator"
        ]
    },
    "image": {
        "name": "Image Tools",
        "description": "Image processing and manipulation tools",
        "tools": [
            "image_resizer", "image_compressor", "format_converter",
            "image_metadata", "color_picker", "image_cropper"
        ]
    },
    "web": {
        "name": "Web Tools",
        "description": "Web development and SEO tools",
        "tools": [
            "url_shortener", "meta_tag_analyzer", "robots_txt_generator",
            "sitemap_generator", "website_screenshot", "ssl_checker",
            "dns_lookup", "whois_lookup", "page_speed_test"
        ]
    },
    "file": {
        "name": "File Tools",
        "description": "File processing and analysis tools",
        "tools": [
            "file_hash", "file_info", "zip_extractor",
            "pdf_tools", "file_converter", "duplicate_finder"
        ]
    }
}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with all tool categories"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "categories": TOOL_CATEGORIES,
        "title": "Ultimate Utility Tools - Free Online Tools Collection",
        "description": "Access 50+ free online utility tools for text processing, conversions, generators, cryptography, image editing, and web development. No registration required."
    })

@app.get("/tools/{category}", response_class=HTMLResponse)
async def category_page(request: Request, category: str):
    """Category page showing tools in a specific category"""
    if category not in TOOL_CATEGORIES:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return templates.TemplateResponse("category.html", {
        "request": request,
        "category": category,
        "category_info": TOOL_CATEGORIES[category],
        "title": f"{TOOL_CATEGORIES[category]['name']} - Free Online Tools",
        "description": TOOL_CATEGORIES[category]['description']
    })

@app.get("/tool/{tool_name}", response_class=HTMLResponse)
async def tool_page(request: Request, tool_name: str):
    """Individual tool page"""
    # Find which category this tool belongs to
    tool_category = None
    for cat, info in TOOL_CATEGORIES.items():
        if tool_name in info["tools"]:
            tool_category = cat
            break
    
    if not tool_category:
        raise HTTPException(status_code=404, detail="Tool not found")
    
    return templates.TemplateResponse("tool.html", {
        "request": request,
        "tool_name": tool_name,
        "category": tool_category,
        "title": f"{tool_name.replace('_', ' ').title()} - Free Online Tool",
        "description": f"Free online {tool_name.replace('_', ' ')} tool. No registration required."
    })

# API Routes for Text Tools
@app.post("/api/text/word-count")
async def word_count(text: str = Form(...)):
    return text_utils.count_words(text)

@app.post("/api/text/case-convert")
async def case_convert(text: str = Form(...), case_type: str = Form(...)):
    return text_utils.convert_case(text, case_type)

@app.post("/api/text/diff")
async def text_diff(text1: str = Form(...), text2: str = Form(...)):
    return text_utils.compare_text(text1, text2)

# API Routes for Converters
@app.post("/api/convert/base64")
async def base64_convert(text: str = Form(...), action: str = Form(...)):
    return converter_utils.base64_convert(text, action)

@app.post("/api/convert/url")
async def url_convert(text: str = Form(...), action: str = Form(...)):
    return converter_utils.url_convert(text, action)

@app.post("/api/convert/json")
async def json_format(text: str = Form(...)):
    return converter_utils.format_json(text)

# API Routes for Generators
@app.post("/api/generate/password")
async def generate_password(length: int = Form(12), include_symbols: bool = Form(True)):
    return generator_utils.generate_password(length, include_symbols)

@app.post("/api/generate/uuid")
async def generate_uuid(version: int = Form(4)):
    return generator_utils.generate_uuid(version)

@app.post("/api/generate/qr")
async def generate_qr(text: str = Form(...)):
    return generator_utils.generate_qr_code(text)

# API Routes for Crypto Tools
@app.post("/api/crypto/hash")
async def create_hash(text: str = Form(...), algorithm: str = Form("md5")):
    return crypto_utils.create_hash(text, algorithm)

@app.post("/api/crypto/jwt-decode")
async def decode_jwt(token: str = Form(...)):
    return crypto_utils.decode_jwt(token)

# API Routes for Image Tools
@app.post("/api/image/resize")
async def resize_image(file: UploadFile = File(...), width: int = Form(...), height: int = Form(...)):
    return await image_utils.resize_image(file, width, height)

@app.post("/api/image/compress")
async def compress_image(file: UploadFile = File(...), quality: int = Form(80)):
    return await image_utils.compress_image(file, quality)

# API Routes for Web Tools
@app.post("/api/web/meta-analyzer")
async def analyze_meta(url: str = Form(...)):
    return await web_utils.analyze_meta_tags(url)

@app.post("/api/web/ssl-check")
async def check_ssl(domain: str = Form(...)):
    return web_utils.check_ssl_certificate(domain)

# API Routes for File Tools
@app.post("/api/file/hash")
async def file_hash(file: UploadFile = File(...), algorithm: str = Form("md5")):
    return await file_utils.calculate_file_hash(file, algorithm)

@app.post("/api/file/info")
async def file_info(file: UploadFile = File(...)):
    return await file_utils.get_file_info(file)

# SEO Routes
@app.get("/sitemap.xml")
async def sitemap():
    """Generate XML sitemap for SEO"""
    sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://your-domain.com/</loc>
        <lastmod>2024-01-01</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>"""
    
    for category in TOOL_CATEGORIES.keys():
        sitemap_content += f"""
    <url>
        <loc>https://your-domain.com/tools/{category}</loc>
        <lastmod>2024-01-01</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>"""
        
        for tool in TOOL_CATEGORIES[category]["tools"]:
            sitemap_content += f"""
    <url>
        <loc>https://your-domain.com/tool/{tool}</loc>
        <lastmod>2024-01-01</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>"""
    
    sitemap_content += "\n</urlset>"
    
    return HTMLResponse(content=sitemap_content, media_type="application/xml")

@app.get("/robots.txt")
async def robots_txt():
    """Generate robots.txt for SEO"""
    robots_content = """User-agent: *
Allow: /

Sitemap: https://your-domain.com/sitemap.xml"""
    return HTMLResponse(content=robots_content, media_type="text/plain")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)