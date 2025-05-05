from flask import Flask, jsonify, request
import cv2  # Import OpenCV
import numpy as np  # Import NumPy for handling frames

app = Flask(__name__)

# ... (other routes) ...

@app.route('/api/connect_camera', methods=['POST'])
def connect_camera():
    data = request.get_json()
    if not data or 'ip' not in data:
        return jsonify({'error': 'Missing camera IP address'}), 400

    ip_address = data['ip']
    username = data.get('username', '')
    password = data.get('password', '')

    print(f"Attempting to connect to camera at: {ip_address} with user: {username}")

    rtsp_url_no_auth = f"rtsp://{ip_address}:554/live/ch00_1"

    cap = None
    success = False
    error_message = ""

    try:
        cap = cv2.VideoCapture(rtsp_url_no_auth)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None and frame.size > 0:
                success = True
                message = f'Successfully accessed video stream from {ip_address} (no authentication)'
            else:
                error_message = f'Failed to read a frame from {ip_address} (no authentication). Check stream or format.'
        else:
            if username and password:
                rtsp_url_with_auth = f"rtsp://{username}:{password}@{ip_address}:554/live/ch00_1"
                cap_auth = cv2.VideoCapture(rtsp_url_with_auth)
                if cap_auth.isOpened():
                    ret_auth, frame_auth = cap_auth.read()
                    if ret_auth and frame_auth is not None and frame_auth.size > 0:
                        success = True
                        message = f'Successfully accessed video stream from {ip_address} (with authentication)'
                        if cap:
                            cap.release() # Release the no-auth capture
                        cap = cap_auth
                    else:
                        error_message = f'Failed to read a frame from {ip_address} (with authentication). Check stream or format.'
                        if cap_auth:
                            cap_auth.release()
                else:
                    error_message = f'Failed to open RTSP stream at {ip_address}. Check IP, path, or credentials.'
            else:
                error_message = f'Failed to open RTSP stream at {ip_address}. Ensure camera is on local network and the RTSP path is correct.'
    except Exception as e:
        error_message = f'Error connecting to camera: {str(e)}'
    finally:
        if cap and success:
            cap.release()

    if success:
        return jsonify({'success': True, 'message': message, 'rtsp_url': rtsp_url_no_auth if not username else rtsp_url_with_auth}), 200
    else:
        return jsonify({'success': False, 'error': error_message}), 400

if __name__ == '__main__':
    app.run(debug=True)
