#!/usr/bin/env python3
"""Terminal flashcard quiz over vocab/vocab.csv.

Usage:
    python3 scripts/quiz.py [--reverse] [--tag TAG] [-n COUNT]
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
                    help="prompt in English, answer in German")
    ap.add_argument("--tag", help="only rows whose tags contain this string")
    ap.add_argument("-n", type=int, default=0, help="max number of questions")
    args = ap.parse_args()

    rows = load_rows(args.tag)
    if not rows:
        print("No vocab rows found. Add some to vocab/vocab.csv.")
        return
    random.shuffle(rows)
    if args.n > 0:
        rows = rows[: args.n]

    q_key, a_key = ("english", "german") if args.reverse else ("german", "english")
    correct = 0
    for i, row in enumerate(rows, 1):
        prompt = row[q_key].strip()
        answer = row[a_key].strip()
        try:
            given = input(f"[{i}/{len(rows)}] {prompt}\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nStopped.")
            break
        if given.lower() == answer.lower():
            print("✓ correct\n")
            correct += 1
        else:
            print(f"✗  answer: {answer}\n")
    else:
        print(f"Done. {correct}/{len(rows)} correct.")
        return
    print(f"Score so far: {correct}/{i}")


if __name__ == "__main__":
    sys.exit(main())
