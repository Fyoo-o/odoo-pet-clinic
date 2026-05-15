# 🐾 Panduan Setup Lokal — Odoo Pet Clinic

Dokumen ini menjelaskan cara menjalankan project Pet Clinic di komputer lokal yang baru.

---

## ✅ Prasyarat (Install Dulu)

| Software | Versi | Link Download |
|---|---|---|
| Python | 3.11 (wajib) | https://www.python.org/downloads/release/python-3119/ |
| PostgreSQL | 15 / 16 | https://www.postgresql.org/download/windows/ |
| Git | Terbaru | https://git-scm.com/download/win |
| wkhtmltopdf | 0.12.6 | https://wkhtmltopdf.org/downloads.html |

> ⚠️ Saat install Python, **centang "Add Python to PATH"** di halaman pertama installer!

---

## 📂 Langkah 1: Persiapan Folder

Buat folder project dan clone repo:

```powershell
# Buat folder utama
mkdir "D:\odoo-pet-clinic"
cd "D:\odoo-pet-clinic"

# Clone custom addons dari GitHub
git clone https://github.com/diprwnto-cyber/odoo-pet-clinic.git "odoo pet clinic"
cd "odoo pet clinic"
```

---

## 🐍 Langkah 2: Download Source Code Odoo 18

Source code Odoo tidak ada di repo (karena ukurannya sangat besar).
Kamu harus download manual dari GitHub Odoo resmi:

```powershell
# Clone Odoo 18 Community ke subfolder 'odoo'
git clone --depth=1 --branch 18.0 https://github.com/odoo/odoo.git odoo
```

> ⏳ Proses ini mungkin memakan waktu 10-30 menit tergantung kecepatan internet.

---

## 🔧 Langkah 3: Buat Virtual Environment

```powershell
# Buat virtual environment Python
python -m venv venv

# Aktifkan venv
.\venv\Scripts\Activate.ps1

# Install semua dependensi Python Odoo
pip install -r odoo\requirements.txt
```

> Jika muncul error "Execution Policy", jalankan dulu:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

## 🗄️ Langkah 4: Setup Database PostgreSQL

Buka **pgAdmin** atau **psql**, lalu jalankan perintah ini:

```sql
-- Buat user odoo
CREATE USER odoo WITH PASSWORD 'odoo';

-- Buat database untuk project
CREATE DATABASE "odoo-pet-clinic" OWNER odoo;

-- Berikan hak akses
GRANT ALL PRIVILEGES ON DATABASE "odoo-pet-clinic" TO odoo;
```

---

## ⚙️ Langkah 5: Buat File Konfigurasi Odoo

Buat file `odoo/odoo.conf` dengan isi berikut:

```ini
[options]
addons_path = odoo/odoo/addons,odoo/addons,custom_addons
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo
db_name = odoo-pet-clinic
http_port = 8069
logfile = False
```

---

## 🚀 Langkah 6: Inisialisasi & Jalankan

**Pertama kali (install module):**
```powershell
python odoo/odoo-bin -c odoo/odoo.conf -i pet_clinic
```

**Selanjutnya (jalankan biasa):**
```powershell
python odoo/odoo-bin -c odoo/odoo.conf
```

**Setelah pull update dari GitHub:**
```powershell
python odoo/odoo-bin -c odoo/odoo.conf -u pet_clinic
```

---

## 🌐 Akses Aplikasi

Buka browser dan akses:
```
http://localhost:8069
```

**Login default:**
- Email: `admin`
- Password: `admin`

---

## 🔄 Cara Update dari GitHub

```powershell
# Tarik update terbaru
git pull origin main

# Restart Odoo dengan update module
python odoo/odoo-bin -c odoo/odoo.conf -u pet_clinic
```

---

## ❗ Troubleshooting Umum

| Error | Solusi |
|---|---|
| `No Python at '...'` | Install Python 3.11 dan centang "Add to PATH" |
| `could not connect to server` | Pastikan PostgreSQL sudah running |
| `module not found` | Jalankan `pip install -r odoo/requirements.txt` |
| Ikon berbentuk kotak `[ ]` | Tekan `Ctrl+F5` di browser untuk hard refresh |
| `Execution Policy error` | Jalankan `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
