import requests
from getpass import getpass

# URL upload TestPyPI
upload_url = "https://test.pypi.org/legacy/"

# Token input (gunakan format: __token__)
username = "__token__"
password = getpass("Masukkan token TestPyPI kamu (tanpa spasi): ")

# Coba upload dummy metadata (tanpa file beneran)
response = requests.post(
    upload_url,
    auth=(username, password),
    data={
        ":action": "file_upload",
        "protocol_version": "1",
    }
)

print("\nStatus:", response.status_code)
if response.status_code == 403:
    print("🚫 Token ditolak (403 Forbidden) — kemungkinan token salah atau tidak punya akses.")
elif response.status_code == 401:
    print("🔒 Tidak otentikasi (401 Unauthorized) — cek kembali token kamu.")
elif response.ok:
    print("✅ Token valid dan bisa digunakan!")
else:
    print(f"⚠️ Hasil tak terduga: {response.status_code}\n{response.text}")
