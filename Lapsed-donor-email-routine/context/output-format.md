# Output Format

- One drafted email per eligible donor, saved to `drafts/<constituent-id>-<lastname>.md` with To (name + email), Subject, and Body.
- Body follows the structure in `context/email-template.md`, personalized with the donor's name and 2-3 sentences on current projects drawn from that run's PDF.
- After drafting, report a run summary in chat (not saved to git): donors in CSV, number skipped as already emailed within the window, number drafted, and any lookup failures or ambiguous matches that need manual follow-up.
- Never auto-send; never write drafts anywhere but `drafts/`.
