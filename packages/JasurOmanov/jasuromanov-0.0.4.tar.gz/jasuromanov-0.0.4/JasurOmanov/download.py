import requests
import zipfile
import io
import os

def book():
    url = "https://github.com/JasurOmanov/Manbalar"
    if url.endswith("/"):
        url = url[:-1]
    repo_zip_url = url + "/archive/refs/heads/main.zip"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        print(f"⏬ Kitoblar yuklab olinmoqda...")
        response = requests.get(repo_zip_url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Yuklab olishda xatolik: {e}")
        return

    try:
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall()
        print("✅ Muvaffaqiyatli yuklandi va saqlandi.")
    except zipfile.BadZipFile:
        print("❌ ZIP faylni ochishda xatolik.")

def news():
    url = "https://github.com/JasurOmanov/Manbalar"
    if url.endswith("/"):
        url = url[:-1]
    repo_zip_url = url + "/archive/refs/heads/main.zip"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        print(f"⏬ Yangiliklar yuklab olinmoqda...")
        response = requests.get(repo_zip_url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Yuklab olishda xatolik: {e}")
        return

    try:
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall()
        print("✅ Muvaffaqiyatli yuklandi va saqlandi.")
    except zipfile.BadZipFile:
        print("❌ ZIP faylni ochishda xatolik.")
