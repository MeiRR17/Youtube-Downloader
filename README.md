# YouTube Video Downloader

A Python script that downloads YouTube videos, increases their speed by 1.5x, manages quality for large files, and organizes them by topic.

## Features

- Downloads YouTube videos from a text file (one URL per line)
- Increases video playback speed by 1.5x
- Automatically reduces quality for videos > 500MB to < 480MB
- Organizes videos by topic in subfolders
- Creates a `Youtube-Videos` folder on your desktop
- Smart topic detection based on video titles

## Requirements

1. Python 3.7 or higher
2. FFmpeg (must be installed and added to PATH)
3. Required Python packages (install with pip)

## Installation

1. Install FFmpeg:
   - Download from https://ffmpeg.org/download.html
   - Add to system PATH

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Create a text file with YouTube URLs (one per line)
   - Default file name: `youtube_urls.txt`
   - Lines starting with `#` are ignored

2. Run the script:
   ```bash
   python youtube_downloader.py
   ```

   Or specify a custom URLs file:
   ```bash
   python youtube_downloader.py my_urls.txt
   ```

## Output Structure

```
Desktop/
└── Youtube-Videos/
    ├── react/
    │   └── React_Tutorial_Sped_Up.mp4
    ├── python/
    │   └── Python_Basics_Sped_Up.mp4
    ├── javascript/
    │   └── JavaScript_Guide_Sped_Up.mp4
    └── general/
        └── Other_Video_Sped_Up.mp4
```

## Topic Detection

The script automatically detects topics from video titles and creates corresponding folders. Common topics include:
- Programming languages (python, javascript, java, etc.)
- Frameworks (react, angular, vue, django, etc.)
- Technologies (docker, kubernetes, aws, etc.)
- Development concepts (machine learning, data science, etc.)

If no specific topic is found, videos are placed in a `general` folder.

## Video Processing

1. **Download**: Videos are downloaded at maximum 720p quality
2. **Quality Check**: If video > 500MB, quality is reduced until < 480MB
3. **Speed Increase**: All videos are sped up by 1.5x
4. **Organization**: Videos are saved in topic-based subfolders

## Example URLs File

```
# YouTube URLs - one per line
# Lines starting with # are comments

https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://youtu.be/abc123def456
```

## Error Handling

- The script includes comprehensive error handling and logging
- Failed downloads are logged but don't stop the entire process
- Temporary files are cleaned up automatically

## Notes

- Processing time depends on video length and your internet speed
- Large videos may take longer to process due to quality reduction
- FFmpeg is required for video processing operations
