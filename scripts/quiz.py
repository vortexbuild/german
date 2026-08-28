#!/usr/bin/env python3
"""Karteikarten-Quiz mit Fortschritt über vocab/vocab.csv.

    python3 scripts/quiz.py                 # fällige Wörter (Status neu/lernen), DE -> EN
    python3 scripts/quiz.py --tag 01        # nur Einheit 01
    python3 scripts/quiz.py --reverse       # EN -> DE
    python3 scripts/quiz.py --all           # auch schon gelernte Wörter
    python3 scripts/quiz.py -n 20           # höchstens 20 Fragen
    python3 scripts/quiz.py --status        # Fortschritt anzeigen, nicht quizzen

Status-Logik (wird nach jeder Runde in vocab.csv zurückgeschrieben):
    neu --(1x richtig)--> lernen --(3x richtig in Folge)--> gelernt
    falsch  -> streak zurück auf 0, Status "lernen"
    "bekannt" von Hand eintragen = nie abfragen.
Eine Einheit ist fertig, wenn alle ihre Wörter "gelernt" oder "bekannt" sind.
"""
import argparse
import csv
import pathlib
import random
import sys

VOCAB = pathlib.Path(__file__).resolve().parent.parent / "vocab" / "vocab.csv"
FIELDS = ["deutsch", "englisch", "tags", "status", "streak", "hinzugefuegt"]
GRADUATE = 3  # so oft richtig in Folge -> "gelernt"


def load():
    with VOCAB.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def save(rows):
    tmp = VOCAB.with_suffix(".csv.tmp")
    with tmp.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    tmp.replace(VOCAB)


def show_status(rows):
    tags = sorted({r["tags"] for r in rows})
    print(f"{'Tag':<8}{'neu':>6}{'lernen':>8}{'gelernt':>9}{'bekannt':>9}{'gesamt':>8}")
    for t in tags:
        sub = [r for r in rows if r["tags"] == t]
        c = {s: sum(1 for r in sub if r["status"] == s)
             for s in ("neu", "lernen", "gelernt", "bekannt")}
        done = "  ✓" if c["neu"] == 0 and c["lernen"] == 0 else ""
        print(f"{t:<8}{c['neu']:>6}{c['lernen']:>8}{c['gelernt']:>9}"
              f"{c['bekannt']:>9}{len(sub):>8}{done}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--reverse", action="store_true", help="EN -> DE")
    ap.add_argument("--tag", help="nur Zeilen mit diesem Tag")
    ap.add_argument("--all", action="store_true", help="auch gelernte Wörter abfragen")
    ap.add_argument("-n", type=int, default=0, help="höchstens N Fragen")
    ap.add_argument("--status", action="store_true", help="nur Fortschritt anzeigen")
    args = ap.parse_args()

    rows = load()
    if not rows:
        print("vocab.csv ist leer. Zuerst: python3 scripts/import_unit.py 01")
        return

    if args.tag:
        rows_scope = [r for r in rows if r["tags"] == args.tag]
    else:
        rows_scope = rows

    if args.status:
        show_status(rows_scope if args.tag else rows)
        return

    if args.all:
        pool = [r for r in rows_scope if r["status"] != "bekannt"]
    else:
        pool = [r for r in rows_scope if r["status"] in ("neu", "lernen")]

    if not pool:
        print("Nichts fällig. --all für schon gelernte Wörter, oder eine andere Einheit.")
        return

    random.shuffle(pool)
    if args.n > 0:
        pool = pool[: args.n]

    q, a = ("englisch", "deutsch") if args.reverse else ("deutsch", "englisch")
    correct = 0
    done = 0
    for i, row in enumerate(pool, 1):
        try:
            given = input(f"[{i}/{len(pool)}] {row[q].strip()}\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAbgebrochen.")
            break
        done = i
        if given.lower() == row[a].strip().lower():
            correct += 1
            streak = int(row["streak"] or 0) + 1
            row["streak"] = streak
            if streak >= GRADUATE:
                row["status"] = "gelernt"
            elif row["status"] == "neu":
                row["status"] = "lernen"
            print("✓ richtig\n")
        else:
            row["streak"] = 0
            if row["status"] == "neu":
                row["status"] = "lernen"
            print(f"✗  Lösung: {row[a].strip()}\n")

    save(rows)
    print(f"Fertig. {correct}/{done} richtig.")
    show_status(rows_scope if args.tag else rows)


if __name__ == "__main__":
    sys.exit(main())
