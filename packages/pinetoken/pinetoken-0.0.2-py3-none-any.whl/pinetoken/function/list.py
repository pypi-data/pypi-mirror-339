# list.py
from .utils import load_data
from tabulate import tabulate

def list_tokens():
    data = load_data()
    if "tokens" not in data or not data["tokens"]:
        print("📭 Tidak ada token yang tersimpan.")
        return

    table = []
    for i, t in enumerate(data["tokens"], 1):
        table.append([
            i,
            t["name"],
            t["desc"],
            t["created_at"],
            t["expires"],
            t["loc"]
        ])

    headers = ["#", "Name", "Description", "Created At", "Expires", "Location"]
    print("\n📋 Daftar Token:")
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

        # Copyright (c) 2025 openpineaplehub

    # Permission is hereby granted, free of charge, to any person obtaining a copy
    # of this software and associated documentation files (the "Software"), to deal
    # in the Software without restriction, including without limitation the rights
    # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    # copies of the Software, and to permit persons to whom the Software is
    # furnished to do so, subject to the following conditions: