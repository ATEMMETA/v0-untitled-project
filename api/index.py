from flask import Flask, jsonify, request

app = Flask(__name__)

# ... (other routes) ...

@app.route('/api/connect_camera', methods=['POST'])
def connect_camera():
    return jsonify({'success': False, 'error': 'Testing a basic response'})


