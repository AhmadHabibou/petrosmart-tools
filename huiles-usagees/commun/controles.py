"""Controles de forme appliques a tout le depot."""
from pathlib import Path

INTERDITS = (chr(0x2014), chr(0x2013))  # tiret long, tiret moyen
EXTENSIONS = {".md", ".py", ".csv", ".txt", ".html", ".js", ".json"}


def tirets_interdits(racine: Path):
    fautes = []
    for p in racine.rglob("*"):
        if p.suffix in EXTENSIONS and p.is_file() and ".git" not in p.parts:
            for i, ligne in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                if any(c in ligne for c in INTERDITS):
                    fautes.append(f"{p.relative_to(racine)}:{i}")
    return fautes
