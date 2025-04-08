import argparse
from .remote_loader import download_ps_file
from .config_manager import save_token, get_config
from .quiz_engine import run_quiz
import os
def main():
    parser = argparse.ArgumentParser(
    description="🍍 PineQuiz CLI - Latihan Soal Encrypted",
    add_help=False  # ⛔️ Matikan bantuan default (-h bawaan argparse)
)

    parser.add_argument('-i', '--inti', action='store_true', help='Mode inti, memulai quiz dari file soal')
    parser.add_argument('-l', '--link', help='Link file .ps dari GitHub (raw URL)')
    parser.add_argument('-x', '--execute', action='store_true', help='Jalankan quiz setelah file diunduh')
    parser.add_argument('-r', '--run', action='store_true', help='Alias dari --execute')
    parser.add_argument('-cfg', '--config', help='Simpan token GitHub untuk akses privat')
    parser.add_argument('-v', '--version', action='store_true', help='Tampilkan versi CLI')
    parser.add_argument('-h', '--helpme', action='store_true', help='Tampilkan bantuan lengkap')

    args = parser.parse_args()

    if args.version:
        print("PineQuiz v1.0.0 🍍")
        return

    if args.helpme:
        parser.print_help()
        return

    if args.config:
        parts = args.config.split(",")
        token = parts[0]
        extra = parts[1] if len(parts) > 1 else None
        save_token(token, extra_path=extra)
        print("✅ Config berhasil disimpan.")

    if args.inti and args.link:
        print("📥 Mengunduh soal...")
        file_path = download_ps_file(args.link)
        print(f"✅ Soal disimpan di: {file_path}")

        if args.execute or args.run:
            run_quiz(file_path)
        return

    print("❗ Gunakan -h atau --helpme untuk bantuan.")

if __name__ == "__main__":
    main()
