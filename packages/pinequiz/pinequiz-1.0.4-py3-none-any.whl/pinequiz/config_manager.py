import os
import json

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

def save_token(token, extra_path=None):
    config = {"token": token}
    if extra_path:
        config["extra_path"] = extra_path
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

def get_config():
    if not os.path.exists(CONFIG_FILE):
        return {}  # kembalikan dict kosong kalau belum ada config
    with open(CONFIG_FILE, encoding="utf-8") as f:
        return json.load(f)  # return full dictionary

def get_extra_path():
    config = get_config()
    return config.get("extra_path")
