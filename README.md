Aplikasi ini adalah tool otomatisasi berbasis antarmuka grafis (GUI) yang dirancang untuk mengecek status nomor telepon secara massal apakah terdaftar di WhatsApp atau tidak. Program ini terintegrasi langsung dengan Google Sheets untuk membaca data target dan menuliskan hasil pengecekan (Aktif/Tidak Aktif) secara real-time.

✨ Fitur Utama
Integrasi Google Sheets Otomatis: Membaca daftar nomor telepon dari Google Sheets dan langsung menuliskan status hasil pengecekan di kolom yang ditentukan tanpa perlu export/import file manual.

Pengecekan Real-time & Looping: Bot akan terus memantau Google Sheets. Jika ada data baru yang masuk, bot akan langsung mengeceknya.

Auto-Formatting Nomor: Mengubah dan membersihkan format nomor telepon secara otomatis (misalnya dari awalan 08... atau 8... menjadi format standar WhatsApp 628...).

Antarmuka Pengguna (GUI) Sederhana: Dilengkapi dengan dashboard untuk mengatur nama kolom, memulai/menghentikan bot, dan melihat log proses pengecekan secara langsung.

Aman dari Banned: Menggunakan metode otomasi peramban (Chromium via Playwright) yang mensimulasikan penggunaan WhatsApp Web secara natural.

🛠️ Persiapan Sebelum Menggunakan
Karena bot ini membaca dan menulis data langsung ke Google Sheets Anda, ada satu langkah wajib yang harus dilakukan:

Buat atau siapkan Google Sheets yang berisi daftar nomor kontak.

Klik tombol Share (Bagikan) di pojok kanan atas Google Sheets Anda.

Masukkan email bot berikut: bot-pembaca-data@sylvan-overview-500904-f1.iam.gserviceaccount.com

Pastikan akses email bot tersebut diatur sebagai Editor, lalu klik Send/Selesai.

🚀 Cara Penggunaan
Unduh dan jalankan file nama_file.exe.

Pada jendela aplikasi yang terbuka, isi detail Google Sheets Anda:

Nama Spreadsheet: Judul file Google Sheets Anda.

Nama Worksheet: Nama tab di bagian bawah sheet (biasanya Sheet1).

Nama Kolom No HP: Nama header atau judul kolom yang berisi nomor telepon.

Nama Kolom Nama: Nama header untuk kolom nama target.

Nama Kolom Hasil: Nama header bebas (misal: Status WA) tempat bot akan menuliskan hasilnya. Jika kolom belum ada, bot akan membuatnya otomatis.

Klik tombol ▶ MULAI BOT.

Jendela peramban Chromium akan terbuka menampilkan WhatsApp Web. Silakan Scan QR Code menggunakan aplikasi WhatsApp di HP Anda.

Setelah berhasil login, biarkan bot bekerja. Bot akan mengecek satu per satu dan memperbarui Google Sheets Anda secara otomatis.

⚠️ Catatan Penting
Selama proses berjalan, jangan menutup jendela browser Chromium secara manual, gunakan tombol ⏹ BERHENTI di aplikasi untuk menyetop proses dengan aman.

Karena aplikasi ini merupakan hasil compile menjadi .exe, Windows Defender atau antivirus mungkin mendeteksinya sebagai Unrecognized app. Klik More info -> Run anyway untuk tetap menjalankannya.
