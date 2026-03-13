#!/bin/bash

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Setup complete!"
echo ""
echo "Starting the application..."
python app.py

echo ""
echo "The application is running at http://localhost:5000"
echo "Press Ctrl+C to stop the server"
