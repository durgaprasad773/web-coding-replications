@echo off
echo Starting Backend Server...
cd backend

echo Checking if .env file exists...
if not exist .env (
    echo ERROR: .env file not found!
    echo Please copy .env.example to .env and add your OpenAI API key
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Starting Flask application...
python app.py