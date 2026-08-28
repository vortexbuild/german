#!/usr/bin/env python3
"""Übernimmt die Wörter einer Themen-Einheit nach vocab/vocab.csv.

    python3 scripts/import_unit.py 01        # fügt alle Wörter aus themen/01-*.md hinzu

Liest die Markdown-Tabellen in vocab/themen/NN-*.md, nimmt Spalte 1 (deutsch) und
Spalte 2 (englisch), taggt die Zeilen mit der Einheitsnummer, Status "neu".
Wörter, die (nach dem deutschen Feld) schon in vocab.csv stehen, werden übersprungen.
Danach: `python3 scripts/quiz.py --tag NN`.
"""
import csv
import datetime as dt
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
VOCAB = ROOT / "vocab" / "vocab.csv"
THEMEN = ROOT / "vocab" / "themen"
FIELDS = ["deutsch", "englisch", "tags", "status", "streak", "richtig", "hinzugefuegt"]


def parse_tables(md_text):
    """Alle Tabellenzeilen als (deutsch, englisch) zurückgeben."""
    out = []
    for line in md_text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        de, en = cells[0], cells[1]
        if not de or de.lower() == "deutsch":      # Kopfzeile
            continue
        if set(de) <= {"-", ":", " "}:             # Trennzeile |---|---|
            continue
        out.append((de, en))
    return out


def main():
    if len(sys.argv) != 2:
        sys.exit("Aufruf: python3 scripts/import_unit.py <Einheitsnummer, z. B. 01>")
    unit = sys.argv[1].zfill(2)

    matches = sorted(THEMEN.glob(f"{unit}-*.md"))
    if not matches:
        sys.exit(f"Keine Datei vocab/themen/{unit}-*.md gefunden.")
    md = matches[0]

    with VOCAB.open(encoding="utf-8", newline="") as f:
        existing_rows = list(csv.DictReader(f))
    have = {r["deutsch"] for r in existing_rows}

    today = dt.date.today().isoformat()
    added = skipped = 0
    with VOCAB.open("a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        for de, en in parse_tables(md.read_text(encoding="utf-8")):
            if de in have:
                skipped += 1
                continue
            w.writerow({"deutsch": de, "englisch": en, "tags": unit,
                        "status": "neu", "streak": 0, "hinzugefuegt": today})
            have.add(de)
            added += 1

    print(f"{md.name}: {added} neu übernommen, {skipped} schon vorhanden.")
    print(f"Jetzt: python3 scripts/quiz.py --tag {unit}")


if __name__ == "__main__":
    main()
