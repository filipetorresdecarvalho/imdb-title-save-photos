# --- CONFIGURATION ---
# How often to check the clipboard (in seconds)
CHECK_INTERVAL = 1
# Folder to save images
SAVE_FOLDER = "~/Pictures"
# API Key (optional, if your API requires it)
API_KEY = None
# --- END CONFIGURATION ---

import os
import re
import time
import json
import requests
import pyperclip
from pathlib import Path
from threading import Timer

class IMDbImageDownloader:
    def __init__(self):
        self.last_clipboard = ""
        self.running = True
        self.api_url = "https://api.imdbapi.dev/titles/{}/images"

    def get_clipboard(self):
        try:
            return pyperclip.paste().strip()
        except:
            return ""

    def is_imdb_url(self, url):
        pattern = r"https://www\.imdb\.com/title/tt\d+/"
        return re.match(pattern, url) is not None

    def extract_imdb_id(self, url):
        match = re.search(r"tt\d+", url)
        return match.group(0) if match else None

    def fetch_images_from_api(self, imdb_id):
        url = self.api_url.format(imdb_id)
        if API_KEY:
            url += f"?api_key={API_KEY}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json().get("images", [])
        except Exception as e:
            print(f"API Error: {e}")
            return []

    def download_image(self, url, save_path):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return True
        except Exception as e:
            print(f"Download Error: {e}")
            return False

    def process_imdb_url(self, imdb_id):
        images = self.fetch_images_from_api(imdb_id)
        if not images:
            print("No images found for this IMDb ID.")
            return

        save_folder = Path(SAVE_FOLDER) / "imdbapi" / "title" / imdb_id
        save_folder.mkdir(parents=True, exist_ok=True)

        print(f"Downloading {len(images)} images...")
        for i, image in enumerate(images):
            if "url" in image:
                image_url = image["url"]
                filename = f"image_{i+1}.jpg"
                save_path = save_folder / filename
                self.download_image(image_url, save_path)
                print(f"Saved: {save_path}")
                time.sleep(1)  # 1-second delay between requests

    def check_clipboard(self):
        if not self.running:
            return

        current_clipboard = self.get_clipboard()
        if current_clipboard and current_clipboard != self.last_clipboard:
            if self.is_imdb_url(current_clipboard):
                imdb_id = self.extract_imdb_id(current_clipboard)
                print(f"Detected IMDb URL: {current_clipboard}")
                print(f"Extracting ID: {imdb_id}")
                self.process_imdb_url(imdb_id)
            self.last_clipboard = current_clipboard

        Timer(CHECK_INTERVAL, self.check_clipboard).start()

    def start(self):
        print("IMDb Image Downloader started. Monitoring clipboard...")
        self.check_clipboard()

    def stop(self):
        self.running = False
        print("IMDb Image Downloader stopped.")

if __name__ == "__main__":
    downloader = IMDbImageDownloader()
    try:
        downloader.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        downloader.stop()
