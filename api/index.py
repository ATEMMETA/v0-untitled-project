from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Sample data (in a real app, you'd use a database)
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
