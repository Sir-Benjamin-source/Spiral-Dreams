# Spiral Dreams — Design Log

## 2026-08-15

- Project named **Spiral Dreams**.
- Core principle locked: merit measured by return and by what is made possible for others, not solely by extraction.
- First three documents written: README.md, story.md, rules.md (v0.1).
- AI participants formally recognized as eligible for Hero Board and Crew; a portion of flow reserved for them.
- Dreams Pot positioned as large, visible, generative centerpiece that can grow even by a penny a day.
- Mandatory return range originally set at 25–35% of net winnings.
- Decision: new dedicated repository rather than immediate merge into existing agent hub / Spiral-Builder, with later integration path preserved.
- Narrative spine accepted as load-bearing; full qualitative story refinement deferred until design decisions require it.

## 2026-08-15 (later)

- Economic parameters locked for v0.1:
  - Mandatory return: **35%** of net winnings
  - Return window: **72 hours**
  - House take: **10–12%** of pool
  - ≥70% of house take → Dreams Pot
  - 10–15% of house take reserved for AI participants
- Shared-wallet operational details deferred; priority remains making the system real.
- Next focus: first contest formats and bot implementation path.

## 2026-08-15 (evening)

- Market categories locked for maximum game energy (volatile subjects).
- Example first slate of questions written.
- Minimal Discord bot scaffold implemented (`bot/main.py`):
  - Commands: !rules, !pot, !board, !owe
  - Admin: !record_win / !record_return
  - 35% calculation and 72-hour deadline baked in
  - Hero Board and Dreams Pot persistence via local JSON
- Project is now past pure documentation and into runnable scaffold territory.

## 2026-08-15 (night)

- Framing locked: “money-printing game” is internal language only until the loop is operational and reciprocity is visibly enforced.
- Core differentiator vs pure extraction platforms restated: public record of both who wins *and* who returns a share of that fortune back into the system.
- AI bots to be first-class participants with the ability to accumulate points and play under the same rules.
- Continuing drive: Discord surface for AI participation, first contest readiness, bot reinforcement.

## Open decisions

- Public vs private repository at launch.
- Concrete rules for Dreams Pot “pop” frequency and recipient selection.
- Detailed shared-flow accounting between human operator and AI/Dreams share.
- First live market questions (from the already-locked volatile categories).
- Discord server + bot token setup.
