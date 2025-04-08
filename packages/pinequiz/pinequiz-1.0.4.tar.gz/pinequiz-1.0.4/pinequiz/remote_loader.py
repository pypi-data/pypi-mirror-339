import requests
import os
from .config_manager import get_config

def download_ps_file(link):
    if not link.endswith('.ps'):
        raise ValueError("❌ Hanya file .ps yang diperbolehkan.")

    headers = {}
    token = get_config().get("token")
    if token:
        headers['Authorization'] = f'token {token}'

    response = requests.get(link, headers=headers)

    if response.status_code != 200:
        raise Exception(f"❌ Gagal mengunduh soal. Status: {response.status_code}")

    os.makedirs("soal_cache", exist_ok=True)
    local_path = os.path.join("soal_cache", "soal.ps")
    with open(local_path, 'w', encoding='utf-8') as f:
        f.write(response.text)

    return local_path
