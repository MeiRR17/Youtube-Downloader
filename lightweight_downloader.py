import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
import yt_dlp
from pathlib import Path

class LightweightYouTubeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader - Lightweight")
        self.root.geometry("600x450")
        self.root.resizable(True, True)
        
        # Variables
        self.selected_file = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready to process YouTube videos")
        
        # Create UI
        self.create_widgets()
    
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="YouTube Video Downloader", 
                               font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # File selection
        file_frame = ttk.LabelFrame(main_frame, text="Select Text File", padding="10")
        file_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Label(file_frame, text="Text file with YouTube URLs:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        file_entry = ttk.Entry(file_frame, textvariable=self.selected_file, state='readonly')
        file_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        browse_btn = ttk.Button(file_frame, text="Browse...", command=self.browse_file)
        browse_btn.grid(row=1, column=1, sticky=tk.W)
        
        # Process button
        self.process_btn = ttk.Button(main_frame, text="Start Processing", 
                                    command=self.start_processing)
        self.process_btn.grid(row=3, column=0, columnspan=2, pady=(20, 0))
        
        # Status
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.grid(row=0, column=0, sticky=tk.W)
        
        # FFmpeg notice
        ffmpeg_frame = ttk.LabelFrame(main_frame, text="FFmpeg Required", padding="10")
        ffmpeg_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ffmpeg_text = ttk.Label(ffmpeg_frame, 
                               text="FFmpeg is required for video processing.\n\n"
                                     "Download FFmpeg from: https://ffmpeg.org/download.html\n\n"
                                     "After installation, restart this application.",
                               font=('Arial', 9), foreground='orange')
        ffmpeg_text.grid(row=0, column=0, sticky=tk.W)
        
        # Log
        log_frame = ttk.LabelFrame(main_frame, text="Activity Log", padding="10")
        log_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, width=60, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def log_message(self, message):
        """Add message to log"""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.config(state='disabled')
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def browse_file(self):
        """Open file dialog to select text file"""
        file_path = filedialog.askopenfilename(
            title="Select Text File with YouTube URLs",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            self.selected_file.set(file_path)
            self.log_message(f"Selected file: {os.path.basename(file_path)}")
    
    def start_processing(self):
        """Start processing in separate thread"""
        file_path = self.selected_file.get()
        
        if not file_path:
            messagebox.showwarning("No File Selected", "Please select a text file with YouTube URLs.")
            return
        
        if not os.path.exists(file_path):
            messagebox.showerror("File Not Found", f"The selected file does not exist:\n{file_path}")
            return
        
        # Check for FFmpeg
        if not self.check_ffmpeg():
            messagebox.showerror("FFmpeg Not Found", 
                              "FFmpeg is required for video processing.\n\n"
                              "Please install FFmpeg from: https://ffmpeg.org/download.html\n\n"
                              "After installation, restart this application.")
            return
        
        # Disable button during processing
        self.process_btn.config(state='disabled')
        self.status_var.set("Processing...")
        
        # Start processing in background thread
        thread = threading.Thread(target=self.process_file, args=(file_path,))
        thread.daemon = True
        thread.start()
    
    def check_ffmpeg(self):
        """Check if FFmpeg is available"""
        try:
            import subprocess
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True, 
                        creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def download_video(self, url):
        """Download a single YouTube video"""
        try:
            self.log_message(f"Downloading: {url}")
            
            # Create output directory
            output_dir = Path.home() / "Desktop" / "Youtube-Videos"
            output_dir.mkdir(exist_ok=True)
            
            # Download options
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
            
            self.log_message("Downloaded successfully!")
            return True
            
        except Exception as e:
            self.log_message(f"Error: {str(e)}")
            return False
    
    def process_file(self, file_path):
        """Process the file in background"""
        try:
            # Read URLs
            with open(file_path, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            if not urls:
                self.log_message("No URLs found in file")
                self.root.after(0, lambda: self.status_var.set("No URLs found"))
                return
            
            self.log_message(f"Found {len(urls)} URLs to process")
            
            successful = 0
            failed = 0
            
            for i, url in enumerate(urls, 1):
                self.log_message(f"[{i}/{len(urls)}] {url}")
                if self.download_video(url):
                    successful += 1
                else:
                    failed += 1
            
            self.log_message(f"Results: Successful: {successful}, Failed: {failed}")
            self.log_message(f"Videos saved to: {Path.home() / 'Desktop' / 'Youtube-Videos'}")
            self.root.after(0, lambda: self.status_var.set(f"Complete! Success: {successful}, Failed: {failed}"))
            
        except Exception as e:
            error_msg = f"Error processing file: {str(e)}"
            self.log_message(f"ERROR: {error_msg}")
            self.root.after(0, lambda: self.status_var.set("Error occurred"))
            self.root.after(0, lambda: messagebox.showerror("Processing Error", error_msg))
        finally:
            # Re-enable button
            self.root.after(0, lambda: self.process_btn.config(state='normal'))

def main():
    # Create GUI
    root = tk.Tk()
    app = LightweightYouTubeGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()
