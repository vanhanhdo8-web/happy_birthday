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
#  ANSI Colors & Styles
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
    GOLD           = "\033[38;5;220m"
    ORANGE         = "\033[38;5;208m"

WIDTH = 50

# ─────────────────────────────────────────
#  Hiệu ứng chuyển động đặc biệt
# ─────────────────────────────────────────

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def typing_effect(text, delay=0.03, color=C.BRIGHT_CYAN):
    """Hiệu chữ gõ từng chữ"""
    for char in text:
        sys.stdout.write(f"{color}{char}{C.RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def wave_effect(lines, color=C.BRIGHT_MAGENTA, wave_delay=0.05):
    """Hiệu ứng sóng cho text"""
    for line in lines:
        for i, char in enumerate(line):
            wave = int(abs((time.time() * 3) % 6 - 3))
            wave_color = f"\033[38;5;{200 + wave}m"
            sys.stdout.write(f"{wave_color}{char}{C.RESET}")
            sys.stdout.flush()
            time.sleep(wave_delay)
        print()
    time.sleep(0.3)

def bouncing_ball():
    """Hiệu ứng trái tim nhảy"""
    frames = [
        "  ❤️     ",
        "   ❤️    ",
        "    ❤️   ",
        "     ❤️  ",
        "      ❤️ ",
        "       ❤️",
        "      ❤️ ",
        "     ❤️  ",
        "    ❤️   ",
        "   ❤️    ",
        "  ❤️     ",
        " ❤️      ",
    ]
    for _ in range(2):
        for frame in frames:
            sys.stdout.write(f"\r{C.BRIGHT_RED}{C.BOLD}{frame}{C.RESET}")
            sys.stdout.flush()
            time.sleep(0.05)
    print()

def firework_effect():
    """Hiệu ứng pháo hoa ASCII"""
    fireworks = [
        ("  ✨  ", C.GOLD),
        (" ✨✨✨ ", C.BRIGHT_YELLOW),
        ("✨🎆✨🎆✨", C.BRIGHT_RED),
        (" ✨✨✨ ", C.BRIGHT_CYAN),
        ("  ✨  ", C.BRIGHT_MAGENTA),
    ]
    for i in range(3):
        for fw, color in fireworks:
            sys.stdout.write(f"\r{color}{fw.center(50)}{C.RESET}")
            sys.stdout.flush()
            time.sleep(0.1)
    print()

def rotating_loading(seconds=1.5):
    """Vòng tròn xoay loading"""
    chars = ["◐", "◓", "◑", "◒"]
    end_time = time.time() + seconds
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r  {C.BRIGHT_CYAN}{chars[i % 4]}{C.RESET} Dang khoi dong he thong...")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\r" + " " * 40 + "\r")

def pulse_heart(beats=3):
    """Trái tim đập chuyển động"""
    heart = [
        "  ┌─┐ ┌─┐  ",
        "─┘ ❤️ └─┘ ❤️ └─",
        "  └─────┘  ",
    ]
    
    for beat in range(beats):
        # Đập to
        for _ in range(3):
            sys.stdout.write("\033[F" * 3)
            for line in heart:
                print(f"{C.DEEP_RED}{C.BOLD}{line.center(60)}{C.RESET}")
            time.sleep(0.15)
        
        # Thu nhỏ
        heart_small = [h.replace("❤️", "💗") for h in heart]
        for _ in range(2):
            sys.stdout.write("\033[F" * 3)
            for line in heart_small:
                print(f"{C.PINK}{line.center(60)}{C.RESET}")
            time.sleep(0.12)
    
    # Clear
    sys.stdout.write("\033[F" * 3)
    for _ in range(3):
        print(" " * 60)

def matrix_rain():
    """Hiệu ứng mưa ký tự Matrix"""
    chars = "01❤️💗✨⭐"
    for _ in range(3):
        line = ""
        for _ in range(50):
            line += chars[int(time.time() * 20) % len(chars)]
        sys.stdout.write(f"\r{C.BRIGHT_GREEN}{line}{C.RESET}")
        sys.stdout.flush()
        time.sleep(0.05)
    print("\r" + " " * 50)

def countdown_animation():
    """Đếm ngược sinh động"""
    for i in range(5, 0, -1):
        clear_screen()
        print(f"\n\n\n{C.BRIGHT_YELLOW}{C.BOLD}{'⭐' * 20}{C.RESET}")
        print(f"\n{C.BRIGHT_MAGENTA}{C.BOLD}🎂 CHUẨN BỊ CHÀO MỪNG 🎂{C.RESET}")
        print(f"\n{C.BRIGHT_CYAN}{C.BOLD}{str(i).center(50)}{C.RESET}")
        print(f"\n{C.BRIGHT_YELLOW}{C.BOLD}{'⭐' * 20}{C.RESET}")
        
        # Tạo hiệu ứng countdown
        for _ in range(5):
            sys.stdout.write(f"\r{C.BRIGHT_RED}{'❤️' * (6 - i)}{C.RESET}")
            sys.stdout.flush()
            time.sleep(0.1)
        time.sleep(0.7)
    
    clear_screen()

