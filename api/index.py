from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

posts = [
    {'id': 1, 'title': 'Getting Started with Flask', 'content': 'Flask is a lightweight WSGI web application framework in Python.'},
    {'id': 2, 'title': 'Deploying to Vercel', 'content': 'Vercel makes it easy to deploy Python applications.'}
]

@app.route('/')
def home():
    return render_template('index.html', posts=posts)

@app.route('/api/posts')
def get_posts():
    return jsonify(posts)

@app.route('/api/posts/<int:post_id>')
def get_post(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if post:
        return jsonify(post)
    return jsonify({"error": "Post not found"}), 404

@app.route('/test_opencv', methods=['POST'])
def test_opencv():
    try:
        import cv2
        return jsonify({"status": "OpenCV imported successfully"})
    except ImportError as e:
        return jsonify({"status": "ImportError", "error": str(e)})
    except Exception as e:
        return jsonify({"status": "Error", "error": str(e)})

# Add this new route
@app.route('/api/hello', methods=['GET'])
def hello_world():
    return jsonify({'message': 'Hello from your Flask backend!'})

if __name__ == '__main__':
    app.run(debug=True)
