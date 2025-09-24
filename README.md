# Web Coding Replication Project

A comprehensive full-stack application for generating unique replicas of HTML/CSS/JS coding questions while preserving functionality and test cases.

## 🚀 Features

- **Dual Mode Generation**: 
  - **Web Coding**: Full HTML + CSS + JavaScript replicas
  - **Responsive**: HTML + CSS only replicas
- **Smart Detection**: Automatically detects question type based on code content
- **Token Tracking**: Real-time monitoring of OpenAI API usage and costs
- **Multiple Export Formats**: Download results as Excel or JSON
- **Interactive UI**: Modern React-based interface with drag-and-drop file upload
- **Validation**: Comprehensive JSON validation for uploaded files

## 🏗️ Architecture

### Backend (Python Flask)
- **OpenAI Integration**: GPT-3.5-turbo for intelligent code generation
- **LangChain**: Advanced prompt engineering and chain management
- **Token Tracking**: Accurate usage monitoring with tiktoken
- **Export Functions**: Excel and JSON generation
- **CORS Enabled**: Frontend-backend communication

### Frontend (React + Vite)
- **Modern UI**: TailwindCSS for responsive design
- **File Upload**: Drag-and-drop with validation
- **Real-time Updates**: Token usage tracking
- **Progressive Steps**: Guided workflow
- **Error Handling**: Comprehensive error messages

## 📋 Prerequisites

- Python 3.8+
- Node.js 18+
- OpenAI API key

## 🛠️ Installation

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   copy .env.example .env  # Windows
   cp .env.example .env    # macOS/Linux
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

5. **Run the backend:**
   ```bash
   python app.py
   ```
   
   Backend will start on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```
   
   Frontend will start on `http://localhost:3000`

## 📊 Usage

1. **Upload JSON**: Drag and drop your coding question JSON file
2. **Configure**: Select replica type (Web Coding/Responsive) and number of replicas
3. **Generate**: AI creates unique replicas while preserving functionality
4. **Download**: Export results in Excel or JSON format

### Expected JSON Format

```json
{
  "question_text": "Create a chocolate calculator application...",
  "short_text": "Chocolate Calculator",
  "solutions_metadata": [{
    "code_details": [
      {
        "default_code": true,
        "code_data": "<!DOCTYPE html>...",
        "language": "HTML"
      },
      {
        "default_code": true,
        "code_data": "body { ... }",
        "language": "CSS"
      },
      {
        "default_code": true,
        "code_data": "document.getElementById...",
        "language": "JAVASCRIPT"
      }
    ]
  }],
  "test_cases": [
    {
      "id": "test-1",
      "display_text": "Test case description",
      "criteria": "function test() { ... }",
      "order": 1,
      "weightage": 10
    }
  ]
}
```

## 🔧 API Endpoints

- `GET /api/health` - Health check
- `GET /api/token-usage` - Token usage statistics
- `POST /api/generate-replicas` - Generate code replicas
- `POST /api/download-excel` - Download Excel file
- `POST /api/download-json` - Download JSON file

## 💰 Token Usage & Costs

The application tracks:
- **Session Tokens**: Current session usage
- **Total Tokens**: Cumulative usage
- **Estimated Cost**: Based on GPT-3.5-turbo pricing (~$0.002/1K tokens)

## 🎨 Replica Generation Features

Each replica includes:
- **Unique Visual Themes**: Different color schemes, typography, and styling
- **Contextual Content**: Domain-appropriate labels and descriptions
- **Preserved Functionality**: All JavaScript logic and interactions maintained
- **Updated Test Cases**: Modified to match new context while testing same logic
- **Complete Code**: HTML, CSS, and JavaScript solutions

## 🔄 Development

### Backend Development
```bash
cd backend
python app.py  # Runs with auto-reload in debug mode
```

### Frontend Development
```bash
cd frontend
npm run dev  # Hot reload enabled
```

### Building for Production
```bash
cd frontend
npm run build
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

If you encounter any issues:
1. Check the console logs for detailed error messages
2. Verify your OpenAI API key is correctly configured
3. Ensure all dependencies are properly installed
4. Review the expected JSON format for uploads

## 🔮 Future Enhancements

- Support for additional programming languages
- Batch processing for multiple files
- Custom prompt templates
- Advanced styling options
- Integration with learning management systems