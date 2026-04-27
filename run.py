#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import webbrowser
import socket
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def open_browser(url, delay=1.5):
    def _open():
        import time
        time.sleep(delay)
        webbrowser.open(url)
    threading.Thread(target=_open, daemon=True).start()

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/scan-images':
            img_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'style', 'img')
            try:
                files = sorted([
                    f for f in os.listdir(img_dir)
                    if f.lower().endswith('.jpg')
                ])
            except FileNotFoundError:
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
        pass

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_dir)

    if not os.path.isfile("index.html"):
        print("=" * 45)
        print("  [LOI] Khong tim thay file index.html!")
        print("  Hay dat run.py cung thu muc voi index.html")
        print("=" * 45)
        input("\nNhan Enter de dong...")
        sys.exit(1)

    port = get_free_port()
    url = f"http://localhost:{port}"

    print("=" * 45)
    print("        HAPPY BIRTHDAY - Phạm Thị Lệ !")
    print("   Chúc bạn có một ngày sinh nhật vui vẻ !")
    print("=" * 45)
    print(f"  Dia chi : {url}")
    print(f"  Thu muc : {root_dir}")
    print()
    print("  Trinh duyet se tu dong mo...")
    print("  Nhan Ctrl+C de dung server.")
    print("=" * 45)

    open_browser(url)

    httpd = HTTPServer(('', port), CustomHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  Dã dừng server.")
        httpd.server_close()
        input("Nhấn Enter dể dóng...")
        sys.exit(0)

if __name__ == "__main__":
    main()
