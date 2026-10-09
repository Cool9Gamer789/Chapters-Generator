# Chapter Splitter

`split_chapters.py` takes one text file containing a whole story and splits it into a separate `.txt` file for each chapter. Chapters are found by looking for marker lines like `* Chapter 1`.

## How to Use

1. Run the script:
   ```
   python split_chapters.py
   ```
2. Paste the path to your text file when prompted (quotes around the path are fine):
   ```
   Path: C:\Users\you\Documents\story.txt
   ```

Requires Python 3.6 or newer. No extra packages are needed.

## Valid Input

A plain-text file (`.txt`) that meets these conditions:

- **Encoding:** UTF-8. A leading BOM (invisible marker some programs add) is handled automatically. Windows (CRLF) and Mac/Linux (LF) line endings both work. Files in other encodings may fail to open.
- **Chapter markers:** At least one marker line in the exact format described below.

### The marker format is strict

Each chapter must begin with a line that contains **only** a marker:

```
* Chapter 1
```

A line counts as a marker only if it follows these rules:

| Rule | Detail |
|---|---|
| Starts with an asterisk | `*` is required. `Chapter 1` or `# Chapter 1` is not a marker. |
| Followed by the word "Chapter" | Upper or lower case is fine (`* chapter 1` works). |
| Followed by a whole number | Digits only. `* Chapter One` is not a marker. |
| Nothing else on the line | Spaces before or after are fine, but no other text. |

| Line | Marker? |
|---|---|
| `* Chapter 1` | Yes |
| `* chapter 12` | Yes |
| `   * Chapter 3   ` | Yes (extra spaces are ignored) |
| `* Chapter 1: The Heist` | **No** (extra text after the number) |
| `* Chapter One` | **No** (number is spelled out) |
| `** Chapter 1` | **No** (two asterisks) |
| `Chapter 1` | **No** (missing asterisk) |
| `He read * Chapter 1 aloud.` | **No** (marker must be the whole line) |

A line that is not an exact marker is **not** an error. The script treats it as ordinary story text and keeps it inside whichever chapter it falls in. If your markers are slightly off, chapters can silently merge into one, so check the "Done" message for the chapter count.

## Output

A new folder is created **next to your input file**, named after it with `_chapters` added:

```
story.txt
story_chapters/
    chapter_01.txt
    chapter_02.txt
    chapter_03.txt
    preamble.txt        (only if there was text before Chapter 1)
```

Each chapter file contains:

- The `* Chapter N` heading, then the chapter's text.
- One blank line between every line, for readability. Blank lines already in the original are removed first, so spacing is always uniform.
- Trailing spaces removed from each line, and a single newline at the end of the file.

File names use the chapter number from the marker, padded with zeros (`chapter_02`, `chapter_10`) so they sort correctly. Padding widens automatically for 100 or more chapters.

**Things to be aware of:**

- Files are named by the number in the marker, not by position. If the file has two `* Chapter 2` markers, the second overwrites the first.
- Re-running the script overwrites files with the same names. It does not delete old files.
- If no markers are found, the script stops with an error and creates nothing.

## Settings

At the top of the script:

```python
STRIP_HEADER = False
```

Set to `True` to leave the `* Chapter N` line out of each chapter file.

## How the Code Works

**`split_into_chapters(lines)`**
Reads the file's lines one at a time. When a line matches the chapter marker, it starts a new chapter. Every other line is added to the current chapter. Lines before the first marker go into a separate "preamble" pile. It returns the preamble and the list of chapters (each with a number, heading, and body lines).

**`write_text(path, lines)`**
Saves a list of lines to a file. It removes empty lines and trailing spaces, puts one blank line between each remaining line, and ends the file with a single newline.

**`clean_path(raw)`**
Tidies the pasted path. It trims extra spaces, removes matching quotes around the path (as pasted by Windows "Copy as path"), and expands `~` to your home folder. It returns a path the rest of the script can use.

**`main()`**
Runs the whole process: asks for the path, checks the file exists, reads it, splits it into chapters, creates the output folder, and writes one file per chapter (plus `preamble.txt` if needed). It then prints a summary.

## Preamble

Any text before the first `* Chapter` marker (a title, author note, etc.) belongs to no chapter. It's saved separately as `preamble.txt` so nothing is lost. There is at most one preamble per file, and none is created if the file starts directly with a chapter marker.
