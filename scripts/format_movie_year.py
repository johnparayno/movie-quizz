#!/usr/bin/env python3
"""
Convert movie format from "Name,Year" or "Name - Year" to "Name (Year)" in quiz JSON files.
"""

import json
import re
from pathlib import Path


def to_display_format(s: str) -> str:
    """Convert 'Rocky,1976' or 'Rocky - 1976' to 'Rocky (1976)'."""
    if not s:
        return s
    # "Name - Year" -> "Name (Year)"
    m = re.match(r"^(.+?)\s+-\s+(\d{4})\s*$", s.strip())
    if m:
        return f"{m.group(1).strip()} ({m.group(2)})"
    # "Name (Year)" -> already correct, pass through
    m = re.match(r"^(.+?)\s*\((\d{4})\)\s*$", s.strip())
    if m:
        return s.strip()
    # "Name,Year" -> "Name (Year)"
    if "," in s:
        parts = s.rsplit(",", 1)
        if len(parts) == 2:
            title, year = parts[0].strip(), parts[1].strip()
            if year.isdigit():
                return f"{title} ({year})"
    return s


def update_file(path: Path) -> int:
    """Update a JSON file; return count of entries updated."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    count = 0
    for entry in data:
        if "options" in entry:
            entry["options"] = [to_display_format(o) for o in entry["options"]]
            count += 1
        if "answer" in entry:
            entry["answer"] = to_display_format(entry["answer"])
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return count


def main():
    base = Path(__file__).parent.parent
    files = [
        base / "data" / "movie_quizz_500_updated.json",
        base / "frontend" / "movie_quizz_500_updated.json",
        base / "data" / "movie_quizz_1000.json",
        base / "frontend" / "movie_quizz_1000.json",
        base / "data" / "movie_quizz.json",
        base / "frontend" / "movie_quizz.json",
    ]
    for path in files:
        if path.exists():
            n = update_file(path)
            print(f"Updated {path.name}: {n} entries")
        else:
            print(f"Skipped {path.name} (not found)")


if __name__ == "__main__":
    main()
