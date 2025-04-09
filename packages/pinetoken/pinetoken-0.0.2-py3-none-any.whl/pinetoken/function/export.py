# export.py
import json
import csv
from .utils import load_data

def export_tokens():
    data = load_data()
    if "tokens" not in data or not data["tokens"]:
        print("📭 Tidak ada token untuk diekspor.")
        return

    format_ = input("📤 Ekspor ke format (json/csv): ").lower()
    filename = input("💾 Nama file output (tanpa ekstensi): ")

    if format_ == "json":
        with open(f"{filename}.json", "w", encoding="utf-8") as f:
            json.dump(data["tokens"], f, indent=4)
        print(f"✅ Token berhasil diekspor ke {filename}.json")

    elif format_ == "csv":
        keys = ["name", "desc", "token", "created_at", "expires", "loc"]
        with open(f"{filename}.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for token in data["tokens"]:
                writer.writerow(token)
        print(f"✅ Token berhasil diekspor ke {filename}.csv")

    else:
        print("❌ Format tidak dikenali. Gunakan 'json' atau 'csv'.")

            # Copyright (c) 2025 openpineaplehub

    # Permission is hereby granted, free of charge, to any person obtaining a copy
    # of this software and associated documentation files (the "Software"), to deal
    # in the Software without restriction, including without limitation the rights
    # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    # copies of the Software, and to permit persons to whom the Software is
    # furnished to do so, subject to the following conditions: