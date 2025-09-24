# Deployment Guide

## Python Version Compatibility

### Recommended Python Versions (in order of preference):
1. **Python 3.11.x** - Best compatibility with all packages
2. **Python 3.10.x** - Excellent compatibility 
3. **Python 3.9.x** - Good compatibility (older but stable)

### Avoid:
- **Python 3.13.x** - Too new, packages may not have wheels available
- **Python 3.8.x** - End of life support

## Installation Commands

### Option 1: Use Python 3.11 (Recommended)
```bash
# Create virtual environment with Python 3.11
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Option 2: If requirements.txt fails, use minimal version
```bash
pip install -r requirements-minimal.txt
```

### Option 3: Manual installation for problematic packages
```bash
# Install packages one by one to identify issues
pip install flask==2.3.3
pip install flask-cors==4.0.0
pip install openai==0.28.1
pip install python-dotenv==1.0.0
pip install tiktoken==0.5.1

# Install pandas with pre-compiled wheels
pip install --only-binary=all pandas==2.0.3
pip install openpyxl==3.1.2

# Skip langchain if it causes issues (app works without it)
# pip install langchain==0.0.292
```

## Deployment Platforms

### Heroku
- Use `runtime.txt` file with `python-3.11.9`
- Heroku supports Python 3.11.x well

### Railway/Render
- Specify Python version in settings
- Use Python 3.11.x for best results

### DigitalOcean/AWS/GCP
- Use Python 3.11 or 3.10 in your Dockerfile
- Pre-install build tools if needed

## Troubleshooting

### If pandas installation hangs:
```bash
# Try installing with pre-compiled wheels only
pip install --only-binary=all pandas

# Or use a lighter version
pip install pandas==2.0.3
```

### If langchain causes issues:
The app works without langchain. Comment out the langchain import in app.py:
```python
# from langchain.llms import OpenAI
# from langchain.prompts import PromptTemplate  
# from langchain.chains import LLMChain
```

## Environment Variables
Make sure to set:
- `OPENAI_API_KEY` - Your OpenAI API key
- `FLASK_ENV=production` (for production deployment)
- `FLASK_DEBUG=False` (for production deployment)