#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import time
import webbrowser
import socket
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

# ─────────────────────────────────────────
#  ANSI Colors
# ─────────────────────────────────────────
class C:
    RESET          = "\033[0m"
    BOLD           = "\033[1m"
    DIM            = "\033[2m"
    CYAN           = "\033[36m"
    YELLOW         = "\033[33m"
    BRIGHT_RED     = "\033[91m"
    BRIGHT_GREEN   = "\033[92m"
    BRIGHT_YELLOW  = "\033[93m"
    BRIGHT_BLUE    = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN    = "\033[96m"
    BRIGHT_WHITE   = "\033[97m"
    PINK           = "\033[38;5;213m"
    DEEP_RED       = "\033[38;5;196m"
    LIGHT_PINK     = "\033[38;5;218m"

WIDTH = 50

# ─────────────────────────────────────────
#  Pixel-art hearts
#  H = highlight  1 = on  0 = off
# ─────────────────────────────────────────
# Tim lúc khởi động (lớn)
HEART_LARGE = [
    "00HHH0HHH00",
    "0H11111111H0",
    "H111111111H",
    "111111111111",
    "111111111111",
    "0111111111110",
    "001111111100",
    "0001111100",
    "000011100",
    "0000010",
]

# Tim đập liên tục (nhỏ) — nhịp nhỏ
HEART_MINI_S = [
    "0H0H0",
    "11111",
    "11111",
    "01110",
    "00100",
]

# Tim đập liên tục (nhỏ) — nhịp lớn
HEART_MINI_L = [
    "0HH0HH0",
    "H11111H",
    "1111111",
    "0111110",
    "001110",
    "00100",
]

# Tim lúc khởi động (nhỏ — nhịp bé)
HEART_SMALL = [
    "0HH0HH0",
    "H11111H",
    "1111111",
    "0111110",
    "001110",
    "00100",
]

def term_width():
    try:
        return os.get_terminal_size().columns
    except Exception:
        return 80

