# SHG Historical Baseline (2023–2026): final Master Synthesis

This folder holds the finished, brand-formatted **Historical Baseline (2023–2026)** for the Self-Help Groups research task.

- `Master Synthesis.docx` is the full 10-pillar baseline: cover page with logo, Executive Summary, Background, all ten pillar sections, Case Studies, Cross-Cutting Recommendations, Conclusion and Works Referenced. It uses Calibri, the brand palette (Orange #E05729 / Blue #0070C0 / Dark Grey #3F403F) and a logo header, and the AI disclosure appears on the cover.
- `Master Synthesis.pdf` is a preview render of the same file (28 pages).
- `build.py` rebuilds the docx from `Master_Synthesis_FULL_DRAFT_all_10_pillars.txt` (in SharePoint). To run it: `python3 -I build.py <draft.txt> <logo.jpg> <out.docx>`

## Why it is here and not in SharePoint

The automated routine can't upload binary files larger than about 15–20 KB to SharePoint. This docx is about 40 KB. A person needs to do the last step:

1. Download `Master Synthesis.docx` from this folder.
2. Upload it to `Ops and Admin/AI INTERNSHIP/Self-Help Groups Research/`. It replaces the old 7-pillar `Master Synthesis.docx`, and the earlier version stays in SharePoint version history.
3. Set `"status": "complete"` in `baseline-progress.json`. Then delete `Food_Security_Findings.txt`, `Refugees_Findings.txt`, `Conflict_Findings.txt` and `Master_Synthesis_FULL_DRAFT_all_10_pillars.txt`.
4. Pause or delete the baseline scheduled task.
