# TST SHG Evidence Scan

## What this is

An automated Claude Code routine that runs once a month and produces a short, formal evidence brief for TST's strategy team. It scans a fixed list of approved external organizations for anything new they've published in the prior calendar month that's relevant to TST's work on Self-Help Groups (SHGs) and related group-based savings and microfinance models, then writes up a ~3-page summary organized by theme and source.

This is a sibling routine to `localization-evidence-scan-routine/` (which tracks locally led development / localization content instead). They share the same operating design but have independent `context/` — separate sources, guidance, and reports — so updating one has no effect on the other.

It is **read-only research and synthesis** — it does not post, publish, or send anything outside this repository, and it does not touch PII, participant data, or confidential/partner information.

## What it produces

Once a month, a file such as `reports/2026-08-evidence-scan.md` — covering the *prior* calendar month (a scan run in September covers August 1–31). Each report:

- States the exact date range and lists every source reviewed, including ones that had nothing relevant that month (no padding to hit a length target).
- Groups findings by theme, with themes that show up across 2+ sources ("cross-cutting") listed first.
- Within each theme, breaks findings down by source, and every finding names its source.
- Keeps the routine's own analysis clearly labeled as opinion/editorial commentary, never blended in with what a source actually said.

Reports are internal-use only (TST strategy team and staff). If a report is ever shared externally, TST's AI-use policy requires human review and an AI-use disclosure first — this routine's output does not carry that on its own.

## How it works, at a glance

Everything the routine needs to run lives in `context/`:

| File | Purpose |
|---|---|
| `purpose.md` | Why this routine exists |
| `audience.md` | Who reads the output |
| `voice.md` | Tone rules for the writeup |
| `output-format.md` | Structure, length, save location |
| `scope.md` | Hard boundaries — what it must not do |
| `sources.md` | **The only organizations it's allowed to search** |
| `guidance.md` | **Trigger words/criteria for what counts as relevant** |
| `ai-policy.md` | TST's AI acceptable-use rules; these override everything else |
| `acronyms.md` | TST/sector shorthand, so it interprets source material correctly |

`routine-prompt.md` is the operating script the agent follows every time it runs — it tells the agent to read all of the above, then either run the monthly scan or handle a slash command (see below).

Every run re-reads all of `context/` first, so any edits you make (via the commands below) take effect on the very next scan — there's nothing else to "redeploy."

## Setting it up

1. This repo (or wherever `shg-evidence-scan-routine/` lives) needs to be the working directory for a Claude Code session that runs on a monthly schedule — e.g., a scheduled/cron-triggered session, or a recurring trigger configured wherever this routine is hosted.
2. Point that scheduled trigger at `routine-prompt.md` (or a session that has it in context) with **no input / an empty prompt** — that's what tells the routine "this is the scheduled run, not a command." Typing something like "run" or "start" also works.
3. Make sure the session has git access to commit and push to a `claude/`-prefixed branch in this repo — that's where reports get saved (`reports/YYYY-MM-evidence-scan.md`) and committed.
4. Review `context/sources.md` and `context/guidance.md` once up front to confirm they match what you actually want tracked (see below for how to change them).

That's it — no separate deployment step. The next scheduled firing will pick up whatever is currently in `context/`.

**Note on current sources:** `context/sources.md` currently carries over the same 7 organizations used by the localization routine (CGD, Peace Direct, TAI, MFAN, ALNAP, NEAR, U.S. Department of State) as a starting point. None of them are SHG-specialist publishers, so early monthly reports from this routine may come back thin — that's expected, not a bug. Swap in SHG/savings-group-focused organizations (e.g., CARE, SEEP Network, Trickle Up, BRAC, Innovations for Poverty Action) via `/add-source` and `/remove-source` as you refine the list.

## Updating what it looks at

You never hand-edit `sources.md` or `guidance.md` directly (or rather — you can, but the intended path is through commands, so there's always a clear commit history of *why* something changed). Send the routine one of these as a message:

### Sources — the organizations it searches

- **`/list-sources`** — show the current list.
- **`/add-source [name] — [one-line description]`** — adds a new organization. If you don't give a description, the routine will write a neutral one-line description itself and flag that it guessed, so you can correct it.
- **`/remove-source [name]`** — removes an organization. If the name doesn't match exactly, it'll show you the current list instead of guessing.

Example:
```
/add-source SEEP Network — A learning network focused on savings-led and group-based microfinance models, including Self-Help Groups and VSLAs.
```

### Guidance — what counts as "relevant"

- **`/list-guidance`** — show the current trigger words/criteria and any framing notes.
- **`/add-guidance [text]`** — adds a new trigger word/criterion, or a broader framing note (the routine figures out which section it belongs in; if it's genuinely ambiguous, it'll ask rather than guess).
- **`/remove-guidance [text]`** — removes a matching line.

Example:
```
/add-guidance financial inclusion for women's groups
```

### Everything else

- **`/help`** — a short description of the routine and the commands above.
- Any plain question (e.g., *"what did last month's report say about VSLAs?"*) gets answered from the context files and past reports — it won't trigger a new scan unless you explicitly ask for one.

Every command results in a commit to a `claude/`-prefixed branch with a message like `Add source: [name]`, and the routine will always show you the exact updated section of the file afterward so you can confirm the change looks right.

## Boundaries (by design, not just documentation)

- It will only ever search the organizations in `sources.md` — it will not add a source on its own initiative, no matter how relevant something looks.
- It only looks at the prior full calendar month, not a rolling window.
- It will never process PII, participant data, or confidential/partner-sensitive data — if a source's content would require that to summarize, it excludes that item and says so in the report rather than working around it.
- `ai-policy.md` overrides any conflicting instruction, including from a command or from this document.

## Known limitation

Some source websites intermittently block or return incomplete results to automated fetches (this affected near.ngo, alnap.org, and parts of peacedirect.org for the sibling localization routine). When that happens, the routine notes it in the report rather than silently treating a blocked fetch the same as "nothing published." If a monthly report looks unusually thin for a source you know published something, it's worth a manual spot-check before assuming there was nothing to report.
