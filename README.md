> **Script consolidation (2026-11-03):** Selected utility scripts from this repository were integrated into [Learning_Modules/tools/youtube-downloader](https://github.com/MeiRR17/Learning_Modules/tree/main/tools/youtube-downloader), via [PR #4](https://github.com/MeiRR17/Learning_Modules/pull/4). The import includes source provenance and CI syntax/content checks. The original repository remains accessible, may contain additional data or configuration, and has **not been archived or deleted**. Consult the consolidated README for exclusions and portability changes.

---

# YouTube Video Downloader

A Python script that downloads YouTube videos, increases their speed by 1.5x, manages quality for large files, and organizes them by topic.

## Features

- Downloads YouTube videos from a text file (one URL per line)
- Tracks the exact file returned by yt-dlp; videos with identical titles have distinct ID-suffixed filenames
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
- Quality and speed changes are encoded into unique temporary MP4 files and promoted only after success
- A failed speed conversion marks that URL as failed, and any failed URL gives the CLI a nonzero exit status

## Notes

- Processing time depends on video length and your internet speed
- Large videos may take longer to process due to quality reduction
- FFmpeg is required for video processing operations

## File isolation and safe video processing

Each requested YouTube URL is downloaded as a **single video** (`noplaylist`), with a filename containing the video's unique YouTube ID. The downloader processes only the file path returned by `yt-dlp` for that request; other MP4, WebM, or MKV files in the same topic folder are never selected by broad directory globbing.

When a download is larger than 500 MiB, the script tries to compress it below 480 MiB. Compression produces a temporary MP4 and promotes it only when the output meets the size requirement. Failed compression leaves the existing source intact and logs a warning if the size target is still not met.

The 1.5× speed operation likewise encodes to a unique temporary MP4. It closes the media file handles before atomically replacing the destination (including on Windows). If the encoding fails, it removes the temporary output and leaves the original file untouched; the URL is reported as failed.

`python youtube_downloader.py urls.txt` now returns **exit code 1** if one or more URLs cannot be processed, and 0 only when every URL succeeds. The script continues processing subsequent URLs after an individual failure. Installation still requires `yt-dlp`, `moviepy`, and the FFmpeg executable.

## Safe repeated runs (processed-video receipts)

The downloader now maintains an atomic processing index at `Desktop/Youtube-Videos/.processed-videos.json`, keyed by YouTube's 11-character video ID. After a successful 1.5× conversion, the index records the exact relative MP4 path, byte size, modification timestamp, SHA-256, and speed setting. On a subsequent invocation, the downloader verifies the on-disk file against this receipt **before downloading or converting it again**. An unchanged previously processed file is skipped, including duplicate URLs within the same input file.

An index entry with a missing file, altered checksum, timestamp or size is treated as stale and the URL is processed again. An unreadable or malformed index causes the affected URLs to fail rather than silently deleting existing processing history. The index is written through a uniquely named temporary file and atomically replaced, with file contents synced before the rename.

Receipts apply to successful processing carried out by this new version. Videos processed using the old implementation do not have receipts and cannot be safely recognized as already sped up. If a process crashes after completing conversion but **before** recording its receipt, that conversion is not yet covered by the index. Keep the `.processed-videos.json` file with the output folder when moving or backing up your library. Concurrent runs writing to the same library are not supported, because they can overwrite each other's receipts.

This capability is implemented in the standalone repository; the older copy consolidated into `Learning_Modules/tools/youtube-downloader` is not automatically updated by this PR.
