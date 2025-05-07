from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import cv2

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://html-starter-sigma-vert.vercel.app"}})

@app.route('/api/connect_camera', methods=['POST'])
def connect_camera():
    try:
        data = request.get_json()
        if not data or 'ip' not in data:
            return jsonify({'error': 'Missing camera IP address'}), 400

        ip_address = data['ip']
        username = data.get('username', '')
        password = data.get('password', '')

        rtsp_url = f"rtsp://{username}:{password}@{ip_address}:554/live/ch00_1" if username and password else f"rtsp://{ip_address}:554/live/ch00_1"
        print(f"Attempting to connect to: {rtsp_url}")

        cap = cv2.VideoCapture(rtsp_url)
        success = cap.isOpened()
        error_message = "" if success else f"Failed to open RTSP stream at {ip_address}. Check IP, credentials, or path."

        if cap:
            cap.release()

        if success:
            return jsonify({'success': True, 'message': f'Successfully accessed stream from {ip_address}', 'rtsp_url': rtsp_url}), 200
        else:
            return jsonify({'success': False, 'error': error_message}), 400

    except Exception as e:
        return jsonify({'error': f"Error processing request: {str(e)}"}), 400

if __name__ == '__main__':
    app.run(debug=True)
