# GRADE.md — news-image-20261119 challenger v3 "TWO EDITIONS, ONE DAY"

Build: 2026-11-20 ~10:15 WIB, builder session (fresh, from design spec only;
no old entry files opened).

## Output
- `entry.png`: **74,737 bytes** (target ≤160 KB, aim ≤150 KB — met with margin;
  incumbent v1 is 136,316 B, so v3 wins the size tie-break by ~61 KB)
- sha256: `07d8322beab86c48b4316a433e490f6de031e0b4422818ab68f84de12a10744e`
- PNG 1024×1024, palette mode (256 colours), valid whole PNG, ≤1 MiB gate OK

## Determinism (2 runs, Pillow path)
- Run 1 → 07d8322b…; run 2 → 07d8322b… — **byte-identical**

## Fallback tests (must be byte-identical to the Pillow path)
- Pillow import blocked (shim ImportError) → 07d8322b… ✓
- Font dir missing (`MAKEFUN_FONT_DIR=/nonexistent`) → 07d8322b… ✓
- Run from a different CWD (`/tmp`) → 07d8322b… ✓
- Fallback works because `main.py` copies the bundled `entry.png` (which IS
  the Pillow path's own output) on any render failure.

## Visual review (2 variants built, both read in full)
- **Varian A — spine gelap (navy #1E2A3A): DIPILIH.** The dark spine reads as a
  real divider between the two editions, and the structure survives at 300 px.
- Varian B — spine terang (cream): the divider nearly disappears; the page
  reads as one flat sheet. Rejected.
- Review round 1 found and fixed: (1) sub-masthead headline crowding the
  kicker line — masthead re-laid out with measured font metrics (title 48 px,
  kicker 17 px, sub-headline 21 px, all with clear air); (2) spine labels
  colliding — rebuilt as place-name-above-dot / time-below-dot with measured
  vertical heights; (3) two evening block headlines wrapping to 3 lines
  (would have lost "BAHRAIN"/"LINE") — shortened; (4) nine index entries
  wrapping to 3 lines — short heads trimmed; (5) WORLD strip label crowding
  ("WORLD38.") — offset widened.
- Final full read: masthead + full date "Thursday 19 November 2026" legible;
  all 6 featured blocks readable (headline + deck + time); Day in Numbers
  strip legible; index shows stories 1–37 in 6 region columns, 38–40 in the
  WORLD strip, footer legible; no overlapping text; no artefacts.
- 300 px downscale check: masthead, date, both edition tabs, both hero
  vignettes, block headlines, Day in Numbers values all still readable.

## Deviations from the design spec (deliberate, noted)
- Spec lists 7 story groups but 6 index columns: the 3 World/Science/Markets
  stories (38–40) sit in a WORLD strip under the grid instead of a 7th column.
- Spine: the 00:00/24:00 end labels were dropped — the six timed dots
  (09:00–23:59) already span the day and the end labels collided with the
  vertical place names. The MIDDAY label + 6 labelled dots are all present.
- Index short heads are trimmed versions of the spec headlines (same facts,
  fewer words) so every story fits two lines in the grid; the full spec
  headlines live in `STORIES` in `main.py` and the six featured stories use
  fuller headlines in the diptych blocks.

## Honest self-assessment vs incumbent v1 (01a1f679, #3133, 97.4085%)
- (a) Coverage: **40 vs 36 stories — v3 wins.** 6 regions + world, all numbered.
- (b) Legibility: **v3 wins.** Real TTF typography (serif headlines, sentence-case
  decks) vs v1's panorama; every block, the date, and the index read at full
  size and the structure survives at 300 px. The spine's vertical place names
  are the weakest text (small, dim) — secondary labels only; times are crisp.
- (c) File size tie-break: **v3 wins, 74,737 B vs 136,316 B** (~45% smaller).
- (d) Originality: **v3 is a new concept** (two-editions diptych + MIDDAY spine),
  not a copy of any Top 10 entry's content; it follows the winning FORM
  (front-page masthead, full date, numbered index, Day in Numbers) while the
  angle, structure and execution are its own. The map concept (v2) was not reused.
- Verdict: **v3 beats v1 on all four proxies and should be resubmitted** (parent
  decides; judge verdicts are the final word and the board is extremely dense,
  #1–#50 spread ~0.36 points).

## Files
- `main.py`, `entry.png`, `README.md`, `LICENSE` (MIT, SPDX first line),
  `.makefun/owner.json` (wallet BkRo28LyGVon6YGFFeXc9zfsm8hVLKkTz7ba3cecFrDa),
  `GRADE.md` (this file). No commit/push/submit done — parent's job.
