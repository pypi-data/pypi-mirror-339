import requests
import zipfile
import io
import os

def book(url="https://github.com/JasurOmanov/uzb_kitoblar"):
    """
    GitHub reposini zip shaklida yuklab olib, ochadi.

    :param url: GitHub reposi manzili (masalan: https://github.com/JasurOmanov/uzb_kitoblar)
    """
    # GitHub zip link hosil qilamiz
    if url.endswith("/"):
        url = url[:-1]
    repo_zip_url = url + "/archive/refs/heads/main.zip"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        print(f"⏬ Yuklab olinmoqda...")
        response = requests.get(repo_zip_url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Yuklab olishda xatolik: {e}")
        return

    # Zip faylni ochamiz
    try:
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall()
        print("✅ Muvaffaqiyatli yuklandi va saqlandi.")
    except zipfile.BadZipFile:
        print("❌ ZIP faylni ochishda xatolik.")
