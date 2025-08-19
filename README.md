# Ultimate Utility Tools 🛠️

A comprehensive collection of **50+ free online utility tools** built with FastAPI and Tailwind CSS. No registration required, privacy-focused, and completely free to use.

## 🌟 Features

- **50+ Utility Tools** across 7 categories
- **No Registration Required** - Use tools instantly
- **Privacy First** - Most processing happens in your browser
- **Mobile Friendly** - Responsive design for all devices
- **SEO Optimized** - Structured data, meta tags, and sitemap
- **Fast & Modern** - Built with FastAPI and Tailwind CSS
- **API Available** - RESTful API for all tools

## 🔧 Tool Categories

### 📝 Text Tools
- Word Counter & Character Counter
- Text Case Converter (camelCase, snake_case, etc.)
- Text Diff Checker
- Text Formatter & Cleaner
- Line Sorter & Duplicate Remover
- Text Encoder/Decoder

### 🔄 Converters
- Base64 Encoder/Decoder
- URL Encoder/Decoder
- JSON Formatter & Validator
- CSV to JSON Converter
- XML to JSON Converter
- Markdown to HTML
- Unit Converter
- Color Converter
- Timestamp Converter

### ⚡ Generators
- Secure Password Generator
- UUID Generator (v1, v4)
- QR Code Generator
- Lorem Ipsum Generator
- Fake Data Generator
- Hash Generator
- Random Number Generator
- Color Palette Generator

### 🔒 Cryptography Tools
- MD5, SHA-1, SHA-256, SHA-512 Hash
- JWT Token Decoder
- Text Encryption/Decryption
- RSA Key Generator
- Certificate Analyzer
- Checksum Calculator

### 🖼️ Image Tools
- Image Resizer
- Image Compressor
- Format Converter
- Image Metadata Extractor
- Color Picker
- Image Cropper

### 🌐 Web Tools
- Meta Tag Analyzer
- SSL Certificate Checker
- DNS Lookup
- WHOIS Lookup
- Page Speed Test
- URL Shortener
- Robots.txt Generator
- Sitemap Generator

### 📁 File Tools
- File Hash Calculator
- File Information Extractor
- ZIP File Analyzer
- Duplicate File Finder
- File Format Converter

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd ultimate-utility-tools

# Run with Docker Compose
docker-compose up -d

# Access the application
open http://localhost
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py

# Access the application
open http://localhost:8000
```

### Manual Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📱 API Usage

All tools are available via RESTful API endpoints:

```python
import requests

# Example: Generate password
response = requests.post('http://localhost:8000/api/generate/password', 
                        data={'length': 16, 'include_symbols': True})
print(response.json())

# Example: Count words
response = requests.post('http://localhost:8000/api/text/word-count', 
                        data={'text': 'Hello world!'})
print(response.json())

# Example: Convert Base64
response = requests.post('http://localhost:8000/api/convert/base64', 
                        data={'text': 'Hello world!', 'action': 'encode'})
print(response.json())
```

### API Documentation

- **Swagger UI**: `http://localhost:8000/api/docs`
- **ReDoc**: `http://localhost:8000/api/redoc`

## 🏗️ Project Structure

```
ultimate-utility-tools/
├── backend/
│   ├── utils/
│   │   ├── text_utils.py      # Text processing functions
│   │   ├── converter_utils.py # Format conversion functions
│   │   ├── generator_utils.py # Data generation functions
│   │   ├── crypto_utils.py    # Cryptography functions
│   │   ├── image_utils.py     # Image processing functions
│   │   ├── web_utils.py       # Web analysis functions
│   │   └── file_utils.py      # File processing functions
│   └── __init__.py
├── templates/
│   ├── base.html             # Base template
│   ├── index.html            # Home page
│   ├── category.html         # Category pages
│   ├── tool.html             # Individual tool pages
│   ├── privacy.html          # Privacy policy
│   ├── terms.html            # Terms of service
│   └── contact.html          # Contact page
├── static/
│   ├── css/
│   │   └── custom.css        # Custom styles
│   └── js/
│       └── main.js           # JavaScript functionality
├── main.py                   # FastAPI application
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
├── nginx.conf              # Nginx configuration
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables

- `ENVIRONMENT`: Set to `production` for production deployment
- `HOST`: Host to bind to (default: 0.0.0.0)
- `PORT`: Port to bind to (default: 8000)

### Customization

1. **Add New Tools**: Create functions in appropriate utils files and add API routes
2. **Modify Styling**: Edit `static/css/custom.css` or Tailwind classes
3. **Update SEO**: Modify meta tags in `templates/base.html`
4. **Add Categories**: Update `TOOL_CATEGORIES` in `main.py`

## 🚀 Deployment

### Production Deployment

1. **With Docker**:
   ```bash
   docker-compose up -d
   ```

2. **With Nginx** (recommended for production):
   - Use the provided `nginx.conf`
   - Configure SSL certificates
   - Update domain names in configuration

3. **Cloud Deployment**:
   - Deploy to AWS, Google Cloud, or Azure
   - Use managed container services
   - Configure load balancing and auto-scaling

### Performance Optimization

- Enable gzip compression (included in nginx.conf)
- Use CDN for static assets
- Implement caching for API responses
- Monitor with health check endpoint (`/health`)

## 🔒 Security Features

- CORS protection
- Rate limiting (via nginx)
- Input validation
- XSS protection headers
- No data persistence (privacy by design)
- HTTPS ready

## 📊 SEO Features

- **Structured Data**: JSON-LD markup for search engines
- **Meta Tags**: Comprehensive Open Graph and Twitter Card tags
- **Sitemap**: Auto-generated XML sitemap (`/sitemap.xml`)
- **Robots.txt**: SEO-friendly robots.txt (`/robots.txt`)
- **Semantic HTML**: Proper heading structure and semantic markup
- **Mobile Optimization**: Responsive design and mobile-first approach
- **Page Speed**: Optimized loading and minimal dependencies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your utility function to the appropriate utils file
4. Add API route in `main.py`
5. Update frontend templates if needed
6. Submit a pull request

### Adding a New Tool

1. **Backend**: Add function to appropriate utils file
2. **API**: Add route in `main.py`
3. **Frontend**: Add tool to `TOOL_CATEGORIES`
4. **Template**: Update `tool.html` with interface
5. **Test**: Verify functionality

## 📄 License

This project is open source and available under the MIT License.

## 🐛 Bug Reports & Feature Requests

- **Issues**: Report bugs via GitHub issues
- **Features**: Suggest new tools or improvements
- **Contact**: Use the contact form on the website

## 🔗 Links

- **Live Demo**: [Your Domain Here]
- **API Documentation**: `/api/docs`
- **GitHub**: [Repository URL]
- **Contact**: `/contact`

## 📈 Analytics & Monitoring

- Health check endpoint: `/health`
- No user tracking (privacy-focused)
- Server monitoring via Docker health checks
- Performance monitoring ready

---

**Made with ❤️ for the developer community**

*Ultimate Utility Tools - Making your work easier, one tool at a time.*