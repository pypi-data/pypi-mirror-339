# show.py
import getpass
from .utils import load_data
from .crypto import decrypt_token

def show_token():
    data = load_data()
    if "tokens" not in data or not data["tokens"]:
        print("📭 Tidak ada token yang tersimpan.")
        return

    name = input("🔍 Masukkan nama token yang ingin dilihat: ")
    password = getpass.getpass("🔑 Masukkan password master: ")

    found = [t for t in data["tokens"] if t["name"].lower() == name.lower()]
    if not found:
        print("❌ Token tidak ditemukan.")
        return

    for t in found:
        try:
            token_plain = decrypt_token(t["token"], password)
        except:
            print("❌ Gagal mendekripsi token. Password salah?")
            return

        print("\n🔓 Token Details:")
        print(f"Nama       : {t['name']}")
        print(f"Deskripsi  : {t['desc']}")
        print(f"Token      : {token_plain}")
        print(f"Dibuat     : {t['created_at']}")
        print(f"Expired    : {t['expires']}")
        print(f"Lokasi     : {t['loc']}")

    # Copyright (c) 2025 openpineaplehub

    # Permission is hereby granted, free of charge, to any person obtaining a copy
    # of this software and associated documentation files (the "Software"), to deal
    # in the Software without restriction, including without limitation the rights
    # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    # copies of the Software, and to permit persons to whom the Software is
    # furnished to do so, subject to the following conditions: