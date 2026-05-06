#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import time
from flask import Flask, send_from_directory, jsonify

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SUPPORTED_EXTENSIONS = ('.jpg', '.JPG', '.PNG', '.png',
                        '.jpeg', '.JPEG', '.gif', '.GIF',
                        '.webp', '.WEBP')

@app.route('/')
def index():
    """Phục vụ file index.html"""
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/<path:path>')
def serve_files(path):
    """Phục vụ các file tĩnh (CSS, JS, ảnh)"""
    return send_from_directory(BASE_DIR, path)

@app.route('/scan-images')
def scan_images():
    """Quét ảnh trong thư mục style/img"""
    img_dir = os.path.join(BASE_DIR, 'style', 'img')
    if not os.path.exists(img_dir):
        img_dir = os.path.join(BASE_DIR, 'img')

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
    print("🌐 Server đang chạy tại: http://localhost:8000/")
    app.run(host='127.0.0.1', port=8000, debug=False)  # ← đổi từ 0.0.0.0
