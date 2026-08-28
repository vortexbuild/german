# Wortschatz-Plan / Vocabulary plan

**Level:** B1 → B2. Goal: close the ~1500–2000 word gap between B1 (~2500 words) and
B2 (~4000+).

20 thematic units in `vocab/themen/`, ~70–90 words each with an example sentence.
Finite and tickable, like `PLAN.md`.

## Per unit — one unit of work

1. `python3 scripts/import_unit.py NN` — pulls every word of unit NN into `vocab.csv`
   (status `neu`, tagged `NN`). The `.md` file itself stays untouched — you read it.
2. Read `vocab/themen/NN-*.md` — the words + example sentences, aloud.
3. Optional: in `vocab.csv`, set `status` to `bekannt` for any word you already know
   cold, to skip it entirely.
4. `python3 scripts/quiz.py --tag NN` — repeat over several sittings. Each word climbs:
   `neu → lernen → gelernt` (3 right in a row) `→ bekannt` (5 right in total).
   `bekannt` words drop out of the quiz for good; a wrong answer resets the streak.
5. `python3 scripts/quiz.py --tag NN --status` — when it shows `✓` (nothing left in
   `neu`/`lernen`), tick the unit below.

No schedule. One unit whenever you sit down. `--status` (no `--tag`) shows all units.
`--all` also re-tests `gelernt` words; nothing re-tests `bekannt`.

## Units

- [ ] 01 — Arbeit & Beruf
- [ ] 02 — Bildung & Studium
- [ ] 03 — Gesundheit & Körper
- [ ] 04 — Umwelt & Klima
- [ ] 05 — Politik & Gesellschaft
- [ ] 06 — Wirtschaft & Finanzen
- [ ] 07 — Medien & Digitalisierung
- [ ] 08 — Wohnen & Zusammenleben
- [ ] 09 — Reisen & Verkehr
- [ ] 10 — Ernährung & Konsum
- [ ] 11 — Recht & Kriminalität
- [ ] 12 — Wissenschaft & Technik
- [ ] 13 — Kunst & Kultur
- [ ] 14 — Gefühle & Charakter
- [ ] 15 — Beziehungen & Familie
- [ ] 16 — Sprache & Kommunikation
- [ ] 17 — Freizeit & Sport
- [ ] 18 — Geschichte & Zeit
- [ ] 19 — Natur & Geografie
- [ ] 20 — Meinung & Argumentation

When all 20 are ticked, you have B2-level vocabulary coverage. Mining new words from
input continues after that — but as maintenance, not as a task with an end.

---

## Deutsch

**Niveau:** B1 → B2. Ziel: die Lücke von ~1500–2000 Wörtern schließen (B1 ~2500 → B2 ~4000+).

20 thematische Einheiten in `vocab/themen/`, je ~70–90 Wörter mit Beispielsatz.
Endlich und abhakbar, wie `PLAN.md`.

**Pro Einheit:** (1) `python3 scripts/import_unit.py NN` — übernimmt alle Wörter der
Einheit nach `vocab.csv` (Status `neu`). (2) `vocab/themen/NN-*.md` lesen, Beispielsätze
laut. (3) Optional: in `vocab.csv` bei Wörtern, die du schon kannst, `status` auf
`bekannt` setzen. (4) `python3 scripts/quiz.py --tag NN` über mehrere Sitzungen —
`neu → lernen → gelernt` (3× richtig in Folge) `→ bekannt` (5× richtig insgesamt).
`bekannt` fällt endgültig aus dem Quiz. (5) Wenn
`python3 scripts/quiz.py --tag NN --status` ein `✓` zeigt: Einheit oben abhaken.

Kein Zeitplan. Eine Einheit, wenn du dich hinsetzt.
`--all` wiederholt auch `gelernt`-Wörter; `bekannt` wird nie wiederholt.
