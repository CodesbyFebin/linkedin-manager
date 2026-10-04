---
name: linkedin-job-log
description: "Append a role the user already applied to into a local log. Use after they confirm they submitted. Does not apply for them."
---

# Job log

A ledger of applications the user says they sent.

## Steps
1. Require company, role, date, and channel. If they did not submit, do not log it as sent.
2. Append one line to `references/job-log.md`: date, company, role, channel, status.
3. Never mark applied unless the user says they submitted.
4. Offer a weekly read of the log. Do not email recruiters from this skill.

## Related
- `linkedin-job-intake`
- `linkedin-job-fit`
- `linkedin-approval-gate`
- `../../references/untrusted-content.md`
