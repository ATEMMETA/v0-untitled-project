import json
from flask import Flask, jsonify, request
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/api/connect_camera', methods=['POST'])
def connect_camera():
    try:
        request_data = request.get_data(as_text=True)
        print(f"Raw request data: {request_data}")
        data = json.loads(request_data)
        print(f"Parsed JSON data: {data}")
        if not data or 'ip' not in data:
            return jsonify({'error': 'Missing camera IP address'}), 400

        ip_address = data['ip']
        username = data.get('username', '')
        password = data.get('password', '')

        print(f"Attempting to connect to camera at: {ip_address} with user: {username}")

        rtsp_url = f"rtsp://{ip_address}:554/live/ch00_1"

        cap = None
        success = False
        error_message = ""

        try:
            cap = cv2.VideoCapture(rtsp_url)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None and frame.size > 0:
                    success = True
                    message = f'Successfully accessed video stream from {ip_address}'
                else:
                    error_message = f'Failed to read a frame from {ip_address}. Check stream or format.'
            else:
                error_message = f'Failed to open RTSP stream at {ip_address}. Check IP or path.'
        except Exception as e:
            error_message = f'Error connecting to camera: {str(e)}'
        finally:
            if cap and cap.isOpened():
                cap.release()

        if success:
            return jsonify({'success': True, 'message': message, 'rtsp_url': rtsp_url}), 200
        else:
            return jsonify({'success': False, 'error': error_message}), 400

    except Exception as e:
        return jsonify({'error': f"Error processing request: {str(e)}"}), 400

if __name__ == '__main__':
    app.run(debug=True)
