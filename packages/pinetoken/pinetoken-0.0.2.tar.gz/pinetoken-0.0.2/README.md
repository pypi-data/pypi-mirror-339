<h1 align="center">pinetoken </h1>

<div align="center">
  <a href="https://github.com/openpineapletools/pinetoken" target="_blank">
    <img src="./src/img/pinetoken.png" alt="pinetoken logo" width="160" />
    <p><strong>pinetoken</strong></p>
  </a>

</div>

<p align="center">
  <i>CLI untuk mengelola token rahasia (GitHub Token, API Key, dll) secara aman dan terenkripsi di komputer lokal.</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version"/>
  <img src="https://img.shields.io/badge/python-3.9%2B-blue.svg" alt="Python"/>
  <img src="https://img.shields.io/github/license/openpineapletools/pinetoken.svg" alt="License"/>
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey" alt="Platform"/>
  <img src="https://img.shields.io/badge/encryption-AES256-green" alt="Encryption"/>
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome"/>
  <img src="https://img.shields.io/github/issues/openpineapletools/pinetoken.svg" alt="Issues"/>
  <img src="https://img.shields.io/github/last-commit/openpineapletools/pinetoken.svg" alt="Last Commit"/>
  <img src="https://img.shields.io/maintenance/yes/2025.svg" alt="Maintained"/>
  <img src="https://img.shields.io/github/stars/openpineapletools/pinetoken.svg?style=social" alt="Stars"/>
  <img src="https://img.shields.io/github/forks/openpineapletools/pinetoken.svg?style=social" alt="Forks"/>
</p>


## Fitur

- Inisialisasi penyimpanan dan proteksi dengan master password
- Menambahkan token baru dengan enkripsi
- Menampilkan daftar semua token
- Melihat detail token tertentu
- Menghapus token berdasarkan nama
- Mengekspor data token ke file eksternal

---

## Instalasi

### Mengunakan pypi
kalau kalian mau instal pakai `pyip` kalian bisa jalankan perintah ini 

```bash
$ pip install pinetoken
$ pinetoken -h
```

atau 

```
$ pip install pinetoken==0.0.1
```

### Mengunakan github repository

```bash
$ git clone https://github.com/openpineapletools/pinetoken.git
$ pip install -r requirements.txt
$ cd main
$ python main.py <-cmd> <--arghs>
```

## install dengan `.Zip`
**download** **di** [release-0.0.1](./release/0.0.1/zip/pinetoken-v0.0.1.zip)
- Download zip
- siapkah folder kosong di `C:\` contoh `C:\my-cli`
- Tambahkan ke PATH agar bisa dijalankan dari terminal mana pun:

- Tambah ke PATH Manual (Windows)
- Buka `System Environment Variables`
- Klik `Environment Variables`
- Di bagian `System variables`, pilih `Path`, klik `Edit`
- Tambahkan folder tempat `pinetoken.exe` diextract, misal: `C:\my-cli`

>[!NOTE]
>tidak di sarankan karna kamitelah mempermudha instalais negna `pip` dan juga `exe` dan `installler`

### Install Dan Auto setup

kami mengaunakan `inno` untuk auto setup dan mempermudah pengunaan nya. download [disini](https://github.com/openpineapletools/pinetoken/releases/tag/v0.0.1/pinetoken-setup-0.0.1.exe)

### Cara Instalasi dengan WHL dan PipLocalHost
Jika kamu baru pertama kali menginstal aplikasi Python, ikuti langkah-langkah berikut untuk memulai.

#### **Langkah 1: Unduh File Instalasi**
Kamu perlu mengunduh file instalasi yang sudah disediakan. Pilih salah satu format berikut:
- **Unduh file `.whl`** [disini](./release/0.0.1/dist/pinetoken-0.0.1-py3-none-any.whl)
- **Unduh file `.tar.gz`** [disini](./release/0.0.1/dist/pinetoken-0.0.1.tar.gz)

**Apa itu file `.whl` dan `.tar.gz`?**
- `.whl` adalah file paket Python yang sudah dibangun dan siap diinstal.
- `.tar.gz` adalah file sumber yang bisa kamu kompilasi dan instal.

#### **Langkah 2: Instalasi dengan Terminal**
Setelah mengunduh file yang kamu pilih, lakukan langkah-langkah berikut:
1. **Letakkan file di lokasi yang kamu inginkan** (misalnya, folder `Downloads`).
2. **Buka Terminal atau Command Prompt** di direktori tempat file berada.
3. Jalankan perintah berikut di terminal:

   ```bash
   $ python -m build
   $ pip install .
   ```

   - Perintah pertama (`python -m build`) akan membangun paket Python.
   - Perintah kedua (`pip install .`) akan menginstal paket yang sudah dibangun tadi.

#### **Langkah 3: Pengujian**
Setelah instalasi selesai, kamu bisa mulai menggunakan aplikasi. Coba jalankan dan pastikan semuanya berfungsi dengan baik!

---

## 📘 Cara Penggunaan

### 🔹 Perintah Utama

```bash
$ pinetoken <-cmd> <-flags> <args>
```

Contoh paling dasar:
```bash
$ pinetoken -h      # Menampilkan bantuan
$ pinetoken --init  # Inisialisasi dan buat password utama
```

---

### Help
```bash
$ pinetoken -h     
$ pinetoken --help
```

**Output `--help`:**
```
usage: pinetoken [-h] [--init] [--add] [--list] [--show TOKEN_NAME] [--del TOKEN_NAME] [--export]
                 [-s SERVICE] [-n NAME] [-d DESC] [-t TOKEN] [-e EXPIRE] [-l LL]

