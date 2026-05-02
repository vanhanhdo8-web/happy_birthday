#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import time
from flask import Flask, send_from_directory, jsonify

app = Flask(__name__)

SUPPORTED_EXTENSIONS = ('.jpg', '.JPG', '.PNG', '.png',
                        '.jpeg', '.JPEG', '.gif', '.GIF',
                        '.webp', '.WEBP')

@app.route('/')
def index():
    """Phục vụ file index.html"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_files(path):
    """Phục vụ các file tĩnh (CSS, JS, ảnh)"""
    return send_from_directory('.', path)

@app.route('/scan-images')
def scan_images():
    """Quét ảnh trong thư mục style/img"""
    img_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'style', 'img'
    )
    if not os.path.exists(img_dir):
        img_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'img'
        )
    
    try:
        if os.path.exists(img_dir):
            files = sorted([
                f for f in os.listdir(img_dir)
                if f.endswith(SUPPORTED_EXTENSIONS)
            ])
        else:
            files = []
    except Exception:
        files = []
    
    return jsonify(files)

# Chạy server (chỉ dùng khi chạy bằng python, không dùng cho gunicorn)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
