import os
import datetime
import requests
from bs4 import BeautifulSoup
import schedule
import time

# --- PENGATURAN GLOBAL ---
LOG_DIRECTORY = 'app_logs'  # Direktori tempat log disimpan
LOG_RETENTION_DAYS = 30     # Log akan dihapus jika lebih tua dari 30 hari
# URL scraping: Menggunakan situs yang menyediakan data nilai tukar mata uang
CURRENCY_URL = 'https://www.google.com/finance/quote/USD-IDR' 

# --- 1. OTOMASI LAPORAN HARIAN (SIMULASI PENGIRIMAN EMAIL) ---
def send_daily_report():
    """Mengumpulkan data dan mensimulasikan pengiriman laporan harian via email."""
    
    # Simulasi pengumpulan data/laporan
    report_data = f"Laporan Otomatis Harian\nTanggal: {datetime.date.today()}\nTotal Pengguna Aktif: 1500\nJumlah Error Semalam: 12"
    
    print("--------------------------------------------------")
    print(f"✅ FITUR 1: Laporan Harian Dikirim ({datetime.datetime.now().strftime('%H:%M:%S')})")
    print(report_data)
    print("Simulasi: Email laporan harian berhasil dikirim ke penerima.")
    print("--------------------------------------------------")

# --- 2. OTOMASI PEMBERSIHAN LOG LAMA ---
def cleanup_logs():
    """Memindai direktori log dan menghapus file yang lebih tua dari N hari."""
    
    # Pengecekan direktori sudah dipastikan ada di __main__
    if not os.path.exists(LOG_DIRECTORY):
        print(f"ℹ️ Direktori log '{LOG_DIRECTORY}' tidak ditemukan. Melewati pembersihan.")
        return

    # Hitung batas waktu (N hari yang lalu)
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=LOG_RETENTION_DAYS)
    deleted_count = 0
    
    print(f"\n--- FITUR 2: Memulai Pembersihan Log ({datetime.datetime.now().strftime('%H:%M:%S')}) ---")
    
    for filename in os.listdir(LOG_DIRECTORY):
        filepath = os.path.join(LOG_DIRECTORY, filename)
        
        # Hanya proses file, abaikan direktori
        if os.path.isfile(filepath):
            try:
                # Dapatkan waktu modifikasi file
                file_mod_time_timestamp = os.path.getmtime(filepath)
                file_mod_time = datetime.datetime.fromtimestamp(file_mod_time_timestamp)
                
                # Bandingkan dengan cutoff date
                if file_mod_time < cutoff_date:
                    os.remove(filepath)
                    deleted_count += 1
                    print(f"🗑️ Dihapus: {filename} (Tanggal: {file_mod_time.strftime('%Y-%m-%d')})")
            except Exception as e:
                print(f"⚠️ Gagal memproses file {filename}: {e}")

    print(f"✅ Pembersihan Log Selesai. Total {deleted_count} file log lama dihapus.")
    print("--------------------------------------------------")


