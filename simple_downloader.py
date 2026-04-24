import os
import sys
import subprocess
import yt_dlp
from pathlib import Path

class SimpleYouTubeDownloader:
    def __init__(self):
        self.desktop_path = Path.home() / "Desktop"
        self.base_folder = self.desktop_path / "Youtube-Videos"
        self.base_folder.mkdir(exist_ok=True)
    
    def download_video(self, url):
        """Simple video download"""
        try:
            # Create output folder
            output_path = self.base_folder
            
            # Simple download options
            ydl_opts = {
                'outtmpl': str(output_path / '%(title)s.%(ext)s'),
                'format': 'worst',
                'quiet': False,
                'no_warnings': False,
                'extract_flat': False,
                'ignoreerrors': True,
                'retries': 2,
            }
            
            print(f"Downloading: {url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            print("Download completed!")
            return True
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return False
    
    def process_urls(self, file_path):
        """Process URLs from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            if not urls:
                print("No URLs found in file")
                return
            
            print(f"Found {len(urls)} URLs to process")
            
            successful = 0
            failed = 0
            
            for i, url in enumerate(urls, 1):
                print(f"\n[{i}/{len(urls)}] Processing: {url}")
                if self.download_video(url):
                    successful += 1
                    print(f"✓ Success!")
                else:
                    failed += 1
                    print(f"✗ Failed!")
            
            print(f"\nComplete! Success: {successful}, Failed: {failed}")
            print(f"Videos saved to: {self.base_folder}")
            
        except Exception as e:
            print(f"Error processing file: {str(e)}")

def main():
    # Simple FFmpeg check
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True, 
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
        print("FFmpeg found!")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERROR: FFmpeg not found!")
        print("This may affect video processing.")
        print("Continuing anyway...")

if __name__ == "__main__":
    # Check for FFmpeg (bundled or system)
    import sys
    import os
    
    ffmpeg_found = False
    
    # First try to use bundled FFmpeg (in PyInstaller temp directory)
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller bundle
        bundle_dir = sys._MEIPASS
        ffmpeg_path = os.path.join(bundle_dir, 'ffmpeg.exe')
        if os.path.exists(ffmpeg_path):
            ffmpeg_found = True
    
    # If not found in bundle, try system PATH
    if not ffmpeg_found:
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True, 
                        creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            ffmpeg_found = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            ffmpeg_found = False
    
    if not ffmpeg_found:
        print("FFmpeg not found. Video processing may be limited.")
    
    downloader = SimpleYouTubeDownloader()
    
    # Get file path
    urls_file = "youtube_urls.txt"
    if len(sys.argv) > 1:
        urls_file = sys.argv[1]
    
    if not os.path.exists(urls_file):
        print(f"File not found: {urls_file}")
        return
    
    downloader.process_urls(urls_file)
    
    print("\nPress Enter to exit...")
    input()
