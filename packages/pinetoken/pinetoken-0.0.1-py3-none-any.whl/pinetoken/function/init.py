import os
import json
from getpass import getpass
from .crypto import encrypt_data  # pastikan nama file: crypto.py

INIT_FILE = 'pinetokeninit.opine'

def init_storage():
    if os.path.exists(INIT_FILE):
        print(f"📁 File '{INIT_FILE}' sudah ada.")
        return

    password = getpass("🔐 Buat password utama: ")
    confirm = getpass("🔐 Konfirmasi password: ")

    if password != confirm:
        print("❌ Password tidak cocok. Coba lagi.")
        return

    data = {
        "tokens": []
    }

    json_data = json.dumps(data)
    encrypted_data = encrypt_data(json_data, password)

    with open(INIT_FILE, "w") as f:
        f.write(encrypted_data)

    print(f"✅ Inisialisasi selesai dan terenkripsi di: {os.path.abspath(INIT_FILE)}")
