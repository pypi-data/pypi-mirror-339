# delete.py
from .utils import load_data, save_data

def delete_token(name):  # ← tambahkan parameter 'name'
    data = load_data()
    if "tokens" not in data or not data["tokens"]:
        print("📭 Tidak ada token yang tersimpan.")
        return

    matched = [t for t in data["tokens"] if t["name"].lower() == name.lower()]

    if not matched:
        print(f"❌ Token dengan nama '{name}' tidak ditemukan.")
        return

    confirm = input(f"❗ Yakin ingin menghapus token '{name}'? (y/n): ")
    if confirm.lower() != "y":
        print("❎ Penghapusan dibatalkan.")
        return

    data["tokens"] = [t for t in data["tokens"] if t["name"].lower() != name.lower()]
    save_data(data)
    print(f"✅ Token '{name}' berhasil dihapus.")

    # Copyright (c) 2025 openpineaplehub

    # Permission is hereby granted, free of charge, to any person obtaining a copy
    # of this software and associated documentation files (the "Software"), to deal
    # in the Software without restriction, including without limitation the rights
    # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    # copies of the Software, and to permit persons to whom the Software is
    # furnished to do so, subject to the following conditions: