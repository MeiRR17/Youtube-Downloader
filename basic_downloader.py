import yt_dlp
import os
import sys
from pathlib import Path

def download_video(url):
    """Download a single YouTube video"""
    try:
        print(f"Downloading: {url}")
        
        # Create output directory
        output_dir = Path.home() / "Desktop" / "Youtube-Videos"
        output_dir.mkdir(exist_ok=True)
        
        # Basic download options with better compatibility
        ydl_opts = {
            'outtmpl': str(output_dir / '%(title)s.%(ext)s'),
            'format': 'worst[ext=mp4]/worst',
            'quiet': False,
            'no_warnings': False,
            'extract_flat': False,
            'ignoreerrors': True,
            'retries': 2,
            'fragment_retries': 2,
            'no_check_certificate': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        print("Downloaded successfully!")
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def main():
    print("=== YouTube Video Downloader ===")
    
    # Check for URLs file
    urls_file = "youtube_urls.txt"
    if not os.path.exists(urls_file):
        print(f"Error: {urls_file} not found!")
        print("Please create this file with YouTube URLs (one per line)")
        return
    
    # Read URLs
    try:
        with open(urls_file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return
    
    if not urls:
        print("No URLs found in file!")
        return
    
    print(f"Found {len(urls)} URLs to process")
    
    # Download each URL
    successful = 0
    failed = 0
    
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] {url}")
        if download_video(url):
            successful += 1
        else:
            failed += 1
    
    print(f"\n=== Results ===")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Videos saved to: {Path.home() / 'Desktop' / 'Youtube-Videos'}")
    
    print("\nPress Enter to exit...")
    input()

if __name__ == "__main__":
    main()
