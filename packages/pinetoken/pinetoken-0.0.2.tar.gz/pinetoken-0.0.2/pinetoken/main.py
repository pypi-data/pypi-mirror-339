    # Copyright (c) 2025 openpineaplehub

    # Permission is hereby granted, free of charge, to any person obtaining a copy
    # of this software and associated documentation files (the "Software"), to deal
    # in the Software without restriction, including without limitation the rights
    # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    # copies of the Software, and to permit persons to whom the Software is
    # furnished to do so, subject to the following conditions:

import argparse
from .function.init import init_storage
from .function.add import add_token
from .function.list import list_tokens
from .function.show import show_token
from .function.delete import delete_token
from .function.export import export_tokens

def main():
    parser = argparse.ArgumentParser(
        prog='pinetoken',
        description='🔐 CLI Token Manager – Simpan dan kelola token API kamu dengan aman.'
    )
    parser.add_argument('--init', action='store_true', help='Inisialisasi storage dan buat password')
    parser.add_argument('--add', action='store_true', help='Tambah token baru')
    parser.add_argument('--list', action='store_true', help='Lihat daftar token')
    parser.add_argument('--show', type=str, metavar='TOKEN_NAME', help='Lihat detail token berdasarkan nama')
    parser.add_argument('--del', dest='delete', type=str, metavar='TOKEN_NAME', help='Hapus token berdasarkan nama')
    parser.add_argument('--export', action='store_true', help='Ekspor token ke file eksternal')
    parser.add_argument('-s', '--service', type=str, help='Nama service (opsional)')
    parser.add_argument('-n', '--name', type=str, help='Nama token')
    parser.add_argument('-d', '--desc', type=str, help='Deskripsi token')
    parser.add_argument('-t', '--token', type=str, help='Token yang ingin disimpan')
    parser.add_argument('-e', '--expire', type=str, help='Tanggal expired (YYYY-MM-DD)')
    parser.add_argument('-l', '--ll', type=str, help='Lokasi/token origin')

    args = parser.parse_args()

    if args.init:
        init_storage()
    elif args.add:
        add_token()
    elif args.list:
        list_tokens()
    elif args.show:
        show_token()
    elif args.delete:
        delete_token(args.delete)
    elif args.export:
        export_tokens()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
