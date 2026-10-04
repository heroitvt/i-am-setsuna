"""
Setsuna Vietnamese Patcher & OTA Updater
Standalone GUI Application built with Tkinter & Custom Styling
"""

import os
import sys
import json
import urllib.request
import urllib.error
import zipfile
import shutil
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Remote configuration URL on GitHub (using API and raw with cache buster)
VERSION_URL = "https://raw.githubusercontent.com/heroitvt/i-am-setsuna/main/version.json"
API_VERSION_URL = "https://api.github.com/repos/heroitvt/i-am-setsuna/contents/version.json"
BASE_RAW_URL = "https://raw.githubusercontent.com/heroitvt/i-am-setsuna/main/patch_files/"

class SetsunaPatcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("I am Setsuna - Bộ Cài Việt Hóa & OTA Updater")
        self.root.geometry("640 x 520".replace(" ", ""))
        self.root.resizable(False, False)

        # Set styling and theme
        self.bg_color = "#1e1e24"
        self.card_bg = "#2b2b36"
        self.accent_color = "#00adb5"
        self.text_color = "#eeeeee"
        self.subtext_color = "#aaaaaa"
        self.success_color = "#4ecca3"
        self.btn_bg = "#393e46"

        self.root.configure(bg=self.bg_color)

        self.game_dir = ""
        self.local_version = "Chưa cài đặt"
        self.remote_version_info = None

        self.setup_ui()
        self.detect_game_dir()
        self.load_local_version()

        # Auto-check update on startup (background thread)
        threading.Thread(target=self.check_update, kwargs={"silent": True}, daemon=True).start()

    def setup_ui(self):
        # Header banner
        header_frame = tk.Frame(self.root, bg="#111116", height=70)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        title_label = tk.Label(
            header_frame,
            text="❄️ I AM SETSUNA - VIỆT HÓA & OTA UPDATER",
            font=("Segoe UI", 14, "bold"),
            fg="#00adb5",
            bg="#111116"
        )
        title_label.pack(pady=(12, 2))

        sub_label = tk.Label(
            header_frame,
            text="Cập nhật bản dịch tự động qua GitHub | Phát triển bởi Chau Homestay",
            font=("Segoe UI", 9),
            fg="#888899",
            bg="#111116"
        )
        sub_label.pack(pady=(0, 10))

        # Main Content container
        main_frame = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. Game directory box
        dir_frame = tk.LabelFrame(
            main_frame,
            text=" 📁 Thư mục cài đặt Game ",
            font=("Segoe UI", 9, "bold"),
            bg=self.card_bg,
            fg=self.accent_color,
            padx=10,
            pady=8
        )
        dir_frame.pack(fill=tk.X, pady=(0, 10))

        self.dir_entry = tk.Entry(
            dir_frame,
            font=("Segoe UI", 9),
            bg="#1f1f27",
            fg="#ffffff",
            insertbackground="white",
            relief=tk.FLAT
        )
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4, padx=(0, 8))

        btn_browse = tk.Button(
            dir_frame,
            text="Chọn Thư Mục...",
            font=("Segoe UI", 9),
            bg="#393e46",
            fg="white",
            activebackground="#4ecca3",
            relief=tk.FLAT,
            command=self.browse_folder
        )
        btn_browse.pack(side=tk.RIGHT)

        # 2. Status & Version Information Frame
        info_frame = tk.LabelFrame(
            main_frame,
            text=" ℹ️ Trạng thái & Phiên bản ",
            font=("Segoe UI", 9, "bold"),
            bg=self.card_bg,
            fg=self.accent_color,
            padx=12,
            pady=10
        )
        info_frame.pack(fill=tk.X, pady=(0, 10))

        # Grid status rows
        row1 = tk.Frame(info_frame, bg=self.card_bg)
        row1.pack(fill=tk.X, pady=2)
        tk.Label(row1, text="Phiên bản trên máy:", font=("Segoe UI", 9), fg=self.subtext_color, bg=self.card_bg, width=20, anchor="w").pack(side=tk.LEFT)
        self.lbl_local_ver = tk.Label(row1, text=self.local_version, font=("Segoe UI", 9, "bold"), fg="#ffffff", bg=self.card_bg)
        self.lbl_local_ver.pack(side=tk.LEFT)

        row2 = tk.Frame(info_frame, bg=self.card_bg)
        row2.pack(fill=tk.X, pady=2)
        tk.Label(row2, text="Phiên bản Cloud (Mới nhất):", font=("Segoe UI", 9), fg=self.subtext_color, bg=self.card_bg, width=20, anchor="w").pack(side=tk.LEFT)
        self.lbl_remote_ver = tk.Label(row2, text="Đang kiểm tra...", font=("Segoe UI", 9, "bold"), fg="#f39c12", bg=self.card_bg)
        self.lbl_remote_ver.pack(side=tk.LEFT)

        row3 = tk.Frame(info_frame, bg=self.card_bg)
        row3.pack(fill=tk.X, pady=(6, 2))
        self.lbl_status = tk.Label(row3, text="Sẵn sàng.", font=("Segoe UI", 9, "italic"), fg=self.success_color, bg=self.card_bg)
        self.lbl_status.pack(side=tk.LEFT)

        # 3. Changelog Details Box
        log_frame = tk.LabelFrame(
            main_frame,
            text=" 📝 Nhật ký cập nhật (Changelog) ",
            font=("Segoe UI", 9, "bold"),
            bg=self.card_bg,
            fg=self.accent_color,
            padx=10,
            pady=8
        )
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.txt_changelog = tk.Text(
            log_frame,
            height=6,
            font=("Segoe UI", 9),
            bg="#1f1f27",
            fg="#dddddd",
            wrap=tk.WORD,
            relief=tk.FLAT
        )
        self.txt_changelog.pack(fill=tk.BOTH, expand=True)
        self.txt_changelog.insert(tk.END, "Nhấn 'Kiểm Tra Cập Nhật' để lấy thông tin phiên bản mới nhất từ GitHub.\n")
        self.txt_changelog.config(state=tk.DISABLED)

        # 4. Progress bar
        self.progress = ttk.Progressbar(main_frame, orient="horizontal", mode="determinate")
        self.progress.pack(fill=tk.X, pady=(0, 12))

        # 5. Buttons footer
        btn_frame = tk.Frame(main_frame, bg=self.bg_color)
        btn_frame.pack(fill=tk.X)

        self.btn_check = tk.Button(
            btn_frame,
            text="🔄 Kiểm Tra Cập Nhật",
            font=("Segoe UI", 9, "bold"),
            bg="#393e46",
            fg="white",
            activebackground="#222831",
            relief=tk.FLAT,
            padx=12,
            pady=6,
            command=lambda: threading.Thread(target=self.check_update, kwargs={"silent": False}, daemon=True).start()
        )
        self.btn_check.pack(side=tk.LEFT, padx=(0, 8))

        self.btn_update = tk.Button(
            btn_frame,
            text="⚡ CẬP NHẬT / CÀI ĐẶT VIỆT HÓA",
            font=("Segoe UI", 9, "bold"),
            bg="#00adb5",
            fg="white",
            activebackground="#4ecca3",
            relief=tk.FLAT,
            padx=16,
            pady=6,
            command=lambda: threading.Thread(target=self.do_update, daemon=True).start()
        )
        self.btn_update.pack(side=tk.RIGHT)

    def detect_game_dir(self):
        # Common locations
        candidates = [
            os.path.abspath("."),
            r"D:\Viet Hoa Game\I am Setsuna",
            r"D:\Games\I am Setsuna",
            r"C:\Program Files (x86)\Steam\steamapps\common\I am Setsuna",
            r"D:\SteamLibrary\steamapps\common\I am Setsuna",
            r"E:\SteamLibrary\steamapps\common\I am Setsuna"
        ]

        found = ""
        for c in candidates:
            if os.path.exists(os.path.join(c, "SETSUNA.exe")):
                found = c
                break

        if found:
            self.game_dir = found
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, self.game_dir)
        else:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, "Chưa tìm thấy game - Vui lòng bấm 'Chọn Thư Mục...'")

    def browse_folder(self):
        folder = filedialog.askdirectory(title="Chọn thư mục chứa SETSUNA.exe")
        if folder:
            if os.path.exists(os.path.join(folder, "SETSUNA.exe")):
                self.game_dir = folder
                self.dir_entry.delete(0, tk.END)
                self.dir_entry.insert(0, self.game_dir)
                self.load_local_version()
                self.lbl_status.config(text="Đã chọn thư mục game hợp lệ!", fg=self.success_color)
            else:
                messagebox.showerror("Lỗi", "Không tìm thấy file 'SETSUNA.exe' trong thư mục đã chọn!")

    def load_local_version(self):
        if not self.game_dir or not os.path.exists(self.game_dir):
            return

        ver_file = os.path.join(self.game_dir, "SETSUNA_Data", "patch_version.json")
        if os.path.exists(ver_file):
            try:
                with open(ver_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.local_version = f"v{data.get('version', '1.0.0')} (Build {data.get('version_code', '100')})"
            except:
                self.local_version = "v1.0.0 (Gốc)"
        else:
            # Check if fontfix exists
            if os.path.exists(os.path.join(self.game_dir, "SETSUNA_Data", "Managed", "SetsunaFontFix.dll")):
                self.local_version = "v1.0.0 (Chưa đồng bộ OTA)"
            else:
                self.local_version = "Chưa cài đặt"

        self.lbl_local_ver.config(text=self.local_version)

    def check_update(self, silent=False):
        self.lbl_status.config(text="Đang kết nối GitHub kiểm tra phiên bản...", fg="#f39c12")
        data = None
        
        # 1. Try GitHub Contents API first (Always fresh, zero CDN cache)
        try:
            req_api = urllib.request.Request(
                API_VERSION_URL,
                headers={
                    "User-Agent": "SetsunaPatcher/1.0",
                    "Accept": "application/vnd.github.v3.raw"
                }
            )
            with urllib.request.urlopen(req_api, timeout=8) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except Exception:
            pass

        # 2. Fallback to Raw URL with random timestamp query param
        if not data:
            try:
                raw_url = f"{VERSION_URL}?_nocache={os.urandom(8).hex()}"
                req = urllib.request.Request(
                    raw_url,
                    headers={
                        "User-Agent": "SetsunaPatcher/1.0",
                        "Cache-Control": "no-cache, no-store, must-revalidate",
                        "Pragma": "no-cache",
                        "Expires": "0"
                    }
                )
                with urllib.request.urlopen(req, timeout=8) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
            except Exception as e:
                self.lbl_status.config(text=f"Không thể kết nối máy chủ GitHub: {e}", fg="#e74c3c")
                if not silent:
                    messagebox.showerror("Lỗi mạng", f"Không thể kiểm tra cập nhật:\n{e}")
                return

        self.remote_version_info = data
        remote_ver = f"v{data.get('version')} (Build {data.get('version_code')})"
        self.lbl_remote_ver.config(text=remote_ver, fg="#00adb5")

        # Show changelog
        self.txt_changelog.config(state=tk.NORMAL)
        self.txt_changelog.delete("1.0", tk.END)
        self.txt_changelog.insert(tk.END, f"📌 TIÊU ĐỀ: {data.get('title', '')}\n")
        self.txt_changelog.insert(tk.END, f"📅 NGÀY PHÁT HÀNH: {data.get('release_date', '')}\n\n")
        self.txt_changelog.insert(tk.END, "✨ CÁC NỘI DUNG MỚI:\n")
        for item in data.get("changelog", []):
            self.txt_changelog.insert(tk.END, f"  • {item}\n")
        self.txt_changelog.config(state=tk.DISABLED)

        # Check version codes
        remote_code = int(data.get("version_code", 100))
        local_code = 0
        ver_marker = os.path.join(self.game_dir, "SETSUNA_Data", "patch_version.json")
        if os.path.exists(ver_marker):
            try:
                with open(ver_marker, "r", encoding="utf-8") as f:
                    local_code = int(json.load(f).get("version_code", 0))
            except:
                local_code = 0

        if "Chưa cài đặt" in self.local_version:
            self.lbl_status.config(text="Chưa cài Việt hóa. Hãy bấm 'CẬP NHẬT / CÀI ĐẶT' ngay!", fg="#e74c3c")
        elif remote_code > local_code or (data.get("version") not in self.local_version):
            self.lbl_status.config(text="⭐ CÓ BẢN VIỆT HÓA MỚI! Nhấn nút 'CẬP NHẬT' để tải.", fg="#e67e22")
            if not silent:
                messagebox.showinfo("Có bản cập nhật mới", f"Đã có bản cập nhật mới: v{data.get('version')} (Build {remote_code})!\nBấm 'CẬP NHẬT' để nâng cấp tự động.")
        else:
            self.lbl_status.config(text="Bản Việt hóa đang là MỚI NHẤT! Bạn có thể bấm để cài đặt lại.", fg=self.success_color)
            if not silent:
                messagebox.showinfo("Thông báo", "Bạn đang sử dụng bản Việt hóa mới nhất!")

    def do_update(self):
        curr_path = self.dir_entry.get().strip()
        if not curr_path or not os.path.exists(os.path.join(curr_path, "SETSUNA.exe")):
            messagebox.showerror("Lỗi", "Vui lòng chọn đúng thư mục game chứa file 'SETSUNA.exe' trước khi cập nhật!")
            return

        self.game_dir = curr_path

        if not self.remote_version_info:
            self.check_update(silent=True)
            if not self.remote_version_info:
                messagebox.showerror("Lỗi", "Không thể lấy thông tin cập nhật từ GitHub. Vui lòng kiểm tra lại mạng!")
                return

        files = self.remote_version_info.get("files", [])
        if not files:
            messagebox.showerror("Lỗi", "Danh sách file cập nhật trống!")
            return

        self.btn_update.config(state=tk.DISABLED)
        self.btn_check.config(state=tk.DISABLED)

        total_files = len(files)
        success_count = 0

        self.lbl_status.config(text=f"Bắt đầu tải {total_files} file cập nhật...", fg="#00adb5")
        self.progress["value"] = 0

        try:
            for idx, rel_path in enumerate(files):
                # Target path in game
                target_file = os.path.join(self.game_dir, rel_path.replace("/", os.sep))
                os.makedirs(os.path.dirname(target_file), exist_ok=True)

                file_url = BASE_RAW_URL + rel_path
                self.lbl_status.config(text=f"Đang tải ({idx+1}/{total_files}): {os.path.basename(rel_path)}...")

                # Download file
                req = urllib.request.Request(file_url, headers={"User-Agent": "SetsunaPatcher/1.0"})
                with urllib.request.urlopen(req, timeout=30) as resp:
                    with open(target_file, "wb") as out_f:
                        out_f.write(resp.read())

                success_count += 1
                self.progress["value"] = int(((idx + 1) / total_files) * 100)

            # Save local version marker
            ver_marker = os.path.join(self.game_dir, "SETSUNA_Data", "patch_version.json")
            with open(ver_marker, "w", encoding="utf-8") as f:
                json.dump(self.remote_version_info, f, ensure_ascii=False, indent=2)

            self.load_local_version()
            self.lbl_status.config(text="🎉 Cập nhật Việt Hóa thành công 100%!", fg=self.success_color)
            messagebox.showinfo("Thành công", f"Đã cập nhật thành công {success_count} file Việt hóa mới nhất!\nBây giờ bạn có thể khởi động game và thưởng thức.")

        except Exception as e:
            self.lbl_status.config(text=f"Lỗi khi cập nhật: {e}", fg="#e74c3c")
            messagebox.showerror("Lỗi cập nhật", f"Quá trình tải file gặp lỗi:\n{e}")

        finally:
            self.btn_update.config(state=tk.NORMAL)
            self.btn_check.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = SetsunaPatcherApp(root)
    root.mainloop()
