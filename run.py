#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import time
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler

# ─────────────────────────────────────────
#  Server handler
# ─────────────────────────────────────────
SUPPORTED_EXTENSIONS = ('.jpg', '.JPG', '.PNG', '.png',
                        '.jpeg', '.JPEG', '.gif', '.GIF',
                        '.webp', '.WEBP')

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/scan-images':
            # Tìm thư mục ảnh
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
            
            body = json.dumps(files).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', len(body))
            self.end_headers()
            self.wfile.write(body)
        else:
            super().do_GET()

    def log_message(self, format, *args):
        # In log đơn giản
        print(f"[{time.strftime('%H:%M:%S')}] {format % args}")

def main():
    # Chuyển đến thư mục chứa script
    root_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_dir)
    
    # Lấy port từ environment (Render) hoặc tự tìm
    port = int(os.environ.get('PORT', 8080))
    host = '0.0.0.0'
    
    # Kiểm tra index.html
    if not os.path.isfile("index.html"):
        print("Warning: index.html not found!")
    
    print("=" * 50)
    print("🎂 Happy Birthday - Pham Thi Le 🎂")
    print("=" * 50)
    print(f"Server running at: http://localhost:{port}")
    print(f"Host: {host}")
    print("=" * 50)
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    # Khởi động server
    httpd = HTTPServer((host, port), CustomHandler)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped")
        httpd.server_close()

if __name__ == "__main__":
    main()
