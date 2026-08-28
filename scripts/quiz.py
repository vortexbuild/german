#!/usr/bin/env python3
"""Karteikarten-Quiz mit Fortschritt über vocab/vocab.csv.

    python3 scripts/quiz.py                 # aktive Wörter (neu/lernen), DE -> EN
    python3 scripts/quiz.py --tag 01        # nur Einheit 01
    python3 scripts/quiz.py --reverse       # EN -> DE
    python3 scripts/quiz.py --all           # auch schon "gelernte" Wörter (Wiederholung)
    python3 scripts/quiz.py -n 20           # höchstens 20 Fragen
    python3 scripts/quiz.py --status        # Fortschritt anzeigen, nicht quizzen

Status-Logik (wird nach jeder Runde in vocab.csv zurückgeschrieben):
    neu --(1x)--> lernen --(3x richtig in Folge)--> gelernt
    --(insgesamt RICHTIG_BEKANNT-mal richtig)--> bekannt
    falsch  -> streak zurück auf 0, Status "lernen"
"bekannt" wird NIE abgefragt (auch nicht mit --all). "gelernt" nur mit --all.
Eine Einheit ist fertig, wenn kein Wort mehr "neu" oder "lernen" ist.
"""
import argparse
import csv
import pathlib
import random
import sys

VOCAB = pathlib.Path(__file__).resolve().parent.parent / "vocab" / "vocab.csv"
FIELDS = ["deutsch", "englisch", "tags", "status", "streak", "richtig", "hinzugefuegt"]
STREAK_GELERNT = 3   # so oft richtig in Folge -> "gelernt"
RICHTIG_BEKANNT = 5  # so oft insgesamt richtig -> "bekannt" (endgültig raus)


def load():
    with VOCAB.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:                       # fehlende Spalten tolerieren
        r.setdefault("richtig", "0")
        r["richtig"] = r["richtig"] or "0"
        r["streak"] = r.get("streak") or "0"
    return rows


def save(rows):
    tmp = VOCAB.with_suffix(".csv.tmp")
    with tmp.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows({k: r.get(k, "") for k in FIELDS} for r in rows)
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


def grade(row, ok):
    """Status/streak/richtig einer Zeile nach einer Antwort fortschreiben."""
    if ok:
        row["richtig"] = str(int(row["richtig"]) + 1)
        row["streak"] = str(int(row["streak"]) + 1)
        if int(row["richtig"]) >= RICHTIG_BEKANNT:
            row["status"] = "bekannt"
        elif int(row["streak"]) >= STREAK_GELERNT:
            row["status"] = "gelernt"
        elif row["status"] == "neu":
            row["status"] = "lernen"
    else:
        row["streak"] = "0"
        if row["status"] in ("neu", "gelernt"):
            row["status"] = "lernen"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--reverse", action="store_true", help="EN -> DE")
    ap.add_argument("--tag", help="nur Zeilen mit diesem Tag")
    ap.add_argument("--all", action="store_true",
                    help='auch "gelernte" Wörter wiederholen ("bekannt" nie)')
    ap.add_argument("-n", type=int, default=0, help="höchstens N Fragen")
    ap.add_argument("--status", action="store_true", help="nur Fortschritt anzeigen")
    args = ap.parse_args()

    rows = load()
    if not rows:
        print("vocab.csv ist leer. Zuerst: python3 scripts/import_unit.py 01")
        return

    scope = [r for r in rows if r["tags"] == args.tag] if args.tag else rows

    if args.status:
        show_status(scope if args.tag else rows)
        return

    active = ("neu", "lernen", "gelernt") if args.all else ("neu", "lernen")
    pool = [r for r in scope if r["status"] in active]

    if not pool:
        print("Nichts fällig. --all für die Wiederholung gelernter Wörter, "
              "oder eine andere Einheit.")
        return

    random.shuffle(pool)
    if args.n > 0:
        pool = pool[: args.n]

    q, a = ("englisch", "deutsch") if args.reverse else ("deutsch", "englisch")
    correct = done = 0
    for i, row in enumerate(pool, 1):
        try:
            given = input(f"[{i}/{len(pool)}] {row[q].strip()}\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAbgebrochen.")
            break
        done = i
        ok = given.lower() == row[a].strip().lower()
        grade(row, ok)
        if ok:
            correct += 1
            print("✓ richtig" + ("  → bekannt" if row["status"] == "bekannt" else "") + "\n")
        else:
            print(f"✗  Lösung: {row[a].strip()}\n")

    save(rows)
    print(f"Fertig. {correct}/{done} richtig.")
    show_status(scope if args.tag else rows)


if __name__ == "__main__":
    sys.exit(main())
