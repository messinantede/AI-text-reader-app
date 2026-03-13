from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import base64
from io import BytesIO
from PIL import Image, ImageDraw
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize Azure AI Vision credentials
ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
ai_key = os.getenv('AI_SERVICE_KEY')

if not ai_endpoint or not ai_key:
    print("Warning: AI_SERVICE_ENDPOINT or AI_SERVICE_KEY not found in .env file")
else:
    if not ai_endpoint.endswith('/'):
        ai_endpoint = ai_endpoint + '/'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/extract-text', methods=['POST'])
def extract_text():
    try:
        # Check if credentials are available
        if not ai_endpoint or not ai_key:
            return jsonify({'error': 'Azure AI Vision client not initialized. Check your .env file.'}), 500

        # Get the uploaded file
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload an image.'}), 400

        # Read the image file
        image_data = file.read()
        
        # Call Azure Computer Vision API using REST
        headers = {
            'Ocp-Apim-Subscription-Key': ai_key,
            'Content-Type': 'application/octet-stream'
        }
        
        url = f"{ai_endpoint}vision/v3.2/read/analyzeImage"
        params = {
            'language': 'en'
        }
        
        response = requests.post(url, headers=headers, params=params, data=image_data)
        response.raise_for_status()
        
        result = response.json()

        # Extract text and coordinates
        extracted_text = ""
        text_data = []
        
        if 'regions' in result:
            for region in result['regions']:
                if 'lines' in region:
                    for line in region['lines']:
                        line_text = ' '.join([word['text'] for word in line['words']])
                        extracted_text += line_text + "\n"
                        
                        # Get bounding box
                        bbox_str = line['boundingBox']
                        bbox = parse_bounding_box(bbox_str)
                        
                        line_data = {
                            'text': line_text,
                            'bounding_box': bbox
                        }
                        text_data.append(line_data)

        # Create annotated image
        annotated_image_base64 = annotate_image(image_data, text_data)

        return jsonify({
            'success': True,
            'extracted_text': extracted_text.strip(),
            'annotated_image': annotated_image_base64,
            'text_data': text_data
        })

    except requests.exceptions.RequestException as ex:
        return jsonify({'error': f'Azure API Error: {str(ex)}'}), 500
    except Exception as ex:
        return jsonify({'error': f'Error processing image: {str(ex)}'}), 500


def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def parse_bounding_box(bbox_string):
    """Parse bounding box string format 'x,y,w,h' to coordinate list"""
    try:
        parts = bbox_string.split(',')
        if len(parts) == 4:
            x, y, w, h = map(int, parts)
            # Return as list of 4 corner points
            return [
                [x, y],           # top-left
                [x + w, y],       # top-right
                [x + w, y + h],   # bottom-right
                [x, y + h]        # bottom-left
            ]
    except:
        pass
    return []


def annotate_image(image_data, text_data):
    """Create annotated image with bounding boxes"""
    try:
        # Open image from bytes
        image = Image.open(BytesIO(image_data))
        draw = ImageDraw.Draw(image)
        
        # Draw bounding boxes
        color = 'cyan'
        width = 2
        
        for item in text_data:
            bbox = item['bounding_box']
            if len(bbox) >= 4:
                # Convert list of tuples to proper format for polygon
                points = [(int(x), int(y)) for x, y in bbox]
                draw.polygon(points, outline=color, width=width)
        
        # Convert back to base64
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return image_base64
    
    except Exception as ex:
        print(f"Error annotating image: {str(ex)}")
        return None


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)