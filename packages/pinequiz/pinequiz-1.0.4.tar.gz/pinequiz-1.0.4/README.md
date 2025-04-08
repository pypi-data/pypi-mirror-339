
# 🍍 PineQuiz CLI

**PineQuiz** adalah aplikasi CLI sederhana untuk menjalankan kuis atau latihan soal terenkripsi dari file `.ps` (format JSON yang sudah di-enkripsi). Soal bisa disimpan di GitHub dan diunduh secara langsung oleh pengguna. CLI ini cocok untuk pembelajaran, evaluasi, atau sekadar latihan soal.

---

## 🚀 Instalasi

### 1. Clone & Install Lokal

```bash
git clone https://github.com/openpineapletools/pinequiz.git
cd pinequiz
pip install .
```

### 2. Jalankan CLI dari manapun:

```bash
pinequiz -h
```

---

## ⚙️ Fitur Utama

| Perintah | Deskripsi |
|----------|-----------|
| `-i`, `--inti` | Memulai kuis dari file soal terenkripsi |
| `-l <link>` | Link GitHub (raw URL) dari file `.ps` |
| `-x`, `--execute` | Jalankan kuis setelah file diunduh |
| `-r`, `--run` | Alias dari `--execute` |
| `-cfg <token,folder>` | Simpan GitHub token + folder ekstra opsional |
| `-v`, `--version` | Tampilkan versi CLI |
| `-h`, `--helpme` | Tampilkan bantuan lengkap |

---

## 🧪 Contoh Penggunaan

### Unduh & Jalankan Kuis dari GitHub

```bash
pinequiz -i -l "" -x
```

### Simpan Token GitHub (untuk file private)

```bash
pinequiz -cfg ghp_yourGithubToken,soal-folder
```

---

## 📦 Format Soal (.ps)

File `.ps` adalah file JSON yang dienkripsi. Contoh format sebelum enkripsi:

```json
[
  {
    "question": "Apa ibu kota Indonesia?",
    "choices": {
      "a": "Bandung",
      "b": "Surabaya",
      "c": "Jakarta",
      "d": "Yogyakarta"
    },
    "answer": "c",  // Akan di-enkripsi
    "explanation": "Jakarta adalah ibu kota Indonesia sejak tahun 1945."
  }
]
```

---

## 🔐 Sistem Enkripsi

- Jawaban soal dienkripsi menggunakan metode `xor` + salt agar tidak mudah dibaca.
- Token GitHub disimpan secara lokal dalam file `config.json` (tidak terenkripsi).

---

## 📂 Struktur Folder

```bash
pinequiz/
├── pinequiz/
│   ├── pinequiz.py        # Entry point CLI
│   ├── config_manager.py
│   ├── quiz_engine.py
│   ├── remote_loader.py
│   ├── crypto_util.py
│   ├── __init__.py
├── setup.py
├── README.md
├── LICENSE
```

---

## 📝 Lisensi

MIT License © 2025 — openpineplehubsetup.py
├── README.md
├── LICENSE
```

---

## 📝 Lisensi

MIT License © 2025 — openpineplehub