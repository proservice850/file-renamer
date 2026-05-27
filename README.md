# File Renamer

A small Python CLI tool that renames files in a folder to a standardized
`YYYY-MM-DD_HHMMSS` format based on each file's modification time.
Handles duplicate timestamps automatically and runs in dry-run mode by default.

Built as Project 1 of learning Python coming from a C/C++ embedded background.

## What it does

For a given folder and file extension, the script:

1. Finds all matching files (e.g. all `.jpg` files)
2. Reads each file's modification timestamp
3. Builds a new name like `2025-08-14_153022.jpg`
4. Renames the file (or previews the rename in dry-run mode)
5. Resolves name collisions by appending `_1`, `_2`, etc.

## Requirements

- Python 3.10 or newer (tested on Python 3.14)
- No third-party packages required (uses only the standard library)

## Setup

Clone or copy the project folder, then from inside it:

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate # macOS/Linux
```

The script has no external dependencies, so no `pip install` step is needed.

## Usage

The script is **dry-run by default** — it prints what *would* happen without
touching anything. Pass `--apply` to actually rename.

### Show help

```bash
python renamer.py --help
```

### Dry-run (preview only) on a folder

```bash
python renamer.py "C:\Users\Naresh\Downloads"
```

### Apply for real

```bash
python renamer.py "C:\Users\Naresh\Downloads" --apply
```

### Use a different extension

```bash
python renamer.py "C:\path\to\folder" --ext png
python renamer.py "C:\path\to\folder" --ext pdf --apply
python renamer.py "C:\Users\Naresh\Downloads" --ext png --apply
```
### Recursively (include subfolders)

```bash
python renamer.py "C:\path\to\folder" --recursive
python renamer.py "C:\path\to\folder" -r --apply
```

## Arguments

| Argument | Type | Default | Description |
|---|---|---|---|
| `folder` | path | (required) | Folder containing files to rename |
| `--ext` | string | `jpg` | File extension to match (without leading dot) |
| `--apply` | flag | off | Without this, runs in dry-run mode |
### Recursively (include subfolders)

```bash
python renamer.py "C:\path\to\folder" --recursive
python renamer.py "C:\path\to\folder" -r --apply
```
## How it handles collisions

If two files share the same modification timestamp (same second), the second
one gets `_1` appended, the third `_2`, and so on. The script also checks
against existing files on disk before settling on a name.

Example:

```
WOULD rename: schutz0.jpg  ->  2025-03-01_185055.jpg
WOULD rename: schutz1.jpg  ->  2025-03-01_185055_1.jpg
```

## Safety notes

- **Always dry-run first.** Confirm the preview looks correct before adding `--apply`.
- **Test on a throwaway folder first.** The script renames files in place;
  there is no built-in undo.
- **Errors don't stop the run.** If one file is locked or permission-denied,
  the script logs the error and continues with the next file.
- **Recursive mode is opt-in.** Without `--recursive`, only the top-level
  folder is processed. This prevents accidental mass-renames of large trees.
## Project structure

```
file-renamer/
├── .venv/         # Python virtual environment (do not edit, do not commit)
├── renamer.py     # The script
└── README.md      # This file
```

## Concepts learned (notes for self)

Coming from C/C++, the Python idioms that came up:

- `pathlib.Path` instead of raw string paths; `/` operator joins paths
- `f"..."` strings for formatted output (better `sprintf`)
- `for x in iterable:` instead of index-based loops
- Sets (`set[str]`) for O(1) "already-seen" tracking
- `try / except OSError as e:` for filesystem error handling
- `argparse` for CLI parsing — auto-generates `--help`
- Type hints (`folder: Path`, `-> str`) — not enforced at runtime, but
  improve editor support and readability
- The `if __name__ == "__main__":` idiom — closest thing to `int main()`
- Virtual environments — one `.venv` per project, isolated dependencies

## Possible next improvements

- Recursive mode (`--recursive`) using `folder.rglob(pattern)`
- Support multiple extensions at once (`--ext jpg,png,heic`)
- Write an undo log so renames can be reversed
- Custom date format via `--format` argument
- Use the photo's EXIF "date taken" instead of file mtime, for jpgs

## License

Personal project — no license specified.