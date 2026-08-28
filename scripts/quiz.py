#!/usr/bin/env python3
"""Karteikarten-Quiz im Terminal über vocab/vocab.csv.

Verwendung:
    python3 scripts/quiz.py [--reverse] [--tag TAG] [-n ANZAHL]
"""
import argparse
import csv
import pathlib
import random
import sys

VOCAB = pathlib.Path(__file__).resolve().parent.parent / "vocab" / "vocab.csv"


def load_rows(tag):
    with VOCAB.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if tag:
        rows = [r for r in rows if tag.lower() in (r.get("tags") or "").lower()]
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--reverse", action="store_true",
                    help="Frage auf Englisch, Antwort auf Deutsch")
    ap.add_argument("--tag", help="nur Zeilen, deren Tags diesen Text enthalten")
    ap.add_argument("-n", type=int, default=0, help="maximale Anzahl an Fragen")
    args = ap.parse_args()

    rows = load_rows(args.tag)
    if not rows:
        print("Keine Vokabeln gefunden. Trage welche in vocab/vocab.csv ein.")
        return
    random.shuffle(rows)
    if args.n > 0:
        rows = rows[: args.n]

    q_key, a_key = ("englisch", "deutsch") if args.reverse else ("deutsch", "englisch")
    correct = 0
    for i, row in enumerate(rows, 1):
        prompt = row[q_key].strip()
        answer = row[a_key].strip()
        try:
            given = input(f"[{i}/{len(rows)}] {prompt}\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAbgebrochen.")
            break
        if given.lower() == answer.lower():
            print("✓ richtig\n")
            correct += 1
        else:
            print(f"✗  Lösung: {answer}\n")
    else:
        print(f"Fertig. {correct}/{len(rows)} richtig.")
        return
    print(f"Zwischenstand: {correct}/{i}")


if __name__ == "__main__":
    sys.exit(main())
