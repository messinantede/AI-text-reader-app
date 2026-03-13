# Text Extraction Web App

A modern web application for extracting text from images using Azure AI Vision API. Upload images through a user-friendly web interface to extract and annotate text with bounding boxes.

## Features

- 🖼️ **Drag-and-drop file upload** or click to select
- 📝 **Text extraction** using Azure AI Vision
- 🎯 **Automatic annotation** with bounding boxes around detected text
- 📋 **Copy text** button for easy copying
- 💻 **Works locally** and can be deployed to the web
- 📱 **Responsive design** for desktop and tablet viewing
- ⚡ **Real-time processing** with loading indicators

## Prerequisites

- Python 3.8 or higher
- An Azure AI Services account with Computer Vision API enabled
- Your Azure AI endpoint and key

## Local Setup

### 1. Clone or Download the Project

```bash
cd your-project-directory
```

### 2. Create a Virtual Environment (Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Azure Credentials

Edit the `.env` file and add your Azure AI Services credentials:

```
AI_SERVICE_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AI_SERVICE_KEY=your-api-key-here
FLASK_ENV=development
```

To get your Azure credentials:
1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your Computer Vision resource
3. Copy the **Endpoint** and **Key** from the Keys and Endpoint section

### 5. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### 6. Use the Application

1. Open your browser and go to `http://localhost:5000`
2. Drag and drop an image or click to select one
3. Click "Process Image" to extract text
4. View the extracted text and annotated image in the results panel
5. Use the "Copy Text" button to copy extracted text to clipboard

## Project Structure

```
project-folder/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── .env                   # Configuration file (add your credentials here)
└── templates/
    └── index.html         # Web interface
```

## Deployment to Web

### Option 1: Deploy to Heroku

1. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

2. Create a `Procfile` in the root directory:
```
web: gunicorn app:app
```

3. Add gunicorn to requirements.txt:
```bash
pip install gunicorn
pip freeze > requirements.txt
```

4. Create a Heroku app:
```bash
heroku create your-app-name
```

5. Set environment variables:
```bash
heroku config:set AI_SERVICE_ENDPOINT=your_endpoint
heroku config:set AI_SERVICE_KEY=your_key
```

6. Deploy:
```bash
git push heroku main
```

### Option 2: Deploy to Azure App Service

1. Install [Azure CLI](https://docs.microsoft.com/cli/azure/install-azure-cli)

2. Create a resource group:
```bash
az group create --name myResourceGroup --location eastus
```

3. Create an App Service plan:
```bash
az appservice plan create --name myAppServicePlan --resource-group myResourceGroup --sku B1 --is-linux
```

4. Create the web app:
```bash
az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name your-app-name --runtime "PYTHON|3.9"
```

5. Configure deployment:
```bash
az webapp deployment user set --user-name <username> --password <password>
az webapp deployment source config-local-git --name your-app-name --resource-group myResourceGroup
```

6. Set environment variables:
```bash
az webapp config appsettings set --resource-group myResourceGroup --name your-app-name --settings AI_SERVICE_ENDPOINT=your_endpoint AI_SERVICE_KEY=your_key
```

### Option 3: Deploy to AWS (Elastic Beanstalk)

1. Install [AWS EB CLI](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html)

2. Initialize Elastic Beanstalk:
```bash
eb init -p python-3.9 your-app-name --region us-east-1
```

3. Create an environment:
```bash
eb create your-env-name
```

4. Set environment variables:
```bash
eb setenv AI_SERVICE_ENDPOINT=your_endpoint AI_SERVICE_KEY=your_key
```

5. Deploy:
```bash
eb deploy
```

## Supported Image Formats

- PNG (.png)
- JPEG/JPG (.jpg, .jpeg)
- GIF (.gif)
- BMP (.bmp)
- TIFF (.tiff)

## File Size Limit

- Maximum file size: 16 MB

## Troubleshooting

### "Azure AI Vision client not initialized"
- Check that your `.env` file exists in the same directory as `app.py`
- Verify that `AI_SERVICE_ENDPOINT` and `AI_SERVICE_KEY` are correctly set
- Ensure your Azure credentials are valid and the Computer Vision API is enabled

### "No module named 'flask'"
- Make sure you've activated the virtual environment
- Run `pip install -r requirements.txt`

### Port 5000 is already in use
- Change the port in `app.py` by modifying the last line:
```python
app.run(debug=True, host='127.0.0.1', port=5001)  # Change 5001 to any available port
```

### CORS issues in production
- Add Flask-CORS to handle cross-origin requests:
```bash
pip install flask-cors
```

Then update `app.py`:
```python
from flask_cors import CORS
CORS(app)
```

## API Endpoints

### POST /api/extract-text
Extract text from an uploaded image

**Request:**
- Content-Type: multipart/form-data
- File: image file

**Response:**
```json
{
  "success": true,
  "extracted_text": "Text extracted from image...",
  "annotated_image": "base64_encoded_image",
  "text_data": [
    {
      "text": "Line of text",
      "bounding_box": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    }
  ]
}
```

## Performance Tips

- Compress images before uploading for faster processing
- Use JPG format for photograph-like images
- Use PNG for images with text and graphics
- Keep image resolution reasonable (max 4096x4096 pixels)

## Security Considerations

- Never commit the `.env` file with real credentials to version control
- Add `.env` to `.gitignore`:
```
.env
__pycache__/
venv/
*.pyc
```

- In production, use environment variables instead of .env files
- Enable HTTPS on your deployment
- Rate limit API requests if needed

## License

This project uses Azure AI Vision services. Refer to Azure's terms of service and pricing.

## Support

For issues with Azure AI Vision API, visit the [Azure documentation](https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/)
