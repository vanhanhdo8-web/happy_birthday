from flask import Flask, send_from_directory, jsonify
import os

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/scan-images')
def scan_images():
    img_dir = os.path.join(os.path.dirname(__file__), 'style', 'img')
    try:
        files = sorted([f for f in os.listdir(img_dir) 
                       if f.endswith(('.jpg', '.png', '.jpeg', '.gif', '.webp'))])
    except FileNotFoundError:
        files = []
    return jsonify(files)

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
