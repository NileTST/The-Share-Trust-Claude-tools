# TST Lapsed Donor Email Routine

## What this is

An on-demand Claude Code routine: give it a CSV of lapsing donors (the format Blackbaud exports — Name, Constituent ID, Email address, Latest gift date/fund, Last action category/type/date, etc.), and it looks each one up in Blackbaud, filters to donors who haven't gotten an email in the last year, and drafts a personalized re-engagement email for each one. It never sends anything — drafts are for a human to review and send.

Two inputs feed the draft besides the CSV:
- **Email template** (`context/email-template.md`) — uploaded once, reused on every run until replaced.
- **Project-update PDF** — uploaded fresh each time the routine runs; a couple of sentences about current project work get pulled from it into each draft.

## How it works, at a glance

Everything the routine needs lives in `context/` — see each file for its one job (purpose, audience, scope, ai-policy, voice, output-format, email-template). `routine-prompt.md` is the operating script the agent follows every run.

## Running it

1. Attach the donor CSV to a Claude Code session with this repo as the working directory (or point it at a file already in `donor-lists/`).
2. First time only: also attach the email template — it gets saved to `context/email-template.md` for future runs.
3. Every run: also attach that run's project-update PDF.
4. The routine looks up each donor in Blackbaud, skips anyone emailed within the lookback window (default 365 days — `/set-window [days]` to change), and writes one draft per eligible donor to `drafts/`.

`donor-lists/` and `drafts/` are gitignored — donor PII never gets committed to this repo.

## Known limitation

The Blackbaud `get_constituent_details` lookup isn't documented to return communication/action history, so "emailed in the last year" leans on the CSV's own `Last action category/type/date` columns as the primary signal, with any fresher data the live lookup happens to return taking precedence. If a donor's last action in the CSV predates the file itself, or the CSV lacks action data entirely, the routine treats them as eligible and flags that as an assumption in the run summary rather than a confirmed negative — worth a spot-check before sending.
