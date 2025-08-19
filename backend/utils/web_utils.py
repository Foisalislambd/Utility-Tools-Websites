"""Web utility functions"""
import requests
import ssl
import socket
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import validators
from typing import Dict, Any
import json

async def analyze_meta_tags(url: str) -> Dict[str, Any]:
    """Analyze meta tags of a website"""
    try:
        if not validators.url(url):
            return {"result": "Invalid URL", "success": False}
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract meta tags
        meta_tags = {}
        for meta in soup.find_all('meta'):
            if meta.get('name'):
                meta_tags[meta.get('name')] = meta.get('content', '')
            elif meta.get('property'):
                meta_tags[meta.get('property')] = meta.get('content', '')
        
        # Extract other important tags
        title = soup.find('title')
        title_text = title.text.strip() if title else ""
        
        # Extract headings
        headings = {}
        for i in range(1, 7):
            h_tags = soup.find_all(f'h{i}')
            headings[f'h{i}'] = [h.text.strip() for h in h_tags]
        
        # Extract links
        links = []
        for link in soup.find_all('a', href=True):
            links.append({
                "url": link['href'],
                "text": link.text.strip()
            })
        
        return {
            "url": url,
            "title": title_text,
            "title_length": len(title_text),
            "meta_tags": meta_tags,
            "headings": headings,
            "links_count": len(links),
            "links": links[:10],  # First 10 links
            "status_code": response.status_code,
            "success": True
        }
    except Exception as e:
        return {"result": str(e), "success": False}

