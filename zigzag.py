import time, sys, math

# --- 1. Variabel Animasi Dasar ---
indent = 0              # Jumlah spasi untuk indentasi
indentIncreasing = True # Arah pergerakan (True = Kanan, False = Kiri)
MAX_INDENT = 20         # Batas maksimum pergerakan

# --- 2. Fitur 1: Auto-Speed Adjustment (Pola Gelombang Sinus) ---
THETA_START = 0.0       # Sudut awal untuk perhitungan sinus
THETA_INCREMENT = 0.1   # Penambahan sudut setiap frame (mengontrol frekuensi)
current_theta = THETA_START

# --- 3. Fitur 2: Auto-Pattern Switching ---
PATTERNS = ['********', '########', '========', '........', '<<<<>>>>', '######**']
PATTERN_SWITCH_CYCLE = 3 # Ganti pola setiap 3 siklus penuh
cycle_count = 0          # Menghitung siklus penuh (0 -> 20 -> 0)
current_pattern_index = 0
current_pattern = PATTERNS[current_pattern_index]

try:
    while True:
        # --- A. Fitur 1: Auto-Speed Adjustment ---
        # math.sin(current_theta) akan menghasilkan nilai dari -1 hingga 1.
        # Kita normalisasi untuk mendapatkan nilai jeda (delay) antara 0.02s (cepat) hingga 0.17s (lambat).
        delay_factor = (math.sin(current_theta) + 1) / 2  # Nilai 0.0 hingga 1.0
        current_delay = 0.02 + (0.15 * delay_factor)      # Jeda dinamis
        
        # 1. Tampilkan Output
        print(' ' * indent, end='')
        print(current_pattern) # Menggunakan pola karakter yang dinamis
        
        # Jeda menggunakan kecepatan yang dihitung
        time.sleep(current_delay) 
        
        # Perbarui theta untuk frame berikutnya
        current_theta += THETA_INCREMENT

        # 2. Logika Pergerakan
        if indentIncreasing:
            indent = indent + 1
            if indent == MAX_INDENT:
                indentIncreasing = False # Balik Arah
                
        else:
            indent = indent - 1
            if indent == 0:
                indentIncreasing = True # Balik Arah
                
                # --- B. Fitur 2: Auto-Pattern Switching ---
                # Hitung satu siklus penuh setiap kali mencapai batas kiri (0)
                cycle_count += 1
                
                # Periksa apakah sudah waktunya ganti pola
                if cycle_count % PATTERN_SWITCH_CYCLE == 0:
                    current_pattern_index = (current_pattern_index + 1) % len(PATTERNS)
                    current_pattern = PATTERNS[current_pattern_index]
                    print(f"\n[NOTIFIKASI] Pola karakter otomatis berubah menjadi: {current_pattern}")
                
except KeyboardInterrupt:
    sys.exit()