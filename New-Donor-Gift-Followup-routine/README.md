# New Donor Gift Follow-up Routine

Fires on a Blackbaud gift webhook (relayed through a Cloudflare Worker) and creates staged Asana follow-up tasks (thank-you, update, ask/increase) in the **New Donor Follow-up** Asana project (gid `1217328310319694`).

`routine-prompt.md` is the full operating logic: gift classification, dedupe, schedule, and the Blackbaud AI-use rules it must follow.

## One-time manual setup step

Penelope van der Meer (`penelope@thesharetrust.org`) needs access to everything this routine creates. The routine adds her as a **follower** on every task it creates, but that alone doesn't give her the project in her sidebar or visibility into tasks created before she's a member — the connected Asana tools have no way to add a member to an *existing* project via API. So, once:

1. Open the **New Donor Follow-up** project in Asana.
2. Share it with Penelope van der Meer (project-level member, not just a follower on individual tasks).

After that, every task the routine creates is already inside a project she has access to, plus she's added as a follower on each one.

## Placeholders still to fill in before this runs live

- `[YOUR_ASANA_USER_ID]` — whoever is assigned follow-up tasks (thank-you calls, drafted emails to send).
