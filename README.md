# Ultimate Utility Tools 🛠️

A comprehensive collection of **300+ free online utility tools** built with FastAPI and Tailwind CSS. No registration required, privacy-focused, and completely free to use.

## 🌟 Features

- **300+ Utility Tools** across 11 categories
- **No Registration Required** - Use tools instantly
- **Privacy First** - Most processing happens in your browser
- **Mobile Friendly** - Responsive design for all devices
- **SEO Optimized** - Structured data, meta tags, and sitemap
- **Fast & Modern** - Built with FastAPI and Tailwind CSS
- **API Available** - RESTful API for all tools

## 🔧 Tool Categories

### 📝 Text Tools (30 Tools)
- Word Counter & Character Counter
- Text Case Converter (camelCase, snake_case, etc.)
- Text Diff Checker & Advanced Text Statistics
- Find & Replace with Regex Support
- Text Formatter & Cleaner
- Language Detection & Sentiment Analysis
- HTML Stripper & Text Extractor
- Regex Tester & Pattern Builder
- Reading Time Calculator
- Keyword Density Analyzer

### 🔄 Converters (36 Tools)
- Base64, URL, ASCII, Unicode Converters
- JSON, YAML, XML, CSV Formatters
- HTML ↔ Text Converters
- SQL, CSS, JavaScript Formatters
- Number Base Converter (Binary, Hex, Oct)
- Roman Numeral Converter
- Morse Code & Binary Converters
- Unit Converters (Length, Weight, Temperature)
- Color Format Converters
- Timestamp & Timezone Converters

### ⚡ Generators (39 Tools)
- Secure Password & API Key Generators
- UUID & GUID Generators
- QR Code & Barcode Generators
- Lorem Ipsum & Fake Data Generators
- Random Name, Email, Username Generators
- Credit Card Number Generator (Testing)
- Random IP, MAC Address Generators
- Color Palette & Gradient Generators
- Placeholder Image Generator
- Random Quote & Fact Generators

### 🔒 Cryptography Tools (30 Tools)
- MD5, SHA-1, SHA-256, SHA-512 Hashing
- AES, DES, Blowfish Encryption
- JWT Token Decoder & Analyzer
- RSA Key Pair Generator
- BCrypt, SCrypt, PBKDF2 Hashing
- HMAC Generator & Digital Signatures
- SSL Certificate Analyzer
- Password Strength Checker
- OTP & TOTP Generators
- Entropy Calculator

### 🖼️ Image Tools (36 Tools)
- Image Resizer & Compressor
- Format Converter (PNG, JPG, WebP)
- Image Metadata Extractor
- Color Picker & Analyzer
- Brightness, Contrast, Saturation Adjusters
- Image Filters (Blur, Sharpen, Vintage)
- Image Effects (Sepia, Grayscale, Invert)
- Watermark & Border Tools
- Image Cropper & Rotator
- Histogram & Color Analysis

### 🌐 Web Tools (39 Tools)
- Meta Tag & SEO Analyzer
- SSL Certificate & Security Checker
- DNS Lookup & Propagation Checker
- WHOIS & Domain Information
- Page Speed & Performance Tester
- Broken Link & Redirect Checker
- HTTP Headers Analyzer
- HTML, CSS, JavaScript Validators
- Open Graph & Twitter Card Testers
- Accessibility & Mobile-Friendly Tester

### 📁 File Tools (30 Tools)
- File Hash Calculator (Multiple Algorithms)
- File Information & Metadata Extractor
- ZIP File Analyzer & Extractor
- File Compressor & Encryptor
- Duplicate File Finder
- Batch File Renamer & Organizer
- MIME Type & Encoding Detector
- File Permissions Analyzer
- Disk Usage Analyzer
- Log File Analyzer

### 💻 Developer Tools (36 Tools)
- Code Formatter & Minifier (Multiple Languages)
- Syntax Highlighter & Code Beautifier
- Regex Builder & Tester
- SQL Query Builder & Optimizer
- API Client & Tester
- JSON Path & XPath Builders
- .gitignore & License Generators
- README & Documentation Generators
- Variable & Function Name Generators
- Code Complexity Analyzer

### 📊 Data Tools (30 Tools)
- Data Validator & Cleaner
- CSV, JSON, XML Analyzers
- Data Merger & Splitter
- Statistical Analysis Tools
- Correlation Calculator
- Pivot Table Generator
- Data Profiler & Quality Checker
- Schema Generator
- ETL Script Generator
- Data Migration Helper

### 🧮 Math Tools (33 Tools)
- Basic & Scientific Calculators
- Matrix & Equation Solvers
- Statistics & Probability Calculators
- Prime Number Checker & Factorization
- GCD & LCM Calculators
- Percentage & Interest Calculators
- Loan & Mortgage Calculators
- Unit Circle & Trigonometry
- Number Base Converters
- Ratio & Proportion Calculators

### 🌐 Network Tools (30 Tools)
- IP Address & Subnet Calculators
- CIDR & Network Analyzers
- Port Scanner & Checker
- MAC Address Lookup
- Bandwidth & Latency Testers
- DNS Propagation Checker
- Email Validator & Domain Checker
- SSL/TLS Analyzer
- Network Security Scanner
- Firewall & Proxy Testers

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