🔐 CLI Token Manager – Simpan dan kelola token API kamu dengan aman.

Options:
  -h, --help            Tampilkan bantuan dan keluar
  --init                Inisialisasi storage dan buat password utama
  --add                 Tambahkan token baru ke penyimpanan
  --list                Tampilkan semua token yang tersimpan
  --show TOKEN_NAME     Tampilkan detail token berdasarkan nama
  --del TOKEN_NAME      Hapus token berdasarkan nama
  --export              Ekspor semua token ke file eksternal
  -s, --service SERVICE Nama service (opsional)
  -n, --name NAME       Nama token
  -d, --desc DESC       Deskripsi token
  -t, --token TOKEN     Token yang ingin disimpan
  -e, --expire EXPIRE   Tanggal kedaluwarsa (format: YYYY-MM-DD)
  -l, --ll LL           Lokasi atau asal token
```

---

### Menambahkan Token

Kamu bisa menambahkan token dengan satu perintah gabungan:

```bash
$ pinetoken --add -s "GitHub" -n "github-main" -d "Token akses utama" -t "ghp_xxx" -e "2025-12-31" -l "PC kantor"
```

Atau satu per satu (tidak disarankan karena hanya flag terakhir yang diproses):

```bash
$ pinetoken --add -s "GitHub"
$ pinetoken --add -n "github-main"
# dan seterusnya...
```
>[!NOTE]
>Disarankan gunakan semua flag dalam satu perintah untuk menghindari konflik antar state.

---

### Lihat Daftar Token
```bash
$ pinetoken --list
```

---

### Tampilkan Detail Token
```bash
$ pinetoken --show "github-main"
```

---

### Hapus Token
```bash
$ pinetoken --del "github-main"
```

---

### Ekspor Token
```bash
$ pinetoken --export
```

###  Catatan Keamanan

-  **Token disimpan secara lokal** di file `pinetokeninit.opine`, dalam bentuk **terenkripsi** menggunakan _master password_.
-  **Jangan lupa password Anda.** Jika lupa, data **tidak bisa dipulihkan** karena sistem ini tidak menyimpan salinan password.
-  **Jangan bagikan** file `.opine` ke siapa pun atau melalui jaringan publik. Perlakukan seperti dompet digital rahasia.
>[!NOTE]
>Selalu backup password Anda di tempat aman (misalnya, password manager offline).

---

### 📄 Lisensi

**MIT License**  
Bebas digunakan, dimodifikasi, dan didistribusikan dengan tetap mencantumkan atribusi.

[📜 Pelajari MIT License](https://opensource.org/licenses/MIT)

---
<div align="center">

  <a href="https://github.com/openpineapletools/pinetoken" target="_blank">
    <img src="https://img.shields.io/github/stars/openpineapletools/pinetoken?style=social" alt="GitHub Stars">
  </a>
  <a href="https://github.com/openpineapletools/pinetoken" target="_blank">
    <img src="https://img.shields.io/github/forks/openpineapletools/pinetoken?style=social" alt="GitHub Forks">
  </a>
  <a href="https://github.com/openpineapletools/pinetoken/blob/main/LICENSE" target="_blank">
    <img src="https://img.shields.io/github/license/openpineapletools/pinetoken?color=blue" alt="License">
  </a>
  <a href="https://github.com/openpineapletools/pinetoken/releases" target="_blank">
    <img src="https://img.shields.io/github/v/release/openpineapletools/pinetoken?label=release" alt="Latest Release">
  </a>

  <p style="margin-top: 20px; font-size: 0.9rem; color: #666;">
    Dibuat dengan ❤️ oleh <a href="https://github.com/openpineapletools" target="_blank">openpineaple </a> • Powered by Python
  </p>

</div>