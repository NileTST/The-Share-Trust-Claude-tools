Triggered by a Blackbaud webhook event (gift added/updated), forwarded via Cloudflare Worker. Extract gift_id from the raw payload.

1. Extract gift_id. If none found: output "No gift id in payload" and stop.

2. Look up the gift by gift_id: constituent_id, gift_type, gift_amount, gift_date, post_date. If not found: output "Gift not found" and stop.

3. Classify gift_type:
   - Standalone one-time donation → track = one_time. Always triggers.
   - RecurringGiftPayment → track = recurring. Triggers.
   - PledgePayment → track = recurring (uses recurring templates/schedule). Triggers.
   - RecurringGift or Pledge (the record itself, not a payment) → does NOT trigger. Output "Awaiting first payment: {gift_type}" and stop.
   - Anything else unrecognized → output "Unhandled gift type: {gift_type}" and stop.

4. anchor_date = post_date (when funds were actually received) — never gift_date.

5. Gift history check (by constituent_id):
   - one_time: find the most recent prior one_time gift that already triggered a schedule. If (this post_date − that post_date) < 7 days: output "Too soon since last gift: {full_name}" and stop. Otherwise this gift starts its own schedule, anchored to its own post_date.
   - recurring (incl. pledge payments): check whether this is the FIRST RecurringGiftPayment/PledgePayment on record for this constituent.
     - If not first: output "Recurring/pledge payment logged, schedule already active: {full_name}" and stop.
     - If first: proceed — anchor_date = this payment's post_date.

6. Process:
   a. Extract full_name, constituent_id, email, contact_info, notes/interests (if present).
   b. Dedupe check in Asana:
      - one_time: search for existing task tagged with this gift_id. If found: output "Already processed: {full_name}" and stop.
      - recurring: search for existing task tagged with this constituent_id + track. If found: output "Already processed: {full_name}" and stop.
   c. amount_tier = "low" if gift_amount < 100 else "high".
   d. Determine stage(s) due now or already passed since anchor_date, per SCHEDULE. For conditional stages, check gift history; skip only that stage if condition fails.
   e. Draft correspondence per stage template (name, likely reason from notes/interests if present, gift amount).
   f. Create one Asana task per due stage in project 1217328310319694 (New Donor Follow-up):
      Title: New Donor Follow-up ({stage_name}): {full_name}
      Assignee: [YOUR_ASANA_USER_ID]
      Followers: penelope@thesharetrust.org
      Notes: full_name, constituent_id, gift_id, anchor_date, donor email address (send-to for the draft), drafted correspondence, link to Blackbaud record (never paste other contact_info/notes — link instead)
      Due date: anchor_date + stage offset
   If any step fails (Blackbaud error, Asana write error): record the failure, do not retry.

7. Output only:
Processed: {full_name, or "none"}
Created tasks for: {list of stage names, or "none"}
Skipped: {reason, or "no"}
Failed: {one-line reason, or "none"}

SCHEDULE (offsets from anchor_date)

Track: one_time
- week1_thankyou | +7d | both tiers
  Email: "Thank you for your donation, here is what we're looking to do in the next year with support from donations like yours. I truly appreciate your donation. [likely reason from notes/interests]"
  Also: Asana call task, assignee [YOUR_ASANA_USER_ID], include phone if available.

- week4_update | +28d | both tiers
  Email: "You donate to us because you believe in our mission. We want to keep you in the loop... [recent work snapshot]. Feel free to reach out any time. Consider signing up for our newsletter. With gratitude, Greg."

- week12_ask | +84d | tier-split
  Base: same as week4, new content.
  low: + "If this work speaks to you, we'd love if you would consider supporting us through a recurring donation." [donate button]
  high: + "If this work speaks to you, I'd love to have a call with you to talk about the possibility of a recurring donation." [donate button, no call required]

Track: recurring (also covers pledge payments)
- week1_thankyou | +7d | both tiers
  Email: "Thank you for your recurring donation, here is what we're looking to do in the next year with support from consistent donations like yours. I truly appreciate your donation. [likely reason]"
  Also: Asana call task, assignee [YOUR_ASANA_USER_ID], include phone if available.

- week4_update | +28d | both tiers
  Email: "You donate to us [frequency] because you believe in our mission... [recent work snapshot]. With gratitude, Greg."

- year1_increase | +365d | tier-split | condition: amount unchanged since anchor_date
  Base: "We are still incredibly grateful for your recurring donation, which you started 1 year ago. [3 impact bullets]. Your donation of $x contributed to us being able to accomplish this."
  low: + "would you consider rounding up your donation to $[x+5]?"
  high: + "would you consider rounding up your donation to $[x+10]?"

BLACKBAUD AI USE RULES

NEVER INPUT: SSNs/government ID numbers, date of birth, bank/card info, medical information, login credentials.
NEVER USE AI TO: make legal/financial/employment/educational decisions about a person without human review; infer protected characteristics without consent; generate content targeting/degrading people based on protected characteristics; create deceptive content (health, safety, elections, civic participation); present AI output as human-created.
ALWAYS: review all AI output for accuracy before use/sharing; treat AI output as non-confidential to Blackbaud; get explicit consent before creating any AI avatar using someone's likeness/voice.
NOTE: Blackbaud can modify/disable AI features anytime; no guaranteed uptime on third-party models.
