# Python File Organizer
A small, production-ready Python utility that organizes files in a folder by file type.

## What It Does
Files are moved into subfolders created inside the source folder:
- Images
- Documents
- Videos
- Audio
- Archives
- Others (unknown extensions)

Files are processed only at the top level of the source folder (non-recursive).  
Directories are ignored.

## Features
- Automatic file organization by extension
- Safe file moves (no overwriting)
- Configurable category mappings
- Command-line interface
- Action logging for traceability

## Logging
All actions (moved files, skipped items, errors) are appended to `log.txt` inside the source folder.

## Usage

Run with an explicit source folder:

```bash
python organizer.py --source "C:\\Users\\YOU\\Downloads"
```

Or use the default (user's Downloads folder):

```bash
python organizer.py
```

Notes
- The script uses safe file moves and will not overwrite existing files. If a filename already exists in the target folder, a suffix like ` (1)` is appended before the extension.
- No external libraries are required.

Example log output (excerpt from `log.txt`):

```
2026-01-16 12:34:10 | INFO | Starting organization for: C:\Users\YOU\Downloads
2026-01-16 12:34:10 | INFO | Moved: C:\Users\YOU\Downloads\photo.jpg -> C:\Users\YOU\Downloads\Images\photo.jpg
2026-01-16 12:34:11 | INFO | Moved: C:\Users\YOU\Downloads\report.pdf -> C:\Users\YOU\Downloads\Documents\report.pdf
2026-01-16 12:34:11 | ERROR | Failed to move C:\Users\YOU\Downloads\locked.docx -> C:\Users\YOU\Downloads\Documents: [Errno 13] Permission denied
2026-01-16 12:34:11 | INFO | Organization complete
```

Files
- `config.py` — category mapping and optional defaults
- `organizer.py` — main script to run

If you want, I can:
- Add a `--dry-run` flag to preview changes without moving files
- Add recursion or per-category destination configuration
# python-file-organizer