# --- 3. OTOMASI WEB SCRAPING DATA KURS ---
def scrape_currency_rate():
    """Mengambil data kurs (USD ke IDR) dari web dan menampilkannya."""
    
    print(f"\n--- FITUR 3: Memulai Web Scraping Kurs ({datetime.datetime.now().strftime('%H:%M:%S')}) ---")
    
    try:
        # 1. Mengirim permintaan HTTP ke URL (Gunakan header sederhana untuk menghindari blokir)
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(CURRENCY_URL, headers=headers, timeout=10)
        response.raise_for_status()  # Memastikan permintaan berhasil
        
        # 2. Parsing konten HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 3. Menemukan elemen yang berisi nilai kurs (Kelas khusus dari Google Finance)
        rate_element = soup.find('div', class_='YMlKec fxKbKc')
        
        if rate_element:
            # Membersihkan teks dan mengganti koma dengan titik untuk konversi float
            rate_text = rate_element.text.replace(',', '').replace('.', '') 
            # Nilai kurs biasanya memiliki format XXX.XXX, kita harus membagi dengan 1000 
            # jika hasil scraping memiliki 5 angka di belakang koma (tergantung sumber)
            
            # Mendapatkan nilai teks murni, misalnya "15,800.00"
            raw_value = rate_element.text.replace(',', '')
            
            # Asumsi output adalah Rp15.800,00 -> 15800.00
            import re
            numeric_match = re.search(r'[\d,.]+', raw_value)
            
            if numeric_match:
                kurs_str = numeric_match.group(0).replace('.', '').replace(',', '.') # Handle comma and dot format
                kurs_idr = float(kurs_str)
            else:
                raise ValueError("Format kurs tidak ditemukan atau tidak valid.")
            
            
            # 4. Menyimpan data (simulasi print)
            print(f"💰 Kurs USD/IDR Terbaru: 1 USD = Rp{kurs_idr:,.2f}")
            
        else:
            print("❌ Gagal menemukan elemen kurs di halaman web. Periksa kembali class HTML.")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Gagal mengambil data kurs (Network/HTTP Error): {e}")
    except ValueError as e:
        print(f"❌ Gagal mengonversi nilai kurs ke angka: {e}")
    except Exception as e:
        print(f"❌ Terjadi error tak terduga saat scraping: {e}")
    
    print("--------------------------------------------------")


# --- PENGATURAN JADWAL (MAIN FUNCTION) ---
def main():
    
    print("--------------------------------------------------")
    print("🚀 Script Otomasi Python Dimulai.")
    print("Aplikasi akan berjalan dan menjadwalkan tugas.")
    print("Tekan Ctrl+C untuk menghentikan.")
    print("--------------------------------------------------")

    # Jadwalkan Fitur 1: Laporan Harian
    # Contoh: Jalankan setiap hari pada pukul 17:00
    schedule.every().day.at("17:00").do(send_daily_report)

    # Jadwalkan Fitur 2: Pembersihan Log
    # Contoh: Jalankan setiap hari pada pukul 03:00 pagi
    schedule.every().day.at("03:00").do(cleanup_logs)

    # Jadwalkan Fitur 3: Web Scraping Data Kurs
    # Untuk pengujian cepat, diubah menjadi setiap 1 menit (Anda bisa ubah kembali ke 1.hour)
    schedule.every(1).minutes.do(scrape_currency_rate)

    # Jalankan loop utama untuk mengecek jadwal
    while True:
        try:
            schedule.run_pending()
            time.sleep(1) # Tunggu 1 detik sebelum cek jadwal lagi
        except KeyboardInterrupt:
            print("\n👋 Script dihentikan oleh pengguna (Ctrl+C).")
            break
        except Exception as e:
            print(f"⚠️ Error tak terduga dalam loop jadwal: {e}")
            time.sleep(5) # Tunggu sebentar sebelum mencoba lagi

if __name__ == "__main__":
    
    # 💡 PERBAIKAN UTAMA: Pastikan direktori log sudah ada sebelum membuat file simulasi
    if not os.path.exists(LOG_DIRECTORY):
        os.makedirs(LOG_DIRECTORY)
        print(f"Setup: Direktori '{LOG_DIRECTORY}' berhasil dibuat.")

    # --- Opsional: Buat beberapa file log simulasi untuk pengujian Fitur 2 ---
    today = datetime.datetime.now()
    old_date = today - datetime.timedelta(days=40)
    
    # Log Lama (akan dihapus)
    with open(os.path.join(LOG_DIRECTORY, 'server_40_days_old.log'), 'w') as f:
        f.write("Log lama")
    # Mengubah waktu modifikasi file agar terlihat tua
    os.utime(os.path.join(LOG_DIRECTORY, 'server_40_days_old.log'), (old_date.timestamp(), old_date.timestamp()))

    # Log Baru (tidak akan dihapus)
    with open(os.path.join(LOG_DIRECTORY, 'app_today.log'), 'w') as f:
        f.write("Log hari ini")
        
    print(f"Setup: 2 file log simulasi dibuat di '{LOG_DIRECTORY}'.")
    
    # Jalankan program utama
    main()