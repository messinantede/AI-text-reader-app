@echo off
echo Creating virtual environment...
py -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Setup complete! 
echo.
echo Starting the application...
py app.py

echo.
echo The application is running at http://localhost:5000
echo Press Ctrl+C to stop the server
