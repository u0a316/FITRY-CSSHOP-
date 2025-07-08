#!/usr/bin/env python3

import os
import datetime
import random
import string

# Path ke file counter
COUNTER_FILE = os.path.expanduser("~/.invoice_counter")

# Tanggal hari ini dalam format YYYYMMDD
tanggal = datetime.datetime.now().strftime("%Y%m%d")

# Baca counter jika ada
if os.path.exists(COUNTER_FILE):
    with open(COUNTER_FILE, "r") as f:
        last_date, last_count = f.read().strip().split()
else:
    last_date, last_count = tanggal, "0"

# Tentukan count baru
if last_date != tanggal:
    count = 1
else:
    count = int(last_count) + 1

# Simpan counter baru
with open(COUNTER_FILE, "w") as f:
    f.write(f"{tanggal} {count}")

# Buat 4 karakter hex acak
random_hex = ''.join(random.choices("ABCDEF0123456789", k=4))

# Cetak nomor faktur
print(f"{tanggal}-{count:03d}-{random_hex}")
