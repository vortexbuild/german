# German / Deutsch

Self-contained reference and training material for learning German, B1 → functional
B2/C1. Explanation first, then tables, then examples. Practice is optional; the
reference is the point.

## Two language trees

Every note exists in both languages, cross-linked at the top of each file.

| | |
|---|---|
| [`de/`](de/) | German version — `de/grammatik/`, `de/referenz/` |
| [`en/`](en/) | English version — `en/grammar/`, `en/reference/` |

Start here: [`de/grammatik/README.md`](de/grammatik/README.md) · [`en/grammar/README.md`](en/grammar/README.md)

## Language-neutral (top level)

| Path | Contents |
|------|----------|
| `PLAN.md` | B1→B2 grammar checklist — the sequence to work through (no schedule) |
| `VOCAB.md` | B1→B2 vocabulary checklist — 20 thematic units + the daily loop |
| `ROADMAP.md` | CEFR levels A1–C1 and what each requires |
| `vocab/themen/` | The 20 thematic word lists (read these) |
| `vocab/vocab.csv` | Generated word store with progress: `deutsch,englisch,tags,status,streak,hinzugefuegt` |
| `scripts/import_unit.py` | `import_unit.py NN` → pulls unit NN's words into `vocab.csv` |
| `scripts/quiz.py` | Stateful flashcard quiz; `--tag NN`, `--status`, `--reverse`, `--all` |
| `journal/` | Writing practice (German). Copy `_template.md` to `YYYY-MM-DD.md` |

## How to use it

Read `grammar/` top to bottom in the given order (in whichever language tree you want).
Each file stands alone: explanation → table → examples. Use `reference/` for lookups.
Add new words to `vocab/vocab.csv`.

Vocabulary: `VOCAB.md` has the loop. Grammar: `PLAN.md` has the topic order.

Your error log — `de/grammatik/fehler.md` (or the `en/` copy) — is the highest-value file.
Keep it in **one** language only; don't maintain both.

---

## Deutsch

Eigenständiges Nachschlagewerk und Trainingsmaterial für Deutsch, B1 → funktionale
Beherrschung auf B2/C1. Erst die Erklärung, dann Tabellen, dann Beispiele. Üben ist
optional; das Nachschlagewerk ist der Kern.

Jede Notiz gibt es in beiden Sprachen (`de/` und `en/`), oben in jeder Datei verlinkt.
Sprachneutral bleiben oben: `vocab/`, `journal/`, `scripts/`, `ROADMAP.md`.

Einstieg: [`de/grammatik/README.md`](de/grammatik/README.md)
