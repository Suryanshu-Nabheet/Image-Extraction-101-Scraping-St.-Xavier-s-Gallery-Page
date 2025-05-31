# 📸 School Photo Gallery Downloader

A simple yet powerful Python script to **download and organize photos** from a school’s photo gallery webpage—whether hosted remotely (like on S3) or served locally.

---

## 🧾 Table of Contents

- [� School Photo Gallery Downloader](#-school-photo-gallery-downloader)
  - [🧾 Table of Contents](#-table-of-contents)
  - [📁 File Structure](#-file-structure)
  - [🛠 Tech Stack](#-tech-stack)
  - [✨ Features](#-features)
  - [🚀 Usage](#-usage)
    - [1. Requirements](#1-requirements)
    - [2. Running the Script](#2-running-the-script)
    - [3. How It Works](#3-how-it-works)
  - [📌 Notes](#-notes)
  - [⚙️ Performance Highlights](#️-performance-highlights)

---

## 📁 File Structure

```
├── index.html               # HTML file containing image references
├── downloader.py            # Main Python script
├── /photos                  # Directory where downloaded photos are saved
├── image_download.log       # Log file for download tracking and errors
```

---

## 🛠 Tech Stack

- **Python 3.x**
- **Libraries Used**:
  - [`beautifulsoup4`](https://pypi.org/project/beautifulsoup4/) – HTML parsing
  - [`requests`](https://pypi.org/project/requests/) – HTTP requests
  - `urllib` – URL parsing and management
  - `logging` – Activity and error logging

---

## ✨ Features

- 🔗 Downloads photos from a **remote S3 bucket**
- 📂 Organizes images into structured **directories**
- 📊 Tracks **download progress**, success rate, and errors
- 🌐 Handles **both remote (HTTP/S3)** and **local** image URLs
- 📝 Detailed logging via `image_download.log`

---

## 🚀 Usage

### 1. Requirements

Ensure Python 3 is installed, then install the required packages:

```bash
pip install beautifulsoup4 requests
```

### 2. Running the Script

```bash
python downloader.py
```

### 3. How It Works

- The script **parses `index.html`** to extract image URLs.
- Remote images (e.g., from `s3-noi.aces3.ai`) are downloaded to the `/photos` directory.
- Local image paths (e.g., starting with `images/`) are logged for **manual copying**.
- A log file (`image_download.log`) tracks:
  - Total images found
  - Download success/failure
  - Progress percentage
  - Time taken
  - Any errors encountered

---

## 📌 Notes

⚠️ **Local interface images** (those with paths starting with `images/`) **cannot be downloaded automatically**. You must copy these manually from the source server.

---

## ⚙️ Performance Highlights

- ✅ Images are **streamed in chunks** to optimize memory usage.
- ♻️ **Duplicate URLs are filtered out** automatically.
- 📈 Console output shows a **real-time progress bar** with completion percentage.

---

Happy downloading! 🎓📷  
Feel free to contribute or suggest improvements via issues or PRs.
