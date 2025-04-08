import datetime
import getpass
from .utils import load_data, save_data
from .crypto import encrypt_token

def add_token(args=None):
    data = load_data()
    if "tokens" not in data:
        print("❌ Token manager belum diinisialisasi.")
        return

    password = getpass.getpass("🔑 Masukkan password master: ")

    # Cek apakah pakai argumen atau mode interaktif
    name = args.name if args and args.name else input("📝 Nama Token: ")
    description = args.desc if args and args.desc else input("📄 Deskripsi: ")
    token = args.token if args and args.token else getpass.getpass("🔐 Token Rahasia: ")
    expire_str = args.expire if args and args.expire else input("📅 Expired Date (YYYY-MM-DD) [opsional]: ")
    location = args.ll if args and args.ll else input("📍 Lokasi/Label: ")

    try:
        expired = datetime.datetime.strptime(expire_str, "%Y-%m-%d").strftime("%Y-%m-%d") if expire_str else ""
    except ValueError:
        print("⚠️  Format tanggal tidak valid. Token tidak ditambahkan.")
        return

    encrypted_token = encrypt_token(token, password)

    new_entry = {
        "name": name,
        "desc": description,
        "token": encrypted_token,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "expires": expired,
        "loc": location
    }

    data["tokens"].append(new_entry)
    save_data(data)
    print("✅ Token berhasil ditambahkan!")

    # Copyright (c) 2025 openpineaplehub

    # Permission is hereby granted, free of charge, to any person obtaining a copy
    # of this software and associated documentation files (the "Software"), to deal
    # in the Software without restriction, including without limitation the rights
    # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    # copies of the Software, and to permit persons to whom the Software is
    # furnished to do so, subject to the following conditions: