# YouTube Video Downloader - Desktop Application

A user-friendly desktop application that downloads YouTube videos, increases their speed by 1.5x, manages quality for large files, and organizes them by topic automatically.

## 🚀 Features

- **Simple GUI Interface** - Easy-to-use desktop application
- **Batch Processing** - Process multiple YouTube URLs from a text file
- **Speed Enhancement** - Automatically increases video speed by 1.5x
- **Smart Quality Management** - Reduces quality for videos >500MB to <480MB
- **Intelligent Topic Detection** - Automatically categorizes videos by topic
- **Organized Storage** - Creates topic-based folders on your desktop
- **Progress Tracking** - Real-time progress updates and activity logging
- **Cross-Platform** - Works on Windows, macOS, and Linux

## 📦 Installation

### Prerequisites

1. **Python 3.7 or higher**
2. **FFmpeg** (required for video processing)
   
   **Option 1: Automatic Installation (Recommended)**
   - FFmpeg is included in the repository - no separate installation needed!
   
   **Option 2: Manual Installation**
   - Download from [ffmpeg.org](https://ffmpeg.org/download.html)
   - Add to system PATH

### Quick Setup

1. **Clone or download this repository**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

#### Option 1: Download EXE (Easiest - No Python Required)
1. **Go to [Releases](https://github.com/YOUR_USERNAME/youtube-video-downloader/releases)**
2. **Download the latest `YouTube-Video-Downloader.exe`**
3. **Double-click to run** - No installation needed!

#### Option 2: GUI Application (Requires Python)
```bash
python gui_app.py
```

#### Option 3: Command Line (Requires Python)
```bash
python youtube_downloader.py
```

## 🎯 How to Use (GUI Version)

1. **Launch the application** by running `gui_app.py`
2. **Click "Browse..."** to select a text file containing YouTube URLs
3. **Click "Start Processing"** to begin downloading and processing videos
4. **Monitor progress** in the activity log
5. **Access processed videos** in the `Youtube-Videos` folder on your desktop

## 📝 Text File Format

Create a text file with YouTube URLs (one per line):

```
# Lines starting with # are comments and will be ignored
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://youtu.be/abc123def456
https://www.youtube.com/watch?v=xyz789uvw012
```

## 🗂️ Output Structure

Videos are automatically organized by topic:

```
Desktop/
└── Youtube-Videos/
    ├── react/
    │   └── React_Tutorial_Sped_Up.mp4
    ├── docker/
    │   └── Docker_Guide_Sped_Up.mp4
    ├── kubernetes/
    │   └── K8s_Basics_Sped_Up.mp4
    └── general/
        └── Other_Video_Sped_Up.mp4
```

## 🧠 Smart Topic Detection

The application automatically detects topics from video titles and creates corresponding folders:

### **Full Stack Development**
- **Frontend**: React, Vue, Angular, Next.js, TypeScript, Tailwind CSS
- **Backend**: Node.js, Express, Django, Flask, Spring Boot, Go, Rust
- **Databases**: PostgreSQL, MySQL, MongoDB, Redis, Prisma

### **DevOps & Infrastructure**
- **Containerization**: Docker, Kubernetes, Helm
- **CI/CD**: Jenkins, GitHub Actions, GitLab CI
- **Cloud**: AWS, Azure, Google Cloud, Heroku, Vercel
- **Monitoring**: Prometheus, Grafana, Datadog

### **Other Technologies**
- **Mobile**: React Native, Flutter, Swift, Kotlin
- **Security**: JWT, OAuth, SSL/TLS
- **Testing**: Unit Testing, Integration Testing, E2E Testing
- **Machine Learning**: TensorFlow, PyTorch, Data Science

## ⚙️ Video Processing Pipeline

1. **Download** - Videos downloaded at maximum 720p quality
2. **Quality Check** - If video >500MB, quality is reduced until <480MB
3. **Speed Enhancement** - All videos sped up by 1.5x
4. **Organization** - Videos saved in topic-based subfolders

## 🛠️ Technical Details

- **Language**: Python 3.7+
- **GUI Framework**: Tkinter (built-in)
- **Video Processing**: MoviePy + FFmpeg
- **YouTube Downloading**: yt-dlp
- **Topic Detection**: Smart pattern matching with 150+ topics

## 📋 Requirements

```
yt-dlp==2023.12.30
moviepy==1.0.3
Pillow==10.1.0
```

## 🔧 Troubleshooting

### FFmpeg Not Found
```
Error: FFmpeg not found. Please install FFmpeg to use this script.
```
**Solution**: Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html) and add to system PATH.

### Video Processing Errors
- Ensure sufficient disk space
- Check internet connection
- Verify YouTube URLs are valid

### Permission Errors
- Run the application with appropriate permissions
- Ensure output folder is writable

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Ensure all prerequisites are installed
3. Create an issue with detailed error information

---

**Enjoy faster, organized YouTube video learning!** 🚀
