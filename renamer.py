"""
File renamer: renames files in a folder to YYYY-MM-DD_HHMMSS based on
each file's modification time. Handles duplicate timestamps, errors,
and optional recursive traversal of subfolders.
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path


def build_new_name(file: Path, used_in_folder: set[str]) -> str:
    """Build a unique new name for `file`, avoiding collisions within its folder."""
    mtime = datetime.fromtimestamp(file.stat().st_mtime)
    base = mtime.strftime("%Y-%m-%d_%H%M%S")
    suffix = file.suffix

    candidate = f"{base}{suffix}"
    counter = 1
    while candidate in used_in_folder or (file.parent / candidate).exists():
        candidate = f"{base}_{counter}{suffix}"
        counter += 1
    return candidate


def rename_folder(folder: Path, extension: str, dry_run: bool, recursive: bool) -> None:
    if not folder.is_dir():
        sys.exit(f"Error: {folder} is not a directory.")

    pattern = f"*.{extension.lstrip('.')}"
    iterator = folder.rglob(pattern) if recursive else folder.glob(pattern)

    # per-folder set of used names, so collisions only count within the same folder
    used_by_folder: dict[Path, set[str]] = {}
    processed = 0
    errors = 0
    log_path = folder / "renames.log"

    for file in iterator:
        if not file.is_file():
            continue  # skip directories that happen to match
        if file == log_path:
            continue  # never rename our own log file

        try:
            used_in_folder = used_by_folder.setdefault(file.parent, set())
            new_name = build_new_name(file, used_in_folder)
            used_in_folder.add(new_name)
            new_path = file.with_name(new_name)

            # show the path relative to the top-level folder for cleaner output
            try:
                shown_old = file.relative_to(folder)
                shown_new = new_path.relative_to(folder)
            except ValueError:
                shown_old, shown_new = file, new_path

            if new_path == file:
                print(f"Skipped (already correct): {shown_old}")
                continue

            if dry_run:
                print(f"WOULD rename: {shown_old}  ->  {shown_new}")
            else:
                file.rename(new_path)
                print(f"Renamed:      {shown_old}  ->  {shown_new}")
                timestamp = datetime.now().isoformat(timespec="seconds")
                with log_path.open("a", encoding="utf-8") as log:
                    log.write(f"{timestamp}\t{file}\t{new_path}\n")
            processed += 1

        except OSError as e:
            print(f"ERROR on {file}: {e}")
            errors += 1

    mode = "dry-run" if dry_run else "real"
    scope = "recursive" if recursive else "top-level only"
    print(f"\nDone ({mode}, {scope}). {processed} processed, {errors} errors.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rename files to YYYY-MM-DD_HHMMSS based on modified time."
    )
    parser.add_argument("folder", type=Path, help="Folder containing files to rename")
    parser.add_argument("--ext", default="jpg", help="File extension to match (default: jpg)")
    parser.add_argument("--apply", action="store_true",
                        help="Actually rename. Without this flag, runs in dry-run mode.")
    parser.add_argument("--recursive", "-r", action="store_true",
                        help="Also process files in subfolders.")
    args = parser.parse_args()

    rename_folder(
        folder=args.folder,
        extension=args.ext,
        dry_run=not args.apply,
        recursive=args.recursive,
    )


if __name__ == "__main__":
    main()