def rainbow_text(text):
    """Chữ cầu vồng"""
    colors = [C.BRIGHT_RED, C.BRIGHT_YELLOW, C.BRIGHT_GREEN, C.BRIGHT_CYAN, C.BRIGHT_MAGENTA]
    result = ""
    for i, char in enumerate(text):
        result += colors[i % len(colors)] + char
    result += C.RESET
    return result

# ─────────────────────────────────────────
#  Pixel-art heart với animation
# ─────────────────────────────────────────
HEART_SMALL = [
    "0HH0HH0",
    "H111111H",
    "1111111",
    "0111110",
    "0011100",
    "0001000",
]

HEART_LARGE = [
    "00HHH0HHH00",
    "0H11111111H0",
    "H1111111111H",
    "111111111111",
    "111111111111",
    "0111111111110",
    "001111111100",
    "000111111000",
    "000011110000",
    "000001000000",
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
    indent = max(0, (tw - heart_w) // 2) * " "
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

def animate_heart(beats=5):
    MAX_ROWS = len(HEART_LARGE) + 4
    print("\n" * MAX_ROWS, end="")
    
    # Thêm hiệu ứng sparkle xung quanh
    sparkles = ["✨", "⭐", "💫", "🌟"]
    
    for beat in range(beats):
        for grid, on_col, hi_col, label, hold in [
            (HEART_SMALL, C.PINK, C.LIGHT_PINK, "💗 Đang khởi động... 💗", 0.2),
            (HEART_LARGE, C.DEEP_RED, C.LIGHT_PINK, "❤️ CHÀO MỪNG SINH NHẬT ❤️", 0.5),
        ]:
            lines = render_heart_lines(grid, on_col, hi_col)
            sys.stdout.write(f"\033[{MAX_ROWS}A")
            
            # Thêm sparkle random
            sparkle_line = "  " + " ".join(sparkles) + "  "
            print(f"{C.BRIGHT_YELLOW}{sparkle_line.center(term_width())}{C.RESET}")
            
            label_str = f"{on_col}{C.BOLD} {label} {C.RESET}"
            pad = " " * max(0, (term_width() - len(label) - 2) // 2)
            print(pad + label_str)
            print()
            
            for line in lines:
                print(line)
            
            used = len(lines) + 3
            for _ in range(MAX_ROWS - used):
                print(" " * term_width())
            sys.stdout.flush()
            time.sleep(hold)
        
        # Hiệu ứng rung nhẹ giữa các nhịp tim
        for _ in range(3):
            sys.stdout.write(f"\033[{MAX_ROWS}A")
            time.sleep(0.05)
    
    # Clear
    sys.stdout.write(f"\033[{MAX_ROWS}A")
    for _ in range(MAX_ROWS):
        print(" " * term_width())
    sys.stdout.write(f"\033[{MAX_ROWS}A")
    sys.stdout.flush()

# ─────────────────────────────────────────
#  Banner hoành tráng
# ─────────────────────────────────────────
def print_banner():
    clear_screen()
    
    # Hiệu ứng chữ xuất hiện dần
    print("\n" * 5)
    
    art_lines = [
        r"  ██╗  ██╗ █████╗ ██████╗ ██████╗ ██╗   ██╗",
        r"  ██║  ██║██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝",
        r"  ███████║███████║██████╔╝██████╔╝ ╚████╔╝ ",
        r"  ██╔══██║██╔══██║██╔═══╝ ██╔═══╝   ╚██╔╝  ",
        r"  ██║  ██║██║  ██║██║     ██║        ██║   ",
        r"  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝        ╚═╝   ",
    ]
    
    # Hiệu ứng gõ từng dòng
    for i, line in enumerate(art_lines):
        colors = [C.BRIGHT_MAGENTA, C.BRIGHT_CYAN, C.BRIGHT_YELLOW,
                  C.BRIGHT_GREEN, C.BRIGHT_BLUE, C.BRIGHT_RED]
        for char in line:
            sys.stdout.write(f"{colors[i]}{C.BOLD}{char}{C.RESET}")
            sys.stdout.flush()
            time.sleep(0.02)
        print()
        time.sleep(0.1)
    
    # Text chính với hiệu ứng cầu vồng
    print()
    birthday_text = "B I R T H D A Y   P A R T Y  🎂 🎉 🎈"
    rainbow_birthday = rainbow_text(birthday_text)
    print(rainbow_birthday.center(len(art_lines[0])))
    print()
    
    time.sleep(0.5)
    
    # Hiệu ứng pháo hoa
    firework_effect()
    time.sleep(0.3)

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

def box_sep(style=C.CYAN):
    print(f"{style}├{'─' * WIDTH}┤{C.RESET}")

def spinner(label="Mở trình duyệt", duration=1.4):
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
#  Info box
# ─────────────────────────────────────────
def print_info_box(url, root_dir):
    print()
    box_top(C.BRIGHT_MAGENTA)
    box_line(f"🎉  PHAM THI LE - HAPPY BIRTHDAY!  🎉",
             style=C.BRIGHT_MAGENTA)
    box_mid()
    box_line(f"🌐  {C.BRIGHT_CYAN}{url}{C.RESET}", style=C.CYAN)
    box_sep()
    box_line(f"📁  {C.DIM}{root_dir}{C.RESET}", style=C.CYAN)
    box_sep()
    box_line(f"✅  {C.BRIGHT_GREEN}Server đang chạy{C.RESET}", style=C.CYAN)
    box_line(f"🛑  {C.YELLOW}Nhấn Ctrl+C để dừng{C.RESET}", style=C.CYAN)
    box_bot(C.BRIGHT_MAGENTA)
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
#  Mở màn hoành tráng
# ─────────────────────────────────────────
def grand_opening():
    """Mở màn với hiệu ứng chuyển động đặc biệt"""
    
    # 1. Countdown + hiệu ứng
    countdown_animation()
    
    # 2. Matrix rain effect
    print(f"{C.BRIGHT_GREEN}{C.BOLD}🌧️  KHỞI TẠO VŨ TRỤ  🌧️{C.RESET}")
    matrix_rain()
    time.sleep(0.5)
    
    # 3. Trái tim nhảy
    print(f"{C.PINK}{C.BOLD}💓 TIM ĐẬP NHỊP SỐNG 💓{C.RESET}")
    bouncing_ball()
    time.sleep(0.3)
    
    # 4. Chữ xuất hiện với hiệu ứng sóng
    welcome_lines = [
        "✨  CHÀO MỪNG ĐẾN VỚI BỮA TIỆC  ✨",
        "🎂  SINH NHẬT PHẠM THỊ LÊ  🎂",
        "💝  NGÀY ĐẶC BIỆT NHẤT TRONG NĂM  💝"
    ]
    wave_effect(welcome_lines, C.BRIGHT_MAGENTA, 0.07)
    time.sleep(0.3)
    
    # 5. Hiệu ứng trái tim đập
    print(f"{C.DEEP_RED}{C.BOLD}❤️  MỞ MÀN ẤN TƯỢNG  ❤️{C.RESET}")
    pulse_heart(2)
    
    # 6. Loading với vòng tròn xoay
    rotating_loading(1.5)
    
    # 7. Chúc mừng với hiệu ứng gõ chữ
    print()
    typing_effect("🎉 Hẹn giờ khởi động hoàn tất! 🎉", 0.05, C.BRIGHT_YELLOW)
    typing_effect("🎈 Đang chuẩn bị điều bất ngờ cho bạn... 🎈", 0.05, C.PINK)
    time.sleep(0.5)

# ─────────────────────────────────────────
#  Main
# ─────────────────────────────────────────
def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_dir)

    if not os.path.isfile("index.html"):
        print(f"\n{C.BRIGHT_RED}[LỖI]{C.RESET} Không tìm thấy file index.html!")
        print(f"  Hãy đặt run.py cùng thư mục với index.html.\n")
        input("Nhấn Enter để đóng...")
        sys.exit(1)

    # MỞ MÀN HOÀNH TRÁNG
    grand_opening()
    
    # Banner chính
    print_banner()
    
    # Hiệu ứng trái tim sinh động
    animate_heart(beats=5)
    
    # Khởi chạy server
    port = get_free_port()
    url = f"http://localhost:{port}"
    
    print_info_box(url, root_dir)
    
    # Mở trình duyệt với hiệu ứng
    open_browser(url, delay=0.4)
    spinner("Đang mở trình duyệt", duration=1.2)
    
    # Thông báo cuối với hiệu ứng sparkle
    print(f"  {C.BRIGHT_GREEN}✨✨✨ TRÌNH DUYỆT ĐÃ MỞ! ✨✨✨{C.RESET}")
    print(f"  {C.BRIGHT_YELLOW}🎉 CHÚC MỪNG SINH NHẬT PHẠM THỊ LÊ! 🎉{C.RESET}\n")
    
    # Chạy server
    httpd = HTTPServer(('', port), CustomHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n\n  {C.BRIGHT_RED}✗{C.RESET} {C.YELLOW}Server đã dừng.{C.RESET}")
        print(f"  {C.PINK}Cảm ơn bạn đã sử dụng! 💝{C.RESET}")
        httpd.server_close()
        print(f"  {C.DIM}Nhấn Enter để đóng...{C.RESET}")
        input()
        sys.exit(0)

if __name__ == "__main__":
    main()
