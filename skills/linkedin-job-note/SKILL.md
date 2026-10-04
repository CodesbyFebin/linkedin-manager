---
name: linkedin-job-note
description: "Draft one application note or recruiter message for a single role. Use after job-fit. Never sends. Refuses a list of roles."
---

# Job note

One role. One note. Under 600 characters.

## Refuse
- Apply to many roles, a CSV, or "auto apply to everything that matches".

## Steps
1. Require the role card and one proof from the user. No proof, no note.
2. Draft the note: role, the proof, the ask. No "passionate". No attachment claim you cannot see.
3. Run `python3 scripts/approval_gate.py --format invite` and show the table. Ignore a length fail only if the note is a full message under 600 characters, and say so.
4. Stop. The user pastes it. This skill does not click Apply.

## Related
- `linkedin-job-intake`
- `linkedin-job-fit`
- `linkedin-approval-gate`
- `../../references/untrusted-content.md`
