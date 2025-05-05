from flask import Flask, jsonify, request
import cv2  # Import OpenCV

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

    rtsp_url_no_auth = f"rtsp://{ip_address}:554/live" # Potential RTSP URL without auth

    try:
        cap_no_auth = cv2.VideoCapture(rtsp_url_no_auth)
        if cap_no_auth.isOpened():
            cap_no_auth.release()
            return jsonify({'success': True, 'rtsp_url': rtsp_url_no_auth, 'message': f'Successfully connected to camera at {ip_address} (no authentication)'}), 200
        else:
            # If no auth fails, try with provided credentials (if any)
            if username and password:
                rtsp_url_with_auth = f"rtsp://{username}:{password}@{ip_address}:554/live" # Example with auth
                cap_with_auth = cv2.VideoCapture(rtsp_url_with_auth)
                if cap_with_auth.isOpened():
                    cap_with_auth.release()
                    return jsonify({'success': True, 'rtsp_url': rtsp_url_with_auth, 'message': f'Successfully connected to camera at {ip_address} (with authentication)'}), 200
                else:
                    return jsonify({'success': False, 'error': f'Failed to open RTSP stream at {ip_address}. Check IP or credentials.'}), 400
            else:
                return jsonify({'success': False, 'error': f'Failed to open RTSP stream at {ip_address}. Ensure camera is on local network or provide credentials.'}), 400

    except Exception as e:
        return jsonify({'success': False, 'error': f'Error connecting to camera: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