def check_ssl_certificate(domain: str) -> Dict[str, Any]:
    """Check SSL certificate information"""
    try:
        # Remove protocol if present
        domain = domain.replace('https://', '').replace('http://', '').split('/')[0]
        
        context = ssl.create_default_context()
        
        with socket.create_connection((domain, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                
                # Parse certificate info
                info = {
                    "domain": domain,
                    "subject": dict(x[0] for x in cert['subject']),
                    "issuer": dict(x[0] for x in cert['issuer']),
                    "version": cert['version'],
                    "serial_number": cert['serialNumber'],
                    "not_before": cert['notBefore'],
                    "not_after": cert['notAfter'],
                    "signature_algorithm": cert.get('signatureAlgorithm', 'Unknown'),
                    "success": True
                }
                
                # Check if certificate is valid
                from datetime import datetime
                not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                days_until_expiry = (not_after - datetime.now()).days
                info["days_until_expiry"] = days_until_expiry
                info["is_valid"] = days_until_expiry > 0
                
                return info
    except Exception as e:
        return {"result": str(e), "success": False}

def dns_lookup(domain: str, record_type: str = "A") -> Dict[str, Any]:
    """Perform DNS lookup"""
    try:
        try:
            import dns.resolver
        except ImportError:
            return {"result": "DNS lookup requires dnspython package", "success": False}
        
        # Remove protocol if present
        domain = domain.replace('https://', '').replace('http://', '').split('/')[0]
        
        resolver = dns.resolver.Resolver()
        answers = resolver.resolve(domain, record_type)
        
        records = []
        for answer in answers:
            records.append(str(answer))
        
        return {
            "domain": domain,
            "record_type": record_type,
            "records": records,
            "ttl": answers.ttl,
            "success": True
        }
    except Exception as e:
        return {"result": str(e), "success": False}

def whois_lookup(domain: str) -> Dict[str, Any]:
    """Perform WHOIS lookup"""
    try:
        try:
            import whois
        except ImportError:
            return {"result": "WHOIS lookup requires python-whois package", "success": False}
        
        # Remove protocol if present
        domain = domain.replace('https://', '').replace('http://', '').split('/')[0]
        
        w = whois.whois(domain)
        
        return {
            "domain": domain,
            "registrar": w.registrar,
            "creation_date": str(w.creation_date) if w.creation_date else None,
            "expiration_date": str(w.expiration_date) if w.expiration_date else None,
            "name_servers": w.name_servers,
            "status": w.status,
            "success": True
        }
    except Exception as e:
        return {"result": str(e), "success": False}

def generate_robots_txt(rules: Dict[str, Any]) -> Dict[str, str]:
    """Generate robots.txt content"""
    try:
        content = []
        
        # User-agent rules
        for user_agent, directives in rules.get('user_agents', {}).items():
            content.append(f"User-agent: {user_agent}")
            
            for directive, paths in directives.items():
                if isinstance(paths, list):
                    for path in paths:
                        content.append(f"{directive.capitalize()}: {path}")
                else:
                    content.append(f"{directive.capitalize()}: {paths}")
            content.append("")
        
        # Sitemap
        if rules.get('sitemap'):
            content.append(f"Sitemap: {rules['sitemap']}")
        
        # Crawl-delay
        if rules.get('crawl_delay'):
            content.append(f"Crawl-delay: {rules['crawl_delay']}")
        
        result = '\n'.join(content)
        
        return {
            "robots_txt": result,
            "lines": len(content),
            "success": True
        }
    except Exception as e:
        return {"result": str(e), "success": False}

def generate_sitemap_xml(urls: list) -> Dict[str, Any]:
    """Generate XML sitemap"""
    try:
        from datetime import datetime
        
        sitemap_content = ['<?xml version="1.0" encoding="UTF-8"?>']
        sitemap_content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
        
        for url_info in urls:
            if isinstance(url_info, str):
                url_info = {"loc": url_info}
            
            sitemap_content.append('  <url>')
            sitemap_content.append(f'    <loc>{url_info["loc"]}</loc>')
            
            if url_info.get("lastmod"):
                sitemap_content.append(f'    <lastmod>{url_info["lastmod"]}</lastmod>')
            else:
                sitemap_content.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
            
            if url_info.get("changefreq"):
                sitemap_content.append(f'    <changefreq>{url_info["changefreq"]}</changefreq>')
            
            if url_info.get("priority"):
                sitemap_content.append(f'    <priority>{url_info["priority"]}</priority>')
            
            sitemap_content.append('  </url>')
        
        sitemap_content.append('</urlset>')
        
        result = '\n'.join(sitemap_content)
        
        return {
            "sitemap": result,
            "url_count": len(urls),
            "success": True
        }
    except Exception as e:
        return {"result": str(e), "success": False}

def shorten_url(url: str, custom_alias: str = None) -> Dict[str, Any]:
    """URL shortener (mock implementation)"""
    try:
        import hashlib
        import random
        import string
        
        if not validators.url(url):
            return {"result": "Invalid URL", "success": False}
        
        # Generate short code
        if custom_alias:
            short_code = custom_alias
        else:
            # Create hash-based short code
            hash_obj = hashlib.md5(url.encode())
            short_code = hash_obj.hexdigest()[:6]
        
        # In a real implementation, you'd store this in a database
        short_url = f"https://short.ly/{short_code}"
        
        return {
            "original_url": url,
            "short_url": short_url,
            "short_code": short_code,
            "clicks": 0,  # Would be tracked in database
            "success": True
        }
    except Exception as e:
        return {"result": str(e), "success": False}

def test_page_speed(url: str) -> Dict[str, Any]:
    """Basic page speed test"""
    try:
        import time
        
        if not validators.url(url):
            return {"result": "Invalid URL", "success": False}
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=30)
        end_time = time.time()
        
        load_time = round((end_time - start_time) * 1000, 2)  # in milliseconds
        
        # Basic analysis
        content_size = len(response.content)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Count resources
        images = len(soup.find_all('img'))
        scripts = len(soup.find_all('script'))
        stylesheets = len(soup.find_all('link', rel='stylesheet'))
        
        # Performance score (basic calculation)
        score = 100
        if load_time > 3000:
            score -= 30
        elif load_time > 1000:
            score -= 15
        
        if content_size > 1000000:  # 1MB
            score -= 20
        elif content_size > 500000:  # 500KB
            score -= 10
        
        return {
            "url": url,
            "load_time_ms": load_time,
            "content_size": content_size,
            "status_code": response.status_code,
            "performance_score": max(score, 0),
            "resources": {
                "images": images,
                "scripts": scripts,
                "stylesheets": stylesheets
            },
            "success": True
        }
    except Exception as e:
        return {"result": str(e), "success": False}