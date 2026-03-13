# Quick Start Guide

## 1️⃣ Setup (5 minutes)

### Windows:
1. Double-click `run-windows.bat`
2. The app will open automatically at `http://localhost:5000`

### Mac/Linux:
```bash
chmod +x run-unix.sh
./run-unix.sh
```

## 2️⃣ Configure Your Azure Credentials

1. Open `.env` in any text editor
2. Replace the placeholders with your Azure AI credentials:
   ```
   AI_SERVICE_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
   AI_SERVICE_KEY=your-api-key-here
   ```
3. Save the file
4. Restart the app if it was already running

## 3️⃣ Using the App

1. Open `http://localhost:5000` in your browser
2. Drag and drop an image or click to select one
3. Click "Process Image"
4. View extracted text and annotated image
5. Click "Copy Text" to copy the text

## File Structure

```
text-extraction-web-app/
├── app.py                    ← Flask server (don't edit unless needed)
├── requirements.txt          ← Python dependencies
├── .env                      ← Your Azure credentials (KEEP SECRET!)
├── README.md                 ← Full documentation
├── .gitignore                ← Git configuration
├── run-windows.bat           ← Start script for Windows
├── run-unix.sh               ← Start script for Mac/Linux
└── templates/
    └── index.html            ← Web interface (don't edit unless needed)
```

## Troubleshooting

**Error: "Azure AI Vision client not initialized"**
→ Check your `.env` file has correct credentials

**Error: "Module not found"**
→ Make sure you ran the setup script and it completed successfully

**Port 5000 already in use**
→ Change port 5000 to 5001 (or higher) in `app.py` line 62

**Want to stop the server?**
→ Press `Ctrl + C` in the terminal

## Next Steps

- See `README.md` for full documentation
- See deployment options in `README.md` to host on the web

## Need Help?

- Azure AI Vision docs: https://docs.microsoft.com/azure/cognitive-services/computer-vision/
- Flask docs: https://flask.palletsprojects.com/
