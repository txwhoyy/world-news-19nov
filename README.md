# world-news-19nov

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/txwhoyy/world-news-19nov/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/txwhoyy/world-news-19nov/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A newspaper front page that sums up the world news of **Thursday 19 November 2026** in a
single 1024×1024 PNG.

## The page

"The World Today" — masthead, the date in red, one lead story with a large drawn
illustration, and seven more stories across regions and fields, each with its own
small drawn illustration, headline, short summary and source line. Every
illustration is drawn from code; there are no photographs and no downloaded
assets.

## The eight stories

All eight were verified against reporting published on 19 November 2026.

1. **Lead — Diplomacy, Shenzhen.** Trump, Xi and Putin meet in Shenzhen in the
   first three-way summit, on the sidelines of the APEC forum; nuclear arms
   control, Ukraine and Iran discussed, no major agreement announced.
   Sources: Associated Press · Reuters.
2. **International Justice, The Hague.** The International Court of Justice rules
   by 9–6 that Myanmar committed genocide against the Rohingya in the 2017
   crackdown, finding about 10,000 were killed. Source: Associated Press.
3. **Business, New York.** Anthropic's $81bn debut is the biggest IPO in
   history: shares in the AI firm behind Claude begin trading on Nasdaq as ANT
   after pricing at $83. Source: Reuters.
4. **Weather, India.** Cyclone Akvan nears India's east coast, due to cross the
   Andhra Pradesh–Odisha coast by noon on Friday with winds gusting to
   110 km/h. Source: India Meteorological Department.
5. **Conflict, Gaza.** Israel ends its ground raid across the Gaza ceasefire
   line near Bureij and Nuseirat, the first raid beyond the truce's "Yellow
   Line". Sources: Agence France-Presse · Reuters.
6. **Politics, Dhaka.** Four killed as unrest grips Bangladesh; an opposition
   shutdown brings renewed violence and the ancestral home of interim leader
   Muhammad Yunus is set on fire. Source: Reuters.
7. **Migration, Dakar.** Dozens missing after a migrant boat carrying about 50
   people bound for Europe capsizes off Yenne, south of Dakar. Source: Reuters.
8. **Security, Vienna.** The IAEA warns North Korea is expanding uranium
   enrichment, as Seoul urges dialogue. Sources: IAEA · Al Jazeera.

## Run it

```sh
python3 render.py        # redraws entry.png (1024x1024, deterministic)
npx tsx main.ts          # validates entry.png and copies it to /output
                         # (or $MAKEFUN_OUTPUT_DIR when set)
```

`render.py` needs only Pillow and the DejaVu system fonts; `main.ts` uses the
Node 22 standard library only and runs with no network. Running the render
twice produces a byte-identical PNG.

## Redraw from source

Edit the story text or the drawing code in `render.py`, run
`python3 render.py`, and check `entry.png` before committing. The layout is
computed from the text, so the middle and bottom rows shift to fit rather than
overflow.

---

<sub>Entered on [make.fun](https://make.fun/?ref=1paa8b6t&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
