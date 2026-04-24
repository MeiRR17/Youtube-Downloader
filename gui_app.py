import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
from pathlib import Path
import logging
from youtube_downloader import YouTubeDownloader

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Set style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Variables
        self.selected_file = tk.StringVar()
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Ready to process YouTube videos")
        
        # Downloader instance
        self.downloader = YouTubeDownloader()
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="YouTube Video Downloader", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="Select Text File", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Label(file_frame, text="Text file with YouTube URLs:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # File path display
        file_entry = ttk.Entry(file_frame, textvariable=self.selected_file, state='readonly')
        file_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Browse button
        browse_btn = ttk.Button(file_frame, text="Browse...", command=self.browse_file)
        browse_btn.grid(row=1, column=1, sticky=tk.W)
        
        # Instructions
        instructions = ttk.Label(file_frame, 
                               text="Each line should contain one YouTube URL. Lines starting with # are ignored.",
                               font=('Arial', 9), foreground='gray')
        instructions.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        progress_frame.columnconfigure(0, weight=1)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Status label
        status_label = ttk.Label(progress_frame, textvariable=self.status_var, 
                               font=('Arial', 10))
        status_label.grid(row=1, column=0, sticky=tk.W)
        
        # Log section
        log_frame = ttk.LabelFrame(main_frame, text="Activity Log", padding="10")
        log_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, width=60, 
                                                 wrap=tk.WORD, state='disabled')
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Buttons section
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=(0, 10))
        
        # Process button
        self.process_btn = ttk.Button(button_frame, text="Start Processing", 
                                    command=self.start_processing, style='Accent.TButton')
        self.process_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Clear log button
        clear_btn = ttk.Button(button_frame, text="Clear Log", command=self.clear_log)
        clear_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Open output folder button
        output_btn = ttk.Button(button_frame, text="Open Output Folder", 
                              command=self.open_output_folder)
        output_btn.grid(row=0, column=2)
        
        # Configure button style
        self.style.configure('Accent.TButton', font=('Arial', 10, 'bold'))
        
    def browse_file(self):
        """Open file dialog to select text file"""
        file_path = filedialog.askopenfilename(
            title="Select Text File with YouTube URLs",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            self.selected_file.set(file_path)
            self.log_message(f"Selected file: {os.path.basename(file_path)}")
    
    def log_message(self, message):
        """Add message to log text area"""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.config(state='disabled')
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Clear the log text area"""
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
    
    def open_output_folder(self):
        """Open the output folder in file explorer"""
        try:
            import subprocess
            import platform
            
            if platform.system() == "Windows":
                os.startfile(str(self.downloader.base_folder))
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", str(self.downloader.base_folder)])
            else:  # Linux
                subprocess.run(["xdg-open", str(self.downloader.base_folder)])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder: {e}")
    
    def start_processing(self):
        """Start processing the selected file"""
        file_path = self.selected_file.get()
        
        if not file_path:
            messagebox.showwarning("No File Selected", "Please select a text file with YouTube URLs.")
            return
        
        if not os.path.exists(file_path):
            messagebox.showerror("File Not Found", f"The selected file does not exist:\n{file_path}")
            return
        
        # Disable button during processing
        self.process_btn.config(state='disabled')
        self.progress_var.set(0)
        self.status_var.set("Starting processing...")
        
        # Start processing in separate thread
        thread = threading.Thread(target=self.process_file, args=(file_path,))
        thread.daemon = True
        thread.start()
    
    def process_file(self, file_path):
        """Process the file in a separate thread"""
        try:
            self.log_message("=" * 50)
            self.log_message(f"Processing file: {os.path.basename(file_path)}")
            self.log_message("=" * 50)
            
            # Read URLs from file
            with open(file_path, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            if not urls:
                self.log_message("No URLs found in the file!")
                self.root.after(0, lambda: self.status_var.set("No URLs found"))
                self.root.after(0, lambda: self.process_btn.config(state='normal'))
                return
            
            self.log_message(f"Found {len(urls)} URLs to process")
            self.root.after(0, lambda: self.status_var.set(f"Processing {len(urls)} videos..."))
            
            successful = 0
            failed = 0
            
            for i, url in enumerate(urls, 1):
                # Update progress
                progress = (i - 1) / len(urls) * 100
                self.root.after(0, lambda p=progress: self.progress_var.set(p))
                self.root.after(0, lambda i=i, total=len(urls): 
                              self.status_var.set(f"Processing video {i}/{total}"))
                
                self.log_message(f"\n[{i}/{len(urls)}] Processing: {url}")
                
                try:
                    # Process video
                    if self.downloader.process_video(url):
                        successful += 1
                        self.log_message(f"✓ Successfully processed video {i}")
                    else:
                        failed += 1
                        self.log_message(f"✗ Failed to process video {i}")
                except Exception as e:
                    failed += 1
                    self.log_message(f"✗ Error processing video {i}: {str(e)}")
            
            # Final update
            self.root.after(0, lambda: self.progress_var.set(100))
            self.root.after(0, lambda: self.status_var.set(
                f"Complete! Successful: {successful}, Failed: {failed}"))
            
            self.log_message("=" * 50)
            self.log_message(f"Processing complete!")
            self.log_message(f"Successful: {successful}, Failed: {failed}")
            self.log_message(f"Videos saved to: {self.downloader.base_folder}")
            self.log_message("=" * 50)
            
        except Exception as e:
            error_msg = f"Error processing file: {str(e)}"
            self.log_message(f"ERROR: {error_msg}")
            self.root.after(0, lambda: self.status_var.set("Error occurred"))
            self.root.after(0, lambda: messagebox.showerror("Processing Error", error_msg))
        
        finally:
            # Re-enable button
            self.root.after(0, lambda: self.process_btn.config(state='normal'))

def main():
    # Check for FFmpeg (bundled or system)
    import subprocess
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
        messagebox.showerror(
            "FFmpeg Not Found", 
            "FFmpeg is required for video processing.\n\n"
            "This should be bundled with the application.\n\n"
            "If this error persists, please install FFmpeg:\n"
            "Download from: https://ffmpeg.org/download.html"
        )
        sys.exit(1)
    
    # Create GUI
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    
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
