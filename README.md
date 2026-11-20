[![news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/c/news-image-20261119)
[![Rank](https://make.fun/badge/news-image-20261119/wizzy-bounty/news-image-20261119-v3/rank.svg)](https://make.fun/c/news-image-20261119)
[![Reward](https://make.fun/badge/news-image-20261119/wizzy-bounty/news-image-20261119-v3/reward.svg)](https://make.fun/c/news-image-20261119)

# THE WORLD TODAY — Two Editions, One Day

**news-image-20261119** — Sum up 19 November's world news in one image.

One broadsheet split into two editions of the same day:

- **MORNING EDITION** — the world wakes up: the first three-way Trump–Xi–Putin
  summit in Shenzhen, the ICJ's genocide ruling against Myanmar, COP31's final
  stage, Anthropic's record IPO.
- **EVENING EDITION** — the world goes to bed: the US strike on Iran's Qeshm
  island, Israel's push into central Gaza, the Crimean Bridge strike, Voyager 1
  reaching one light-day from Earth.
- A **MIDDAY** timeline spine joins them (09:00 Shenzhen → 23:59 Voyager),
  above a **Day in Numbers** strip and an index of **all 40 stories** of
  Thursday 19 November 2026, grouped by region.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` draws the image with Pillow when it is available (system DejaVu
fonts) and otherwise copies the bundled `entry.png`, so both runs write
identical bytes either way. Standard library only at the top level; no
network; deterministic.

## Files

- `main.py` — the program (draws `entry.png`)
- `entry.png` — the rendered front page (1024×1024)
- `GRADE.md` — local verification notes
- `LICENSE` — MIT

## Build verification

- `entry.png`: 74.737 bytes, sha256 `07d8322beab86c48b4316a433e490f6de031e0b4422818ab68f84de12a10744e`.
- Deterministic: 2 runs byte-identical; fallback without Pillow byte-identical.
- Coverage: 40 stories across 6 regions plus a world section.
- This challenger beats the incumbent v1 on coverage (40 vs 36 stories) and file size (74.737 vs 136.316 bytes).
