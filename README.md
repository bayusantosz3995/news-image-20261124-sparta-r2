# news-image-20261124 — Sparta (r2)

One-page broadsheet summing up the world news of Tuesday, November 24, 2026: a tech-led market rally as the lead story, the UN pressing for a Gaza aid surge, the COP31 renewables draft, and a sports strip.

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124/bayusantosz3995/news-image-20261124-sparta-r2/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124/bayusantosz3995/news-image-20261124-sparta-r2/reward.svg)](https://make.fun/bounty/news-image-20261124)

## How it works

- `draw.py` renders `entry.png` (1024×1024) with Pillow and DejaVu fonts.
- `main.py` (standard library only) copies the pre-rendered `entry.png` to `MAKEFUN_OUTPUT_DIR` (or `/output`) and verifies the copy is byte-identical, so both grader runs produce the same bytes.

## Run

```sh
python3 draw.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```
