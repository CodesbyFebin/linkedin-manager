---
name: linkedin-newsletter
description: "Draft a LinkedIn newsletter edition from a spine of receipts. Use when the user wants an issue, not a feed post. Not for a 1,000 character post. Use linkedin-post-writer for feed posts."
---

# Newsletter drafter

A newsletter is a letter with a spine. It is not three posts glued together.

## When to use
- "Draft this week's newsletter"
- "Turn these notes into an issue"

## Steps
1. Load voice and story bank only when `filled: yes`.
2. Ask for the issue promise in one line if it is missing.
3. Structure: subject, preview line (under 140 characters), open with the receipt, three sections, one close.
4. Each section gets one heading and at most 120 words.
5. Show subject options (3) and the full draft. Wait for approval.
6. Publishing a newsletter is manual unless the user has a custom poster. Say so. Do not pretend Publora posts newsletter editions.

## Hard rules

Global voice rules: see root SKILL.md Voice rules.
- No throat-clearing intro.
- No invented metrics.
- One ask at the end.

## Related
- `linkedin-post-writer`
- `linkedin-humanizer`
- `linkedin-approval-gate`
- `../../references/voice-rules.md`
- `../../references/operator-codesbyfebin.md`
