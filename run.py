#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import webbrowser
import socket
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def open_browser(url):
    webbrowser.open(url)

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
        pass

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_dir)

    if not os.path.isfile("index.html"):
        print("\n  Không tìm thấy file index.html")
        input("Nhấn Enter để thoát...")
        sys.exit(1)

    port = get_free_port()
    url = f"http://localhost:{port}"

    print(f"\n  Đang chạy web tại: {url}")
    print("  Nhấn Ctrl+C để dừng server\n")

    threading.Timer(0.5, open_browser, args=[url]).start()

    httpd = HTTPServer(('', port), CustomHandler)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  Đã dừng server.\n")
        httpd.shutdown()

if __name__ == "__main__":
    main()
