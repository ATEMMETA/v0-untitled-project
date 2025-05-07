from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS
import cv2

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins (for testing)

@app.route('/api/test_opencv')
def test_opencv():
    try:
        cap = cv2.VideoCapture(0)  # Try opening the default camera (index 0)
        if cap.isOpened():
            cap.release()
            return jsonify({'success': True, 'message': 'OpenCV VideoCapture works'})
        else:
            return jsonify({'success': False, 'message': 'OpenCV VideoCapture failed'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'OpenCV error: {str(e)}'})
        
