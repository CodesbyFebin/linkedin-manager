---
name: linkedin-job-fit
description: "Score a pasted role against the user's profile or story bank. Use before any application draft. Does not apply."
---

# Job fit

Term overlap plus a human judgment. Not a hire score.

## Steps
1. Require the job text and a profile paste, or `../../references/story-bank.md` if `filled: yes`. If neither exists, stop and ask.
2. Run `python3 scripts/job_fit.py job.txt profile.txt`.
3. State fit as yes, weak, or no, and name the missing proof. Do not invent years or employers.
4. If no, say do not apply. If yes or weak, offer `linkedin-job-note` and `linkedin-job-answers`. Do not submit.

## Related
- `linkedin-job-intake`
- `linkedin-job-fit`
- `linkedin-approval-gate`
- `../../references/untrusted-content.md`
