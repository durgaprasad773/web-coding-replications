# Web Coding Replication Backend

## Setup Instructions

1. **Create Virtual Environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Setup:**
   ```bash
   copy .env.example .env
   # Edit .env file and add your OpenAI API key
   ```

4. **Run the Application:**
   ```bash
   python app.py
   ```

The server will start on `http://localhost:5000`

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/token-usage` - Get current token usage statistics
- `POST /api/generate-replicas` - Generate code replicas
- `POST /api/download-excel` - Download results as Excel file
- `POST /api/download-json` - Download results as JSON file

## Features

- OpenAI GPT integration for code generation
- Token usage tracking
- Excel export functionality
- JSON export functionality
- CORS enabled for frontend integration