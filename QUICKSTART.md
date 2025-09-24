# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Setup (One-time)
**Windows:**
```bash
# Run the setup script
setup.bat
```

**Manual Setup:**
```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
cp .env.example .env

# Frontend
cd ../frontend
npm install
```

### Step 2: Configure API Key
Edit `backend/.env` file:
```
OPENAI_API_KEY=your_actual_api_key_here
```

### Step 3: Run the Application
**Windows:**
```bash
# Terminal 1: Start Backend
start-backend.bat

# Terminal 2: Start Frontend
start-frontend.bat
```

**Manual:**
```bash
# Terminal 1: Backend
cd backend
venv\Scripts\activate     # Windows
source venv/bin/activate  # macOS/Linux
python app.py

# Terminal 2: Frontend
cd frontend
npm run dev
```

## 📱 Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000

## 🎯 Usage Flow
1. Upload your JSON file (see `sample-data.json` for format)
2. Select replica type (Web Coding or Responsive)
3. Choose number of replicas (1-5)
4. Generate and download results

## 🆘 Troubleshooting

**Backend won't start:**
- Check if Python 3.8+ is installed
- Verify OpenAI API key in `.env` file
- Ensure virtual environment is activated

**Frontend won't start:**
- Check if Node.js 18+ is installed
- Run `npm install` in frontend directory
- Clear npm cache: `npm cache clean --force`

**Generation fails:**
- Verify OpenAI API key has credits
- Check JSON format matches expected structure
- Review browser console for errors

## 📊 Expected Input Format
```json
{
  "question_text": "Your question description...",
  "short_text": "Brief title",
  "solutions_metadata": [{ 
    "code_details": [
      {"language": "HTML", "code_data": "..."},
      {"language": "CSS", "code_data": "..."},
      {"language": "JAVASCRIPT", "code_data": "..."}
    ]
  }],
  "test_cases": [
    {
      "id": "test-1",
      "display_text": "Test description",
      "criteria": "test function code",
      "order": 1,
      "weightage": 10
    }
  ]
}
```

## 💡 Tips
- Start with 1-2 replicas for testing
- Monitor token usage in the top-right corner
- Use the sample-data.json as a template
- Download results in both Excel and JSON formats for backup