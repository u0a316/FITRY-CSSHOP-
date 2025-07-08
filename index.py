#!/data/data/com.termux/files/usr/bin/python

import subprocess
import sys
import json
import urllib.parse
import requests
import os
import re

password = os.environ.get('MY_PASS')
# === Otentikasi Fingerprint ===
try:
    result = subprocess.check_output(["termux-fingerprint"])
    auth = json.loads(result)
    auth_result = auth.get("auth_result")
except Exception as e:
    print(f"Gagal membaca fingerprint: {e}")
    sys.exit(1)

if auth_result == "AUTH_RESULT_SUCCESS":
    print("✅ Otentikasi berhasil!")
    os.chdir(os.path.expanduser("~/FITRY-CSSHOP-/"))
elif auth_result == "AUTH_RESULT_FAILURE":
    print("❌ Otentikasi gagal!")
    sys.exit(1)
else:
    print(f"❌ Status tidak dikenal: {auth_result}")
    sys.exit(2)

# === Ambil argumen dari command-line ===
if len(sys.argv) < 4:
    print("Usage: script.py <nama> <harga> <email>")
    sys.exit(3)

name, price, email_customer = sys.argv[1:4]

# === Jalankan script Python untuk nomor order ===
try:
    getnumber = subprocess.check_output(["python3", "./modules/__gen_number.py"]).decode().strip()
    print(f"Nomor invoice: {getnumber}")  # tampilkan ke terminal 
    subprocess.run(["termux-clipboard-set"], input=getnumber.encode())
except Exception as e:
    print(f"Gagal menjalankan __gen_number.py: {e}")
    sys.exit(4)

# === Ambil token dari shortcut.luisadha.my.id ===
try:
    res = requests.get(f"http://shortcut.luisadha.my.id/register?key={password}", timeout=10)

    if res.status_code == 502 or "502 Bad Gateway" in res.text:
        print("❌ Server mengalami 502 Bad Gateway.")
        sys.exit(4)

    # Ambil token dari href
    match = re.search(r'href="/([^"]+)"', res.text)
    if match:
        token = match.group(1)
    else:
        print("❌ Token tidak ditemukan dalam HTML!")
        sys.exit(5)

except requests.exceptions.RequestException as e:
    print(f"❌ Gagal menghubungi server: {e}")
    sys.exit(4)

# === Buat link produk
link_product = f"https://shortcut.luisadha.my.id/{token}"

# === Ambil subject
try:
    subject = subprocess.check_output(["./modules/__gen_subj.sh", getnumber]).decode().strip()
except Exception as e:
    print(f"❌ Gagal mengambil subject: {e}")
    sys.exit(6)

# === Ambil body
body_input = f"{name}\n{price}\n{email_customer}\n{link_product}"
try:
    body = subprocess.run(
        ["bash", "modules/__gen_body.sh"],
        input=body_input.encode(),
        stdout=subprocess.PIPE,
        check=True
    ).stdout.decode().strip()
except subprocess.CalledProcessError as e:
    print(f"❌ Gagal menghasilkan body email: {e}")
    sys.exit(7)

# === Encode subject & body untuk mailto URL
encoded_subject = urllib.parse.quote(subject)
encoded_body = urllib.parse.quote(body)

# === Kirim email via mailto
mailto_url = f"mailto:{email_customer}?subject={encoded_subject}&body={encoded_body}"
print("📧 Membuka email draft...")
subprocess.run(["termux-open-url", mailto_url])
