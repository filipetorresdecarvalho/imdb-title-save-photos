# imdb-title-save-photos


Here’s a **background service** that monitors your clipboard for IMDb movie URLs, fetches the images using the `imdbapi.dev` API, and saves them to a structured folder in `~/Pictures/imdbapi/title/{movie_id}/`. It also adds a 1-second delay between API/image requests to avoid rate limiting.

---

### **Python Script: IMDb Image Downloader (Background Service)**


---

### **How to Use**
1. **Install dependencies**:
   ```bash
   pip install requests pyperclip
   ```
2. **Run the script**:
   ```bash
   python imdb_image_downloader.py
   ```
3. **Copy an IMDb URL** (e.g., `https://www.imdb.com/title/tt20969586/`) to your clipboard.
4. The script will automatically detect the URL, fetch the images, and save them to:
   ```
   ~/Pictures/imdbapi/title/tt20969586/
   ```
5. Press `Ctrl+C` to stop the service.

---

### **Features**
- **Background monitoring**: Checks clipboard every second.
- **Structured saving**: Folders are created as `~/Pictures/imdbapi/title/{movie_id}/`.
- **Rate limiting**: 1-second delay between API/image requests.
- **Error handling**: Skips failed downloads and prints errors.
