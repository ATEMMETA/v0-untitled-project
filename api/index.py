from flask import Flask, jsonify, request
import cv2  # Import OpenCV

app = Flask(__name__)

# ... (other routes) ...

@app.route('/api/connect_camera', methods=['POST'])
def connect_camera():
    data = request.get_json()
    if not data or 'ip' not in data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing camera details'}), 400

    ip_address = data['ip']
    username = data['username']
    password = data['password']
    wifi_ssid = data.get('wifi_ssid', '')
    wifi_password = data.get('wifi_password', '')

    print(f"Attempting to connect to camera at: {ip_address} with user: {username}")
    print(f"Wi-Fi SSID: {wifi_ssid}, Password: {wifi_password}")

    rtsp_url = f"rtsp://{username}:{password}@{ip_address}:554/live" # Example RTSP URL format - adjust as needed

    try:
        cap = cv2.VideoCapture(rtsp_url)
        if cap.isOpened():
            cap.release()
            return jsonify({'success': True, 'rtsp_url': rtsp_url, 'message': f'Successfully connected to camera at {ip_address}'}), 200
        else:
            return jsonify({'success': False, 'error': f'Failed to open RTSP stream at {rtsp_url}. Check credentials or URL.'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error connecting to camera: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