def render_heart_lines(grid, on_color, hi_color):
    PIXEL = "██"
    EMPTY = "  "
    tw = term_width()
    cols = max(len(row) for row in grid)
    heart_w = cols * 2
    indent = " " * max(0, (tw - heart_w) // 2)
    lines = []
    for row in grid:
        line = indent
        for ch in row:
            if ch == 'H':
                line += hi_color + PIXEL + C.RESET
            elif ch == '1':
                line += on_color + PIXEL + C.RESET
            else:
                line += EMPTY
        lines.append(line.ljust(tw))
    return lines

# ─────────────────────────────────────────
#  Startup heart animation (chạy 1 lần)
# ─────────────────────────────────────────
def animate_heart_startup(beats=4):
    MAX_ROWS = len(HEART_LARGE) + 4
    print("\n" * MAX_ROWS, end="")
    for beat in range(beats):
        for grid, on_col, hi_col, label, hold in [
            (HEART_SMALL, C.PINK,     C.LIGHT_PINK, "dang khoi dong...", 0.18),
            (HEART_LARGE, C.DEEP_RED, C.LIGHT_PINK, "dang khoi dong...", 0.45),
        ]:
            lines = render_heart_lines(grid, on_col, hi_col)
            tw = term_width()
            sys.stdout.write(f"\033[{MAX_ROWS}A")
            pad = " " * max(0, (tw - len(label) - 4) // 2)
            print(pad + f"{on_col}{C.BOLD} ❤  {label} {C.RESET}")
            print()
            for line in lines:
                print(line)
            used = len(lines) + 2
            for _ in range(MAX_ROWS - used):
                print(" " * tw)
            sys.stdout.flush()
            time.sleep(hold)
        time.sleep(0.20)
    # Xóa
    sys.stdout.write(f"\033[{MAX_ROWS}A")
    tw = term_width()
    for _ in range(MAX_ROWS):
        print(" " * tw)
    sys.stdout.write(f"\033[{MAX_ROWS}A")
    sys.stdout.flush()

# ─────────────────────────────────────────
#  Live animation: tim nhỏ + mũi tên chỉ URL
# ─────────────────────────────────────────
TRAVEL_STEPS = 7   # số bước mũi tên di chuyển

def live_animation_loop(url, stop_event):
    """Chạy trong thread riêng, liên tục vẽ lại vùng animation."""

    MAX_HEART = len(HEART_MINI_L)   # 6 dòng
    TOTAL     = MAX_HEART + 4       # tim + khoảng + mũi tên + hint

    print("\n" * TOTAL, end="", flush=True)

    # Chuỗi nhịp tim: S S L L S S L L ...
    beat_seq  = [
        (HEART_MINI_S, C.PINK,     C.LIGHT_PINK, 0.18),
        (HEART_MINI_S, C.PINK,     C.LIGHT_PINK, 0.18),
        (HEART_MINI_L, C.DEEP_RED, C.LIGHT_PINK, 0.42),
        (HEART_MINI_L, C.DEEP_RED, C.LIGHT_PINK, 0.08),
    ]
    beat_i   = 0
    arrow_i  = 0  # vị trí mũi tên (0..TRAVEL_STEPS)

    while not stop_event.is_set():
        tw = term_width()

        grid, on_col, hi_col, hold = beat_seq[beat_i % len(beat_seq)]
        beat_i += 1
        lines = render_heart_lines(grid, on_col, hi_col)

        # --- Mũi tên ---
        step = arrow_i % (TRAVEL_STEPS + 2)
        arrow_i += 1

        if step < TRAVEL_STEPS:
            spaces = " " * step
            arrow_str  = f"{C.PINK}{spaces}►{C.RESET}"
            url_display = f"{C.BRIGHT_CYAN}{url}{C.RESET}"
        elif step == TRAVEL_STEPS:
            # Tới nơi — flash
            arrow_str   = f"{C.DEEP_RED}{C.BOLD}❯❯❯{C.RESET}"
            url_display = f"{C.BRIGHT_YELLOW}{C.BOLD}{url}{C.RESET}"
        else:
            # Reset — dòng trống 1 tick
            arrow_str   = " "
            url_display = f"{C.BRIGHT_CYAN}{url}{C.RESET}"

        # --- Vẽ lại ---
        sys.stdout.write(f"\033[{TOTAL}A")

        print()  # blank trên
        for line in lines:
            print(line)
        # Điền dòng thừa nếu tim nhỏ ít dòng hơn
        for _ in range(MAX_HEART - len(lines)):
            print(" " * tw)
        print()  # blank giữa

        # Dòng mũi tên
        arrow_line = f"  {arrow_str}  {url_display}"
        print(arrow_line.ljust(tw))

        # Hint
        hint = f"  {C.DIM}Nhan Ctrl+C de dung{C.RESET}"
        print(hint.ljust(tw))

        sys.stdout.flush()
        time.sleep(hold)

# ─────────────────────────────────────────
#  Box helpers
# ─────────────────────────────────────────
def box_line(text="", style=C.CYAN):
    inner = WIDTH - 2
    print(f"{style}│{C.RESET} {text.ljust(inner)} {style}│{C.RESET}")

def box_top(style=C.CYAN):
    print(f"{style}╔{'═' * WIDTH}╗{C.RESET}")

def box_mid(style=C.CYAN):
    print(f"{style}╠{'═' * WIDTH}╣{C.RESET}")

def box_bot(style=C.CYAN):
    print(f"{style}╚{'═' * WIDTH}╝{C.RESET}")

def spinner(label="Mo trinh duyet", duration=1.2):
    frames = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    end_t = time.time() + duration
    i = 0
    while time.time() < end_t:
        f = frames[i % len(frames)]
        print(f"\r  {C.BRIGHT_CYAN}{f}{C.RESET} {label}...", end="", flush=True)
        time.sleep(0.08)
        i += 1
    print("\r" + " " * 40 + "\r", end="", flush=True)

# ─────────────────────────────────────────
#  Banner
# ─────────────────────────────────────────
def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    art = [
        r"  ██╗  ██╗ █████╗ ██████╗ ██████╗ ██╗   ██╗",
        r"  ██║  ██║██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝",
        r"  ███████║███████║██████╔╝██████╔╝ ╚████╔╝ ",
        r"  ██╔══██║██╔══██║██╔═══╝ ██╔═══╝   ╚██╔╝  ",
        r"  ██║  ██║██║  ██║██║     ██║        ██║   ",
        r"  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝        ╚═╝   ",
    ]
    colors = [C.BRIGHT_MAGENTA, C.BRIGHT_CYAN, C.BRIGHT_YELLOW,
              C.BRIGHT_GREEN, C.BRIGHT_BLUE, C.BRIGHT_RED]
    print()
    for line, color in zip(art, colors):
        print(f"{color}{C.BOLD}{line}{C.RESET}")
        time.sleep(0.07)
    sub = "B I R T H D A Y  🎂"
    print(f"\n{C.BRIGHT_YELLOW}{C.BOLD}{sub.center(len(art[0]))}{C.RESET}\n")
    time.sleep(0.2)

# ─────────────────────────────────────────
#  Info box (bỏ path + "server đang chạy")
# ─────────────────────────────────────────
def print_info_box(url):
    print()
    box_top()
    box_line(f"🎉  Pham Thi Le - Happy Birthday!  🎉",
             style=C.BRIGHT_MAGENTA)
    box_mid()
    box_line(f"🌐  {C.BRIGHT_CYAN}{url}{C.RESET}", style=C.CYAN)
    box_bot()
    print()

# ─────────────────────────────────────────
#  Server
# ─────────────────────────────────────────
SUPPORTED_EXTENSIONS = ('.jpg', '.JPG', '.PNG', '.png',
                        '.jpeg', '.JPEG', '.gif', '.GIF',
                        '.webp', '.WEBP')

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def open_browser(url, delay=0.4):
    def _open():
        time.sleep(delay)
        webbrowser.open(url)
    threading.Thread(target=_open, daemon=True).start()

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/scan-images':
            img_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 'style', 'img'
            )
            try:
                files = sorted([
                    f for f in os.listdir(img_dir)
                    if f.endswith(SUPPORTED_EXTENSIONS)
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

# ─────────────────────────────────────────
#  Main
# ─────────────────────────────────────────
def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_dir)

    if not os.path.isfile("index.html"):
        print(f"\n{C.BRIGHT_RED}[LOI]{C.RESET} Khong tim thay file index.html!")
        input("Nhan Enter de dong...")
        sys.exit(1)

    print_banner()
    animate_heart_startup(beats=4)

    port = get_free_port()
    url  = f"http://localhost:{port}"

    print_info_box(url)

    open_browser(url, delay=0.4)
    spinner("Dang mo trinh duyet", duration=1.0)
    print(f"  {C.BRIGHT_GREEN}✓ Trinh duyet da mo!{C.RESET}\n")

    # Bắt đầu live animation trong thread riêng
    stop_event = threading.Event()
    anim_thread = threading.Thread(
        target=live_animation_loop,
        args=(url, stop_event),
        daemon=True
    )
    anim_thread.start()

    httpd = HTTPServer(('', port), CustomHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        stop_event.set()
        tw = term_width()
        # Xuống dưới vùng animation rồi in thông báo
        TOTAL = len(HEART_MINI_L) + 4
        print("\n" * TOTAL)
        print(f"\n  {C.BRIGHT_RED}✗{C.RESET} {C.YELLOW}Server da dung.{C.RESET}")
        httpd.server_close()
        print(f"  {C.DIM}Nhan Enter de dong...{C.RESET}")
        input()
        sys.exit(0)

if __name__ == "__main__":
    main()
