from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import sys
from typing import Optional, List
import json

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import utility modules
from backend.utils import (
    text_utils, converter_utils, generator_utils, 
    crypto_utils, image_utils, web_utils, file_utils,
    advanced_text_utils, advanced_converter_utils, advanced_generator_utils,
    developer_utils, math_utils, network_utils
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
            "sort_lines", "reverse_text", "text_encoder_decoder",
            "text_statistics", "find_replace", "text_splitter",
            "text_merger", "line_counter", "paragraph_counter",
            "sentence_counter", "reading_time", "text_summarizer",
            "keyword_density", "text_cleaner", "whitespace_remover",
            "html_stripper", "text_extractor", "regex_tester",
            "text_validator", "spell_checker", "grammar_checker",
            "text_translator", "language_detector", "text_sentiment"
        ]
    },
    "converters": {
        "name": "Converters",
        "description": "Convert between different formats and units",
        "tools": [
            "base64_converter", "url_encoder", "json_formatter",
            "csv_to_json", "xml_to_json", "markdown_to_html",
            "unit_converter", "color_converter", "timestamp_converter",
            "html_to_text", "text_to_html", "yaml_converter",
            "sql_formatter", "css_formatter", "js_formatter",
            "number_base_converter", "roman_numeral_converter", "currency_converter",
            "temperature_converter", "length_converter", "weight_converter",
            "area_converter", "volume_converter", "speed_converter",
            "pressure_converter", "energy_converter", "frequency_converter",
            "angle_converter", "data_size_converter", "time_zone_converter",
            "coordinate_converter", "ascii_converter", "unicode_converter",
            "emoji_converter", "morse_code_converter", "binary_converter"
        ]
    },
    "generators": {
        "name": "Generators",
        "description": "Generate passwords, UUIDs, QR codes, and more",
        "tools": [
            "password_generator", "uuid_generator", "qr_generator",
            "lorem_ipsum", "fake_data", "hash_generator",
            "random_number", "color_palette", "barcode_generator",
            "credit_card_generator", "name_generator", "email_generator",
            "username_generator", "api_key_generator", "token_generator",
            "slug_generator", "guid_generator", "random_string",
            "random_date", "random_ip", "random_mac",
            "random_user_agent", "random_address", "random_phone",
            "random_company", "random_domain", "random_url",
            "random_quote", "random_joke", "random_fact",
            "placeholder_image", "gradient_generator", "pattern_generator",
            "noise_generator", "avatar_generator", "icon_generator",
            "css_generator", "html_generator", "sql_generator"
        ]
    },
    "crypto": {
        "name": "Cryptography",
        "description": "Encryption, decryption, and hashing tools",
        "tools": [
            "md5_hash", "sha_hash", "encrypt_decrypt",
            "jwt_decoder", "certificate_info", "rsa_generator",
            "aes_encrypt", "des_encrypt", "blowfish_encrypt",
            "bcrypt_hash", "scrypt_hash", "pbkdf2_hash",
            "hmac_generator", "digital_signature", "key_generator",
            "entropy_calculator", "password_strength", "hash_cracker",
            "ssl_decoder", "pgp_tools", "base32_converter",
            "hex_converter", "crc_calculator", "checksum_validator",
            "random_bytes", "secure_compare", "otp_generator",
            "totp_generator", "hotp_generator", "secret_sharing"
        ]
    },
    "image": {
        "name": "Image Tools",
        "description": "Image processing and manipulation tools",
        "tools": [
            "image_resizer", "image_compressor", "format_converter",
            "image_metadata", "color_picker", "image_cropper",
            "image_rotator", "image_flipper", "brightness_adjuster",
            "contrast_adjuster", "saturation_adjuster", "hue_adjuster",
            "blur_filter", "sharpen_filter", "noise_filter",
            "edge_detector", "histogram_analyzer", "color_analyzer",
            "dominant_colors", "image_splitter", "image_merger",
            "watermark_adder", "border_adder", "corner_rounder",
            "shadow_adder", "reflection_adder", "vintage_filter",
            "sepia_filter", "grayscale_filter", "invert_colors",
            "pixelate_filter", "oil_painting_filter", "sketch_filter",
            "cartoon_filter", "emboss_filter", "solarize_filter"
        ]
    },
    "web": {
        "name": "Web Tools",
        "description": "Web development and SEO tools",
        "tools": [
            "url_shortener", "meta_tag_analyzer", "robots_txt_generator",
            "sitemap_generator", "website_screenshot", "ssl_checker",
            "dns_lookup", "whois_lookup", "page_speed_test",
            "seo_analyzer", "broken_link_checker", "redirect_checker",
            "http_headers", "response_time", "ping_test",
            "traceroute", "port_scanner", "ip_lookup",
            "user_agent_parser", "referrer_parser", "cookie_parser",
            "html_validator", "css_validator", "js_validator",
            "accessibility_checker", "mobile_friendly_test", "schema_validator",
            "open_graph_tester", "twitter_card_tester", "favicon_generator",
            "htaccess_generator", "csp_generator", "cors_tester",
            "webhook_tester", "api_tester", "json_path_tester",
            "xpath_tester", "css_selector_tester", "regex_url_tester"
        ]
    },
    "file": {
        "name": "File Tools",
        "description": "File processing and analysis tools",
        "tools": [
            "file_hash", "file_info", "zip_extractor",
            "pdf_tools", "file_converter", "duplicate_finder",
            "file_splitter", "file_merger", "file_compressor",
            "file_encryptor", "file_shredder", "file_renamer",
            "batch_renamer", "file_organizer", "directory_tree",
            "disk_usage", "file_permissions", "file_timestamps",
            "mime_detector", "encoding_detector", "line_endings",
            "bom_detector", "virus_scanner", "malware_detector",
            "file_recovery", "deleted_files", "temp_cleaner",
            "cache_cleaner", "log_analyzer", "config_parser"
        ]
    },
    "developer": {
        "name": "Developer Tools",
        "description": "Programming and development utilities",
        "tools": [
            "code_formatter", "code_minifier", "syntax_highlighter",
            "regex_builder", "regex_tester", "xpath_builder",
            "sql_builder", "query_optimizer", "api_client",
            "json_path", "xml_path", "css_selector",
            "html_parser", "xml_parser", "csv_parser",
            "log_parser", "config_generator", "env_generator",
            "gitignore_generator", "license_generator", "readme_generator",
            "changelog_generator", "documentation_generator", "comment_generator",
            "variable_namer", "function_namer", "class_namer",
            "package_namer", "project_namer", "commit_message",
            "code_reviewer", "complexity_analyzer", "dependency_checker",
            "vulnerability_scanner", "code_duplicator", "refactoring_helper"
        ]
    },
    "data": {
        "name": "Data Tools",
        "description": "Data processing and analysis utilities",
        "tools": [
            "data_validator", "data_cleaner", "data_transformer",
            "csv_analyzer", "json_analyzer", "xml_analyzer",
            "data_merger", "data_splitter", "data_sampler",
            "duplicate_remover", "null_handler", "outlier_detector",
            "statistical_analyzer", "correlation_calculator", "trend_analyzer",
            "pivot_table", "cross_tab", "group_by",
            "sort_data", "filter_data", "search_data",
            "data_profiler", "schema_generator", "data_dictionary",
            "data_lineage", "data_quality", "data_governance",
            "etl_generator", "sql_generator", "migration_helper"
        ]
    },
    "math": {
        "name": "Math Tools",
        "description": "Mathematical calculators and utilities",
        "tools": [
            "basic_calculator", "scientific_calculator", "programmer_calculator",
            "matrix_calculator", "equation_solver", "derivative_calculator",
            "integral_calculator", "limit_calculator", "series_calculator",
            "statistics_calculator", "probability_calculator", "combinatorics_calculator",
            "number_theory", "prime_checker", "factorization",
            "gcd_calculator", "lcm_calculator", "modular_arithmetic",
            "base_converter", "fraction_calculator", "percentage_calculator",
            "interest_calculator", "loan_calculator", "mortgage_calculator",
            "investment_calculator", "retirement_calculator", "tax_calculator",
            "tip_calculator", "discount_calculator", "markup_calculator",
            "ratio_calculator", "proportion_calculator", "unit_circle"
        ]
    },
    "network": {
        "name": "Network Tools",
        "description": "Network analysis and testing utilities",
        "tools": [
            "ip_calculator", "subnet_calculator", "cidr_calculator",
            "mac_lookup", "port_checker", "bandwidth_tester",
            "latency_tester", "jitter_tester", "packet_loss_tester",
            "network_scanner", "vulnerability_scanner", "security_checker",
            "firewall_tester", "proxy_checker", "vpn_tester",
            "dns_propagation", "mx_lookup", "txt_lookup",
            "cname_lookup", "aaaa_lookup", "ptr_lookup",
            "reverse_dns", "dns_cache", "dns_benchmark",
            "email_validator", "domain_checker", "ssl_analyzer",
            "certificate_chain", "cipher_checker", "tls_tester"
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
        "categories": TOOL_CATEGORIES,
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
        "categories": TOOL_CATEGORIES,
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

@app.post("/api/text/format")
async def format_text(text: str = Form(...), operation: str = Form(...)):
    return text_utils.format_text(text, operation)

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

@app.post("/api/convert/csv-to-json")
async def csv_to_json(text: str = Form(...)):
    return converter_utils.csv_to_json(text)

@app.post("/api/convert/units")
async def convert_units(value: float = Form(...), from_unit: str = Form(...), to_unit: str = Form(...), unit_type: str = Form(...)):
    return converter_utils.convert_units(value, from_unit, to_unit, unit_type)

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

@app.post("/api/generate/lorem")
async def generate_lorem(paragraphs: int = Form(3), words_per_paragraph: int = Form(50)):
    return generator_utils.generate_lorem_ipsum(paragraphs, words_per_paragraph)

@app.post("/api/generate/fake-data")
async def generate_fake_data(data_type: str = Form(...), count: int = Form(1)):
    return generator_utils.generate_fake_data(data_type, count)

# API Routes for Crypto Tools
@app.post("/api/crypto/hash")
async def create_hash(text: str = Form(...), algorithm: str = Form("md5")):
    return crypto_utils.create_hash(text, algorithm)

@app.post("/api/crypto/jwt-decode")
async def decode_jwt(token: str = Form(...)):
    return crypto_utils.decode_jwt(token)

@app.post("/api/crypto/encrypt")
async def encrypt_text(text: str = Form(...), key: str = Form(...), operation: str = Form("encrypt")):
    return crypto_utils.encrypt_decrypt_text(text, key, operation)

# API Routes for Image Tools
@app.post("/api/image/resize")
async def resize_image(file: UploadFile = File(...), width: int = Form(...), height: int = Form(...)):
    return await image_utils.resize_image(file, width, height)

@app.post("/api/image/compress")
async def compress_image(file: UploadFile = File(...), quality: int = Form(80)):
    return await image_utils.compress_image(file, quality)

@app.post("/api/image/metadata")
async def image_metadata(file: UploadFile = File(...)):
    return await image_utils.get_image_metadata(file)

# API Routes for Web Tools
@app.post("/api/web/meta-analyzer")
async def analyze_meta(url: str = Form(...)):
    return await web_utils.analyze_meta_tags(url)

@app.post("/api/web/ssl-check")
async def check_ssl(domain: str = Form(...)):
    return web_utils.check_ssl_certificate(domain)

@app.post("/api/web/page-speed")
async def page_speed_test(url: str = Form(...)):
    return web_utils.test_page_speed(url)

# API Routes for File Tools
@app.post("/api/file/hash")
async def file_hash(file: UploadFile = File(...), algorithm: str = Form("md5")):
    return await file_utils.calculate_file_hash(file, algorithm)

@app.post("/api/file/info")
async def file_info(file: UploadFile = File(...)):
    return await file_utils.get_file_info(file)

# Advanced Text Tools API Routes
@app.post("/api/text/statistics")
async def text_statistics(text: str = Form(...)):
    return advanced_text_utils.text_statistics(text)

@app.post("/api/text/find-replace")
async def find_replace(text: str = Form(...), find: str = Form(...), replace: str = Form(...), 
                      case_sensitive: bool = Form(True), whole_word: bool = Form(False)):
    return advanced_text_utils.find_replace(text, find, replace, case_sensitive, whole_word)

@app.post("/api/text/splitter")
async def text_splitter(text: str = Form(...), delimiter: str = Form("\n"), max_length: int = Form(None)):
    return advanced_text_utils.text_splitter(text, delimiter, max_length)

@app.post("/api/text/keyword-density")
async def keyword_density(text: str = Form(...), keywords: str = Form(None)):
    keyword_list = keywords.split(',') if keywords else None
    return advanced_text_utils.keyword_density(text, keyword_list)

@app.post("/api/text/cleaner")
async def text_cleaner(text: str = Form(...), remove_extra_spaces: bool = Form(True),
                      remove_line_breaks: bool = Form(False), remove_punctuation: bool = Form(False)):
    options = {
        "remove_extra_spaces": remove_extra_spaces,
        "remove_line_breaks": remove_line_breaks,
        "remove_punctuation": remove_punctuation
    }
    return advanced_text_utils.text_cleaner(text, options)

@app.post("/api/text/html-stripper")
async def html_stripper(text: str = Form(...)):
    return advanced_text_utils.html_stripper(text)

@app.post("/api/text/regex-tester")
async def regex_tester(text: str = Form(...), pattern: str = Form(...), flags: str = Form("")):
    return advanced_text_utils.regex_tester(text, pattern, flags)

@app.post("/api/text/language-detector")
async def language_detector(text: str = Form(...)):
    return advanced_text_utils.language_detector(text)

@app.post("/api/text/sentiment")
async def text_sentiment(text: str = Form(...)):
    return advanced_text_utils.text_sentiment(text)

# Advanced Converter Tools API Routes
@app.post("/api/convert/html-to-text")
async def html_to_text(html_content: str = Form(...)):
    return advanced_converter_utils.html_to_text(html_content)

@app.post("/api/convert/text-to-html")
async def text_to_html(text: str = Form(...), preserve_line_breaks: bool = Form(True)):
    options = {"preserve_line_breaks": preserve_line_breaks}
    return advanced_converter_utils.text_to_html(text, options)

@app.post("/api/convert/yaml")
async def yaml_converter(text: str = Form(...), action: str = Form("to_json")):
    return advanced_converter_utils.yaml_converter(text, action)

@app.post("/api/convert/sql-formatter")
async def sql_formatter(sql: str = Form(...)):
    return advanced_converter_utils.sql_formatter(sql)

@app.post("/api/convert/number-base")
async def number_base_converter(number: str = Form(...), from_base: int = Form(10), to_base: int = Form(2)):
    return advanced_converter_utils.number_base_converter(number, from_base, to_base)

@app.post("/api/convert/roman-numeral")
async def roman_numeral_converter(value: str = Form(...), action: str = Form("to_roman")):
    return advanced_converter_utils.roman_numeral_converter(value, action)

@app.post("/api/convert/ascii")
async def ascii_converter(text: str = Form(...), action: str = Form("to_ascii")):
    return advanced_converter_utils.ascii_converter(text, action)

@app.post("/api/convert/morse-code")
async def morse_code_converter(text: str = Form(...), action: str = Form("to_morse")):
    return advanced_converter_utils.morse_code_converter(text, action)

@app.post("/api/convert/binary")
async def binary_converter(text: str = Form(...), action: str = Form("to_binary")):
    return advanced_converter_utils.binary_converter(text, action)

# Advanced Generator Tools API Routes
@app.post("/api/generate/credit-card")
async def credit_card_generator(card_type: str = Form("visa")):
    return advanced_generator_utils.credit_card_generator(card_type)

@app.post("/api/generate/name")
async def name_generator(gender: str = Form("random"), origin: str = Form("english")):
    return advanced_generator_utils.name_generator(gender, origin)

@app.post("/api/generate/email")
async def email_generator(domain: str = Form(None), username: str = Form(None)):
    return advanced_generator_utils.email_generator(domain, username)

@app.post("/api/generate/username")
async def username_generator(style: str = Form("random")):
    return advanced_generator_utils.username_generator(style)

@app.post("/api/generate/api-key")
async def api_key_generator(length: int = Form(32), format_type: str = Form("hex")):
    return advanced_generator_utils.api_key_generator(length, format_type)

@app.post("/api/generate/random-ip")
async def random_ip(version: int = Form(4)):
    return advanced_generator_utils.random_ip(version)

@app.post("/api/generate/random-mac")
async def random_mac():
    return advanced_generator_utils.random_mac()

@app.post("/api/generate/user-agent")
async def random_user_agent():
    return advanced_generator_utils.random_user_agent()

@app.post("/api/generate/placeholder-image")
async def placeholder_image(width: int = Form(300), height: int = Form(200), format: str = Form("png")):
    return advanced_generator_utils.placeholder_image(width, height, format)

@app.post("/api/generate/gradient")
async def gradient_generator(colors: int = Form(2)):
    return advanced_generator_utils.gradient_generator(colors)

@app.post("/api/generate/quote")
async def random_quote():
    return advanced_generator_utils.random_quote()

# Developer Tools API Routes
@app.post("/api/developer/code-formatter")
async def code_formatter(code: str = Form(...), language: str = Form("javascript")):
    return developer_utils.code_formatter(code, language)

@app.post("/api/developer/code-minifier")
async def code_minifier(code: str = Form(...), language: str = Form("javascript")):
    return developer_utils.code_minifier(code, language)

@app.post("/api/developer/regex-builder")
async def regex_builder(pattern_type: str = Form("email")):
    return developer_utils.regex_builder(pattern_type)

@app.post("/api/developer/gitignore-generator")
async def gitignore_generator(project_type: str = Form("python")):
    return developer_utils.gitignore_generator(project_type)

@app.post("/api/developer/license-generator")
async def license_generator(license_type: str = Form("mit"), author: str = Form("Your Name"), year: str = Form(None)):
    return developer_utils.license_generator(license_type, author, year)

@app.post("/api/developer/variable-namer")
async def variable_namer(description: str = Form(...), naming_convention: str = Form("camelCase")):
    return developer_utils.variable_namer(description, naming_convention)

# Math Tools API Routes
@app.post("/api/math/calculator")
async def basic_calculator(expression: str = Form(...)):
    return math_utils.basic_calculator(expression)

@app.post("/api/math/scientific")
async def scientific_calculator(operation: str = Form(...), values: str = Form(...)):
    try:
        value_list = [float(x.strip()) for x in values.split(',')]
        return math_utils.scientific_calculator(operation, value_list)
    except:
        return {"error": "Invalid values format"}

@app.post("/api/math/statistics")
async def statistics_calculator(data: str = Form(...)):
    try:
        data_list = [float(x.strip()) for x in data.split(',')]
        return math_utils.statistics_calculator(data_list)
    except:
        return {"error": "Invalid data format"}

@app.post("/api/math/prime-checker")
async def prime_checker(number: int = Form(...)):
    return math_utils.prime_checker(number)

@app.post("/api/math/gcd")
async def gcd_calculator(a: int = Form(...), b: int = Form(...)):
    return math_utils.gcd_calculator(a, b)

@app.post("/api/math/percentage")
async def percentage_calculator(operation: str = Form(...), **kwargs):
    return math_utils.percentage_calculator(operation, **kwargs)

@app.post("/api/math/loan")
async def loan_calculator(principal: float = Form(...), rate: float = Form(...), time: float = Form(...)):
    return math_utils.loan_calculator(principal, rate, time)

@app.post("/api/math/unit-circle")
async def unit_circle(angle: float = Form(...), unit: str = Form("degrees")):
    return math_utils.unit_circle(angle, unit)

# Network Tools API Routes
@app.post("/api/network/ip-calculator")
async def ip_calculator(ip: str = Form(...), operation: str = Form("info")):
    return network_utils.ip_calculator(ip, operation)

@app.post("/api/network/subnet-calculator")
async def subnet_calculator(network: str = Form(...)):
    return network_utils.subnet_calculator(network)

@app.post("/api/network/mac-lookup")
async def mac_lookup(mac: str = Form(...)):
    return network_utils.mac_lookup(mac)

@app.post("/api/network/port-checker")
async def port_checker(host: str = Form(...), port: int = Form(...), timeout: int = Form(5)):
    return network_utils.port_checker(host, port, timeout)

@app.post("/api/network/dns-propagation")
async def dns_propagation(domain: str = Form(...), record_type: str = Form("A")):
    return network_utils.dns_propagation(domain, record_type)

@app.post("/api/network/bandwidth-test")
async def bandwidth_tester():
    return network_utils.bandwidth_tester()

@app.post("/api/network/email-validator")
async def email_validator(email: str = Form(...)):
    return network_utils.email_validator(email)

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

@app.get("/privacy", response_class=HTMLResponse)
async def privacy_page(request: Request):
    """Privacy policy page"""
    return templates.TemplateResponse("privacy.html", {"request": request})

@app.get("/terms", response_class=HTMLResponse)
async def terms_page(request: Request):
    """Terms of service page"""
    return templates.TemplateResponse("terms.html", {"request": request})

@app.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request):
    """Contact page"""
    return templates.TemplateResponse("contact.html", {"request": request})

@app.get("/all-tools", response_class=HTMLResponse)
async def all_tools_page(request: Request):
    """All tools page"""
    return templates.TemplateResponse("all_tools.html", {
        "request": request,
        "categories": TOOL_CATEGORIES,
        "title": "All Tools - Ultimate Utility Tools",
        "description": "Browse all 300+ free online utility tools across 11 categories"
    })

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "Ultimate Utility Tools"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)