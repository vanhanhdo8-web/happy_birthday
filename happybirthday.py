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
#  Màu sắc
# ─────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    PINK    = "\033[38;5;213m"
    ORANGE  = "\033[38;5;208m"
    GOLD    = "\033[38;5;220m"

# ─────────────────────────────────────────
#  Tiện ích
# ─────────────────────────────────────────

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def type_text(text, color=C.CYAN, delay=0.07):
    for char in text:
        sys.stdout.write(f"{color}{char}{C.RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def move_text(text, color=C.PINK, steps=20):
    for i in range(steps):
        sys.stdout.write("\r" + " " * i + f"{color}{text}{C.RESET}")
        sys.stdout.flush()
        time.sleep(0.07)   # chậm hơn so với 0.03 cũ
    print()

# ─────────────────────────────────────────
#  Đếm ngược 3 - 2 - 1
# ─────────────────────────────────────────

BIG_3 = [
    "  ██████╗ ",
    "       ╚═╝",
    "   ████╗  ",
    "       ██╗",
    "  ██████╝ ",
]
BIG_2 = [
    "  ██████╗ ",
    "       ██╗",
    "   █████╝ ",
    "  ██╔════ ",
    "  ███████╗",
]
BIG_1 = [
    "   ██╗ ",
    "  ███╗ ",
    "   ██╗ ",
    "   ██╗ ",
    "  ████╗",
]
BIG_GO = [
    "   ██████╗  ██████╗ ",
    "  ██╔════╝ ██╔═══██╗",
    "  ██║  ███╗██║   ██║",
    "  ██║   ██║██║   ██║",
    "  ╚██████╔╝╚██████╔╝",
    "   ╚═════╝  ╚═════╝ ",
]

def countdown_intro():
    msgs = [
        (3, BIG_3, C.GOLD,   "Chuẩn bị nhé..."),
        (2, BIG_2, C.ORANGE, "Sắp đến rồi..."),
        (1, BIG_1, C.PINK,   "Còn 1 giây nữa thôi!"),
    ]
    for n, big, color, sub in msgs:
        clear_screen()
        print()
        print(f"{C.CYAN}{'─' * 44}{C.RESET}")
        print(f"{C.WHITE}{'🎂  SINH NHẬT PHẠM THỊ LỆ  🎂':^44}{C.RESET}")
        print(f"{C.CYAN}{'─' * 44}{C.RESET}")
        print()
        for line in big:
            print(f"{color}{line:^44}{C.RESET}")
        print()
        print(f"{C.MAGENTA}{sub:^44}{C.RESET}")
        print()

        # Thanh tiến trình — chậm hơn (0.13s/ô)
        dots = 12
        for i in range(dots):
            bar = "█" * (i + 1) + "░" * (dots - i - 1)
            sys.stdout.write(f"\r  {color}[{bar}]{C.RESET}")
            sys.stdout.flush()
            time.sleep(0.13)
        time.sleep(0.8)

    # Màn hình GO!
    clear_screen()
    print()
    for line in BIG_GO:
        print(f"{C.PINK}{line:^44}{C.RESET}")
    print()
    print(f"{C.YELLOW}{'✨ HAPPY BIRTHDAY! ✨':^44}{C.RESET}")
    time.sleep(1.5)

# ─────────────────────────────────────────
#  Hoạt cảnh bánh sinh nhật
# ─────────────────────────────────────────

CAKE_FRAMES = [
    # Frame 0 – bánh chưa có nến
    (C.YELLOW, [
        "                                  ",
        "      |   |   |   |   |          ",
        "      |   |   |   |   |          ",
        "   ___________________________   ",
        "  /  H  A  P  P  Y   B  D  ! \\  ",
        "  \\___________________________/  ",
        "   |_________________________|   ",
        "                                  ",
    ], "  Chiếc bánh sinh nhật đang chờ...  "),

    # Frame 1 – nến bắt đầu thắp
    (C.ORANGE, [
        "     *       *       *       *    ",
        "     |   .   |   .   |   .   |   ",
        "     |   |   |   |   |   |   |   ",
        "   ___________________________   ",
        "  /  H  A  P  P  Y   B  D  ! \\  ",
        "  \\___________________________/  ",
        "   |_________________________|   ",
        "                                  ",
    ], "  Nến đang được thắp lên...         "),

    # Frame 2 – nến cháy sáng
    (C.GOLD, [
        "    (*)     (*)     (*)     (*)   ",
        "     |   ( )|   ( )|   ( )|   () ",
        "     |   |   |   |   |   |   |   ",
        "   ___________________________   ",
        "  /~~H~~A~~P~~P~~Y~~~B~~D~~!~~\\  ",
        "  \\___________________________/  ",
        "   |_________________________|   ",
        "                                  ",
    ], "  Nến đã sáng rực rỡ!               "),

    # Frame 3 – pháo hoa nhỏ
    (C.PINK, [
        "  *  . (*)* .  (*) *  .(*) *  .  ",
        "  .   * | * .   |  * . | *  .    ",
        "    .   |   .   |   .  |   .     ",
        "   ___________________________   ",
        "  ( ~H~~A~~P~~P~~Y~~~B~~D~~!~ )  ",
        "  (___________________________/  ",
        "   |_________________________|   ",
        "        *    .    *    .         ",
    ], "  Chúc mừng sinh nhật!!!            "),

    # Frame 4 – bùng nổ
    (C.MAGENTA, [
        " * . * (*)* . * (*) * .(*)* . *  ",
        "  * .  *|* .   *|*  . *|  * .   ",
        "  . *   |  * .  |  * . |  * .   ",
        "   ___________________________   ",
        "  < ~H~~A~~P~~P~~Y~~~B~~D~~!~ >  ",
        "  <___________________________>  ",
        "   |_________________________|   ",
        "  * . * * . * * . * * . * * . * ",
    ], " 🎉 HAPPY BIRTHDAY PHẠM THỊ LỆ! 🎉 "),
]

def animated_cake():
    clear_screen()
    print("\n" * 2)

    # Dành vùng vẽ trước
    for _ in range(10):
        print()

    # Thời gian dừng mỗi frame — chậm rãi, dễ nhìn
    pauses = [1.2, 1.0, 1.0, 0.9, 2.0]

    for frame_idx, (color, lines, msg) in enumerate(CAKE_FRAMES):
        sys.stdout.write(f"\033[{len(lines) + 3}A")

        for line in lines:
            sys.stdout.write(f"\r{color}{line}{C.RESET}\n")

        sys.stdout.write(f"\r{' ' * 40}\n")
        sys.stdout.write(f"\r{color}{msg:^44}{C.RESET}\n")
        sys.stdout.flush()

        time.sleep(pauses[frame_idx])

    time.sleep(1.2)

# ─────────────────────────────────────────
#  Banner
# ─────────────────────────────────────────

def print_banner():
    clear_screen()
    banner = [
        "╔════════════════════════════════════════════╗",
        "║    🌟  HAPPY BIRTHDAY PHAM THI LE  🌟     ║",
        "║                                            ║",
        "║       🎂 🎉 🎈 🎁 🎀 🎂 🎉 🎈 🎁 🎀     ║",
        "╚════════════════════════════════════════════╝",
    ]
    for line in banner:
        print(f"{C.YELLOW}{line}{C.RESET}")
        time.sleep(0.15)
    print()

# ─────────────────────────────────────────
#  Thư chúc mừng
# ─────────────────────────────────────────

def show_letter():
    clear_screen()
    letter_lines = [
        "╔════════════════════════════════════════════╗",
        "║                                            ║",
        "║     📨   THƯ CHÚC MỪNG SINH NHẬT   📨     ║",
        "║                                            ║",
        "║   Gửi:  Phạm Thị Lê                        ║",
        "║                                            ║",
        "║   Hôm nay là ngày đặc biệt của cậu,        ║",
        "║   chúc cậu có một ngày sinh nhật thật      ║",
        "║   vui vẻ, tràn ngập tiếng cười và nhận     ║",
        "║   được thật nhiều yêu thương!              ║",
        "║                                            ║",
        "║   Mong rằng mọi ước mơ của cậu đều         ║",
        "║   thành hiện thực. Hãy luôn mỉm cười       ║",
        "║   và tận hưởng cuộc sống này nhé!          ║",
        "║                                            ║",
        "║                        Thân thương,        ║",
        "║                        Một người bạn       ║",
        "║                                            ║",
        "╚════════════════════════════════════════════╝",
    ]
    for i in range(1, len(letter_lines) + 1):
        clear_screen()
        for j in range(i):
            print(f"{C.PINK}{letter_lines[j]}{C.RESET}")
        time.sleep(0.07)
    time.sleep(2.5)

# ─────────────────────────────────────────
#  Server
# ─────────────────────────────────────────

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
        print(f"\n  Không tìm thấy file index.html")
        input("Nhấn Enter để thoát...")
        sys.exit(1)

    # 1. Đếm ngược 3-2-1
    countdown_intro()

    # 2. Banner
    print_banner()
    time.sleep(1.0)

    # 3. Chữ chạy ngang — có dấu tiếng Việt đầy đủ
    move_text("  Chào mừng đến với bữa tiệc sinh nhật!  ", C.CYAN, 22)
    time.sleep(0.5)

    # 4. Hoạt cảnh bánh sinh nhật
    animated_cake()

    # 5. Thư chúc mừng
    show_letter()

    # 6. Lời nhắn cuối — có dấu tiếng Việt đầy đủ
    clear_screen()
    print(f"\n{C.GREEN}{'═' * 50}{C.RESET}")
    type_text("  Gửi Phạm Thị Lê,", C.PINK, 0.08)
    type_text("  Chúc cậu sinh nhật thật vui vẻ và hạnh phúc!", C.MAGENTA, 0.08)
    type_text("  Mong rằng ngày hôm nay sẽ là kỷ niệm đẹp trong tim cậu! 💖", C.BLUE, 0.08)
    print(f"{C.GREEN}{'═' * 50}{C.RESET}")
    time.sleep(2.5)

    # 7. Khởi động server
    port = get_free_port()
    url  = f"http://localhost:{port}"

    # Màn hình cuối — HAPPY BIRTHDAY banner lớn + link
    clear_screen()

    balloon_left = [
        f"{C.CYAN}   (o) (o)  {C.RESET}",
        f"{C.MAGENTA}  (o) (o) (o) {C.RESET}",
        f"{C.YELLOW} (o)(o)(o)(o)  {C.RESET}",
        f"{C.CYAN}  | || || |   {C.RESET}",
        f"{C.MAGENTA}  | || || |   {C.RESET}",
    ]
    balloon_right = [
        f"{C.PINK}   (o) (o)  {C.RESET}",
        f"{C.ORANGE}  (o) (o) (o) {C.RESET}",
        f"{C.GREEN} (o)(o)(o)(o)  {C.RESET}",
        f"{C.PINK}   | || || |  {C.RESET}",
        f"{C.ORANGE}   | || || |  {C.RESET}",
    ]

    happy = [
        " ██╗  ██╗ █████╗ ██████╗ ██████╗ ██╗   ██╗",
        " ██║  ██║██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝",
        " ███████║███████║██████╔╝██████╔╝ ╚████╔╝ ",
        " ██╔══██║██╔══██║██╔═══╝ ██╔═══╝   ╚██╔╝  ",
        " ██║  ██║██║  ██║██║     ██║        ██║   ",
        " ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝        ╚═╝   ",
    ]
    birthday = [
        " ██████╗ ██╗██████╗ ████████╗██╗  ██╗██████╗  █████╗ ██╗   ██╗",
        " ██╔══██╗██║██╔══██╗╚══██╔══╝██║  ██║██╔══██╗██╔══██╗╚██╗ ██╔╝",
        " ██████╔╝██║██████╔╝   ██║   ███████║██║  ██║███████║ ╚████╔╝ ",
        " ██╔══██╗██║██╔══██╗   ██║   ██╔══██║██║  ██║██╔══██║  ╚██╔╝  ",
        " ██████╔╝██║██║  ██║   ██║   ██║  ██║██████╔╝██║  ██║   ██║   ",
        " ╚═════╝ ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝   ╚═╝   ",
    ]
    to_you = [
        "  ████████╗ ██████╗      ██╗   ██╗ ██████╗ ██╗   ██╗",
        "     ██╔══╝██╔═══██╗     ╚██╗ ██╔╝██╔═══██╗██║   ██║",
        "     ██║   ██║   ██║      ╚████╔╝ ██║   ██║██║   ██║",
        "     ██║   ██║   ██║       ╚██╔╝  ██║   ██║██║   ██║",
        "     ██║   ╚██████╔╝        ██║   ╚██████╔╝╚██████╔╝",
        "     ╚═╝    ╚═════╝         ╚═╝    ╚═════╝  ╚═════╝ ",
    ]

    colors_happy    = [C.RED, C.ORANGE, C.YELLOW, C.GREEN, C.CYAN, C.BLUE]
    colors_birthday = [C.MAGENTA, C.PINK, C.CYAN, C.YELLOW, C.ORANGE, C.RED]
    colors_toyou    = [C.PINK, C.MAGENTA, C.PINK, C.MAGENTA, C.PINK, C.MAGENTA]

    print()
    # Bóng bay 2 bên + chữ HAPPY
    for i, line in enumerate(happy):
        left  = balloon_left[i]  if i < len(balloon_left)  else " " * 14
        right = balloon_right[i] if i < len(balloon_right) else " " * 14
        print(f"{left}{colors_happy[i]}{line}{C.RESET}{right}")
        time.sleep(0.05)

    print()

    # Chữ BIRTHDAY
    for i, line in enumerate(birthday):
        print(f"  {colors_birthday[i]}{line}{C.RESET}")
        time.sleep(0.05)

    print()

    # Chữ to you
    for i, line in enumerate(to_you):
        print(f"  {colors_toyou[i]}{line}{C.RESET}")
        time.sleep(0.05)

    print()
    print(f"{C.CYAN}{'─' * 72}{C.RESET}")
    print(f"{C.WHITE}{'🎈  Phạm Thị Lê  🎈':^72}{C.RESET}")
    print(f"{C.CYAN}{'─' * 72}{C.RESET}")
    print()

    # Link căn giữa, mũi tên nhấp nháy liên tục
    print(f"{C.YELLOW}{'🌐  Mở trang sinh nhật của bạn tại đây:':^72}{C.RESET}")
    print()
    

    threading.Timer(0.8, open_browser, args=[url]).start()

    arrow_frames = [
        f"{'👉  ' + url + '  👈':^80}",
        f"{'  ──►  ' + url + '  ◄──  ':^80}",
        f"{'👉  ' + url + '  👈':^80}",
        f"{'  ==>  ' + url + '  <==  ':^80}",
    ]
    arrow_colors = [C.PINK, C.CYAN, C.YELLOW, C.GREEN]

    httpd = HTTPServer(('', port), CustomHandler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()

    i = 0
    try:
        while True:
            sys.stdout.write(f"\r{arrow_colors[i % 4]}{arrow_frames[i % 4]}{C.RESET}")
            sys.stdout.flush()
            i += 1
            time.sleep(0.6)
    except KeyboardInterrupt:
        print(f"\n\n{C.PINK}  👋 Cảm ơn bạn đã ghé thăm!{C.RESET}\n")
        httpd.shutdown()

if __name__ == "__main__":
    main()
