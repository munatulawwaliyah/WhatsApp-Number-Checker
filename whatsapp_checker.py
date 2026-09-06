import os
import sys

# Konfigurasi PENTING agar browser Playwright bisa dibungkus ke dalam .exe
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "0"

import time
import random
import threading
import asyncio
import re
import gspread
import tkinter as tk
from tkinter import scrolledtext, messagebox
from google.oauth2.service_account import Credentials
from playwright.sync_api import sync_playwright

class WhatsAppCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WhatsApp Number Checker Bot")
        self.root.geometry("650x700") 
        
        self.is_running = False
        
        # --- KONFIGURASI DEVELOPER ---
        self.json_path = "sylvan-overview-500904-f1-6d5df1dc971f.json" 
        self.bot_email = "bot-pembaca-data@sylvan-overview-500904-f1.iam.gserviceaccount.com" 
        # -----------------------------
        
        self.DELAY_MIN = 0.1    
        self.DELAY_MAX = 0.3      
        self.CEK_DATA_BARU_DELAY = 10
        
        self.setup_ui()

    def setup_ui(self):
        frame_instruksi = tk.LabelFrame(self.root, text="Langkah 1: Wajib Baca!", fg="blue", font=("Arial", 10, "bold"))
        frame_instruksi.pack(pady=10, padx=20, fill="x")

        tk.Label(frame_instruksi, text="Agar bot bisa membaca data, bagikan (Share) Google Sheet Anda ke email berikut\ndengan akses sebagai EDITOR:", justify="left").pack(pady=(5,0))
        
        email_entry = tk.Entry(frame_instruksi, width=50, justify="center", font=("Arial", 10, "bold"), fg="red")
        email_entry.insert(0, self.bot_email)
        email_entry.config(state="readonly")
        email_entry.pack(pady=5)

        frame_input = tk.Frame(self.root)
        frame_input.pack(pady=10)

        tk.Label(frame_input, text="Nama Spreadsheet:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_sheet = tk.Entry(frame_input, width=35)
        self.entry_sheet.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Nama Worksheet:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_worksheet = tk.Entry(frame_input, width=35)
        self.entry_worksheet.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Nama Kolom No HP:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_col_hp = tk.Entry(frame_input, width=35)
        self.entry_col_hp.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Nama Kolom Nama:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.entry_col_nama = tk.Entry(frame_input, width=35)
        self.entry_col_nama.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Nama Kolom Hasil:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.entry_col_status = tk.Entry(frame_input, width=35)
        self.entry_col_status.grid(row=4, column=1, padx=5, pady=5)

        frame_btn = tk.Frame(self.root)
        frame_btn.pack(pady=5)
        
        self.btn_start = tk.Button(frame_btn, text="▶ MULAI BOT", bg="green", fg="white", width=15, font=("Arial", 10, "bold"), command=self.start_bot)
        self.btn_start.pack(side=tk.LEFT, padx=10)
        
        self.btn_stop = tk.Button(frame_btn, text="⏹ BERHENTI", bg="red", fg="white", width=15, font=("Arial", 10, "bold"), state=tk.DISABLED, command=self.stop_bot)
        self.btn_stop.pack(side=tk.LEFT, padx=10)

        tk.Label(self.root, text="Status Proses:", font=("Arial", 10, "bold")).pack()
        self.log_area = scrolledtext.ScrolledText(self.root, width=75, height=12, state='disabled', bg="#1e1e1e", fg="#00ff00", font=("Consolas", 9))
        self.log_area.pack(padx=10, pady=5)

    def get_resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def cetak_log(self, pesan):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, pesan + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def jeda(self, detik):
        langkah = int(detik * 10)
        for _ in range(langkah):
            if not self.is_running:
                break
            time.sleep(0.1)

    def koneksi_google_sheets(self, spreadsheet_name, worksheet_name):
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        real_json_path = self.get_resource_path(self.json_path)
        
        if not os.path.exists(real_json_path):
            raise FileNotFoundError(f"File kredensial tidak ditemukan di sistem!")

        creds = Credentials.from_service_account_file(real_json_path, scopes=scopes)
        client = gspread.authorize(creds)
        sheet = client.open(spreadsheet_name).worksheet(worksheet_name)
        return sheet

    def proses_whatsapp_background(self):
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

        spreadsheet_name = self.entry_sheet.get().strip()
        worksheet_name = self.entry_worksheet.get().strip()
        header_hp = self.entry_col_hp.get().strip()
        header_nama = self.entry_col_nama.get().strip()
        header_status = self.entry_col_status.get().strip()

        self.cetak_log("[*] Menghubungkan ke Google Sheets...")
        try:
            sheet = self.koneksi_google_sheets(spreadsheet_name, worksheet_name)
            self.cetak_log("[+] Berhasil terhubung ke Google Sheets.")
        except Exception as e:
            self.cetak_log(f"[-] Gagal terhubung! Pastikan nama Sheet benar dan email sudah di-share.\nDetail Error: {e}")
            self.reset_tombol()
            return

        with sync_playwright() as p:
            self.cetak_log("[*] Membuka browser Chromium...")
            browser = p.chromium.launch(headless=False, channel="chrome")
            page = browser.new_page()

            self.cetak_log("[*] Membuka WhatsApp Web... Silakan scan QR Code.")
            page.goto("https://web.whatsapp.com")

            try:
                page.wait_for_selector("div[data-testid='chat-list-search'], header", timeout=150000)
                self.cetak_log("[+] Login Berhasil! Memulai pemantauan data real-time...\n")
            except Exception as e:
                self.cetak_log("[-] Gagal memuat WhatsApp Web (Timeout/Error).")
                browser.close()
                self.reset_tombol()
                return

            while self.is_running:
                try:
                    all_values = sheet.get_all_values()
                    
                    if not all_values:
                        self.cetak_log("[-] Spreadsheet kosong. Menunggu data...")
                        self.jeda(self.CEK_DATA_BARU_DELAY)
                        continue

                    headers = all_values[0] 

                    if header_hp not in headers:
                        self.cetak_log(f"[-] Error: Kolom '{header_hp}' tidak ditemukan di baris pertama Sheet!")
                        self.jeda(10)
                        continue
                    
                    idx_nomor = headers.index(header_hp)
                    idx_nama = headers.index(header_nama) if header_nama in headers else -1
                    
                    if header_status in headers:
                        idx_status = headers.index(header_status)
                        col_status_sheet = idx_status + 1
                    else:
                        col_status_sheet = len(headers) + 1
                        sheet.update_cell(1, col_status_sheet, header_status)
                        idx_status = col_status_sheet - 1
                        self.cetak_log(f"[*] Membuat kolom baru '{header_status}' di Sheet.")
                        all_values = sheet.get_all_values()

                    data_ditemukan = False

                    for i, row_data in enumerate(all_values[1:]):
                        if not self.is_running:
                            break 

                        baris_sheet = i + 2 
                        nomor_asli = str(row_data[idx_nomor]).strip() if idx_nomor < len(row_data) else ""
                        nama_peserta = str(row_data[idx_nama]).strip() if idx_nama != -1 and idx_nama < len(row_data) else "Tanpa Nama"
                        status_sekarang = str(row_data[idx_status]).strip() if idx_status < len(row_data) else ""

                        if not nomor_asli or status_sekarang != "":
                            continue
                        
                        data_ditemukan = True

                        if "E+" in nomor_asli or "e+" in nomor_asli:
                            self.cetak_log(f"[{baris_sheet}] {nama_peserta} ({nomor_asli}) -> TIDAK AKTIF (Format Rusak)")
                            sheet.update_cell(baris_sheet, col_status_sheet, "Tidak Aktif (Format Rusak)")
                            continue
                        
                        nomor_bersih = re.sub(r'\D', '', nomor_asli)
                        if nomor_bersih.startswith("0"):
                            nomor_format = "62" + nomor_bersih[1:]
                        elif nomor_bersih.startswith("8"):
                            nomor_format = "62" + nomor_bersih
                        else:
                            nomor_format = nomor_bersih

                        try:
                            page.goto(f"https://web.whatsapp.com/send/?phone={nomor_format}&text&app_absent=0", wait_until="commit")
                            status_wa = "Tidak Aktif" 

                            for _ in range(50):
                                if not self.is_running:
                                    break

                                is_chat_open = page.locator("div[data-testid='conversation-panel-wrapper']").count() > 0 or \
                                               page.locator("div[data-testid='conversation-panel-messages']").count() > 0
                                
                                if is_chat_open:
                                    status_wa = "Aktif"
                                    break
                                
                                is_error = page.locator("text=tidak valid").count() > 0 or \
                                           page.locator("text=invalid").count() > 0 or \
                                           page.locator("text=No WhatsApp account").count() > 0
                                
                                if is_error:
                                    status_wa = "Tidak Aktif"
                                    page.keyboard.press("Escape") 
                                    break
                                
                                page.wait_for_timeout(200)

                            if self.is_running:
                                self.cetak_log(f"[{baris_sheet}] {nama_peserta} ({nomor_format}) -> {status_wa}")
                                sheet.update_cell(baris_sheet, col_status_sheet, status_wa)

                        except Exception as e:
                            self.cetak_log(f"[{baris_sheet}] {nama_peserta} ({nomor_format}) -> ERROR PAGE")
                            sheet.update_cell(baris_sheet, col_status_sheet, "ERROR")

                        self.jeda(random.uniform(self.DELAY_MIN, self.DELAY_MAX))
                        self.jeda(1) 

                    if not data_ditemukan and self.is_running:
                        self.cetak_log(f"[*] Semua data dicek. Menunggu {self.CEK_DATA_BARU_DELAY} detik...")
                        self.jeda(self.CEK_DATA_BARU_DELAY)

                except Exception as e:
                    self.cetak_log(f"[-] Terjadi kesalahan Sheet API: {e}")
                    self.jeda(10)

            self.cetak_log("[*] Menutup Browser WhatsApp...")
            browser.close()
            self.cetak_log("[*] Bot berhasil dihentikan.")
            self.reset_tombol()

    def start_bot(self):
        if not self.entry_sheet.get().strip() or not self.entry_worksheet.get().strip() or not self.entry_col_hp.get().strip() or not self.entry_col_status.get().strip():
            messagebox.showwarning("Peringatan", "Mohon isi semua kolom dengan benar sebelum memulai bot!")
            return

        self.is_running = True
        self.btn_start.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        self.log_area.config(state='normal')
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state='disabled')
        
        pekerja = threading.Thread(target=self.proses_whatsapp_background, daemon=True)
        pekerja.start()

    def stop_bot(self):
        self.is_running = False
        self.cetak_log("\n[*] Menerima instruksi berhenti. Menunggu siklus saat ini selesai...")
        self.btn_stop.config(state=tk.DISABLED) 
        
    def reset_tombol(self):
        self.is_running = False
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = WhatsAppCheckerApp(root)
    root.mainloop()