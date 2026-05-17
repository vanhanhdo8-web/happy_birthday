#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/scan-images':
            img_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 'style', 'img'
            )
            try:
                files = sorted([
                    f for f in os.listdir(img_dir)
                    if f.endswith(('.jpg', '.png', '.jpeg', '.gif', '.webp'))
                ])
            except FileNotFoundError:
                files = []
            import json
            body = json.dumps(files).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', len(body))
            self.end_headers()
            self.wfile.write(body)
        else:
            super().do_GET()

    def log_message(self, format, *args):
        print(f"{format % args}")

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_dir)

    if not os.path.isfile("index.html"):
        print("Không tìm thấy file index.html")
        sys.exit(1)

    port = int(os.environ.get('PORT', 10000))
    
    print(f"Server đang chạy trên cổng {port}")
    
    httpd = HTTPServer(('0.0.0.0', port), CustomHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    main()
