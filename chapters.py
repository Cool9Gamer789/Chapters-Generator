import re
import sys
from pathlib import Path
 
# Set to True to leave the "* Chapter N" line out of each chapter file.
STRIP_HEADER = True
 
# Matches a whole line like "* Chapter 12" (case-insensitive, tolerant of extra spaces).
CHAPTER_RE = re.compile(r"^\s*\*\s*Chapter\s+(\d+)\s*$", re.IGNORECASE)
 
 
def split_into_chapters(lines):
    """Return (preamble_lines, [(chapter_number, header_line, body_lines), ...])."""
    preamble = []
    chapters = []
    current = None
 
    for line in lines:
        match = CHAPTER_RE.match(line)
        if match:
            current = (int(match.group(1)), line, [])
            chapters.append(current)
        elif current is None:
            preamble.append(line)
        else:
            current[2].append(line)
 
    return preamble, chapters
 
 
def write_text(path, lines):
    """Write lines to path with a blank line between each, ending in one newline.
    Any blank lines already in the original are dropped first so the spacing
    stays uniform (exactly one blank line between lines).
    """
    kept = [line.rstrip() for line in lines if line.strip()]
    text = "\n\n".join(kept) + "\n"
    path.write_text(text, encoding="utf-8")
 
 
def clean_path(raw):
    """Tidy a pasted path: trim whitespace and surrounding quotes, expand ~."""
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in ("'", '"'):
        raw = raw[1:-1].strip()
    return Path(raw).expanduser()
 
 
def main():
    input_file = clean_path(input("Path: "))
 
    if not input_file.is_file():
        sys.exit(f"Error: file not found: {input_file}")

    # Chooses the folder name
    out_dir = input_file.with_name(input_file.stem + "_chapters")
 
    # utf-8-sig drops a leading BOM; text mode normalizes CRLF to LF.
    with open(input_file, "r", encoding="utf-8-sig") as f:
        lines = f.read().splitlines()

    # Sort the lines into chapters
    preamble, chapters = split_into_chapters(lines)
 
    if not chapters:
        sys.exit("Error: no '* Chapter [NUMBER]' markers found in the file.")
 
    out_dir.mkdir(parents=True, exist_ok=True)
 
    # Zero-pad so files sort correctly (chapter_02 before chapter_10).
    width = max(2, len(str(max(num for num, _, _ in chapters))))
 
    if "".join(preamble).strip():
        write_text(out_dir / "preamble.txt", preamble)
        print("Text found before the first chapter was saved to preamble.txt")
 
    for number, header, body in chapters:
        content = body if STRIP_HEADER else [header.strip()] + body
        filename = f"chapter_{number:0{width}d}.txt"
        write_text(out_dir / filename, content)
        print(f"Wrote {out_dir / filename}")
 
    print(f"\nDone: {len(chapters)} chapter(s) saved in '{out_dir}'")
 
 
if __name__ == "__main__":
    main()