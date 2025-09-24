@echo off
echo Setting up Web Coding Replication Project...
echo.

echo Setting up Backend...
cd backend
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
copy .env.example .env
echo Backend setup complete!
echo.
echo Please edit backend\.env file and add your OpenAI API key
echo.

cd..
echo Setting up Frontend...
cd frontend
npm install
echo Frontend setup complete!
echo.

echo Setup complete! 
echo.
echo Next steps:
echo 1. Edit backend\.env file and add your OpenAI API key
echo 2. Run 'start-backend.bat' to start the backend server
echo 3. Run 'start-frontend.bat' to start the frontend server
echo.
pause