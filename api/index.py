import cv2
from flask import Flask, jsonify

app = Flask(__name__)

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
        
