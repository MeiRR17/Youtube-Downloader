#!/usr/bin/env python3
"""
YouTube Video Downloader - Launcher
Simple launcher script for the GUI application
"""

import sys
import os

def main():
    """Launch the GUI application"""
    try:
        # Import and run the GUI app
        from gui_app import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"Error importing GUI application: {e}")
        print("Please ensure all dependencies are installed:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error launching application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
