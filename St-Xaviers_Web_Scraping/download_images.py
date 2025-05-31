#!/usr/bin/env python3
import os
import re
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='image_download.log',
    filemode='w'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

# Constants
HTML_FILE = 'index.html'
INTERFACE_DIR = 'images/interface'
PHOTOS_DIR = 'images/photos'
BASE_URL = 'https://s3-noi.aces3.ai/franciscan/SchImg/SXSPAT/PhotoAlbum/Full/'
LOCAL_BASE = '/images/'

# Ensure directories exist
os.makedirs(INTERFACE_DIR, exist_ok=True)
os.makedirs(PHOTOS_DIR, exist_ok=True)

def get_image_urls_from_html():
    """Extract all image URLs from the HTML file."""
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    img_tags = soup.find_all('img')
    
    local_urls = []
    remote_urls = []
    
    for img in img_tags:
        src = img.get('src')
        if not src:
            continue
            
        if src.startswith('/images/'):
            # Local image
            local_urls.append(src)
        elif 'franciscan' in src and 'PhotoAlbum' in src:
            # Remote photo album image
            remote_urls.append(src)
        else:
            # Other image - log it for inspection
            logging.info(f"Other image URL found: {src}")
    
    # Remove duplicates
    local_urls = list(set(local_urls))
    remote_urls = list(set(remote_urls))
    
    return local_urls, remote_urls

def download_image(url, save_path, is_remote=True):
    """Download an image from URL and save it to the specified path."""
    try:
        if is_remote:
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return True
        else:
            # For local URLs, note that we can't actually download them
            # Just log that we would need to access them from the server
            logging.info(f"Local image would need to be copied from the server: {url} -> {save_path}")
            return False
            
    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading {url}: {str(e)}")
        return False

def main():
    """Main function to coordinate the image download process."""
    start_time = time.time()
    logging.info("Starting image download process...")
    
    # Get image URLs from HTML
    local_urls, remote_urls = get_image_urls_from_html()
    
    logging.info(f"Found {len(local_urls)} local images and {len(remote_urls)} remote images")
    
    # Process local images
    local_success = 0
    for i, url in enumerate(local_urls):
        filename = os.path.basename(url)
        save_path = os.path.join(INTERFACE_DIR, filename)
        
        logging.info(f"Processing local image [{i+1}/{len(local_urls)}]: {filename}")
        if download_image(url, save_path, is_remote=False):
            local_success += 1
    
    # Process remote images
    remote_success = 0
    for i, url in enumerate(remote_urls):
        filename = os.path.basename(url)
        save_path = os.path.join(PHOTOS_DIR, filename)
        
        logging.info(f"Downloading remote image [{i+1}/{len(remote_urls)}]: {filename}")
        if download_image(url, save_path, is_remote=True):
            remote_success += 1
            
            # Log progress for every 10 images or at specific percentage milestones
            if (i+1) % 10 == 0 or (i+1) / len(remote_urls) in [0.25, 0.5, 0.75, 1.0]:
                percent = (i+1) / len(remote_urls) * 100
                logging.info(f"Progress: {percent:.1f}% ({i+1}/{len(remote_urls)})")
    
    # Summary
    elapsed_time = time.time() - start_time
    logging.info("\n===== Download Summary =====")
    logging.info(f"Total time: {elapsed_time:.1f} seconds")
    logging.info(f"Local images: {local_success}/{len(local_urls)} noted")
    logging.info(f"Remote images: {remote_success}/{len(remote_urls)} downloaded")
    logging.info(f"Success rate: {(remote_success/len(remote_urls))*100:.1f}%")
    logging.info("===========================")
    
    # Additional instructions for local images
    if local_urls:
        logging.info("\nNOTE: Local images (/images/*) need to be copied manually from the source server.")
        logging.info("These typically include interface elements like logos, buttons, etc.")

if __name__ == "__main__":
    main()

