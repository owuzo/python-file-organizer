from pathlib import Path

# Category-to-extension mapping used by the organizer.
# Extensions should be lowercase and without the leading dot.
CATEGORY_MAP = {
    "Images": [
        "jpg",
        "jpeg",
        "png",
        "gif",
        "bmp",
        "tiff",
        "webp",
        "svg",
    ],
    "Documents": [
        "pdf",
        "doc",
        "docx",
        "txt",
        "rtf",
        "odt",
        "xls",
        "xlsx",
        "ppt",
        "pptx",
        "md",
        "csv",
    ],
    "Videos": [
        "mp4",
        "mkv",
        "mov",
        "avi",
        "wmv",
        "flv",
        "webm",
    ],
    "Audio": [
        "mp3",
        "wav",
        "aac",
        "flac",
        "ogg",
        "m4a",
    ],
    "Archives": [
        "zip",
        "rar",
        "7z",
        "tar",
        "gz",
        "bz2",
        "xz",
    ],
}

# Optional: default source folder (commented out)
# You can set DEFAULT_SOURCE in the application or pass --source to the script.
DEFAULT_SOURCE = str(Path.home() / "Downloads")
