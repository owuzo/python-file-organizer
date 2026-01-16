"""
File organizer script
- Scans a source folder (non-recursive)
- Detects file types by extension using mappings from `config.py`
- Moves files into category subfolders (created if missing)
- Avoids overwriting by choosing a safe name when conflicts occur
- Logs all actions to `log.txt` in the source folder using Python's logging

Usage:
    python organizer.py --source "C:\\Users\\...\\Downloads"

No external libraries required.
"""
from __future__ import annotations

import argparse
import logging
import os
import shutil
from pathlib import Path
from typing import Dict, Iterable, Optional

from config import CATEGORY_MAP, DEFAULT_SOURCE

LOG_FILENAME = "log.txt"


def setup_logger(log_path: Path) -> logging.Logger:
    """Configure and return a logger that writes to log_path."""
    logger = logging.getLogger("file_organizer")
    logger.setLevel(logging.INFO)

    # Avoid adding multiple handlers if setup_logger is called multiple times
    if not logger.handlers:
        handler = logging.FileHandler(log_path, encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def normalize_extension(name: str) -> str:
    """Return the file extension in lowercase without leading dot."""
    return Path(name).suffix.lower().lstrip(".")


def get_category(ext: str, mapping: Dict[str, Iterable[str]]) -> str:
    """Return the category name for the given extension. Unknown extensions go to 'Others'."""
    if not ext:
        return "Others"
    for category, exts in mapping.items():
        if ext in exts:
            return category
    return "Others"


def ensure_dir(path: Path) -> None:
    """Create directory if it does not exist."""
    path.mkdir(parents=True, exist_ok=True)


def make_safe_target(target_dir: Path, filename: str) -> Path:
    """Return a safe (non-colliding) Path inside target_dir for filename.

    If a file with the same name exists, append a numeric suffix before the extension.
    e.g. file.txt -> file (1).txt
    """
    target = target_dir / filename
    if not target.exists():
        return target

    name = target.stem
    suffix = target.suffix  # includes the dot if present
    counter = 1
    while True:
        new_name = f"{name} ({counter}){suffix}"
        new_target = target_dir / new_name
        if not new_target.exists():
            return new_target
        counter += 1


def safe_move(src: Path, dest_dir: Path, logger: logging.Logger) -> Optional[Path]:
    """Move src file into dest_dir safely (no overwrite). Returns the final path or None on error."""
    try:
        ensure_dir(dest_dir)
        target = make_safe_target(dest_dir, src.name)
        shutil.move(str(src), str(target))
        logger.info(f"Moved: {src} -> {target}")
        return target
    except Exception as exc:  # Catch broad exceptions to ensure logging
        logger.error(f"Failed to move {src} -> {dest_dir}: {exc}")
        return None


def organize_folder(source: Path, mapping: Dict[str, Iterable[str]], logger: logging.Logger) -> None:
    """Scan `source` (non-recursive) and move files into category folders.

    Directories are ignored. Hidden files are processed like ordinary files.
    """
    if not source.exists() or not source.is_dir():
        logger.error(f"Source folder does not exist or is not a directory: {source}")
        raise FileNotFoundError(f"Source folder not found: {source}")

    # Iterate only top-level entries
    with os.scandir(source) as it:
        for entry in it:
            try:
                if entry.is_file():
                    ext = normalize_extension(entry.name)
                    category = get_category(ext, mapping)
                    dest_dir = source / category
                    safe_move(Path(entry.path), dest_dir, logger)
                else:
                    # Skip directories
                    logger.debug(f"Skipped directory: {entry.path}")
            except Exception as exc:
                logger.error(f"Error processing {entry.path}: {exc}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Organize files in a folder by file type.")
    parser.add_argument(
        "--source",
        "-s",
        dest="source",
        default=DEFAULT_SOURCE,
        help="Path to the source folder to organize. Defaults to user's Downloads folder.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = Path(args.source).expanduser().resolve()

    log_path = source / LOG_FILENAME
    logger = setup_logger(log_path)

    logger.info(f"Starting organization for: {source}")
    try:
        organize_folder(source, CATEGORY_MAP, logger)
        logger.info("Organization complete")
        return 0
    except Exception as exc:
        logger.exception(f"Unhandled error: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
