# Scope

- Only process donors present in the supplied CSV — never pull in additional donors from Blackbaud on its own.
- "Emailed in the last year" = an action on the constituent whose category/type mentions email/e-comm/newsletter/mailing, dated within the lookback window. Check `Last action category`/`Last action type` + `Last action completed date` (fall back to `Last action date`) from the CSV first; if the Blackbaud lookup returns any more-recent action/communication data for that constituent, that wins. If nothing on either side mentions an email, treat the donor as eligible and note that the "no email on record" read is an assumption, not a confirmed negative.
- Lookback window: 365 days from the run date. Adjustable with `/set-window [days]`.
- Draft only — never send an email or otherwise contact a donor. A human sends after review.
- A run needs both `context/email-template.md` (not the placeholder) and a project-update PDF attached that run. Missing either → ask for it, don't guess or draft without it.
- Never commit donor PII (name, email, address, giving history) to git. Donor lists and drafts live only in `donor-lists/` and `drafts/`, both gitignored.
